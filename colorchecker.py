

from cffi import FFI
import random
from sys import exit, platform
import cv2
import numpy as np
import utils

mcclib = utils.ffi_module_import( 'build/mcclib/libmcclib' )


def find( image ):
    r"""Find: Patch Color Recognition and Pose Estimation
    Args:
        image: image path or image 
        min_error:
        min_resolution:    
        box: return box of colorchecker    
    """

    img = image
    ub_img = img.reshape(-1,1).astype('ubyte')
    box = np.zeros( (8), dtype=np.float32 )

    ffi = FFI() 
    ffi_ub_img = ffi.cast("unsigned char *", ub_img.ctypes.data)
    ffi_f_box = ffi.cast("float *", box.ctypes.data)

    mcclib.wmccfind( 
        ffi_ub_img,         # image
        img.shape[1],       # int h, int w, 
        img.shape[0],  
        ffi_f_box,          # float *box,
        2.0,                # float f_min_error,
        1,                  # unsigned int ui_num_checker,
        1500                # unsigned int ui_min_resolution  
        )

    # array to vector
    box  = np.array([ 
        [box[0], box[1]], 
        [box[2], box[3]], 
        [box[4], box[5]], 
        [box[6], box[7]] 
        ]).astype(int)

    return box


