cmake_minimum_required(VERSION 3.5)
project(STLIB VERSION 3.0)

include(cmake/environment.cmake)

find_package(Sofa.Config REQUIRED)

set(HEADER_FILES src/initPlugin.h)
set(SOURCE_FILES src/initPlugin.cpp)

file(GLOB_RECURSE RESOURCE_FILES  "*.md" "*.psl" "*.py" "*.pyscn" "*.scn" "*.rst")

add_library(${PROJECT_NAME} SHARED ${HEADER_FILES} ${SOURCE_FILES} ${RESOURCE_FILES})
set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "-DSOFA_BUILD_STLIB")
set_target_properties(${PROJECT_NAME} PROPERTIES DEBUG_POSTFIX "_d")
target_link_libraries(${PROJECT_NAME} Sofa.Config)

## Install rules for the library and headers; CMake package configurations files
sofa_create_package_with_targets(
    PACKAGE_NAME STLIB
    PACKAGE_VERSION ${PROJECT_VERSION}
    TARGETS ${PROJECT_NAME} AUTO_SET_TARGET_PROPERTIES
    INCLUDE_INSTALL_DIR STLIB
    INCLUDE_SOURCE_DIR "src"
    RELOCATABLE "plugins"
    )

install(DIRECTORY docs DESTINATION share/sofa/${PROJECT_NAME})
install(FILES "README.md" "LICENSE" DESTINATION .)

# Install python2 scripts (macro defined in SOFA)
sofa_install_pythonscripts(PLUGIN_NAME ${PROJECT_NAME} PYTHONSCRIPTS_SOURCE_DIR "python" PYTHONSCRIPTS_INSTALL_DIR "python")

# Install python3 scripts (macro defined in SofaPython3)
find_file(SofaPython3Tools NAMES "SofaPython3/lib/cmake/SofaPython3/SofaPython3Tools.cmake")
if(SofaPython3Tools)
    message("-- Found SofaPython3Tools. Python3 packages will be installed.")
    include(${SofaPython3Tools})
    set(SP3_PYTHON_PACKAGES_DIRECTORY "python3/site-packages")
else()
    # try again with the find_package mechanism
    find_package(SofaPython3 COMPONENTS Plugin QUIET) # only to get SofaPython3Tools.cmake
endif()
if(SofaPython3Tools OR SofaPython3_FOUND)
    SP3_add_python_package(
        SOURCE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python3/src/splib3
        TARGET_DIRECTORY splib3
    )
    SP3_add_python_package(
        SOURCE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python3/src/stlib3
        TARGET_DIRECTORY stlib3
    )
endif()

include(cmake/packaging.cmake)
