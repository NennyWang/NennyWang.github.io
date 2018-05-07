# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
DO THE VERY FISRT STEP FOR CONVERTING DICOM FILES INTO NIFTI

edited by Yin-Shan Wang 2016-10-27

email: wangyinshan@psych.ac.cn

"""

# Import required modules
import os
import os.path as op
import argparse
import commands
import shutil
import numpy as np

# Change to script directory
cwd = op.realpath(op.curdir)
scriptdir = op.dirname(op.abspath(__file__))
os.chdir(scriptdir)


#-------------------------------------------- PARSER --------------------------------------------#
parser = argparse.ArgumentParser(description = 'Script to convert DICOM files into NIFTI on PYTHON See the manual for further information')

#Required options
reqoptions = parser.add_argument_group('Required arguments')
reqoptions.add_argument('-s','-subj',dest="subjects_list",required=True, help="subjects list of your exp")
reqoptions.add_argument('-i','-in',dest="in_dir",required=True, help="source directory name")
reqoptions.add_argument('-o','-out',dest="out_dir",required=True, help="target directory name")

print '\n------------------------------- RUNNING DICOM TO NIFTI ------------------------------- '



args = parser.parse_args()
Cancel = False
#setup each input parameters
#subjectlist
subjects_list = args.subjects_list
if not subjects_list:
    print 'Could not find subjects list file. Please make sure to put it together with dcm2nii.py'
    Cancle = True
    
#input dir
input_dir = args.in_dir
if not op.isdir(input_dir):
    print 'Please add the source absolute path \'-i\' argument and make sure its existance'
    Cancel = True

#out_dir
output_dir = args.out_dir
if output_dir:    
    if not op.isdir(output_dir):
        print 'Please check your out put directory.'
        Cancel = True
    else:
        if not op.exists(output_dir):
            os.mkdir(output_dir)
else:
    output_dir=scriptdir

if Cancel:
	print '\n----------------------------- DCM2NII IS CANCELED -----------------------------\n'
	exit()
    
#------------------------------------------- PREPARE -------------------------------------------#
#Turing subjects list into an 1d array
if op.isfile(subjects_list):
    subjects_list = np.loadtxt(subjects_list,dtype=str)
else:
    subjects_list = np.array([subjects_list],dtype=str)
    
#make output dir
for subject in subjects_list:
    target_dir = op.join(output_dir,subject)
    if not op.isdir(target_dir):
        os.mkdir(target_dir)

#LOOP FOR EACH SUBJECT TO CONVERT DICOM INTO NIFTI
for subject in subjects_list:
    print 'Coverting %s\'s DICOM FILE INTO NIFTI'% subject
    target_dir = op.join(output_dir,subject)
    source_dir = op.join(input_dir,subject)
    if op.isdir(source_dir):
        source_dir = op.join(input_dir,subject,'*')
        os.system(' '.join(['dcm2nii','-a y -d n -r y -x y -o',target_dir,source_dir]))
    
    
        
    
    
    
    
 
    
