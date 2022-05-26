cmake_minimum_required(VERSION 3.14)

project(magent)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

file(GLOB autopilot_sources src/*.cc src/gridworld/*.cc src/utility/*.cc)
set(LIB_SRC_FILES ${autopilot_sources})


set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -Wall -std=c++11 -O3")
IF (WIN32)
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W0 /wd4711 /wd4710")
ELSE()
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-variable -Wno-reorder -Wno-sign-compare -Wno-missing-braces")
ENDIF()
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DDEBUG")

# runtime library
add_library(magent SHARED ${LIB_SRC_FILES})
add_executable(testlib ${LIB_SRC_FILES})
