cmake_minimum_required(VERSION 3.14)

project(magent)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

# Use CMake's standard mechanism instead of -std=c++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(GLOB autopilot_sources src/*.cc src/gridworld/*.cc src/utility/*.cc)
set(LIB_SRC_FILES ${autopilot_sources})

if(MSVC)
  add_compile_options(/W0 /wd4711 /wd4710)
  add_compile_definitions(DEBUG)
else()
  add_compile_options(-g -Wall -O3
    -Wno-unused-variable -Wno-reorder -Wno-sign-compare -Wno-missing-braces)
  add_compile_definitions(DEBUG)
endif()

# runtime library
add_library(magent SHARED ${LIB_SRC_FILES})
add_executable(testlib ${LIB_SRC_FILES})
