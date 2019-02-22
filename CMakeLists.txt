cmake_minimum_required(VERSION 3.5)

# Force cmake to use the NEW policy regarding the "VERSION" management.
cmake_policy(SET CMP0048 NEW)

project(STLIB VERSION 1.0)

find_package(SofaFramework REQUIRED)
find_package(SofaPython REQUIRED)

include(cmake/environment.cmake)

set(HEADER_FILES src/initPlugin.h)
set(SOURCE_FILES src/initPlugin.cpp)

file(GLOB_RECURSE RESOURCE_FILES  "*.md" "*.psl" "*.py" "*.pyscn" "*.scn" "*.rst")

# Config files and install rules for pythons scripts
sofa_set_python_directory(${PROJECT_NAME} "python")

add_library(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES} ${RESOURCE_FILES})
set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "-DSOFA_BUILD_STLIB")
target_link_libraries(${PROJECT_NAME} SofaCore SofaPython)
target_include_directories(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/include>")
target_include_directories(${PROJECT_NAME} PUBLIC "$<INSTALL_INTERFACE:include>")

## Install rules for the library and headers; CMake package configurations files

sofa_generate_package(NAME STLIB VERSION ${PROJECT_VERSION} TARGETS ${PROJECT_NAME}
    INCLUDE_INSTALL_DIR STLIB
    INCLUDE_SOURCE_DIR "src")

install(DIRECTORY docs DESTINATION share/sofa/${PROJECT_NAME})
install(FILES "README.md" "LICENSE" DESTINATION .)

include(cmake/packaging.cmake)
