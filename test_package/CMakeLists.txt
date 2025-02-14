project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

# Use the env variable QT6_DIR to add Qt's cmake directory to CMAKE_PREFIX_PATH
if(NOT DEFINED ENV{QT6_DIR})
  message(STATUS "The environment variable QT6_DIR has not been set. It should point to the root location of your Qt6 installation")
endif()
list(APPEND CMAKE_PREFIX_PATH "$ENV{QT6_DIR}/lib/cmake")

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 COMPONENTS Widgets PrintSupport Core5Compat REQUIRED)
find_package(qplot REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example
    ${CONAN_LIBS}
    QPlot
    Qt6::Widgets
    Qt6::PrintSupport
    Qt6::Core5Compat
    )

# ------------------------------------------------------------------------------
# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
