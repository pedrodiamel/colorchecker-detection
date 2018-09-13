

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2
import operator

import utils as utl
import numpy.matlib as mth
from . import colorchecker as chc

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


STANDARD_COLORS = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]



#-------------------------------------------------------------------
# Visualization
#-------------------------------------------------------------------

# plot chart
def plotchart(chart):
    "Plot chart color"
    chart = np.array(chart);
    n = chart.shape[0]; 
    indx = np.array([0, 2, 4, 6, 0]);    
    for i in range(n):
        c = chart[i,:];
        plt.plot(c[indx],c[indx+1]);

def plotbbox(bbox, color=[1,0,0]):
    "Plot bounding box"
    x = bbox[:,0]; y = bbox[:,1]; 
    bbox = np.array([[x[0],y[0]],[x[1],y[0]],[x[1],y[1]],[x[0],y[1]],[x[0],y[0]]]);
    #plt.plot(bbox[:,0],bbox[:,1],'or-');
    plt.plot(bbox[:,0],bbox[:,1],'o-', color=color);

def imageshow(im):
    "Show color image"
    plt.imshow(im, interpolation = 'bicubic');
    plt.xticks([]), plt.yticks([]);  # to hide tick values on X and Y axis


def draw_bounding_box(image, label,  color='red', thickness=4):
    
    bbox = label.bbox;
    image_pil = Image.fromarray(np.uint8(image)).convert('RGB') 
    im_width, im_height = image_pil.size

    draw = ImageDraw.Draw(image_pil)
    xmin = bbox[0,0]; ymin = bbox[0,1];
    xmax = bbox[1,0]; ymax = bbox[1,1];
    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

    draw.line([(left, top), (left, bottom), (right, bottom),
             (right, top), (left, top)], width=thickness, fill=color)
    
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', 32) #'arial.ttf'
    except IOError:
        font = ImageFont.load_default()
    
    text_bottom = top
    
    # Reverse list and print from bottom to top.
    #for display_str in display_str_list[::-1]:
    
    display_str = '{}  '.format(label.stype);
    text_width, text_height = font.getsize(display_str)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle(
        [(left, text_bottom - text_height - 2 * margin), 
        (left + text_width, text_bottom)],
        fill=color)
    
    draw.text(
        (left + margin, text_bottom - text_height - margin),
        display_str,
        fill='black',
        font=font)
    text_bottom -= text_height - 2 * margin
    
    np.copyto(image, np.array(image_pil))

def draw_bounding_box_dic(image, label,  color='red', thickness=4):
    
    bbox = label['bbox'];
    image_pil = Image.fromarray(np.uint8(image)).convert('RGB') 
    im_width, im_height = image_pil.size

    draw = ImageDraw.Draw(image_pil)
    xmin = bbox[0,0]; ymin = bbox[0,1];
    xmax = bbox[1,0]; ymax = bbox[1,1];
    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

    draw.line([(left, top), (left, bottom), (right, bottom),
             (right, top), (left, top)], width=thickness, fill=color)
    
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', 32) #'arial.ttf'
    except IOError:
        font = ImageFont.load_default()
    
    text_bottom = top
    
    # Reverse list and print from bottom to top.
    #for display_str in display_str_list[::-1]:
    
    display_str = '{}  '.format(label['stype']);
    text_width, text_height = font.getsize(display_str)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle(
        [(left, text_bottom - text_height - 2 * margin), 
        (left + text_width, text_bottom)],
        fill=color)
    
    draw.text(
        (left + margin, text_bottom - text_height - margin),
        display_str,
        fill='black',
        font=font)
    text_bottom -= text_height - 2 * margin
    
    np.copyto(image, np.array(image_pil))






def display_random_images( images ):
    """
    Display random images from augmented dataset
    For debug only
    """

    for i in range(9):
        rand_idx = np.random.randint(images.num)
        image = images.getimage(rand_idx)
        plt.subplot(3, 3, i+1)
        plt.imshow(image)
        plt.title('Image Idx: %d \n Name: %s' % (rand_idx, images.getimagename()  ))

    plt.tight_layout()
    plt.show()


def plotboxcv(image,bbox,color=(0,255,0)):
    image1 = image.copy()
    x = bbox[0,:]; y = bbox[1,:];
    cv2.rectangle(image1,(int(bbox[0,0]),int(bbox[0,1])),(int(bbox[1,0]),int(bbox[1,1]) ),color,4)
    return image1

def plotpolycv(image,box,color=(0,255,255), thickness=10):
    img = image.copy()
    cv2.polylines(img,[box],True, color, thickness=thickness)
    return img



def plotcameracv(image, vbox, color=(255,0,0)):
    
    nl = 75;
    image_sh = image.copy()
    cv2.line(image_sh, (vbox[0,0],vbox[0,1]),(vbox[1,0],vbox[1,1]),color,3)
    cv2.line(image_sh, (vbox[1,0],vbox[0,1]),(vbox[0,0],vbox[1,1]),color,3)
    cv2.line(image_sh, (vbox[0,0],vbox[0,1]),(vbox[0,0]+nl,vbox[0,1]),color,3)
    cv2.line(image_sh, (vbox[0,0],vbox[0,1]),(vbox[0,0],vbox[0,1]+nl),color,3)
    cv2.line(image_sh, (vbox[1,0],vbox[1,1]),(vbox[1,0]-nl,vbox[1,1]),color,3)
    cv2.line(image_sh, (vbox[1,0],vbox[1,1]),(vbox[1,0],vbox[1,1]-nl),color,3)
    cv2.line(image_sh, (vbox[1,0],vbox[0,1]),(vbox[1,0]-nl,vbox[0,1]),color,3)
    cv2.line(image_sh, (vbox[1,0],vbox[0,1]),(vbox[1,0],vbox[0,1]+nl),color,3)
    cv2.line(image_sh, (vbox[0,0],vbox[1,1]),(vbox[0,0],vbox[1,1]-nl),color,3)
    cv2.line(image_sh, (vbox[0,0],vbox[1,1]),(vbox[0,0]+nl,vbox[1,1]),color,3)
    return image_sh;





def center(p):
    "Center point"
    c = np.mean(p,axis=0);
    return mth.repmat(c,p.shape[0],1);

def projection(P, H):
    #P = center(P)
    P = np.concatenate((P,np.ones([P.shape[0],1])),axis=1);   
    p = np.dot(H,P.T);
    p = p[0:2]/p[2,:];     
    return p.T;

def drawcolorchecker(image, box, color=[0,255,0], thickness=10):
    
    model = chc.createColorChecker( 1 );
    mod_chart = np.array(model.chart)
    mod_box = np.array(model.box)
    ccT = cv2.getPerspectiveTransform( mod_box.astype( np.float32 ) , box.astype( np.float32 ) );
    for pt in mod_chart:    
        pt = pt.reshape(4,-1)
        pt = projection(pt, ccT)  
        c = center(pt)
        pt = (pt - c)*0.75 + c
        image = plotpolycv( image, pt.astype(int), color, thickness=thickness )    
    return image

