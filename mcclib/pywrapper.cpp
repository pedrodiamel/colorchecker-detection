

#include "pywrapper.h"

#include "core.h"
#include "checker_detector.h"



/**MccFind
 * @brief colorchecker detection
 * @param [in]:  image 
 * @param [in]:  h, w 
 * @param [in]:  f_min_error minimun error (2.0)
 * @param [in]:  ui_num_checker number of checker color (1)
 * @param [in]:  ui_min_resolution minimum resolution dimension (1500 default)
 * @param [out]: box
*/
void wmccfind( 
    unsigned char *image, 
    int h, int w, 
    float *box,
    float f_min_error,
    unsigned int ui_num_checker,
    unsigned int ui_min_resolution
    )
{
       
    
    cv::Mat mat_image(w, h, CV_8UC3, image);

	mcc::CCheckerDetector mmd( 
        f_min_error, 
        ui_num_checker,
        ui_min_resolution 
        );
    

    if (!mmd.process( mat_image ) ){
        printf("ColorChecker not detected \n");
        return;
    }

    std::vector< mcc::CChecker > checkers;
	mmd.getListColorChecker(checkers);
	
    if ( checkers.size() == 0 ){
        printf("ColorChecker not detected \n");
        return;
    }
    else{
        printf("ColorChecker detected (%d) \n", int(checkers.size()) );
    }

    mcc::CChecker checker;
    checker = checkers[0];

    // copy box values
    box[0] = checker.box[0].x; box[1] = checker.box[0].y;
    box[2] = checker.box[1].x; box[3] = checker.box[1].y;
    box[4] = checker.box[2].x; box[5] = checker.box[2].y;
    box[6] = checker.box[3].x; box[7] = checker.box[3].y;


    //mcc::CCheckerDraw cdraw(&checker);
    //cdraw.draw(mat_image);
    //cv::imwrite("output.png", mat_image);
    //printf("MCCFIND DONE!!! \n");


}