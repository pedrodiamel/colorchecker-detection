

import numpy as np
from skimage import color

from . import utils as utl

class ColorChecker(object):
    """ColorChecker Classic model"""

    stype = '';
    chartcolor = [[0,0,0,0,0,0]];
    dim = [1,1];
    sRgb = [1, 2, 3];
    cieLab = [4, 5, 6];
    boxsize = [1,1];
    box = [[0,1],[1,1],[1,0],[0,0]];
    chart = [[0,1],[1,1],[1,0],[0,0]];

class Factory(object):
    def creator(self):
        pass



#-------------------------------------------------------------------
# ColorChecker Classic model
#-------------------------------------------------------------------


class ColorCheckerClassicFactory(Factory):
    """ColorChecker Classic Factory"""

    chartcolor = [    

    #       sRGB              CIE L*a*b*          Munsell Notation
    # ---------------  ----------------------     Hue Value/Chro],a
    # R     G     B       L*     a*      b*    

    [115.0,  82.0,  68.0,  37.986,  13.555,  14.059,   3.00,  3.70,   3.0], #1.  dark shin
    [194.0, 150.0, 130.0,  65.711,  18.130,  17.810,   2.20,  6.47,   4.1], #2.  light skin
    [ 98.0, 122.0, 157.0,  49.927,  -4.880, -21.925,   4.30,  4.95,   5.5], #3.  blue skin
    [ 87.0, 108.0,  67.0,  43.139, -13.095,  21.905,   6.70,  4.20,   4.1], #4.  foliage
    [133.0, 128.0, 177.0,  55.112,   8.844, -25.399,   9.70,  5.47,   6.7], #5.  blue flower
    [103.0, 189.0, 170.0,  70.719, -33.395, -0.199 ,   2.50,  7.00,   6.0], #6.  bluish green
    [214.0, 126.0,  44.0,  62.661,  36.067,  57.096,   5.00,  6.00,  11.0], #7.  orange
    [ 80.0,  91.0, 166.0,  40.020,  10.410, -45.964,   7.50,  4.00,  10.7], #8.  purplish blue
    [193.0,  90.0,  99.0,  51.124,  48.239,  16.248,   2.50,  5.00,  10.0], #9.  moderate red
    [ 94.0,  60.0, 108.0,  30.325,  22.976, -21.587,   5.00,  3.00,   7.0], #10. purple
    [157.0, 188.0,  64.0,  72.532, -23.709,  57.255,   5.00,  7.10,   9.1], #11. yelow green
    [224.0, 163.0,  46.0,  71.941,  19.363,  67.857,  10.00,  7.00,  10.5], #12. orange yellow
    [ 56.0,  61.0, 150.0,  28.778,  14.179, -50.297,   7.50,  2.90,  12.7], #13. blue
    [ 70.0, 148.0,  73.0,  55.261, -38.342,  31.370,   0.25,  5.40,  8.65], #14. green
    [175.0,  54.0,  60.0,  42.101,  53.378,  28.190,   5.00,  4.00,  12.0], #15. red
    [231.0, 199.0,  31.0,  81.733,   4.039,  79.819,   5.00,  8.00,  11.1], #16. yellow
    [187.0,  86.0, 149.0,  51.935,  49.986, -14.574,   2.50,  5.00,  12.0], #17. magenta
    [  8.0, 133.0, 161.0,  51.038, -28.631, -28.638,   5.00,  5.00,   8.0], #18. cyan
    [243.0, 243.0, 242.0,  96.539,  -0.425,   1.186,   0.00,  9.50,   0.0], #19. white(.05*)
    [200.0, 200.0, 200.0,  81.257,  -0.638,  -0.335,   0.00,  8.00,   0.0], #20. neutral 8(.23*)
    [150.0, 160.0, 160.0,  66.766,  -0.734,  -0.504,   0.00,  6.50,   0.0], #21. neutral 6.5(.44*)
    [122.0, 122.0, 121.0,  50.867,  -0.153,  -0.270,   0.00,  5.00,   0.0], #22. neutral 5(.70*)
    [ 58.0,  85.0,  85.0,  35.656,  -0.421,  -1.231,   0.00,  3.50,   0.0], #23. neutral 3.5(.1.05*)
    [ 52.0,  52.0,  52.0,  20.461,  -0.079,  -0.973,   0.00,  2.00,   0.0], #24. black (1.50*)
    ];


    def creator(self):
           
               
       sRgb = [1, 2, 3];
       cieLab = [4, 5, 6];

       #cell = np.array([2.5, 2.5]); # cm
       #step = np.array([0.25, 0.25]); # cm 
       cell = np.array([3.8, 3.8]); # cm
       step = np.array([0.60, 0.60]); # cm 

       dim  = np.array([4, 6]);     # u
       
       boxsize = (cell+step)*dim + step;
       box = [  
       [      0.00,       0.00],
       [boxsize[1],       0.00],
       [boxsize[1], boxsize[0]],
       [      0.00, boxsize[0]] 
       ]; 

       chart = np.zeros([dim[0]*dim[1],8]);
       k = 0;
       for y in range(dim[0]):
           for x in range(dim[1]):
               px = x*(cell[1]+step[1]) + step[1];
               py = y*(cell[0]+step[0]) + step[0];            
               chart[k,:] = [px, py, px+cell[1], py, px+cell[1], py+cell[0], px, py+cell[0]];
               k = k+1


       cc = ColorChecker();
       cc.chartcolor = self.chartcolor;
       cc.chart = chart;
       cc.dim = dim;
       cc.sRgb = sRgb;
       cc.cieLab = cieLab;
       cc.boxsize = boxsize;
       cc.box = box;
       cc.stype = 'classic';
       
       return cc;





#-------------------------------------------------------------------
# ColorChecker Digital SG model
#-------------------------------------------------------------------

class ColorCheckerDigitalSgFactory(Factory):
    """ColorChecker digital Sg Factory"""

    chartcolor = [
       # LAB_L,	 LAB_A	 LAB_B
       [ 96.55,	 -0.91,   0.57],
       [  6.43,	 -0.06,  -0.41],
       [  49.7,	 -0.18,   0.03],
       [  96.5,	 -0.89,   0.59],
       [   6.5,	 -0.06,  -0.44],
       [ 49.66,	  -0.2,   0.01],
       [ 96.52,  -0.91,   0.58],
       [  6.49,  -0.02,  -0.28],
       [ 49.72,	  -0.2,   0.04],
       [ 96.43,	 -0.91,   0.67],
       [ 49.72,	 -0.19,   0.02],
       [  32.6,	 51.58, -10.85],
       [ 60.75,	 26.22, -18.69],
       [ 28.69,	 48.28, -39.00],
       [ 49.38,	-15.43, -48.48],
       [ 60.63,	-30.77, -26.23],
       [ 19.29,	-26.37,  -6.15],
       [ 60.15,	-41.77, -12.60],
       [ 21.42,	  1.67,   8.79],
       [ 49.69,	  -0.2,   0.01],
       [   6.5,	 -0.03,  -0.67],
       [ 21.82,	 17.33, -18.35],
       [ 41.53,	 18.48, -37.26],
       [ 19.99,	 -0.16, -36.29],
       [ 60.16,	-18.45, -31.42],
       [ 19.94,	-17.92, -20.96],
       [ 60.68,	 -6.05, -32.81],
       [ 50.81,	 -49.8,  -9.63],
       [ 60.65,	-39.77,  20.76],
       [  6.53,	 -0.03,  -0.43],
       [ 96.56,	 -0.91,   0.59],
       [ 84.19,	 -1.95,  -8.23],
       [ 84.75,	 14.55,   0.23],
       [ 84.87,	-19.07,  -0.82],
       [ 85.15,	 13.48,   6.82],
       [ 84.17,	-10.45,  26.78],
       [ 61.74,	 31.06,  36.42],
       [ 64.37,	 20.82,  18.92],
       [  50.4,	-53.22,  14.62],
       [ 96.51,	 -0.89,   0.65],
       [ 49.74,	 -0.19,   0.03],
       [ 31.91,	 18.62,  21.99],
       [ 60.74,	 38.66,  70.97],
       [ 19.35,	 22.23, -58.86],
       [ 96.52,	 -0.91,   0.62],
       [  6.66,	  0.00,  -0.30],
       [ 76.51,	 20.81,  22.72],
       [ 72.79,	 29.15,  24.18],
       [ 22.33,	-20.70,   5.75],
       [  49.7,	 -0.19,   0.01],
       [  6.53,	 -0.05,  -0.61],
       [ 63.42,	 20.19,  19.22],
       [ 34.94,	 11.64, -50.70],
       [ 52.03,	-44.15,  39.04],
       [ 79.43,	  0.29,  -0.17],
       [ 30.67,	 -0.14,  -0.53],
       [  63.6,	 14.44,  26.07],
       [ 64.37,	 14.50,  17.05],
       [ 60.01,	-44.33,   8.49],
       [ 6.63 ,  -0.01,  -0.47],
       [ 96.56,	 -0.93,   0.59],
       [ 46.37,	 -5.09, -24.46],
       [ 47.08,	 52.97,  20.49],
       [ 36.04,	 64.92,  38.51],
       [ 65.05,	  0.00,  -0.32],
       [ 40.14,	 -0.19,  -0.38],
       [ 43.77,	 16.46,  27.12],
       [ 64.39,	 17.00,  16.59],
       [ 60.79,	-29.74,  41.50],
       [ 96.48,	 -0.89,   0.64],
       [ 49.75,	 -0.21,   0.01],
       [ 38.18,	-16.99,  30.87],
       [ 21.31,	 29.14, -27.51],
       [ 80.57,	  3.85,  89.61],
       [ 49.71,	 -0.20,   0.03],
       [ 60.27,	  0.08,  -0.41],
       [ 67.34,	 14.45,  16.90],
       [ 64.69,	 16.95,  18.57],
       [ 51.12,	-49.31,  44.41],
       [  49.7,	 -0.20,   0.02],
       [  6.67,	 -0.05,  -0.64],
       [ 51.56,	  9.16, -26.88],
       [ 70.83,	-24.26,  64.77],
       [ 48.06,	 55.33, -15.61],
       [ 35.26,	 -0.09,  -0.24],
       [ 75.16,	  0.25,  -0.20],
       [ 44.54,	 26.27,  38.93],
       [ 35.91,	 16.59,  26.46],
       [ 61.49,	-52.73,  47.30],
       [  6.59,	 -0.05,  -0.50],
       [ 96.58,	 -0.90,   0.61],
       [ 68.93,	-34.58,  -0.34],
       [ 69.65,	 20.09,  78.57],
       [ 47.79,	-33.18, -30.21],
       [ 15.94,	 -0.42,  -1.20],
       [ 89.02,	 -0.36,  -0.48],
       [ 63.43,	 25.44,  26.25],
       [ 65.75,	 22.06,  27.82],
       [ 61.47,	 17.10,  50.72],
       [ 96.53,	 -0.89,   0.66],
       [ 49.79,	 -0.20,   0.03],
       [ 85.17,	 10.89,  17.26],
       [ 89.74,	-16.52,   6.19],
       [ 84.55,	  5.07,  -6.12],
       [ 84.02,	-13.87,  -8.72],
       [ 70.76,	  0.07,  -0.35],
       [ 45.59,	 -0.05,   0.23],
       [  20.3,	  0.07,  -0.32],
       [ 61.79,	-13.41,  55.42],
       [ 49.72,	 -0.19,   0.02],
       [  6.77,	 -0.05,  -0.44],
       [ 21.85,	 34.37,   7.83],
       [ 42.66,	 67.43,  48.42],
       [ 60.33,	 36.56,   3.56],
       [ 61.22,	 36.61,  17.32],
       [ 62.07,	 52.80,  77.14],
       [ 72.42,	 -9.82,  89.66],
       [ 62.03,	  3.53,  57.01],
       [ 71.95,	-27.34,  73.69],
       [  6.59,	 -0.04,  -0.45],
       [ 49.77,	 -0.19,   0.04],
       [ 41.84,	 62.05,  10.01],
       [ 19.78,	 29.16,  -7.85],
       [ 39.56,	 65.98,  33.71],
       [ 52.39,	 68.33,  47.84],
       [ 81.23,	 24.12,  87.51],
       [  81.8,	  6.78,  95.75],
       [ 71.72,	-16.23,  76.28],
       [ 20.31,	 14.45,  16.74],
       [ 49.68,	 -0.19,   0.05],
       [ 96.48,	 -0.88,   0.68],
       [ 49.69,	 -0.18,   0.03],
       [  6.39,	 -0.04,  -0.33],
       [ 96.54,	 -0.90,   0.67],
       [ 49.72,	 -0.18,   0.05],
       [  6.49,	 -0.03,  -0.41],
       [ 96.51,	 -0.90,   0.69],
       [  49.7,	 -0.19,   0.07],
       [  6.47,	  0.00,  -0.38],
       [ 96.46,	 -0.89,   0.71]
    ];  



    def creator(self):

               
       sRgb = [1, 2, 3];
       cieLab = [4, 5, 6];

       cell = np.array([1.33, 1.33]); # cm
       step = np.array([0.41, 0.41]); # cm 
       dim  = np.array([10, 14]);     # u
       
       boxsize = (cell+step)*dim + step;
       box = [  
       [      0.00,       0.00],
       [boxsize[1],       0.00],
       [boxsize[1], boxsize[0]],
       [      0.00, boxsize[0]] 
       ]; 

       chart = np.zeros([dim[0]*dim[1],8]);
       k = 0;
       for y in range(dim[0]):
           for x in range(dim[1]):
               px = x*(cell[1]+step[1]) + step[1];
               py = y*(cell[0]+step[0]) + step[0];            
               chart[k,:] = [px, py, px+cell[1], py, px+cell[1], py+cell[0], px, py+cell[0]];
               k = k+1
       
       lba = np.array(self.chartcolor, dtype=np.float64);
       lba = [lba];       
       rgb = color.lab2rgb(lba)*255;       
       chartcolor = np.concatenate((rgb, lba), axis=2)[0,:,:].tolist();
               
       cc = ColorChecker();
       cc.chartcolor = chartcolor;
       cc.chart = chart;
       cc.dim = dim;
       cc.sRgb = sRgb;
       cc.cieLab = cieLab;
       cc.boxsize = boxsize;
       cc.box = box;
       cc.stype = 'digitalsg';
       
       return cc;



def createColorChecker(itype=1):
    '''Create checker color'''
        
    if itype > 2: raise Exception('type not defined');

    if itype == 1: #clasic
        fact = ColorCheckerClassicFactory();
    if itype == 2: #DigitalSg
        fact = ColorCheckerDigitalSgFactory();    
    return fact.creator();


