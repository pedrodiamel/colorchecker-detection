#include "app_system.h"
#include <assert.h>


CAppSystem* CAppSystem::m_instance = NULL;


/*!
* \fn	int main()
*
* \brief	Main entry-point for this application.
*
* \author	Pedro
* \date	27/12/2015
*
* \return	Exit-code for the process - 0 for success, else an error code.
*/

int main(int argc, char** argv)
{
	CAppSystem *app = Application();
	assert(app);

	try {
		
		app->Init(argc, argv);
		app->Run();
		app->Terminate();
		
	}
	catch (CAppError &err) {

		printf(err.GetError());
		delete app;
		return -1;

	}

	delete app;
	return 0;

}



CAppSystem::CAppSystem()
{

	if (m_instance) {
	throw new CAppError("This class not instance"); // este constructor es privado
	}m_instance = this;

}


CAppSystem::~CAppSystem()
{
}

