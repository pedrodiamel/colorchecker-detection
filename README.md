# MacBeth Color Chart Detector BRRES - 59 #

ColorCheckers are reference standards that professional photographers and filmmakers use to ensure predictable results under every lighting condition. The objective of this work is to propose a new fast and robust method for automatic ColorChecker detection. The process is divided into two steps: (1) ColorCheckers localization and (2) ColorChecker patches recognition. 

![Pipeline](rec/pipeline_general.png)


Requirements
------------
You need OpenCV v3.1.0 or later and NVidia Caffe.
This installation package contains support for opencv compilation for Windows in vs.12, vs.14 and mingw.

- apt-get update 
- apt-get upgrade
- [nvcaffe](http://www.nvidia.com/object/caffe-installation.html)
- echo "export PYTHONPATH=/opt/nvcaffe/python" >> ~/.bashrc
- exho "export PATH=/opt/nvcaffe/build/tools:/opt/nvcaffe/python:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin " >> ~/.bashrc
- source ~/.bashrc
- [opencv]( http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)



Installation
------------
Building the project using CMake from the command-line:

    export OpenCV_DIR="./extern/opencv"
    mkdir build
    cd build
    cmake -D OpenCV_DIR=$OpenCV_DIR ..
    make 



How to use it
-------------

### Preparing the chart

You should have done a photo or video of the ColorChecker Passport.

![Photo of the ColorChecker Passport](rec/img-colorchecker.jpg)

### Running the MCCFind:

	./build/src/mcc ../db/img-colorchecker.jpg -o=../out -t=1 -sh -gt -nc=0
	./build/src/mcc ../db/vdo-colorchecker.mp4 -o=../out -t=2 -sh -gt -nc=2
	./build/src/mcc ../db/sec-colchecker-0.jpg -o=../out -t=3 -sh -gt -nc=2 -me=10.0

options:

	 -t   # application type - 1 single image, 2 video, 3 image sequence
	 -o   # output dir - default current dir
	 -me  # minimum error
	 -nc  # number maximum of checker color in the image
	 -sh  # show result
	 -gt  # generate table .csv format
      []  # input dir


### Running the MCCFindNet:

	usage: mccfindnet.py [-h] --configurate C [--no-gpu] [--json] [--no-show]
                     [--draw-cam] [--camdevice N] [--border N]



### Results

![Results](rec/mcc.gif)