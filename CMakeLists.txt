cmake_minimum_required(VERSION 3.14)

project(magent)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

IF (APPLE)
    set(CMAKE_CXX_COMPILER "/usr/local/opt/llvm/bin/clang++")
    link_directories("/usr/local/opt/llvm/lib")
    include_directories( "/usr/local/include" )
    link_directories("/usr/local/lib/")
ENDIF()

file(GLOB autopilot_sources src/*.cc src/gridworld/*.cc src/utility/*.cc)
set(LIB_SRC_FILES ${autopilot_sources})


set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -Wall -std=c++11 -O3")
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-variable -Wno-reorder -Wno-sign-compare -Wno-missing-braces")
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DDEBUG")

# runtime library
add_library(magent SHARED ${LIB_SRC_FILES})
add_executable(testlib ${LIB_SRC_FILES})
