#pragma once
#ifndef _MCC_CORE_H
#define _MCC_CORE_H

#include <limits>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>


#ifndef FLT_MAX
# define FLT_MAX std::numeric_limits<double>::max()
#endif

#ifndef M_PI
# define M_PI 3.141592653589793238462643
#endif


#include "common.h"



#endif //_MCC_CORE_H