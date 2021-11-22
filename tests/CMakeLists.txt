project(STLIB_tests)

set(SOURCE_FILES
      ${CMAKE_CURRENT_SOURCE_DIR}/STLIB_test.cpp
)

find_package(SofaPython3 REQUIRED)
find_package(SofaGTestMain REQUIRED)
find_package(SofaFramework REQUIRED)

set(TEST_FILES
   )

enable_testing()
add_executable(${PROJECT_NAME} ${SOURCE_FILES} ${TEST_FILES})
set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "-DSTLIB_SRC_DIR=${CMAKE_CURRENT_SOURCE_DIR}/../src/python3/")
target_link_libraries(${PROJECT_NAME} SofaGTestMain SofaHelper SofaPython3::Plugin)

add_test(NAME ${PROJECT_NAME} COMMAND ${PROJECT_NAME})

#file(COPY python3/ DESTINATION ${CMAKE_BINARY_DIR}/bin/stlib-tests/tests)
