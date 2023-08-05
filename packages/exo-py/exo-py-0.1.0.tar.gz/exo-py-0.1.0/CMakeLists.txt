cmake_minimum_required(VERSION 3.11)

project(exo LANGUAGES CXX VERSION 0.1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(${PROJECT_SOURCE_DIR}/cmake/ExoMakeAvailable.cmake)

option(EXO_DOWNLOAD_PYBIND11 "Download Pybind11" ON)

if(EXO_DOWNLOAD_PYBIND11)
  FetchContent_Declare(pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.4.3
  )

  Exo_MakeAvailable(pybind11 EXCLUDE_FROM_ALL)
else()
  find_package(pybind11 REQUIRED)
endif()

option(EXO_DOWNLOAD_SPAN_LITE "Download span-lite" ON)

if(EXO_DOWNLOAD_SPAN_LITE)
  FetchContent_Declare(span-lite
    GIT_REPOSITORY https://github.com/martinmoene/span-lite.git
    GIT_TAG e03d1166ccc8481d993dc02aae703966301a5e6e
  )

  Exo_MakeAvailable(span-lite EXCLUDE_FROM_ALL)
else()
  find_package(span-lite REQUIRED)
endif()

add_library(exo STATIC)

target_sources(exo
  PRIVATE
    ${PROJECT_SOURCE_DIR}/src/exo/exo.cpp
    ${PROJECT_SOURCE_DIR}/src/exo/exo.hpp
    ${PROJECT_SOURCE_DIR}/src/exo/matrix_span.hpp
)

set_target_properties(exo
  PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

target_include_directories(exo
  PUBLIC
    ${PROJECT_SOURCE_DIR}/src
)

target_link_libraries(exo
  PUBLIC
    nonstd::span-lite
)

pybind11_add_module(exopy ${PROJECT_SOURCE_DIR}/src/exopy/exopy.cpp)

target_include_directories(exopy
  PRIVATE
    ${PROJECT_SOURCE_DIR}/src
)

target_link_libraries(exopy
  PRIVATE
    exo
)

# this is necessary for pybind11 v2.4.3 when compiled for C++ 17 with clang
# pybind11 assumes that the compiler is fully compliant with the standard
# but through at least clang 8 this option in off by default
# this is problem is fixed in a later pybind11 commit but there is no official release yet
# referenced in issue https://github.com/pybind/pybind11/issues/1604
# fixed in commit 759221f5c56939f59d8f342a41f8e2d2cacbc8cf
if (${CMAKE_CXX_COMPILER_ID} STREQUAL "GNU" OR ${CMAKE_CXX_COMPILER_ID} STREQUAL "Clang" OR ${CMAKE_CXX_COMPILER_ID} STREQUAL "AppleClang")
  target_compile_options(exopy PUBLIC -fsized-deallocation)
endif()

install(TARGETS exopy
  EXPORT exopyTargets
  LIBRARY DESTINATION .
  ARCHIVE DESTINATION .
  RUNTIME DESTINATION .
  INCLUDES DESTINATION .
)

option(EXO_ENABLE_PACKAGING "Enabling packaging for exopy" ON)

if(EXO_ENABLE_PACKAGING)
  include(CPack)
endif()
