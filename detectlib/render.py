

import numpy as np
import numpy.matlib as mth
import cv2
import random

from skimage import color

from . import utls as utl
from . import colorchecker as chc

class ObjectType:
    
    Dontcare, CCClassic, CCDigitalSG  = range(3);
    def __init__(self):
        pass

class DetectionGT:    
    """ 
    This class is the data ground-truth
    """

    # default class mappings
    OBJECT_TYPES = {
        'classic': ObjectType.CCClassic,
        'digitalsg': ObjectType.CCDigitalSG,
    }



    def __init__(self):
            self.stype = ''
            self.truncated = 0
            self.occlusion = 0
            self.angle = 0
            self.height = 0
            self.width = 0
            self.length = 0
            self.locx = 0
            self.locy = 0
            self.locz = 0
            self.roty = 0
            
            self.bbox = np.zeros((2,2))
            self.box = [];
            self.chart = [];

    
    def assignment(self, cc):

            self.stype = cc.stype;
            self.truncated = cc.truncation;
            self.occlusion = cc.occlusion;
            self.angle = cc.fi[0];
            self.height = 11.25;
            self.width = 1;
            self.length = 16.75;
            self.locx = -cc.t[0][0]
            self.locy = -cc.t[0][1] + self.height/2;
            self.locz = -cc.t[0][2]
            self.roty = cc.fi[1];
            self.bbox = cc.bbox;
            self.object = self.OBJECT_TYPES.get(cc.stype, ObjectType.Dontcare);

            self.box = cc.box;
            self.chart = cc.chart;


    def gt_to_kitti_format(self):
        '''
        Convert to kitti format 
        '''
        result = [

            # set label, truncation, occlusion
            self.stype,
            np.bool(self.truncated).numerator,
            self.occlusion,
            self.angle,
            # set 2D bounding box in 0-based C++ coordinates
            self.bbox[0,0],
            self.bbox[0,1],
            self.bbox[1,0],
            self.bbox[1,1],
            # set 3D bounding box
            self.height,
            self.width,
            self.length,
            self.locx,
            self.locy,
            self.locz, 
            self.roty
        ];
        return result;

    @classmethod
    def lmdb_format_length(cls):
        """
        width of an LMDB datafield returned by the gt_to_lmdb_format function.
        :return:
        """
        return 16

    def gt_to_lmdb_format(self):
        """
        For storage of a bbox ground truth object into a float32 LMDB.
        Sort-by attribute is always the last value in the array.
        """
        result = [
            # bbox in x,y,w,h format:
            self.bbox[0,0],
            self.bbox[0,1],
            self.bbox[1,0] - self.bbox[0,0],
            self.bbox[1,1] - self.bbox[0,1],
            # alpha angle:
            self.angle,
            # class number:
            self.object,
            0,
            # Y axis rotation:
            self.roty,
            # bounding box attributes:
            self.truncated,
            self.occlusion,
            # object dimensions:
            self.length,
            self.width,
            self.height,
            self.locx,
            self.locy,
            # depth (sort-by attribute):
            self.locz,
        ]
        assert(len(result) is self.lmdb_format_length())
        return result



class ccModel(object):
    "Model for mcc generator result"

    stype = '' 
    chart = np.zeros((24,8));
    box = np.zeros((4,2));
    bbox = np.zeros((4,2));
    truncation = False;
    occlusion = 0;
    fi = np.zeros((1,3))
    t  = np.zeros((1,3))

    
class Render(object):
    
   
    #def __init__(self):

    # function cc = chartcolorboard( K, R, T )
    # Example:
    # import matplotlib.pyplot as plt
    # K = np.array([[10, 0, 0],[0, 10, 0],[0, 0, 1]]);
    # R = utl.angle2mat([np.pi/4,0,np.pi/4]);
    # t = np.array([[0,0,-10]]);
    # cc = Render().chartcolorboard( K, R, t);
    # plt.figure(1)
    # utl.plotchart(cc[0])
    # utl.plotbbox(cc[2]);
    # plt.show();
    #
    @staticmethod
    def chartcolorboard(K, R, T, itype):
        "Get chart color board"        
        
        # get model      
        model = chc.createColorChecker(itype);

        boxsize = np.array(model.boxsize);
        chartcolor = np.array(model.chartcolor)[:,0:7];
        box = utl.projection(np.array(model.box), K, R, T);
        chart = np.array(model.chart);
        chart = np.reshape(chart,(-1,2));
        chart = utl.projection(chart, K, R, T).reshape((-1,8));
        bbox = utl.boundingbox(box);
        stype = model.stype;

        return stype, chart, box, bbox, chartcolor, boxsize;


    
    @staticmethod
    def getsyntheticcharcolorimage(im, K, fi, t, itype):
        "Get synthetic color chart image"

        # Roatation matrix
        R = utl.angle2mat(fi);

        # Get color chart
        stype, chart, box, bbox, chartcolor, boxsize = Render().chartcolorboard( K, R, t, itype);
        
        # Is truncate
        truncation = utl.isboxtruncate(box, im.shape );

        # calculate ligth
        # W = l_scenne/l_patter
        l_p = np.array(chartcolor[:,3]).mean();
        bbox = utl.validimagebox(bbox, im.shape);
        im_box = im[
            np.int(bbox[0,1]):np.int(bbox[1,1]),        
            np.int(bbox[0,0]):np.int(bbox[1,0]),:]; 

        l_s = color.rgb2lab(im_box)[:,:,0].reshape(-1,1).mean();
        w_ligth = l_s/(l_p + np.finfo(float).eps);    

        # create pattern
        box = np.array(box, np.int32);
        im = cv2.fillConvexPoly(im,box,[0, 0, 0]);
        chart = np.array(chart, np.int32);

        for i in range(chart.shape[0]):
            ch_i = chart[i,:];
            #color_rgb = np.array(chartcolor[i,0:4],dtype=np.float64);
            color_lab = np.array(chartcolor[i,3:6],dtype=np.float64);
            color_lab[0] = np.clip( color_lab[0]*w_ligth, 10, 100 ); # change
            color_lab = [[color_lab.tolist()]];          
            color_rgb = (color.lab2rgb(color_lab))[0,0,:]*255;
            im = cv2.fillConvexPoly(im,ch_i.reshape((-1,2)),color_rgb);
                
        #im[:,:,0] = cv2.equalizeHist(im[:,:,0]);
        #im[:,:,1] = cv2.equalizeHist(im[:,:,1]);
        #im[:,:,2] = cv2.equalizeHist(im[:,:,2]);

        cc = ccModel();
        cc.stype = stype;
        cc.chart = chart;
        cc.box = box;
        cc.bbox = bbox;
        cc.boxsize = boxsize;
        cc.occlusion = 0;
        cc.truncation = truncation;
        cc.fi = fi;
        cc.t = t;

        return im, cc

    @staticmethod
    def getsyntheticmultcharcolorimage(im, num=5):
        "Generate multi chart in the image"

        imsize = im.shape;
        K = np.array([[100, 0, (imsize[1]-1)/2],[0, 100, (imsize[0]-1)/2],[0, 0, 1]]);
        t_front = 2;
        t_depth = 45;

        k = 0;
        ccs = []; 
        for i in range(num):
            
            itype = random.randint(1,2);
            #itype = 1;

            rx = ((np.pi/2 - (np.pi)*random.random()))/8.0;
            ry = ((np.pi/2 - (np.pi)*random.random()))/8.0;
            rz = np.pi + np.pi/2 - np.pi*random.random();
            tx = 40 - 80*random.random();
            ty = 20 - 40*random.random();
            tz = -(t_front + t_depth*random.random());
            
            fi = np.array([rx, ry, rz]);
            t  = np.array([[tx, ty, tz]]);
            
            # generate
            im_i, cct = Render().getsyntheticcharcolorimage(im[:,:,:].copy(), K, fi, t, itype);            
            if cct.truncation == 1: 
                continue;

            # is occlude
            bocc = 0;
            for j in range(1,k+1):             
                bocc = utl.isboxocclude(ccs[j-1].bbox, cct.bbox);
                if bocc == 1: break;  
            
            if bocc == 1: 
                continue;
            
            im = im_i;
            ccs.append(cct);
            k+=1;
        
        return im, ccs


    @staticmethod
    def generatennt(data, num = 5):
        '''
        Generate data and label for detectionNet
        data.shape = [n,k,h,w]    
        '''
        datasize = data.shape;
        data = data.transpose(0, 3, 2, 1);
        n = datasize[0];
        labels = [];
        for i in range(n):
            im = data[i,...][:,:,(2, 1, 0)];
            im, cc = Render().getsyntheticmultcharcolorimage(im, num);
            
            # data
            data[i,...] = im[:,:,(2, 1, 0)];
            
            # label
            label_per_img = list();
            for c in cc:              
                gt = DetectionGT();
                gt.assignment(c);               
                label_per_img.append(gt);
            labels.append(label_per_img);
         
        #restore shapes
        data = data.transpose(0, 3, 2, 1);
        return data, labels;


    @staticmethod
    def generate(im, num = 5):
        '''
        Generate for image   
        '''           
        im, cc = Render().getsyntheticmultcharcolorimage(im, num);
        labels= list();
        for c in cc:              
            gt = DetectionGT();
            gt.assignment(c);               
            labels.append(gt);
            
        return im, labels;


    @staticmethod
    def generate_for_segmentation_mask(im, num = 5):
        '''
        Generate image and mask   
        '''           
        im, cc = Render().getsyntheticmultcharcolorimage(im, num);
        mask = np.zeros(im.shape[:2], dtype="uint8") * 255
        for i in range( len(cc) ):
            bbox = np.array([cc[i].box])
            cv2.fillPoly(mask, [bbox], 1)   
            
        return im, mask;

