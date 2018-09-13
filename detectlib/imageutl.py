

import os
import numpy as np
import PIL.Image
import scipy.misc

class imageProvide(object):
    '''
    Management the image resources  
    '''

    def __init__(self, path, ext='jpg', fn_image=''):
        
        if os.path.isdir(path) is not True:
            raise ValueError('Path {} is not directory'.format(path))
        
        self.fn_image = fn_image;
        self.path = path;
        self.pathimage = os.path.join(path, fn_image);

        #self.files = os.listdir(self.pathimage);
        self.files = [ f for f in sorted(os.listdir(self.pathimage)) if f.split('.')[-1] == ext ];
        self.num = len(self.files);
        
        self.ext = ext;
        self.index = 0;

    def getimage(self, i):
        '''
        Get image i
        '''
        #check index
        if i<0 and i>self.num: raise ValueError('Index outside range');
        self.index = i;
        pathname = os.path.join(self.path,self.fn_image,self.files[i]);        
        return np.array(self._loadimage(pathname));

    def next(self):
        '''
        Get next image
        '''
        i = self.index;        
        pathname = os.path.join(self.pathimage, self.files[i]); 
        im = self._loadimage(pathname);
        self.index = (i + 1) % self.num;
        return im;

    def getimagename(self):
        '''
        Get current image name
        '''
        return self.files[self.index];



    def _loadimage(self, pathname):
        '''
        Load image using pathname
        '''

        if os.path.exists(pathname):
            try:
                image = PIL.Image.open(pathname)
                image.load()
            except IOError as e:
                raise ValueError('IOError: Trying to load "%s": %s' % (pathname, e.message) ) 
        else:
            raise ValueError('"%s" not found' % pathname)


        if image.mode in ['L', 'RGB']:
            # No conversion necessary
            return image
        elif image.mode in ['1']:
            # Easy conversion to L
            return image.convert('L')
        elif image.mode in ['LA']:
            # Deal with transparencies
            new = PIL.Image.new('L', image.size, 255)
            new.paste(image, mask=image.convert('RGBA'))
            return new
        elif image.mode in ['CMYK', 'YCbCr']:
            # Easy conversion to RGB
            return image.convert('RGB')
        elif image.mode in ['P', 'RGBA']:
            # Deal with transparencies
            new = PIL.Image.new('RGB', image.size, (255, 255, 255))
            new.paste(image, mask=image.convert('RGBA'))
            return new
        else:
            raise ValueError('Image mode "%s" not supported' % image.mode);
        
        return image;


class dataProvide(imageProvide):
    '''
    Management dataset <images, labes>
    '''
    def __init__(self, path, ext='jpg', fn_image='images', fn_label='labels', posfix='_mask'):
        super(dataProvide, self).__init__(path, ext, fn_image );
        self.fn_label = fn_label;
        self.posfix = posfix;
        self.current_label_area = 0
                
    def getlabel(self):
        '''
        Get current label
        '''
        i = self.index;
        name = self.files[i].split('.');
        pathname = os.path.join(self.path,self.fn_label,'{}{}.{}'.format(name[0],self.posfix,name[1]) );        
        label = np.array(self._loadimage(pathname));
        if label.ndim == 3: label = label[:,:,0];
        self.current_label_area = np.sum(label)
        label = (label > 128).astype( np.uint8 )
        
        return label;


class kittiProvide(imageProvide):
    '''
    Management dataset <images, labes>
    '''
    def __init__(self, path, ext='jpg', fn_image='images', fn_label='labels', posfix='_mask'):
        super(kittiProvide, self).__init__(path, ext, fn_image );
        self.fn_label = fn_label;
        self.posfix = posfix;
                
    def getlabelkitti(self):
        '''
        Get current label
        '''
        i = self.index;
        name = self.files[i].split('.');
        pathname = os.path.join(self.path,self.fn_label,'{}{}.{}'.format(name[0],self.posfix,'txt') );        
        
        # get labels 
        labels = list();
        with open(pathname, 'r') as f:
            for line in f:
                labels.append(line.split());       
        return labels;

    def getlabel(self):
        
        labelkitti = self.getlabelkitti();
        label = list();
        for l in labelkitti:
            stype = l[0];
            bbox  = np.array(l[4:8], dtype=np.float);
            bbox  = np.array([[bbox[0], bbox[1]],[bbox[2], bbox[3]]]);
            label.append({'stype':stype, 'bbox':bbox});
        return label;



def image_to_array(image,
                   channels=None):
    """
    Returns an image as a np.array

    Arguments:
    image -- a PIL.Image or numpy.ndarray

    Keyword Arguments:
    channels -- channels of new image (stays unchanged if not specified)
    """

    if channels not in [None, 1, 3, 4]:
        raise ValueError('unsupported number of channels: %s' % channels)

    if isinstance(image, PIL.Image.Image):
        # Convert image mode (channels)
        if channels is None:
            image_mode = image.mode
            if image_mode not in ['L', 'RGB', 'RGBA']:
                raise ValueError('unknown image mode "%s"' % image_mode)
        elif channels == 1:
            # 8-bit pixels, black and white
            image_mode = 'L'
        elif channels == 3:
            # 3x8-bit pixels, true color
            image_mode = 'RGB'
        elif channels == 4:
            # 4x8-bit pixels, true color with alpha
            image_mode = 'RGBA'
        if image.mode != image_mode:
            image = image.convert(image_mode)
        image = np.array(image)
    elif isinstance(image, np.ndarray):
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        if image.ndim == 3 and image.shape[2] == 1:
            image = image.reshape(image.shape[:2])
        if channels is None:
            if not (image.ndim == 2 or (image.ndim == 3 and image.shape[2] in [3, 4])):
                raise ValueError('invalid image shape: %s' % (image.shape,))
        elif channels == 1:
            if image.ndim != 2:
                if image.ndim == 3 and image.shape[2] in [3, 4]:
                    # color to grayscale. throw away alpha
                    image = np.dot(image[:, :, :3], [0.299, 0.587, 0.114]).astype(np.uint8)
                else:
                    raise ValueError('invalid image shape: %s' % (image.shape,))
        elif channels == 3:
            if image.ndim == 2:
                # grayscale to color
                image = np.repeat(image, 3).reshape(image.shape + (3,))
            elif image.shape[2] == 4:
                # throw away alpha
                image = image[:, :, :3]
            elif image.shape[2] != 3:
                raise ValueError('invalid image shape: %s' % (image.shape,))
        elif channels == 4:
            if image.ndim == 2:
                # grayscale to color
                image = np.repeat(image, 4).reshape(image.shape + (4,))
                image[:, :, 3] = 255
            elif image.shape[2] == 3:
                # add alpha
                image = np.append(image, np.zeros(image.shape[:2] + (1,), dtype='uint8'), axis=2)
                image[:, :, 3] = 255
            elif image.shape[2] != 4:
                raise ValueError('invalid image shape: %s' % (image.shape,))
    else:
        raise ValueError('resize_image() expected a PIL.Image.Image or a numpy.ndarray')

    return image






def resize_image(image, height, width,
                 channels=None,
                 resize_mode=None,
                 ):
    """
    Resizes an image and returns it as a np.array

    Arguments:
    image -- a PIL.Image or numpy.ndarray
    height -- height of new image
    width -- width of new image

    Keyword Arguments:
    channels -- channels of new image (stays unchanged if not specified)
    resize_mode -- can be crop, squash, fill or half_crop
    """

    if resize_mode is None:
        resize_mode = 'squash'
    if resize_mode not in ['crop', 'squash', 'fill', 'half_crop']:
        raise ValueError('resize_mode "%s" not supported' % resize_mode)

    # convert to array
    image = image_to_array(image, channels)

    # No need to resize
    if image.shape[0] == height and image.shape[1] == width:
        return image

    # Resize
    interp = 'bilinear'

    width_ratio = float(image.shape[1]) / width
    height_ratio = float(image.shape[0]) / height
    if resize_mode == 'squash' or width_ratio == height_ratio:
        return scipy.misc.imresize(image, (height, width), interp=interp)
    elif resize_mode == 'crop':
        # resize to smallest of ratios (relatively larger image), keeping aspect ratio
        if width_ratio > height_ratio:
            resize_height = height
            resize_width = int(round(image.shape[1] / height_ratio))
        else:
            resize_width = width
            resize_height = int(round(image.shape[0] / width_ratio))
        image = scipy.misc.imresize(image, (resize_height, resize_width), interp=interp)

        # chop off ends of dimension that is still too long
        if width_ratio > height_ratio:
            start = int(round((resize_width - width) / 2.0))
            return image[:, start:start + width]
        else:
            start = int(round((resize_height - height) / 2.0))
            return image[start:start + height, :]
    else:
        if resize_mode == 'fill':
            # resize to biggest of ratios (relatively smaller image), keeping aspect ratio
            if width_ratio > height_ratio:
                resize_width = width
                resize_height = int(round(image.shape[0] / width_ratio))
                if (height - resize_height) % 2 == 1:
                    resize_height += 1
            else:
                resize_height = height
                resize_width = int(round(image.shape[1] / height_ratio))
                if (width - resize_width) % 2 == 1:
                    resize_width += 1
            image = scipy.misc.imresize(image, (resize_height, resize_width), interp=interp)
        elif resize_mode == 'half_crop':
            # resize to average ratio keeping aspect ratio
            new_ratio = (width_ratio + height_ratio) / 2.0
            resize_width = int(round(image.shape[1] / new_ratio))
            resize_height = int(round(image.shape[0] / new_ratio))
            if width_ratio > height_ratio and (height - resize_height) % 2 == 1:
                resize_height += 1
            elif width_ratio < height_ratio and (width - resize_width) % 2 == 1:
                resize_width += 1
            image = scipy.misc.imresize(image, (resize_height, resize_width), interp=interp)
            # chop off ends of dimension that is still too long
            if width_ratio > height_ratio:
                start = int(round((resize_width - width) / 2.0))
                image = image[:, start:start + width]
            else:
                start = int(round((resize_height - height) / 2.0))
                image = image[start:start + height, :]
        else:
            raise Exception('unrecognized resize_mode "%s"' % resize_mode)

        # fill ends of dimension that is too short with random noise
        if width_ratio > height_ratio:
            padding = (height - resize_height) / 2
            noise_size = (padding, width)
            if channels > 1:
                noise_size += (channels,)
            noise = np.random.randint(0, 255, noise_size).astype('uint8')
            image = np.concatenate((noise, image, noise), axis=0)
        else:
            padding = (width - resize_width) / 2
            noise_size = (height, padding)
            if channels > 1:
                noise_size += (channels,)
            noise = np.random.randint(0, 255, noise_size).astype('uint8')
            image = np.concatenate((noise, image, noise), axis=1)

        return image
