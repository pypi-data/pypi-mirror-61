#! /usr/bin/env python

"Generate TPT script to load Teradata table(s)"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2017, Paresh Adhia"
__license__ = "GPL"

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Callable, Tuple
from pathlib import Path
import re

from tdtypes.tpt import TPTJob, QB1, Instances, UtilSize, DDLStep, OdbcOp, ExportOp, FileReaderOp, InserterOp, StreamOp, LoadOp, LoadStep, TPTVars
from tdtypes import Table
from tdtools import util
from .util import AuthArg, tablename

logger = util.getLogger(__name__)

def main():
	"script entry-point"
	args = user_args()

	job = build_job(args)

	if args.run:
		rc = job.run(args.jobvar, args.chkp, capture_counts=args.counts)
		if rc:
			return rc
		if args.counts:
			from yappt import pprint
			pprint(((c.step, c.rows_in, c.rows_out) for c in job.step_counts), ['Step', 'Ins', 'Sel'])
	else:
		print(str(job))

def user_args():
	"run-time options"
	import argparse
	import textwrap
	import functools
	import yappt

	def src(pat: str) -> Callable[[Table], str]:
		"source is a file name or a patten-pair that derives filename from tablename"
		if not '=' in pat:
			return lambda t:pat

		try:
			pat, repl = pat.split('=')
			return functools.partial(re.compile(pat,re.IGNORECASE).sub, repl)
		except:
			raise argparse.ArgumentTypeError("Pattern shoud be of type <match>=<repl>")

	def size(pat: str) -> int:
		"A non-negative number representing file-size"

		num = int(float(pat)) # float allows numbers like 1e6
		if num < 0:
			raise argparse.ArgumentTypeError("SIZE must be a non-negative number")
		return num

	thresholds = [int(v) for v in [10e3, 1e6, 100e6, 10e9]]

	p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description = __doc__, epilog=textwrap.dedent("""\
	Examples:
	  %(prog)s --db dev_stg table1 table2 table3
	  %(prog)s --dir /path/to/files/ --src '$=.tar.gz'  --db TGTDB --stats --qb 'JOBNAME=MYJOB;' table1 table2 table3
	  %(prog)s --td --src '^dev_=prd_'  --stats --trunc-sql "CALL {name.sch}.PrepTableForLoad('{name.name}')" dev_db1.table1 dev_db2.table2 dev_db2.table3
	  %(prog)s --odbc ODBCDSN --src '(.*)=SRCDB..\\1' --no-trunc --stats table1 table2 table3"""))

	p.add_argument('tbl', metavar='TABLE', type=tablename, nargs='+', help='Table names')

	g = p.add_argument_group('Job options')
	g.add_argument('-j', '--job',    metavar='NAME',             help='TPT Jobname')
	g.add_argument('-z', '--chkp',   metavar='INT',              help='Checkpoint interval')
	g.add_argument('-v', '--jobvar', metavar='STR',              help='TPT Job variable file')
	g.add_argument('--qb', type=QB1.parse, metavar='NAME=VALUE', nargs='*', help='QUERY_BAND information')
	g.add_argument('--no-trunc', dest='trunc', action='store_false',  help='Assume tables to be empty; do not generate SQL to truncate tables')
	g.add_argument('--trunc-sql',    metavar='SQL', default='DELETE FROM {name}', help='Custom SQL for truncating table')
	g.add_argument('--stats',        action='store_true',        help='Collect stats after load')
	g.add_argument('--run',          action='store_true',        help='Run the resulting TPT script (only on Linux)')
	g.add_argument('--auth', type=AuthArg, metavar='AUTH',       help=AuthArg.__doc__)
	g.add_argument('--counts',       action='store_true',        help='Capture and show counts after TPT job run')

	g = p.add_argument_group('Source options')
	x = g.add_mutually_exclusive_group()
	x.add_argument('--td', nargs='?', type=AuthArg, metavar='AUTH', const=True, help='Load data from another Teradata system, optional authentication information')
	x.add_argument('--odbc', metavar='CONN', help='Load data from ODBC connection')
	g.add_argument('--src', '-f', metavar='SRC', type=src, help='File name or regex sub expression <match>=<repl>')

	g = p.add_argument_group('File only options')
	g.add_argument('--dirpath', metavar='PATH', default='', help='Directory containing input file(s)')
	g.add_argument('--dlm',    metavar='CHAR/INT', nargs='?', default='', const='09', help='Field delimiter (--dlm with no value defaults to TAB)')
	g.add_argument('--empty', action='store_true', help="Use empty string for missing values")
	g.add_argument('--binary', action='store_const', dest='dlm', const=None, help='Input data is in Teradata BINARY format')
	g.add_argument('--fit',    action='store_true', help='Truncate large data values')
	g.add_argument('--esc',    metavar='CHAR', nargs='?', const='\\', help='Escape for Text delimiter (CHAR --esc with no value defaults to \\)')
	g.add_argument('--skip1', '-1', action='store_true', help='Skip first row')
	x = g.add_mutually_exclusive_group()
	x.add_argument('--quoted', action='store_const',  const='Yes', dest='quote', help="Quoted data")
	x.add_argument('--quote-opt', action='store_const', const='Optional', dest='quote', help="Optionally quoted data")
	g.add_argument('--limits', metavar='SIZE', type=size, default=thresholds, nargs=4,
		help='File size thresholds for choosing consumer operator. Default: {}'.format(' '.join([format(yappt.HumanInt(v),'s') for v in thresholds])))

	g = p.add_argument_group('Load options')
	g.add_argument('-d', '--db','--database',                       help='Default database name')
	g.add_argument('-e', '--errlim', metavar='INT', type=int,       help='Error limit (default 1)')
	g.add_argument('-w', '--tempdb', metavar='DB',                  help='Use named database for creating temporary tables')
	g.add_argument('-p', '--pinst',  metavar='INT', type=Instances, help='Number of producer instances')
	g.add_argument('-c', '--cinst',  metavar='INT', type=Instances, help='Number of consumer instances')

	x = g.add_mutually_exclusive_group()
	x.add_argument('--large',  dest='util_sz', action='store_const', const=UtilSize.LARGE,  help='Use UtilityDataSize=LARGE')
	x.add_argument('--medium', dest='util_sz', action='store_const', const=UtilSize.MEDIUM, help='Use UtilityDataSize=MEDIUM')
	x.add_argument('--small',  dest='util_sz', action='store_const', const=UtilSize.SMALL,  help='Use UtilityDataSize=SMALL')
	x.add_argument('--tiny',   dest='util_sz', action='store_const', const=UtilSize.TINY,   help='Use STREAM operator to load data')
	x.add_argument('--micro',  dest='util_sz', action='store_const', const=UtilSize.MICRO,  help='Use INSERTER operator to load data')

	g = p.add_argument_group('Stream/Inserter only options')
	g.add_argument('-s', '--sess', metavar='INT',   default=None, type=int, help='Number of sessions for STREAM/INSERTER operator')
	g.add_argument('-k', '--pack', metavar='INT',   default=None, type=int, help='Pack factor for STREAM operator')
	g.add_argument('-m', '--macdb', metavar='DB',                           help='Database for creating macros')

	args = p.parse_args()

	return args

def build_job(args):
	"Return TPTJob instance built from command line parameters"
	def src_name(tb):
		s = args.src(str(tb)) if args.src else str(tb)
		if args.odbc:
			return f'SELECT * FROM {s}'
		if args.td:
			return f'LOCK ROW ACCESS SELECT * FROM {s}'
		if args.src:
			return s
		if args.dlm is not None:
			return f'{tb.name}.txt'
		return f'{tb.name}.dat'

	def pop(tb, uz, pinst):
		if args.odbc:
			return OdbcOp(tb, src=src_name, inst=pinst, conn=args.odbc)
		if args.td:
			return ExportOp(tb, src=src_name, inst=pinst, qb=args.qb, util_sz=uz)
		return FileReaderOp(tb, src=src_name, inst=pinst, dirpath=args.dirpath, dlm=args.dlm,
					esc=args.esc, quote=args.quote, empty=args.empty, fit=args.fit, skip1=args.skip1)

	def cop(tb, uz, cinst):
		if uz == UtilSize.MICRO:
			return InserterOp(sess=args.sess, inst=cinst, qb=args.qb)
		if uz == UtilSize.TINY:
			return StreamOp(tb, temp_db=args.tempdb, mac_db=args.macdb,
						pack=args.pack, sess=args.sess, errlim=args.errlim, inst=cinst, qb=args.qb)
		return LoadOp(tb, util_sz=uz, temp_db=args.tempdb, errlim=args.errlim, inst=cinst, qb=args.qb)

	def tb_size(tb):
		from urllib.parse import urlparse
		from tdtypes.tpt.util import path_obj

		if args.util_sz:
			return (args.util_sz, args.pinst, args.cinst)
		if args.odbc:
			return (UtilSize.SMALL, args.pinst, args.cinst)
		if args.td:
			return (UtilSize.MEDIUM, args.pinst, args.cinst)

		if (args.dirpath or args.src) and isinstance(path_obj(args.dirpath, args.src(str(tb))), Path): #local file
			uz, pinst, cinst = file_sizer(src_name(tb), folder=args.dirpath, thresholds=args.limits)
			logger.info('Using UtilSize={} for {}'.format(uz.name,tb))
			return (uz, pinst, cinst)

		return (UtilSize.MEDIUM, args.pinst, args.cinst)

	def make_step(tb):
		uz, pi, ci = tb_size(tb)
		return LoadStep(tb, pop(tb, uz, pi), cop(tb, uz, ci))

	def make_job(tblist):
		job = TPTJob(args.job or tblist[0].name if len(tblist) == 1 else 'TPTLoad')
		if args.td and isinstance(args.td, AuthArg):
			job.varlist.append(args.td.tptvars('Source'))
		if args.auth:
			job.varlist.append(args.auth.tptvars('Target'))

		job.vars['TargetWorkingDatabase'] = args.db
		if args.trunc:
			job.steps.append(DDLStep('TruncAll', tblist, lambda t: args.trunc_sql.format(name=t), qb=args.qb))
		job.steps.extend(make_step(tb) for tb in tblist)
		if args.stats:
			job.steps.append(DDLStep('CollStats', tblist, 'COLLECT STATS ON {}'.format, qb=args.qb, errors=['3624']))
		job.refactor_attrs()

		return job

	return make_job(args.tbl)

def file_sizer(src, folder, thresholds):
	"Recommend utility size and operator instances for given set of files"
	folder = Path(folder) / Path(src).parent
	files = list(folder.glob(Path(src).name))

	if not files:
		logger.warning("No files found '%s'", str(Path(folder) / Path(src)))
		return (UtilSize.MEDIUM, Instances(1), Instances(1))

	if files:
		pinst = max(len(files),1)
		if pinst > 1:
			pinst += 1
	else:
		pinst = 1

	cinst = max(min(4, pinst // 2), 1)

	util_sz = UtilSize.LARGE
	filesz = sum([Path(f).stat().st_size for f in files])
	for e, th in enumerate(thresholds, start=1):
		if filesz < th:
			util_sz = UtilSize(e)
			break

	logger.debug("Looking for '%s' in directory '%s': number of files found=%d, cumulative size=%d, thresholds=%s",
		src, folder, len(files), filesz, thresholds)

	return (util_sz, Instances(pinst), Instances(cinst))

if __name__ == '__main__':
	import sys
	sys.exit(main())
