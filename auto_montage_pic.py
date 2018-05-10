# -*- coding: utf-8 -*-
"""
Created on Thu May 10 15:53:39 2018
@author: Yinshan Wang
"""

#!/usr/bin/env python

# Import required modules
from __future__ import print_function
from skimage import io
import numpy as np
import os
import os.path as op
import argparse
from PIL import Image as im


## basic functions
def find_pixchange(array):
    loc = []
    for i in range(array.shape[0]-1):
        a = array[i]
        b = array[i+1]
        if a!=b:
            loc.append(i)
    return loc

def find_loc(fname,hemi='lh'):
    img=io.imread(fname,as_grey=True)
    loc={'lateral':[0,0,0,0],'medial':[0,0,0,0],'anterior':[0,0,0,0],'posterior':[0,0,0,0],'colormap':[0,0,0,0],'dorsal':[0,0,0,0],
            'ventral':[0,0,0,0]}

    #locate colorbar
    y_cmp = img.sum(axis=1)
    y_bin = np.where(y_cmp==img.shape[1],0,1)
    y_cp=find_pixchange(y_bin)
    
    img_nocm,img_cm = img[:y_cp[2],:],img[y_cp[2]:y_cp[-1],:]
    
    #assign know labels to loc
    loc['dorsal'][1]=y_cp[0]
    loc['ventral'][3]=y_cp[1]
    loc['colormap'][1]=y_cp[2]
    loc['colormap'][3]=y_cp[-1]
    
    #draw colormap
    x_cmp_cm = img_cm.sum(axis=0)
    x_cm_bin = np.where(x_cmp_cm==img_cm.shape[0],0,1)
    cm_x_cp = find_pixchange(x_cm_bin)
    loc['colormap'][0]=cm_x_cp[0]
    loc['colormap'][2]=cm_x_cp[1]
    
    #draw x border of different views
    x_cmp_img = img_nocm.sum(axis=0)
    x_img_bin = np.where(x_cmp_img==img_nocm.shape[0],0,1)
    img_x_cp = find_pixchange(x_img_bin)
    #cut lm view
    img_lm = img_nocm[:,:img_x_cp[2]]
    y_cmp_lm = img_lm.sum(axis=1)
    y_lm_bin = np.where(y_cmp_lm==img_lm.shape[1],0,1)
    img_lm_cp = find_pixchange(y_lm_bin)
    if hemi=='lh':
        loc['lateral']=[img_x_cp[0]-1,img_lm_cp[0]-1,img_x_cp[1]+2,img_lm_cp[1]+8]
        loc['medial']=[img_x_cp[0]-1,img_lm_cp[2]-1,img_x_cp[1]+2,img_lm_cp[3]+8]
    else:
        loc['medial']=[img_x_cp[0]-1,img_lm_cp[0]-1,img_x_cp[1]+2,img_lm_cp[1]+8]
        loc['lateral']=[img_x_cp[0]-1,img_lm_cp[2]-1,img_x_cp[1]+2,img_lm_cp[3]+8]
    #cut ap view
    img_ap=img_nocm[:,img_x_cp[3]:]
    y_cmp_ap = img_ap.sum(axis=1)
    y_ap_bin = np.where(y_cmp_ap==img_ap.shape[1],0,1)
    img_ap_cp = find_pixchange(y_ap_bin)
    loc['anterior']=[img_x_cp[4]-1,img_ap_cp[0]-1,img_x_cp[5]+2,img_ap_cp[1]+2]
    loc['posterior']=[img_x_cp[4]-1,img_ap_cp[2]-1,img_x_cp[5]+2,img_ap_cp[3]+2]
    
    
    #cut dv view so that can compare each view's y loc
    img_dv = img_nocm[:,img_x_cp[2]:img_x_cp[3]]
    y_cmp_dv = img_dv.sum(axis=1)
    y_dv_bin = np.where(y_cmp_dv==img_dv.shape[1],0,1)
    img_dv_cp = find_pixchange(y_dv_bin)
    loc['dorsal']=[img_x_cp[2]-1,img_dv_cp[0]-1,img_x_cp[3]+2,img_dv_cp[1]+2]
    loc['ventral']=[img_x_cp[2]-1,img_dv_cp[2]-1,img_x_cp[3]+2,img_dv_cp[3]+2]
    return loc

def resize_images(images,template_image):
    images_re=images
    for key,value in images.items():
        size=template_image[key].size
        resized=images[key].resize(size)
        images_re[key]=resized
    return images_re

def montage_images(im1,im2,direct='x'):
    width=[im1.size[0],im2.size[0]]
    height=[im1.size[1],im2.size[1]]
    if direct=='x':
        total_width=sum(width)
        max_height=max(height)
        new_im = im.new('RGB',(total_width,max_height))
        new_im.paste(im1,(0,0));new_im.paste(im2,(im1.size[0],0))
    elif direct=='y':
        max_width=max(width)
        total_height=sum(height)
        new_im = im.new('RGB',(max_width,total_height))
        new_im.paste(im1,(0,0));new_im.paste(im2,(0,im1.size[1]))
    return new_im

parser = argparse.ArgumentParser(description='Script to montage images from')


# Required options                    
reqoptions = parser.add_argument_group('Required arguments')
reqoptions.add_argument('-o', '-out', dest="outDir", required=True, help='Output directory name')
reqoptions.add_argument('-lh', '-l', dest="left", required=True, help='full path name of left hemi pic')
reqoptions.add_argument('-rh', '-r', dest="right", required=True, help='full path name of right hemi pic')


## Optional options
optoptions = parser.add_argument_group('Optional arguments')
optoptions.add_argument('-i', '-in', dest="inDir", required=True, help='Input directory name')

print('\n------------------------------- MONTAGING PICTURES ------------------------------- ')


#parser
args = parser.parse_args()


output_dir=args.outDir
if args.inDir:
    input_dir=args.inDir
    lh_name=args.left
    rh_name=args.right
    flh=op.join(input_dir,lh_name)
    frh=op.join(input_dir,rh_name)
else:
    flh=args.left
    rh=args.right


view_names = ['lateral','medial','anterior','posterior','colormap','dorsal','ventral']
view_names_sec = ['lm','dv','ap','lmlh','lmrh']

if not op.isdir(output_dir):
    print("Fatel Error %s is not a directory"%output_dir)
    exit()
else:
    print("Starting montage image .......")
    os.mkdir(output_dir+'/montaged')

if not op.isfile(flh) or not op.isfile(frh):
    print("%s or %s is not a picture.please chekc and add the full path of your pic in"%(flh,frh))
    exit()

lh_loc=find_loc(flh,hemi='lh')
rh_loc=find_loc(flh,hemi='rh')
#crop images and save into a list
lh_im=im.open(flh)
lh_images={key:lh_im.crop(box=value) for key,value in lh_loc.items()}
rh_im=im.open(frh)
rh_images={key:rh_im.crop(box=value) for key,value in rh_loc.items()}
lh_images_resized=resize_images(lh_images,rh_images)

montaged_images={}
for key in view_names:
    if key != 'anterior': 
        im_montaged = montage_images(lh_images_resized[key],rh_images[key])
    elif key=='colormap':
        im_montaged = lh_images_resized[key]
    else:
        im_montaged = montage_images(rh_images[key],lh_images_resized[key])
    fnames = op.join(output_dir,'montaged/%s.png'%key)
    im_montaged.save(fnames)
    montaged_images[key]=im_montaged
    
#lm view   
fnames = op.join(output_dir,'montaged/lm.png')
lm_view = montage_images(montaged_images['lateral'],montaged_images['medial'],'y')
lm_view.save(fnames)

#dv view
fnames = op.join(output_dir,'montaged/dv.png')
dv_view = montage_images(montaged_images['dorsal'],montaged_images['ventral'],'y')
dv_view.save(fnames)

# ap view
fnames = op.join(output_dir,'montaged/ap.png')
ap_view = montage_images(montaged_images['anterior'],montaged_images['posterior'])
ap_view.save(fnames)

#lmlr
fnames = op.join(output_dir,'montaged/lmlr.png')
lmlh_view = montage_images(lh_images_resized['lateral'],lh_images_resized['medial'])
lmrh_view = montage_images(rh_images['lateral'],rh_images['medial'])
lmlr_view = montage_images(lmlh_view,lmrh_view)
lmlr_view.save(fnames)

print("Done")
