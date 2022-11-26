cmake_minimum_required(VERSION 3.16)
set (CMAKE_CXX_STANDARD 20)

project(IsingModel)

find_package(OpenMP REQUIRED)

add_executable(test src/main.cpp)

add_executable(cluster src/cluster.cpp)

add_executable(mdist src/mdistribution.cpp)
