cmake_minimum_required (VERSION 2.6) 

set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/install" CACHE PATH "Installation Directory")

# Name proyect
PROJECT(MCC)
SET(MCC_VERSION 0.01)

# Requires OpenCV v2.4.1 or later
FIND_PACKAGE( OpenCV REQUIRED )
IF (${OpenCV_VERSION} VERSION_LESS 2.4.1)
    MESSAGE(FATAL_ERROR "OpenCV version is not compatible : ${OpenCV_VERSION}. MCC requires atleast OpenCV v2.4.1")
ENDIF()

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_C_FLAGS "-fPIC ${CMAKE_C_FLAGS}")

# Debug build
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -Wall -g -O0")
# Release build
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -Os") # -Os optimizes for size (includes -O2 with a couple of flags disabled)
#set(CMAKE_EXE_LINKER_FLAGS_RELEASE "-s") # -s strip binary



ADD_SUBDIRECTORY(mcclib)
ADD_SUBDIRECTORY(src)
ADD_SUBDIRECTORY(extern)
ADD_SUBDIRECTORY(tests)


SET(RESOURCES 
    README.md
    rec
    )

FOREACH(f ${RESOURCES})
FILE( COPY ${f} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/)
ENDFOREACH(f)