# -*- coding: utf-8 -*-
"""
Created on Mon May  7 08:52:00 2018

@author: King of Chiji
"""

import os
import os.path as op
from PIL import Image as im


workdir='E:/Projects/XiNian_Zuo/psready/'
conditions=os.listdir(workdir)
conditions=[x for x in conditions if op.isdir(workdir+x)]

#for condi in conditions:
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


# change the specific loc for diff pics this one is applyed for 3333*3333     
lh_loc={'lateral':(180,255,180+980,255+690),'medial':(180,1355,180+980,1355+690),'anterior':(2173,259,2173+390,259+682),
        'posterior':(2173,1359,2173+390,1359+682),'colormap':(1155,2950,1155+1015,2950+155),'dorsal':(1410,98,1410+512,98+1302),
        'ventral':(1410,1433,1410+512,1433+1302)}
rh_loc={'lateral':(180,1350,180+980,1350+700),'medial':(180,250,180+980,250+700),'anterior':(2175,250,2175+395,250+700),
        'posterior':(2175,1350,2175+395,1350+700),'colormap':(1155,2950,1155+1015,2950+155),'dorsal':(1405,100,1405+525,100+1300),
       'ventral':(1405,1433,1405+525,1433+1300)}
view_names = ['lateral','medial','anterior','posterior','colormap','dorsal','ventral']
view_names_sec = ['lm','dv','ap','lmlh','lmrh']


#loop for each folder 
for i in range(len(conditions)):
    workpath=workdir #op.join(workdir,conditions[i])
    if not op.isdir(workpath+'/montaged'): os.mkdir(workpath+'/montaged',555)
    
    #if there are more than 2 pics in a folder write a looop here
    flh=op.join(workpath,'Yeo2011.7networks.lh.png')
    frh=op.join(workpath,'Yeo2011.7networks.rh.png')
    
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
        fnames = op.join(workpath,'montaged/%s.png'%key)
        im_montaged.save(fnames)
        montaged_images[key]=im_montaged
        
    #lm view   
    fnames = op.join(workpath,'montaged/lm.png')
    lm_view = montage_images(montaged_images['lateral'],montaged_images['medial'],'y')
    lm_view.save(fnames)
    
    #dv view
    fnames = op.join(workpath,'montaged/dv.png')
    dv_view = montage_images(montaged_images['dorsal'],montaged_images['ventral'],'y')
    dv_view.save(fnames)
    
    # ap view
    fnames = op.join(workpath,'montaged/ap.png')
    ap_view = montage_images(montaged_images['anterior'],montaged_images['posterior'])
    ap_view.save(fnames)
    
    #lmlr
    fnames = op.join(workpath,'montaged/lmlr.png')
    lmlh_view = montage_images(lh_images_resized['lateral'],lh_images_resized['medial'])
    lmrh_view = montage_images(rh_images['lateral'],rh_images['medial'])
    lmlr_view = montage_images(lmlh_view,lmrh_view)
    lmlr_view.save(fnames)