#!/usr/bin/python

import sys
import argparse
import os
import re
import glob

def main(argv):
	parser = argparse.ArgumentParser(description="Parse all files in directory for credentials from responder")
	parser.add_argument('-i', '--inputfile', help='The folder with the txt outputs')
	parser.add_argument('-o', '--outputfile', help='The output filename')
	parser.add_argument('-n', '--noheaders', action='store_true', help='This flag removes the header from the CSV output File')
	args = parser.parse_args()
	
	outputfile = "ResponderOutput.csv"
	if(args.outputfile!=None):
		outputfile = args.outputfile
	fo = open(outputfile, 'w+')
	if(args.noheaders != True):
		out = "Username,Domain,Password,Method,IP Address, \n"
		fo.write (out)
	ext = '*.txt'
	if(args.inputfile!=None):
		if(args.inputfile.endswith(os.sep)):
			folder = args.inputfile
		else:
			folder = args.inputfile + os.sep
	ext = folder + ext
	folderl = len(folder)
	method = "Responder"
	ip = ""
	username = ""
	domain = ""
	password = ""
	filecount = pwcount = 0
			
	for filename in glob.glob(ext):
		filecount += 1
		fi = open(filename, 'r+')
		
		#ip = regex to get IP address
		ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', filename )
		
		if(filename[folderl:folderl+10] == "HTTP-Clear"):
			for line in fi.readlines():
				line = line.split(':')
				if(len(line) >1):
					username = line[0].split('\\')
					if(len(username) >1):
						domain = username[0]
						if(domain == '.'):
							domain = "localhost"
						username = username[1]
						password = line[1].strip()
						pwcount += 1
						fo.write(username + ',' + domain  + ',' + password  + ',' + method  + ',' + ip[0] + '\n')
		elif(filename[folderl:folderl+9] == "HTTP-NTLM"):
			for line in fi.readlines():
				line = line.split('::')
				if(len(line) >1):
					username = line[0]
					password = line[1].strip()
					domain = ""
					pwcount += 1
					fo.write(username + ',' + domain  + ',' + password  + ',' + method  + ',' + ip[0] + '\n')
		elif(filename[folderl:folderl+3] == "SMB"):
			for line in fi.readlines():
				line = line.split('::')
				if(len(line) >1):
					username = line[0]
					temp = line[1].find(':')
					domain = line[1][:temp]
					if(domain == '.'):
							domain = "localhost"
					password = line[1][temp:].strip()
					pwcount += 1
					fo.write(username + ',' + domain  + ',' + password  + ',' + method  + ',' + ip[0] + '\n')
				
		fi.close()
		
	fo.close()
	print(str(filecount) + " file(s) processed.  " + str(pwcount) + " passwords found")
	
if __name__ == "__main__":
   main(sys.argv)
