/**
  *  @file app_mcc.h
  *  @brief this main file 
  *  @autor: Pedro D. Marrero Fernandez
  *  @data: 16/05/2016
  */

#ifndef APP_MCC_H
#define APP_MCC_H

#include "app_system.h"
#include "core.h"
#include "checker_detector.h"

/// CAppMCC
/** @brief main class
  *  @autor: Pedro D. Marrero Fernandez
  *  @data: 16/05/2016
  */
class CAppMCC :
	public CAppSystem
{
public:

	CAppMCC();
	virtual ~CAppMCC();

	/** @brief initilization app*/
	virtual void Init(int argc, char** argv) {
	
		m_appWndName = "MCC"; m_version = "v0.01";

		// parser input 		
		b_app_init = parse_arguments(argc, argv);	
		
	}

	/** @brief pipeline run*/  
	virtual void Run() {
	
		if (!b_app_init)return;
		switch (ui_t)
		{
		case 1: process_image(); break;		// singel image			
		case 2: process_frame(); break;		// video			
		case 3: process_image_sec(); break; // sequence image			
		}
	}

	virtual void Terminate() {}

private:

	bool b_app_init;						// init app
	std::string s_path_in, s_path_out;		// path
	std::string s_filename;					// file name inmage
	std::string s_ext;						// extension file
	std::string s_path;						// path 
	unsigned int ui_t;						// app type (1 image, 2 video, 3 sequence)
	unsigned int ui_nc;						// maximum number of checker color 
	float f_me;								// minimun error
	float f_derr;							// delta err
	unsigned int ui_mr;						// minimum resolution dimension (1500 default)
	bool b_sh;								// show result
	bool b_gt;								// generate table


	// tracking checkert color
	std::vector< cv::Point2f > l_ordchart_centers;


private:
	
	/** @brief process singel image*/
	bool process_image();

	/** @brief process video*/
	bool process_frame();

	/** @brief process imagen sequence*/
	bool process_image_sec();

private:


	/** @brief show help */
	void show_help();

	/** @brief parser input data
	  * exemple:
	  * @code
	  * ./MCC ./db/image.jpg -o ./result -t=1 -sh -gt
	  * @endcode
	  * @param[in] argc
	  * @param[in] argv
	  * @return state
	  */
	bool parse_arguments(int argc, char ** argv);
	
	/** @brief get filename
	  * @param[in]  s pash name input
	  * @param[out] fn file name
	  * @param[out] ext extencion
	  * @param[out] path
	  * @return state
	  */
	bool get_filename(const std::string &s, std::string &fn, std::string &ext, std::string &path);
	
	/** @brief get position checker*/
	int get_position_checker(const mcc::CChecker &chker);


};

CAppSystem * Application() { return new CAppMCC(); }
#endif //APP_MCC_H