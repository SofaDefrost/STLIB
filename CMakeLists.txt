cmake_minimum_required(VERSION 3.5)

# Force cmake to use the NEW policy regaringthe "VERSION" management.
cmake_policy(SET CMP0048 NEW)

project(STLIB VERSION 1.0)

find_package(SofaPython QUIET)
if(!SofaPython_FOUND)
    message(FATAL_ERROR "-- STLIB requires the SofaPython plugin to be activated.")
endif()

set(HEADER_FILES src/initPlugin.h)
set(SOURCE_FILES src/initPlugin.cpp)

file(GLOB_RECURSE RESOURCE_FILES  "*.md" "*.psl" "*.py" "*.pyscn" "*.scn" "*.rst")

# Config files and install rules for pythons scripts
sofa_set_python_directory(${PROJECT_NAME} "python")

add_library(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES} ${RESOURCE_FILES})

set_target_properties(${PROJECT_NAME} PROPERTIES PUBLIC_HEADER "${HEADER_FILES}")
# target_include_directories(${PROJECT_NAME} PUBLIC "$<INSTALL_INTERFACE:include>")

## Install rules for the library and headers; CMake package configurations files

sofa_create_package(STLIB ${PROJECT_VERSION} ${PROJECT_NAME} STLIB)
