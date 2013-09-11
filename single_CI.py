#!/usr/bin/env python
# -*- coding: latin-1 -*-


import sys, os
import glob
import ci_library as cil
from argparse import ArgumentParser

# Input parameters definition 
if __name__ == '__main__':
	parser = ArgumentParser(
				description='Perform the cluster index analysis on one trajectory.'
				, epilog='''The analysis depends on several files available only on Cesena server. ''') 
	parser.add_argument('-f', '--trajFile', help='trajectory file handle', default='')
	parser.add_argument('-e', '--sampleType', type=int, help='Sampling method, normal or GA', default=0)
	args = parser.parse_args()

	print "|- Sampling Method: ", args.sampleType	
	print "|- File to analyse: ", args.trajFile
	strPath = os.path.abspath(os.path.dirname(args.trajFile))
	print "|- File Path: ", strPath
	cil.clusterIndexComputation(tmpStrPath=strPath,tmpTrajFile=args.trajFile,tmpSamplingMethod=args.sampleType)
