print
print
print
print
print
print
print
print
print
print
print
print

print "Start"	

from pylab import *
from decimal import Decimal
import os
import subprocess
from fnmatch import fnmatch
from scipy import fftpack
from scipy import optimize
from datetime import datetime
print "Done importing stuff."

#subprocess.call("start_xray")

def getFilePaths(superpath = "/scratch/janna/project_data", pattern = 'FS46*.gz', get_obs_ids=False):
	# FS46*,gz for standard 1 data, FS37*.gz for event data, *.lc.txt for lightcurve ascii files
	# NOTE: filepaths now without file at the end, only directory.
	filepaths = []
	filenames = []
	
	if get_obs_ids:
		obs_ids = []
	
	for dirpath, dirnames, files in os.walk(superpath):
		for f in files:
			if fnmatch(f, pattern):
				filepath = os.path.join(superpath, dirpath)
				filepaths.append(filepath)
				filenames.append(f)
				if get_obs_ids:
					obs_ids.append(dirpath[len(superpath) + 1:-4])
			
	print len(filepaths), "files found in ", superpath

	if get_obs_ids:
		return filepaths, filenames, obs_ids
	else:
		return filepaths, filenames


def runsaextrct(filepath, filename, binwidth = "0.1"):
	os.chdir(str(filepath))
	print "changed directory to: "
	os.system('pwd')

	full_filepath = os.path.join(filepath, filename)
	extract_filename = filename + "_extract"
	
	extract_args = ["saextrct", full_filepath, "APPLY", "-", extract_filename, "ONE", "TIME", "GOOD", binwidth, "lightcurve", "RATE", "SUM", \
"INDEF", "INDEF", "INDEF", "INDEF", "INDEF", "INDEF", "INDEF"]
	subprocess.call(extract_args)
	extract_out = os.path.join(filepath, extract_filename)
	extract_out += ".lc"

	columns_in = extract_out
	columns_args = ["flcol", columns_in]
	subprocess.call(columns_args)

	#plot_in = extract_out
	#plot_args = ["fplot", plot_in, "TIME", "RATE", "-", "/XW", "offset=yes", "NONE"]
	#subprocess.call(plot_args)

	dump_in = extract_out
	dump_out = dump_in + ".txt"
	dump_args = ["fdump", dump_in, dump_out, "TIME, RATE", "-", "prhead=no", "showcol=no", "showunit=no", "showrow=no"]
	subprocess.call(dump_args)


def runseextrct(filepath, filename, binwidth = "0.1"):
	os.chdir(str(filepath))
	print "changed directory to: "
	os.system('pwd')

	full_filepath = os.path.join(filepath, filename)
	extract_filename = filename + "_extract"

	extract_args = ["seextrct", full_filepath, "APPLY", "-", extract_filename, "TIME", "Event", binwidth, "lightcurve", "RATE", "SUM", \
"INDEF", "INDEF", "INDEF", "INDEF", "INDEF", "INDEF", "INDEF"]
	subprocess.call(extract_args)
	extract_out = os.path.join(filepath, extract_filename)
	extract_out += ".lc"

	columns_in = extract_out
	columns_args = ["flcol", columns_in]
	subprocess.call(columns_args)

	dump_in = extract_out
	dump_out = dump_in + ".txt"
	dump_args = ["fdump", dump_in, dump_out, "TIME, RATE", "-", "prhead=no", "showcol=no", "showunit=no", "showrow=no"]
	subprocess.call(dump_args)
	

def getData(filepath, filename, starttime):
	print "loading data from file: ", filename, "..."

	full_filepath = os.path.join(filepath, filename)
	datafile = open(full_filepath, 'rb')
	TIME = []
	RATE = []

	for row in datafile:
		entries = row.split()
		if len(entries) > 0:
			#print "entries ", entries
			#print "Time ", entries[0], type(entries[0])
			TIME.append(Decimal(entries[0]) - starttime)
			#print "Rate ", entries[1], type(entries[1])
			#print Decimal(entries[1])	
			RATE.append(Decimal(entries[1]))

	return TIME, RATE


# TAI-UTC dictionary:
tai_utc_dict = {}
tai_utc_filepath = "/scratch/janna/tai-utc.dat"
tai_utc_file = open(tai_utc_filepath, 'rb')

for row_t in tai_utc_file:
	entries_t = row_t.split()

	JD_date = Decimal(entries_t[4])
	number1 = Decimal(entries_t[6])
	number2 = Decimal(entries_t[11][:-2])
	number3 = Decimal(entries_t[13])
	
	MJD_date = JD_date - Decimal("2400000.5")
	tai_min_utc = number1 + (MJD_date - number2) * number3
	tai_utc_dict[MJD_date] = tai_min_utc
	

def MJD_UTC_to_MET_TT(MJD_UTC):
	# Tested this function, it's ok!
	MJD_UTC = Decimal(str(MJD_UTC))

	MJD_dates = array(sorted(tai_utc_dict.keys()))
	MJD_date = MJD_dates[MJD_dates.searchsorted(MJD_UTC) - 1]
	tai_min_utc = tai_utc_dict[MJD_date]

	RXTE_zero = Decimal("49353.00073567628")
	TT_TAI = Decimal("32.184")
	MET_TT = (MJD_UTC - RXTE_zero) * 3600 * 24 + tai_min_utc + TT_TAI
	return MET_TT


# obs-ids dictionary:
obs_ids_dict = {}
obs_ids_filepath = "/scratch/janna/obs_ids_Tullio.txt"
obs_ids_file = open(obs_ids_filepath, 'rb')

for row_o in obs_ids_file:
	entries_o = row_o.split()
	obs_id = entries_o[0]
	starttime_MJD = Decimal(entries_o[1])
	starttime_MET = MJD_UTC_to_MET_TT(starttime_MJD)
	obs_ids_dict[obs_id] = starttime_MET


def plotLightcurves(filepath, filename, obs_id, binwidth = "0.1", make_figs = True):
	starttime = Decimal(obs_ids_dict[obs_id])
	print "start time: ", starttime, type(starttime)
	TIME, RATE = getData(filepath, filename, starttime)
	
	if make_figs:
		title_ = "Lightcurve of burst " + str(obs_id) + ", file " + str(filename[:-17])
		x_label = "time (s) rel. to starttime " + str(starttime) + " MET"
		y_label = "photon counts per " + binwidth + " s"
		figpath = os.path.join(filepath, filename)
		figpath1 = figpath[:-7] + "_plot.png"
		print figpath

		plot(TIME, RATE)
		title(title_)
		xlabel(x_label)
		ylabel(y_label)
		ylabel(y_label)
		savefig(figpath1)
		close()

	start_index = searchsorted(array(TIME), -50)
	end_index = searchsorted(array(TIME), 200)
	
	if make_figs:
		title2_ = "Zoomed l" + title_[1:]
		figpath2 = figpath[:-7] + "_zoom_plot.png"

		plot(TIME[start_index:end_index], RATE[start_index:end_index])
		title(title_)
		xlabel(x_label)
 		ylabel(y_label)
 		ylabel(y_label)
		savefig(figpath2)
		close()

	zoom_filepath = os.path.join(filepath, filename)
	zoom_filepath = zoom_filepath[:-4] + "_zoom.txt"
	zoom_file = open(zoom_filepath, 'w+')
	for i in range(start_index, end_index):
		row = str(TIME[i]) + " " + str(RATE[i])
		zoom_file.write(row)
	zoom_file.close()

	
def do_stuff(datatype, make_figures = True):

	if datatype == 1:
		gz_pattern = "FS46*.gz"
		txt_pattern = "FS46*.txt"
		binwidth = "0.1"

	elif datatype == 2:
		gz_pattern = "FS37*.gz"
		txt_pattern = "FS37*.txt"
		binwidth = "0.1"

	else:
		print "Invalid datatype, choose 1 for standard1 data and 2 for event data."
		return

	extract_errorlist = []
	extract_errorlist_paths = []
	obs_id_errorlist = []
	plot_errorlist = []
	plot_errorlist_obs_ids = []

	filepaths_gz, filenames_gz = getFilePaths(pattern = gz_pattern)

	assert len(filepaths_gz) == len(filenames_gz)

	for i in range(len(filepaths_gz)):
		filepath = filepaths_gz[i]
		filename = filenames_gz[i]
		try:
			if datatype == 1:
				runsaextrct(filepath, filename, binwidth)
			elif datatype == 2:
				runseextrct(filepath, filename, binwidth)
		except:
			print "An error occured in file ", filename
			extract_errorlist.append(filename)
			extract_errorlist_paths.append(filepath)

	filepaths_txt, filenames_txt, obs_ids = getFilePaths(pattern = txt_pattern, get_obs_ids=True)

	assert len(filepaths_txt) == len(filenames_txt) == len(obs_ids)

	for i in range(len(filepaths_txt)):
		filepath = filepaths_txt[i]
		filename = filenames_txt[i]
		try:
			obs_id = obs_ids[i]
		except: 
			print "obs id ", obs_id, " not in dictionary"
			obs_id_errorlist.append(obs_id)

		#plotLightcurves(filepath, filename, obs_id, make_figs = make_figures)
		try:
			plotLightcurves(filepath, filename, obs_id, make_figs = make_figures)
		except: 
			print "An error occured in plotting file ", filename
			plot_errorlist.append(filename)
			plot_errorlist_obs_ids.append(obs_id)

	print "Done :D"

	print
	print "Errors in saextrct part in files: "
	for i in range(len(extract_errorlist)):
		print "file: ", extract_errorlist[i]
		print "in directory: ", extract_errorlist_paths[i]

	print
	print "obs-ids not in list: "
	for obs_id_err in obs_id_errorlist:
		print obs_id_err

	print
	print "Errors in plot part in files: "
	for i in range(len(plot_errorlist)):
		print "File: ", plot_errorlist[i]
		print "	with obs id: ", plot_errorlist_obs_ids[i]

def do_stuff_event_data():

	filepaths, filenames = getFilePaths(pattern = "FS37*.gz")
	assert len(filepaths) == len(filenames)

	maxfrequency = 1000
	binwidth = 1 / Decimal(2 * maxfrequency)
	binwidth = str(binwidth)

	for i in range(len(filepaths)):
		runsaextrct(filepaths[i], filenames[i], binwidth)


do_stuff(2)



def remove_stuff():
	filepaths_rm, filenames_rm = getFilePaths(pattern = "*.gz_extract*")
	print filenames_rm
	for i in range(len(filepaths_rm)):
		full_path_rm = os.path.join(filepaths_rm[i], filenames_rm[i])
		rm_args = ["rm", full_path_rm]
		subprocess.call(rm_args)



	
	



