#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Cluster index functions library
# Functions contained in this file are strictly dipentent to the cluster index analysis binary file present on the 
# server placed in Cesena


import sys, os
import glob

def clusterIndexComputation(tmpStrPath='',tmpTrajFile='handmade.traj',tmpFilesNumber=1,tmpSamplingMethod=0):
	# File name extraction and extension removing 
				if strPath != '':
					strPath = os.path.abspath(tmpStrPath)
					os.chdir(tmpStrPath)
				filname = os.path.basename(tmpTrajFile)
				filnameNoExt = os.path.splitext(filname)[0]
				# Compute the analysis progress 
				percentage = count / tmpFilesNumber * 100
				print "|- ANALYSING TRAJECTORY ", filname, ' ', percentage, '% completed'
				# create file names according to the different steps of the analysis
				randomHypFileName = filnameNoExt + '.rnd'
				clusterFileName = filnameNoExt + '.clusters'
				clusterNullFileName = filnameNoExt + '.rnd.clusters'
				final_ci_fileName = filnameNoExt + '.ci.final'
				final_nci_fileName = filnameNoExt + '.nci.final'
				final_tci_fileName = filnameNoExt + '.tci.final'
				final_z_fileName = filnameNoExt + '.z.final'
				#### GO INTO THE FOLDER
				os.chdir(os.path.dirname(os.path.abspath(trajFile)))
			
				exeRight = 1
				if os.path.isfile(filname):
					# Random hypotesis creation
					if os.path.isfile('/data/md/tools/script/generic_random_hypothesis.py'):
						try:
							stringToExecute = 'python /data/md/tools/script/generic_random_hypothesis.py -s 1 ' + filname + ' > ' + randomHypFileName
							print '\t|- Executing ', stringToExecute
							os.system(stringToExecute)
						except:
							print 'ERROR: Problem with generic_random_hypothesis.py generation'	
							exeRight = 0
				
					# Trajectory cluster creation
					if tmpSamplingMethod == 0:
						if os.path.isfile('/data/md/tools/bin/generic_trajectory_clusters'):
							if exeRight == 1:
								try:
									stringToExecute = '/data/md/tools/bin/generic_trajectory_clusters ' + filname + ' 1 1000 1 > ' + clusterFileName
									print '\t|- Executing ', stringToExecute
									os.system(stringToExecute)
								except:
									print 'ERROR: Problem with generic_trajectory_clusters analysis on trajectory file'	
									exeRight = 0
					
							# Null hypotesis cluster creation
							if exeRight == 1:
								try:
									stringToExecute = '/data/md/tools/bin/generic_trajectory_clusters ' + randomHypFileName + ' 1 1000 0 > ' + clusterNullFileName
									print '\t|- Executing ', stringToExecute
									os.system(stringToExecute)
								except:
									print 'ERROR: Problem with generic_trajectory_clusters analysis on null hypotesis'	
									exeRight = 0
					else:
						if os.path.isfile('/data/stewie/workspace/md/bin/max_ci'):
							if exeRight == 1:
								try:
									stringToExecute = '/data/stewie/workspace/md/bin/max_ci ' + filname + ' popsize 100 timeout 1800 ngen 500 prepl 0.9 nconv 100 >> ' + clusterFileName
									print '\t|- Executing ', stringToExecute
									os.system(stringToExecute)
								except:
									print 'ERROR: Problem with max_ci analysis on trajectory file'	
									exeRight = 0
					
							# Null hypotesis cluster creation
							if exeRight == 1:
								try:
									stringToExecute = '/data/md/tools/bin/generic_trajectory_clusters ' + randomHypFileName + ' 1 1000 0 > ' + clusterNullFileName
									print '\t|- Executing ', stringToExecute
									os.system(stringToExecute)
								except:
									print 'ERROR: Problem with generic_trajectory_clusters analysis on null hypotesis'	
									exeRight = 0					
					
					# Clustering ordering 
					if os.path.isfile('/data/md/tools/script/sorted_clusters.py'):
						if exeRight == 1:
							try:
								stringToExecute = 'python /data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -sci -n30 > ' + final_ci_fileName
								print '\t|- Executing ', stringToExecute
								os.system(stringToExecute)
								stringToExecute = 'python /data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -sn_ci -n30 > ' + final_nci_fileName
								print '\t|- Executing ', stringToExecute
								os.system(stringToExecute)
								stringToExecute = 'python /data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -st_ci -n30 > ' + final_tci_fileName
								print '\t|- Executing ', stringToExecute
								os.system(stringToExecute)
								stringToExecute = 'python /data/md/tools/script/sorted_clusters.py ' + clusterFileName + ' ' + clusterNullFileName + ' -sz -n30 > ' + final_z_fileName
								print '\t|- Executing ', stringToExecute
								os.system(stringToExecute)						
							except:
								print 'ERROR: Problem with clustering ranking procedure'	
								exeRight = 0	