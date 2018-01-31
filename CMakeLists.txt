cmake_minimum_required(VERSION 3.5)

# Force cmake to use the NEW policy regaringthe "VERSION" management.
cmake_policy(SET CMP0048 NEW)

project(STLIB VERSION 1.0)

set(HEADER_FILES src/initPlugin.h)
set(SOURCE_FILES src/initPlugin.cpp)

file(GLOB_RECURSE RESOURCE_FILES  "*.md" "*.psl" "*.py" "*.pyscn" "*.scn")

add_library(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES} ${RESOURCE_FILES})



