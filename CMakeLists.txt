cmake_minimum_required(VERSION 3.5)
project(stlib VERSION 1.0)

include(cmake/environment.cmake)

find_package(SofaPython3 REQUIRED)

# Config files and install rules for pythons scripts
SP3_add_python_package(
  SOURCE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/stlib
  TARGET_DIRECTORY stlib
  )

set (PYTHON_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/communication/UDP_controller.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/components/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/components/all.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/debug/__init__.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/loader/__init__.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/numerics/__init__.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/rigid/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/rigid/rigidobject.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/deformable/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/deformable/elasticmaterialobject.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/constraints/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/constraints/fixedbox.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/constraints/partiallyfixedbox.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/constraints/subTopology.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/collision/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/collision/collision.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/mixedmaterial/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/physics/mixedmaterial/rigidification.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/scene/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/scene/mainheader.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/scene/contactheader.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/scene/wrapper.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/scene/interaction.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/solver/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/solver/defaultsolver.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/tools/__init__.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/units/__init__.py

    ${CMAKE_CURRENT_SOURCE_DIR}/stlib/visuals/__init__.py
    )


add_library(STLIB_SCRIPTS INTERFACE)
target_sources(STLIB_SCRIPTS INTERFACE "${PYTHON_FILES}")

install(DIRECTORY docs DESTINATION share/sofa/${PROJECT_NAME})
install(FILES "README.md" "LICENSE" DESTINATION .)

include(cmake/packaging.cmake)
