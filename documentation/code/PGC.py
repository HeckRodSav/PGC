#!/usr/bin/python3

from PGC_functions import *
from image_list import img_array_names_filtered as img_array_names

import signal


plt.rcParams.update({'figure.max_open_warning': 0})

CHECK_VARIANTS = True
VERB_ALL = False
VERB_LIST = True
PLOT_ALL = False
PLOT_MIDDLE = False
TEST_ALL = True
ONLINE_CHECK = True
WAIT_TO_NEXT = False
LOG_FILE = True
BAIXAR_BULA = True

keepGoing = True

is_raw = ''

def sigQuit(signal, frame):
	global keepGoing
	if not keepGoing: exit(0)
	keepGoing = False

signal.signal(signal.SIGINT, sigQuit)

index_range = range(len(img_array_names))

if len(sys.argv) >= 2:
	if sys.argv[1] == 'raw':
		CHECK_VARIANTS = False
		is_raw = '_raw'
	else:
		index = int(sys.argv[1])
		index_range = range(index, len(img_array_names))

if len(sys.argv) >= 3:
	index = int(sys.argv[1])
	if sys.argv[2] == 'raw':
		CHECK_VARIANTS = False
		is_raw = '_raw'
	else:
		index_range = range(index, int(sys.argv[2])+1)

if len(sys.argv) >= 4:
	if sys.argv[3] == 'raw':
		CHECK_VARIANTS = False
		is_raw = '_raw'

t = time.time()

logTitle = time.strftime(f'./logs/%Y-%m-%d{is_raw}.log', time.localtime(t))

logFile = None
if LOG_FILE:
	logFile = open(logTitle, 'a+')
	print(logTitle, file=logFile)
	print(f'range: [{index_range.start}, {index_range.stop})', file=logFile)
	print(file=logFile, flush=True)

print()

times = []

for i in index_range:
	delay = pgc(
		i,
		img_array_names,
		logFile=logFile,
		check_variants=CHECK_VARIANTS,
		verb_all=VERB_ALL,
		plot_all=PLOT_ALL,
		test_all=TEST_ALL,
		plot_middle=PLOT_MIDDLE,
		verb_list=VERB_LIST,
		online_check=ONLINE_CHECK,
		baixa_bula=BAIXAR_BULA)

	times.append(delay)

	if WAIT_TO_NEXT: input(f"Enter para prosseguir")

	print('\n'+('-'*80)+'\n', flush=True)
	if(logFile): print('\n'+('-'*80)+'\n', file=logFile)

	if logFile: print(file=logFile, flush=True, end='')
	if logFile: # Forçar salvamento do log
		logFile.flush()
		os.fsync(logFile.fileno())
	if not keepGoing:
		print('saída com sigInt	\n')
		break

print(f"{sum(times) / len(times):.3f}")

input(f"Enter para encerrar")
