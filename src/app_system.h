#pragma once

#ifndef APP_SYSTEM_H
#define APP_SYSTEM_H

#include <stdio.h>
#include <string>
#include <iostream>
#include <fstream>
#include <locale>


/*!
 * \class	CAppError
 *
 * \brief	An application error.
 *
 * \author	Pedro
 * \date	28/12/2015
 */

class CAppError {

private:
	std::string m_strError;

public:

	CAppError(const char* error) { 	m_strError = "Error: " +  std::string(error) + "\n";}
	const char* GetError() { return m_strError.c_str(); }

};


/*!
 * \class	Singleton CAppSystem
 *
 * \brief	An application system for run.
 *
 * \author	Pedro
 * \date	28/12/2015
 */

class CAppSystem
{
public:
	CAppSystem();
	~CAppSystem();


	static CAppSystem* getInstance() {

		if (!m_instance) {
			m_instance = new CAppSystem;
		}return m_instance;

	}


	//virtual function
	virtual void Init(int argc, char** argv) {}
	virtual void Run() {}
	virtual void Terminate() {}
	virtual void InitIO() {}


protected:
	std::string m_appWndName;
	std::string m_version;

private:
	static CAppSystem *m_instance;

};

CAppSystem* Application();

#endif
