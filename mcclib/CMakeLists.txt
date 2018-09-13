
SET(MCC_LIBRERY    
	checker_detector.h
    checker_detector.cpp
	bound_min.h
    bound_min.cpp
	checker_model.h
    checker_model.cpp   
	common.h
    common.cpp    
	charts.h
    charts.cpp
	core.h
    core.cpp
	debug.h
    debug.cpp
	graph_cluster.h
    graph_cluster.cpp
	wiener_filter.h
	wiener_filter.cpp
	mcc.h
    mcc.cpp
	pywrapper.h
	pywrapper.cpp
)

# SHARED, STATIC

ADD_LIBRARY(mcclib SHARED ${CMAKE_CURRENT_SORCE_DIR} ${MCC_LIBRERY} ) 
TARGET_INCLUDE_DIRECTORIES(mcclib PUBLIC ${CMAKE_CURRENT_SORCE_DIR} )
TARGET_LINK_LIBRARIES(mcclib ${OpenCV_LIBS} )

INSTALL(TARGETS mcclib DESTINATION lib)
INSTALL(FILES ${MCC_LIBRERY} DESTINATION include)

