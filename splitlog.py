#!/usr/bin/python
import sys
import os
import string
import getopt
import types
#import xreadlines
import re

def usage():
	print "Usage :"
	print "-c configfile , --config=configfile : Read config from file (syntax : logfile:hosttomatch)"
	print "-d dir , --outputdir=dir            : Set output directory (default '.')"
	print "-i inputfile, --inputfile=logfile   : Set input file"
	print "-r regex, --regex=regex             : Regex to use for matching host (backreference 1 must be the name of the virtualhost). Default : '.* ([a-zA-Z0-9-_.]+)$'"
	print "-h , --help                         : Print this help page"

def parsearg():
	config = {}
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:c:d:r:", ["help", "inputfile=", "config=", "outputdir=", "regex="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	config["configfile"] = None
	config["outputdir"] = "."
	config["inputfile"] = sys.stdin
	config["regex"] = ".* ([a-zA-Z0-9-_.]+)$" 
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		if o in ("-c", "--config"):
			f=open(a)
			config["configfile"]=f.readlines()
			f.close()
		if o in ("-d", "--outputdir"):
			config["outputdir"] = a
		if o in ("-i", "--inputfile"):
			config["inputfile"] = open(a)
		if o in ("-r", "--regex"):
			config["regex"] = a
	if config["configfile"] == None:
		usage()
		sys.exit()
	return config

def regroupsplit (chaine):
	tmp = string.split(string.strip(chaine),":")
	if logfiles.has_key(tmp[0]):
		logfiles[tmp[0]].append(tmp[1])
	else:
		logfiles[tmp[0]] = [tmp[1]]

def openfile (logfiles):
	for f in logfiles.keys():
		fi = open(config["outputdir"]+"/"+f,"a+")
		logfiles[fi] = logfiles[f]
		del logfiles[f]
		for k in logfiles[fi]:
			if filekeys.has_key(k):
				filekeys[k] = filekeys[k] + [fi]
			else:
				filekeys[k] = [fi]

def closefile (logfiles):
	for f in logfiles.keys():
		if type(f) is types.FileType:
			f.close()

config=parsearg()
logfiles={}
filekeys={}
map(regroupsplit, config["configfile"])
openfile(logfiles)
i=0
reg=re.compile(config["regex"])
for line in config["inputfile"]:
	try:
		tmp = reg.match(line).group(1)
		if filekeys.has_key(tmp):
			domain = tmp
		else:
			domain = "__DEFAULT__"
	except AttributeError:
		domain = "__DEFAULT__"
	for f in filekeys[domain]:
		f.write(line)
	i = i + 1
	if (i%10000 == 0):
		print "%d records ..."%i

print "%d record : Ok"%i
closefile(logfiles)
config["inputfile"].close()
