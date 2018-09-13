
ENABLE_TESTING()

MACRO(NEW_TEST name )
	ADD_EXECUTABLE(${name} ${name}.cpp)
	TARGET_LINK_LIBRARIES(
		${name} 
		${OpenCV_LIBS} 
		mcclib 
		gtest	
		)
ENDMACRO(NEW_TEST)



INCLUDE_DIRECTORIES("${PROJECT_SOURCE_DIR}/extern/gtest/include"
					"${PROJECT_SOURCE_DIR}/extern/gtest/src"
					"${PROJECT_SOURCE_DIR}/mcclib" 
					"${PROJECT_SOURCE_DIR}"
					)


NEW_TEST( "mcctest" )
