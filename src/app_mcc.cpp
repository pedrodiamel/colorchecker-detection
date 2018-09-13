#include "app_mcc.h"


CAppMCC::CAppMCC()
	: b_app_init(false)
	, f_derr(1.5)
{
}

CAppMCC::~CAppMCC()
{
}

void CAppMCC::
show_help()
{
	printf("\n>> MCC Application [v0.01].\n"
		">> This app will detect the Macbeth ColorChecker inside an image.\n"
		">> [input_data] # input dir\n"
		">> -t   # application type - 1 single image, 2 video, 3 image sequence \n"
		">> -o   # output dir - default current dir \n"
		">> -me  # minimum error\n"
		">> -nc  # number maximum of checker color in the image\n"
		">> -sh  # show result\n"
		">> -gt  # generate table .csv format\n"
		">> -mr  # minimum resolution dimension (1500 default)\n"
		"\n");
}

bool CAppMCC::
parse_arguments(int argc, char ** argv)
{
	// parser
	cv::CommandLineParser parser(argc, argv,
		"{help h||}"
		"{o|.|}"
		"{t|1|}"
		"{me|2.0|}"
		"{sh||}"
		"{nc|1|}"
		"{gt||}"
		"{mr|1500|}"
		"{@input||}"
		);

	// help
	if (parser.has("help"))
	{
		show_help();
		return false;
	}

	s_path_out = parser.get<std::string>("o");		// path out		
	s_path_in = parser.get<std::string>("@input");	// path in

	if (s_path_in.empty() )
	{
		show_help();
		return false;
	}

	if(!get_filename(s_path_in, s_filename, s_ext, s_path))
	{
		show_help();
		return false;
	}

	f_me = parser.get<float>("me"); // minimun error
	if (f_me < 0)
	{
		show_help();
		return false;
	}
	
	b_sh = parser.has("sh"); // show result
	b_gt = parser.has("gt"); // generate table

	ui_t = parser.get<unsigned int>("t"); // app type
	if (ui_t < 1 || ui_t>3)
	{
		show_help();
		return false;
	}

	ui_nc = parser.get<unsigned int>("nc"); // number maximum fo checker color s
	ui_mr = parser.get<unsigned int>("mr");
	
	if (!parser.check())
	{
		show_help();
		return false;
	}

	return true;
}



bool CAppMCC::
get_filename(const std::string & s, std::string & fn, 
	std::string & ext, std::string &path) {

	char sep = '/';
	char sepExt = '.';
	std::string str;
	size_t n;

	/*#ifdef _WIN32
	sep = '\\';
	#endif*/

	n = s.length();
	size_t i = s.rfind(sep, s.length());
	path = s.substr(0, i);

	if (i != std::string::npos) {

		str = (s.substr(i + 1, s.length() - i));
		size_t j = str.rfind(sepExt, str.length());

		if (i != std::string::npos && j < n) {

			fn = str.substr(0, j);
			ext = (str.substr(j + 1, str.length() - 1));
			return true;
		}
		else {

			fn = str;
			ext = "";
			return true;
		}
	}
	else {
		return false;
	}
}

/**\brief process singel image*/
bool CAppMCC::
process_image()
{

	cv::Mat image;
	mcc::CCheckerDetector mmd(f_me, ui_nc, ui_mr);
	std::string imgnamePrefix, pathNameOut;
	std::stringstream dir;
	
	// create path name out
	imgnamePrefix = s_filename;
	imgnamePrefix += "-MCC-values";
	dir << s_path_out << "/" << imgnamePrefix;
	pathNameOut = dir.str();
	mcc::CCheckerStreamIO io(pathNameOut + ".csv");


	// read image
	image = imread(s_path_in, CV_LOAD_IMAGE_COLOR);
	if (image.empty())
	{
		printf("Cannot read image file: %s \n", s_path_in.c_str());
		return false;
	}

	// preocess image
#ifndef _DEBUG
	if (!mmd.process(image))
#else
	if (!mmd.process(image, s_path_out))
#endif // !_DEBUG				
	{
		printf("ChartColor not detected \n");
		return false;
	}


	// get checker
	std::vector< mcc::CChecker > checkers;
	mmd.getListColorChecker(checkers);
	mcc::CChecker checker;

	
	if(b_gt)
	{
		io.open();
		io.createHeaderCsv();
	}


	for (size_t ck = 0; ck < checkers.size(); ck++)
	{
		// current checker 
		checker = checkers[ck];

		// write
		if (b_gt)
		io.writeCSV(checker, s_filename, image.size(), ck);
			

		// show result
		if (b_sh)
		{
			mcc::CCheckerDraw cdraw(&checker);
			cdraw.draw(image);
		}

	}

	if(b_gt) io.close();


	// show result
	if (b_sh)
	{
		mcc::imshow_250xN("image result | q or esc to quit", image);
		cv::imwrite(pathNameOut + ".png", image);
		char key = (char)waitKey(500);
		if (key == 'q' || key == 'Q' || key == 27)
			return true;

	}
	
	return true;

}

/**\brief process video*/
bool CAppMCC::
process_frame()
{

	cv::Mat frame;
	mcc::CCheckerDetector mmd(f_me, ui_nc, ui_mr);
	bool btrack_succeeded = false;
	bool bstate;
	std::vector< std::vector<cv::Point2f > > colorCharts;	
	std::vector< mcc::CChecker > checkers;
	mcc::CChecker checker;
	mcc::CCheckerStreamIO io(s_path_out + "/" + s_filename + "-MCC-values" + ".csv");
	int pos;
	float oldJ = 0, J;
	bool bread_frame = true;


	l_ordchart_centers.clear();
	

	// open video
	cv::VideoCapture capture(s_path_in);
	if (!capture.isOpened())
	{
		std::printf("Error when reading steam ... \n");
		return false;
	}

	
	if (b_gt)
	{   
		io.open();
		io.createHeaderCsv();
	}
	
	std::printf(">> Start tracking ...\n");
	std::printf(">> N0. frame | state | error \n");
	
	for (int i = 0;;i++)
	{			

		// read current frame 		
		if(bread_frame)
		{ 
			capture >> frame;
			if (frame.empty()) break;
		} 
		bread_frame = true;
				

		// print
		std::printf(">> frame %003d", i);
		

		if (!btrack_succeeded)
		{
			std::printf("	-st");
			bstate = mmd.startTracking(frame, colorCharts);			
		}
		else
		{
			std::printf("	-ct");
			bstate = mmd.continueTracking(frame, colorCharts);
		}
		
		
		if (bstate)
		{

			// get checker				
			mmd.getBestColorChecker(checker);			
			J = checker.cost;			
			bstate =  (oldJ==0) || (std::abs(oldJ - J) < f_derr);
			

			// print error
			std::printf("	%0.3f", J);
			

			if (bstate)
			{
				
				// get checker				
				mmd.getListColorChecker(checkers);
				for (size_t ck = 0; ck < checkers.size(); ck++)
				{
					// current ckecker
					checker = checkers[ck];		
					// write table
					if (b_gt)
					{	
						pos = get_position_checker(checker);
						io.writeCSV(checker, s_filename, frame.size(), pos, i);
					}
					// show result
					if (b_sh)
					{
						mcc::CCheckerDraw cdraw(&checker);
						cdraw.draw(frame);
					}
				}

				oldJ = J;

			}
			else
			{ 
				oldJ = 0;
				bread_frame = !btrack_succeeded; i -= btrack_succeeded;
				std::printf("	-not detected");
			}
			
			btrack_succeeded = bstate;

		}
		else
		{
			oldJ = 0;
			bread_frame = !btrack_succeeded; i -= btrack_succeeded;
			btrack_succeeded = false;
			printf("	-not detected");

		}

		// show result
		if (b_sh)
		{
			// dir out
			stringstream dir;
			dir << s_path_out << "/" << s_filename  << i << ".png";

			// show frame_i
			mcc::imshow_250xN("frame result | q or esc to quit", frame);
			cv::imwrite(dir.str(), frame);
			char key = (char)waitKey(500); // waits to display frame
			if (key == 'q' || key == 'Q' || key == 27)
				break;
		}
		std::printf("\n");
	}

	if (b_gt) io.close();


	return true;

}

/**\brief process imagen sequence*/

bool CAppMCC::
process_image_sec()
{
	cv::Mat image;
	mcc::CCheckerDetector mmd(f_me, ui_nc, ui_mr);
	std::string pathName, pathNameOut, prefijo;
	bool track_succeeded = false, bstate;
	std::vector< std::vector<cv::Point2f > > colorCharts;
	std::vector< mcc::CChecker > checkers;
	mcc::CChecker checker;
	mcc::CCheckerStreamIO io(s_path_out + "/" + s_filename + "-MCC-values" + ".csv");
	int pos;
	float oldJ = 0, J;

	char sep = '-';
	size_t ipos = s_filename.rfind(sep, s_filename.length());
	prefijo = s_filename.substr(0, ipos);

	l_ordchart_centers.clear();

	std::printf(">> Start preocess ...\n");
	std::printf(">> N0. image | state | error \n");

	int i = 0;
	for (;;)
	{
		// create dir path
		stringstream dir_in;
		dir_in << s_path << "/" << prefijo << sep << i << "." << s_ext;
		pathName = dir_in.str();

		// read image
		image = imread(pathName, CV_LOAD_IMAGE_COLOR);
		if (image.empty())	break;

		// print 		
		std::printf(">> image %003d", i);


		if (!track_succeeded)
		{
			std::printf("	-st");
			bstate = mmd.startTracking(image, colorCharts);
		}
		else
		{
			std::printf("	-ct");
			bstate = mmd.continueTracking(image, colorCharts);
		}

		if (bstate)
		{
			// get checker				
			mmd.getBestColorChecker(checker);
			J = checker.cost;
			bstate = (oldJ == 0) || (std::abs(oldJ - J) < f_derr);

			// print error
			std::printf("	%0.3f", J);

			if (bstate)
			{

				// get checker				
				mmd.getListColorChecker(checkers);
				for (size_t ck = 0; ck < checkers.size(); ck++)
				{
					// current ckecker
					checker = checkers[ck];
					// write table
					if (b_gt)
					{
						pos = get_position_checker(checker);
						io.writeCSV(checker, s_filename, image.size(), pos, i);
					}
					// show result
					if (b_sh)
					{
						mcc::CCheckerDraw cdraw(&checker);
						cdraw.draw(image);
					}
				}

				oldJ = J;

			}
			else
			{
				oldJ = 0;
				i -= track_succeeded;
				std::printf("	-not detected");
			}

			track_succeeded = bstate;


		}
		else
		{
			oldJ = 0;
			i -= track_succeeded;
			track_succeeded = false;
			printf("	-not detected");

		}

		// show result
		if (b_sh)
		{
			// path out
			stringstream dir_out;
			dir_out << s_path_out << "/" << prefijo << sep << i << "_out.png";
			
			// show frame_i
			mcc::imshow_250xN("frame result | q or esc to quit", image);
			cv::imwrite(dir_out.str(), image);
			char key = (char)waitKey(500); // waits to display frame
			if (key == 'q' || key == 'Q' || key == 27)
				break;
		}

		i++;

		std::printf("\n");

	}

	if (b_gt) io.close();
	return true;
}

int CAppMCC::
get_position_checker(const mcc::CChecker & chker)
{

	if (l_ordchart_centers.empty())
	{
		l_ordchart_centers.push_back(chker.center);
		return 0;
	}

	cv::Point2f tcenter;
	float l = cv::norm(chker.box[0] - chker.box[1]);
	float d, min_d;
	int min_pos = 0;

	tcenter = l_ordchart_centers[0];
	min_d = cv::norm(tcenter - chker.center);

	for (size_t i = 1; i < l_ordchart_centers.size(); i++)
	{
		tcenter = l_ordchart_centers[i];
		d = cv::norm(tcenter - chker.center);
		if (d < min_d)
		{
			min_d = d; min_pos = i;

		}
	}

	if (min_d > l) //add
	{
		l_ordchart_centers.push_back(chker.center);
		min_pos = l_ordchart_centers.size() - 1;
	}

	l_ordchart_centers[min_pos] = chker.center;
	return min_pos;

}