
import os
import matplotlib.pyplot as plt
import numpy as np
import json
import caffe
import scipy.misc

from cffi import FFI
from sys import exit, platform
import cv2

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import detectlib.utils as utl
import detectlib.visualizationutl as view
import detectlib.imageutl as imutl
import detectlib.netutility as netutl

import colorchecker
import utils

from argparse import ArgumentParser

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

CAMDEVICE = 0; # camera device number
BORDER = 0;


def arg_parser():
    
    parser = ArgumentParser();    
    parser.add_argument('--configurate',
            dest='configurate', help='configurate file',
            required=True, metavar='C')
    parser.add_argument('--no-gpu', help='no used gpu',
            dest='bgpu', action='store_false')     
    parser.add_argument('--json', help='write json',
            dest='bjson', action='store_true') 
    parser.add_argument('--no-show', help='not show display',
            dest='bshow', action='store_false' )    
    parser.add_argument('--draw-cam', help='draw camera',
            dest='bdrawcam', action='store_true' )    
    parser.add_argument('--camdevice',
            dest='camdevice', help='camera device', type=int,
            metavar='N', default=CAMDEVICE)       
    parser.add_argument('--border',
            dest='border', help='border',  type=int,
            metavar='N', default=BORDER)            
    return parser;
    


def mccfindnet( 
    pathconfig,
    bgpu,
    bshow,
    bjson,
    bdrawcam,
    camdevice,
    border,
    ):
    
    # load configurate
    config = netutl.loadconfig( pathconfig );
    modelpath  = str(config['netpath']);
    modelproto = str(config['netproto']);    
    modelcaffe = str(config['netmodel']);
    imagesize = config['image_dimensions'];
    
    # camera device
    cap = cv2.VideoCapture(camdevice);
    #cap = cv2.VideoCapture( pathname )

    # create detection filter
    det = netutl.cDetectionNet(
        modelpath, 
        modelproto, 
        modelcaffe, 
        image_size=imagesize, 
        bgpu=bgpu,
        border=border,
        );
    det.create();

    iter = 0;
    # for every frame
    while(cap.isOpened()):
        
        # Step 1: localization 

        # process
        det.process( frame );
        image = frame;

        # draw camera
        if bdrawcam: image = view.plotcameracv(image, det.vbox);

        # draw bbox
        ccc = det.colorcheckers;
        netutl.draw_all(image, ccc);
        
        # Step 2: recognition 
        paths = utils.selected_image_paths( frame, ccc, pad )       
            
        for  (imagepath, left, top) in paths:
            try:                
                box = colorchecker.find( imagepath[:,:,(2,1,0)] )
                # res-localitation
                box[:,0] = box[:,0]+left
                box[:,1] = box[:,1]+top
            except:
                logging.info('Not recognition path colorchecker in iter {} '.format(iter));

            # draw box
            if box.sum() != 0:                   
                image_output = view.plotpolycv( image_output, box, thickness=4 )
                image_output = view.drawcolorchecker(image_output, box, [0,255,0], thickness=4)

        if bshow: 
            cv2.imshow('frame processing:', image_output)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break;
        
        # write frame 
        #cv2.imwrite('{}/{:06d}.png'.format('../out', iter), image)

        iter += 1;
        logging.info('frame processing: {}'.format(iter));
   
    
    cap.release()




def main():
    '''
    Main: colorchecker detection net
    '''
    parser = arg_parser();
    options = parser.parse_args();

    pathconfig = options.configurate;
    bgpu = options.bgpu;
    bshow = options.bshow;
    bjson = options.bjson;
    bdrawcam = options.bdrawcam;
    camdevice = options.camdevice;
    border = options.border;

    mccfindnet(
        pathconfig,
        bgpu,
        bshow,
        bjson,
        bdrawcam,
        camdevice,
        border,
        );
    

if __name__ == '__main__':
    main()

