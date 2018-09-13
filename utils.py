

from cffi import FFI
import random
from sys import exit, platform
import cv2
import numpy as np


def ffi_module_import( pathlib ):
    """FFI MODULE LODAER
    """
    
    ffi = FFI()   
    ffi.cdef(""" 
    void wmccfind( 
        unsigned char *image, 
        int h, int w, 
        float *box,
        float f_min_error,
        unsigned int ui_num_checker,
        unsigned int ui_min_resolution     
        );
    """)
    
    # cdef_from_file = None
    # try:
    #     with open(header, 'r') as libtestcffi_header:
    #         cdef_from_file = libtestcffi_header.read() #.replace('\n', '')
    # except FileNotFoundError:
    #     print('Unable to find "%s"' % header)
    #     exit(2)
    # except IOError:
    #     print('Unable to open "%s"' % header)
    #     exit(3)
    # finally:
    #     if cdef_from_file == '':
    #         print('File "%s" is empty' % header)
    #         exit(1)
    # ffi.cdef(cdef_from_file)

    lib_extension = ''
    if platform.startswith('freebsd') or platform.startswith('linux'):
        lib_extension = '.so'
    elif platform.startswith('win'):
        lib_extension = '.dll'

    # lib = ffi.dlopen("build/mcclib/libmcclib.so")
    lib = ffi.dlopen(pathlib + lib_extension)
    return lib



def selected_image_paths( image, ccc, pad=40 ):
        
    paths = []
    for k,vs in ccc.items():
        if len(vs) == 0: continue
        for v in vs:    
            bbox = v.bbox.astype(int)    

            xmin,ymin,xmax,ymax = bbox[0,0], bbox[0,1], bbox[1,0], bbox[1,1]
            (left, right, top, bottom) = (xmin-pad, xmax+pad, ymin-pad, ymax+pad)

            # boundary condition
            left   = max(0, left)
            top    = max(0, top)
            right  = min(image.shape[1], right)
            bottom = min(image.shape[0], bottom)

            # crop
            imagepath = image[top:bottom,left:right,:]
            
            paths.append( (imagepath, left, top) )

    return paths