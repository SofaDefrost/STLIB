cmake_minimum_required(VERSION 3.5)
project(STLIB VERSION 3.0)

include(cmake/environment.cmake)

find_package(SofaFramework REQUIRED)
find_package(SofaPython3 REQUIRED)

if(SofaPython3_FOUND)
    message("-- Found SofaPython3")
    SP3_add_python_package(
        SOURCE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src/python3/stlib
        TARGET_DIRECTORY stlib
    )
    SP3_add_python_package(
        SOURCE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src/python3/stlib3
        TARGET_DIRECTORY stlib3
    )
    set(SofaPythonAny_FOUND TRUE)
endif()


find_package(SPLIB REQUIRED)

set(HEADER_FILES src/cpp/stlib/initPlugin.h)
set(SOURCE_FILES src/cpp/stlib/initPlugin.cpp)

file(GLOB_RECURSE RESOURCE_FILES  "*.md" "*.psl" "*.py" "*.pyscn" "*.scn" "*.rst")

add_library(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES} ${RESOURCE_FILES})
set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "-DSOFA_BUILD_STLIB")
set_target_properties(${PROJECT_NAME} PROPERTIES DEBUG_POSTFIX "_d")
target_link_libraries(${PROJECT_NAME} SofaCore)

## Install rules for the library and headers; CMake package configurations files
sofa_create_package_with_targets(
    PACKAGE_NAME STLIB
    PACKAGE_VERSION ${PROJECT_VERSION}
    TARGETS ${PROJECT_NAME} AUTO_SET_TARGET_PROPERTIES
    INCLUDE_INSTALL_DIR STLIB
    INCLUDE_SOURCE_DIR "src/cpp/stlib/"
    RELOCATABLE "plugins"
    )

install(DIRECTORY docs DESTINATION share/sofa/${PROJECT_NAME})
install(FILES "README.md" "LICENSE" DESTINATION .)

include(cmake/packaging.cmake)
