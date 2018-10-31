cmake_minimum_required(VERSION 3.5)

# Force cmake to use the NEW policy regarding the "VERSION" management.
cmake_policy(SET CMP0048 NEW)

## Change default install prefix
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/install CACHE PATH "Install path prefix, prepended onto install directories." FORCE)
endif()
message(STATUS "Install prefix: ${CMAKE_INSTALL_PREFIX}")

## Set the output directories globally
set(ARCHIVE_OUTPUT_DIRECTORY lib)
set(RUNTIME_OUTPUT_DIRECTORY bin)
if(WIN32)
    set(LIBRARY_OUTPUT_DIRECTORY ${RUNTIME_OUTPUT_DIRECTORY})
else()
    set(LIBRARY_OUTPUT_DIRECTORY ${ARCHIVE_OUTPUT_DIRECTORY})
endif()
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${ARCHIVE_OUTPUT_DIRECTORY})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${RUNTIME_OUTPUT_DIRECTORY})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${LIBRARY_OUTPUT_DIRECTORY})

project(STLIB VERSION 1.0)

find_package(SofaFramework)
find_package(SofaPython REQUIRED)

set(HEADER_FILES src/initPlugin.h)
set(SOURCE_FILES src/initPlugin.cpp)

file(GLOB_RECURSE RESOURCE_FILES  "*.md" "*.psl" "*.py" "*.pyscn" "*.scn" "*.rst")

# Config files and install rules for pythons scripts
sofa_set_python_directory(${PROJECT_NAME} "python")

add_library(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES} ${RESOURCE_FILES})
set_target_properties(${PROJECT_NAME} PROPERTIES PUBLIC_HEADER "${HEADER_FILES}")

set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "-DSOFA_BUILD_STLIB")
target_link_libraries(${PROJECT_NAME} SofaCore SofaPython)

## Install rules for the library and headers; CMake package configurations files

sofa_create_package(STLIB ${PROJECT_VERSION} ${PROJECT_NAME} STLIB)
