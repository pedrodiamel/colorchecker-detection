

import os
import matplotlib.pyplot as plt
import numpy as np
import json
import cv2
import caffe
import scipy.misc

import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import utils as utl
import visualizationutl as view
import imageutl as imutl



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


def loadconfig(pathconfigurate):
    ''' configurate '''
    with open(pathconfigurate, "r" ) as f: 
        config = json.load(f)
    for cf,v in config.items():
        print('{} : {}'.format(cf, v))
    return config;
    

def bboxadjust(bbox, aspX=1.0, aspY=1.0, minX=0.0, minY=0.0):
    p=bbox[4];   
    bbox = np.array([[bbox[0], bbox[1]],[bbox[2], bbox[3]]]);            
    bbox[:,0] = bbox[:,0]*(1/aspX)  + minX;
    bbox[:,1] = bbox[:,1]*(1/aspY)  + minY;
    o = np.array([bbox[0,0], bbox[0,1], bbox[1,0], bbox[1,1], p ]);  
    return list(o.tolist());

def draw_bounding_box(image, pieces, thickness=4):
    
    bbox = pieces.bbox;
    image_pil = Image.fromarray(np.uint8(image)).convert('RGB') 
    im_width, im_height = image_pil.size

    draw = ImageDraw.Draw(image_pil)
    xmin = bbox[0,0]; ymin = bbox[0,1];
    xmax = bbox[1,0]; ymax = bbox[1,1];
    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

    draw.line([(left, top), (left, bottom), (right, bottom),
             (right, top), (left, top)], width=thickness, fill=pieces.color)
    
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', 32) #'arial.ttf'
    except IOError:
        font = ImageFont.load_default()
    
    text_bottom = top
    
    # Reverse list and print from bottom to top.
    #for display_str in display_str_list[::-1]:
    
    display_str = '{}: {:.2f} '.format(pieces.sname, pieces.prob);
    text_width, text_height = font.getsize(display_str)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle(
        [(left, text_bottom - text_height - 2 * margin), 
        (left + text_width, text_bottom)],
        fill=pieces.color)
    
    draw.text(
        (left + margin, text_bottom - text_height - margin),
        display_str,
        fill='black',
        font=font)
    text_bottom -= text_height - 2 * margin
    
    np.copyto(image, np.array(image_pil))

    
def draw_all(image, objects, thickness=4):
    for k, vs in objects.items():
        if len(vs) == 0: continue;    
        for v in vs:
            draw_bounding_box(image, v, thickness);




class ObjectType:
    
    Dontcare, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16 = range(17);
    def __init__(self):
        pass

class cColorChecker(object):
    '''Colorchecker model
    '''
    clase=0;
    bbox=np.zeros((4,2));
    center=[0,0];
    r=0;
    sname='';
    color=[];
    f=0;
    prob=0;
    
    # default class mappings
    OBJECT_TYPES = {
         'bbox-list-class0': ObjectType.p1,
         'bbox-list-class1': ObjectType.p2,
         'bbox-list-class2': ObjectType.p3,
         'bbox-list-class3': ObjectType.p4,
         'bbox-list-class4': ObjectType.p5,
         'bbox-list-class5': ObjectType.p6,
         'bbox-list-class6': ObjectType.p7,
         'bbox-list-class7': ObjectType.p8,
         'bbox-list-class8': ObjectType.p9,
         'bbox-list-class9': ObjectType.p10,
        'bbox-list-class10': ObjectType.p11,
        'bbox-list-class11': ObjectType.p12,
        'bbox-list-class12': ObjectType.p13,
        'bbox-list-class13': ObjectType.p14,
        'bbox-list-class14': ObjectType.p15,
        'bbox-list-class15': ObjectType.p16,
    }
    
    
    
    def __init__(self, k, v):
        self._assignment(k,v);
    
    def _assignment(self, k, v):
        
        self.bbox = np.array([[v[0], v[1]],[v[2], v[3]]]);
        self.prob = v[4];
        self.center = 0;
        self.r=0; 
        self.clase = self.OBJECT_TYPES.get(k, ObjectType.Dontcare);
        self.color = STANDARD_COLORS[self.clase];
        self.sname = 'p{}'.format(self.clase)
            
    

class cDetectionNet(object):
    '''
    Detection net filter
    '''        
    def __init__(self, modelpath, modelproto, modelcaffe, image_size=[640, 1024, 3], 
        bgpu=False, border=0, offsetx=0, offsety=0):
        
        self.modelpath = modelpath;
        self.modelproto = os.path.join(modelpath, modelproto);
        self.modelcaffe = os.path.join(modelpath, modelcaffe);        
        self.imagesize  = image_size;
        self.asp = float(image_size[1])/image_size[0];
        self.bgpu = bgpu;
        self.net = [];
        self.border = border;
        self.offsetx = offsetx;
        self.offsety = offsety;
        self.colorcheckers = [];
        self.netout = [];
        self.vbox = [];
        self.aspX = 1;
        self.aspY = 1;

    
    def configuration(self, bgpu):
        self.bgpu = bgpu;
    
    def create(self):
        '''
        initialize net
        '''        
        if self.bgpu: caffe.set_mode_gpu();
        else: caffe.set_mode_cpu();
        self.net = caffe.Net(self.modelproto, self.modelcaffe, caffe.TEST);
        
        
    def process(self, frame):
        '''
        process frame 
        '''        
        #H, W original image size
        H=frame.shape[0]; W=frame.shape[1];
        
        #image canonization
        if H>W: frame = frame.transpose(1,0,2)
        H=frame.shape[0]; W=frame.shape[1]     
        
        H1 = int(H - self.border)
        W1 = int(H1 * self.asp)
        offsetx=self.offsetx
        offsety=self.offsety
        Wdif = int(np.abs(W - W1) / 2.0)
        Hdif = int(np.abs(H - H1) / 2.0)
        vbox = np.array([[Wdif, Hdif], [W - Wdif, H - Hdif]])

        frame_p = frame[vbox[0, 1]+offsety:vbox[1, 1]+offsety, vbox[0, 0]+offsetx:vbox[1, 0]+offsetx, : ]; #(2, 1, 0)
        #frame_p = frame[vbox[0, 1]:vbox[1, 1], vbox[0, 0]:vbox[1, 0], (2, 1, 0) ]; 
        aspY = float(self.imagesize[0]) / frame_p.shape[0]
        aspX = float(self.imagesize[1]) / frame_p.shape[1]

        frame_p = scipy.misc.imresize(frame_p, (self.imagesize[0], self.imagesize[1]), interp='bilinear')
        #cv2.imwrite('{}/{:06d}.png'.format('.', 1), frame_p)

        im_input = frame_p[np.newaxis, :, :].transpose(0, 3, 1, 2);
                
        # frame processing
        self.net.blobs['data'].data[...] = im_input;
        netout = self.net.forward();        
        
        # serializar pecas list
        kys = netout.keys();
        colorcheckers = dict(zip(kys, [[] for x in range(0, len(kys))]));
        for k,v in netout.items():
            colorcheckers[k] = [cColorChecker(k, bboxadjust(o, aspX, aspY, vbox[0, 0], vbox[0, 1])) for o in v[0] if o[-1] > 0]

        self.netout = netout;
        self.colorcheckers = colorcheckers;
        self.vbox = vbox;
        self.aspX = aspX;
        self.aspY = aspY;


    def writejson(self, pathname ):
        '''
        Write bbox json
        '''    
        kys = self.netout.keys();
        bboxes = dict(zip(kys, [[] for x in range(0, len(kys))]))
        for key, outputs in self.netout.items():
            bboxes[key] = [bboxadjust(o, self.aspX, self.aspY, self.vbox[0, 0], self.vbox[0, 1]) for o in outputs[0] if o[-1] > 0]
            with open(pathname, 'w') as f: 
                json.dump(bboxes, f, indent = 4)
        


class cFrame(object):
    '''
    Frames porcess
    '''        
    def __init__(self, image_size=[640, 1024, 3], 
        border=0, offsetx=0, offsety=0):        
       
        self.imagesize  = image_size;
        self.asp = float(image_size[1])/image_size[0];
        self.border = border;
        self.offsetx = offsetx;
        self.offsety = offsety;
              
    
    def configuration(self):
        pass
    
    def create(self):
        pass
        
        
    def process(self, frame):
        '''
        process frame 
        '''        
        #H, W original image size
        H=frame.shape[0]; W=frame.shape[1];
        
        #image canonization
        if H>W: frame = frame.transpose(1,0,2)
        H=frame.shape[0]; W=frame.shape[1]     
        
        H1 = int(H - self.border)
        W1 = int(H1 * self.asp)
        offsetx=self.offsetx
        offsety=self.offsety
        Wdif = int(np.abs(W - W1) / 2.0)
        Hdif = int(np.abs(H - H1) / 2.0)
        vbox = np.array([[Wdif, Hdif], [W - Wdif, H - Hdif]])

        frame_p = frame[vbox[0, 1]+offsety:vbox[1, 1]+offsety, vbox[0, 0]+offsetx:vbox[1, 0]+offsetx, : ]; #(2, 1, 0)
        aspY = float(self.imagesize[0]) / frame_p.shape[0]
        aspX = float(self.imagesize[1]) / frame_p.shape[1]

        frame_p = scipy.misc.imresize(frame_p, (self.imagesize[0], self.imagesize[1]), interp='bilinear')
        
        return frame_p;
