#!/usr/bin/env python
# -*- coding: latin-1 -*-


import sys, os
import glob
from argparse import ArgumentParser

if __name__ == '__main__':
	parser = ArgumentParser(
				description='Routine to perform the cluster index analysis on different trajectories stored in different folders.'
				, epilog='''Remember to use a distinctive substring in naming the trajectory files. ''') 
	parser.add_argument('-p', '--strPath', help='Path where trajectories are stored.', default='./')
	parser.add_argument('-s', '--trajsubStr', help='trajectory filename', default='')
	args = parser.parse_args()
	
	# Go into the folder containing the trajectories
	# Convert path in absolute path
	strPath = os.path.abspath(args.strPath)
	os.chdir(strPath)

	# Explore the subtree starting from strPath
	for root, dirs, files in os.walk(strPath):
		# For each file
		for file in files:
			# If a trajectory file is found 
			trajFiles = glob.glob(os.path.join(root,args.trajsubStr))
			if len(trajFiles) > 0:
				for trajFile in trajFiles:
					filname = os.path.basename(trajFile)
					filnameNoExt = os.path.splitext(filname)[0]
					print "|- ANALYSING TRAJECTORY ", filname
					# create file names according to the different step of the analysis
					randomHypFileName = filnameNoExt + '.rnd'
					clusterFileName = filnameNoExt + '.clusters'
					clusterNullFileName = filnameNoExt + '.rnd.clusters'
					final_ci_fileName = filnameNoExt + '.ci.final'
					final_nci_fileName = filnameNoExt + '.nci.final'
					final_tci_fileName = filnameNoExt + '.tci.final'
					final_z_fileName = filnameNoExt + '.z.final'
					#### GO INTO THE FOLDER
					print os.path.dirname(os.path.abspath(trajFile))
					os.chdir(os.path.dirname(os.path.abspath(trajFile)))
				
					exeRight = 1
					if os.path.isfile(filname):
						# Random hypotesis creation
						try:
							stringToExecute = '/data/md/tools/script/generic_random_hypothesis.py -s 1 ' + filname + ' > ' + randomHypFileName
							os.python(stringToExecute)
						except:
							print 'ERROR: Problem with generic_random_hypothesis.py generation'	
							exeRight = 0
					
						# Trajectory cluster creation
						if exeRight == 1:
							try:
								stringToExecute = '/data/md/tools/bin/generic_trajectory_clusters ' + filname + ' 1 1000 1 > ' + clusterFileName
								os.python(stringToExecute)
							except:
								print 'ERROR: Problem with generic_trajectory_clusters analysis on trajectory file'	
								exeRight = 0
						
						# Null hypotesis cluster creation
						if exeRight == 1:
							try:
								stringToExecute = '/data/md/tools/bin/generic_trajectory_clusters ' + randomHypFileName + ' 1 1000 0 > ' + clusterNullFileName
								os.python(stringToExecute)
							except:
								print 'ERROR: Problem with generic_trajectory_clusters analysis on null hypotesis'	
								exeRight = 0
						
						# Clustering ordering 
						if exeRight == 1:
							try:
								stringToExecute = '/data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -sci -n30 > ' + final_ci_fileName
								os.python(stringToExecute)
								stringToExecute = '/data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -sn_ci -n30 > ' + final_nci_fileName
								os.python(stringToExecute)
								stringToExecute = '/data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -st_ci -n30 > ' + final_tci_fileName
								os.python(stringToExecute)
								stringToExecute = '/data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -sz -n30 > ' + final_z_fileName
								os.python(stringToExecute)						
							except:
								print 'ERROR: Problem with clustering ranking procedure'	
								exeRight = 0					
						