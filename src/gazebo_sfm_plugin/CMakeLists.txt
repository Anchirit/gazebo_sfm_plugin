cmake_minimum_required(VERSION 3.8)
project(gazebo_sfm_plugin)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 寻找依赖项
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(Boost REQUIRED COMPONENTS thread)
find_package(gazebo REQUIRED)

# 手动查找lightsfm（因为它是头文件库）
# find_path(LIGHTSFM_INCLUDE_DIRS
#   NAMES sfm.hpp
#   PATHS /usr/local/include /opt/ros/${ROS_DISTRO}/include ${CMAKE_INSTALL_PREFIX}/include
#   PATH_SUFFIXES lightsfm
# )

set(LIGHTSFM_INCLUDE_DIRS ../lightsfm/include)
include_directories(${LIGHTSFM_INCLUDE_DIRS})

message(STATUS "Using lightsfm from: ${LIGHTSFM_INCLUDE_DIRS}")

if(NOT LIGHTSFM_INCLUDE_DIRS)
  message(WARNING "lightsfm not found in standard paths, trying src directory")
  find_path(LIGHTSFM_INCLUDE_DIRS
    NAMES sfm.hpp
    PATHS ${CMAKE_CURRENT_SOURCE_DIR}/../../lightsfm/include
    PATH_SUFFIXES lightsfm
  )
endif()

if(LIGHTSFM_INCLUDE_DIRS)
  message(STATUS "Found lightsfm at: ${LIGHTSFM_INCLUDE_DIRS}")
else()
  message(FATAL_ERROR "lightsfm not found. Please install it or clone to the workspace.")
endif()

# 包含目录
include_directories(include)
include_directories(SYSTEM
  ${LIGHTSFM_INCLUDE_DIRS}
  ${Boost_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
)

# 设置C++标准
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 添加库
add_library(PedestrianSFMPlugin SHARED src/PedestrianSFMPlugin.cpp)
target_include_directories(PedestrianSFMPlugin PUBLIC 
  include
  ${LIGHTSFM_INCLUDE_DIRS}
)

# 添加依赖
ament_target_dependencies(PedestrianSFMPlugin 
  rclcpp
  gazebo_ros
  geometry_msgs
  std_msgs
)

# 链接库
target_link_libraries(PedestrianSFMPlugin 
  ${GAZEBO_LIBRARIES}
  ${Boost_LIBRARIES}
)

ament_export_libraries(PedestrianSFMPlugin)

# 安装目标
install(TARGETS PedestrianSFMPlugin
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include
)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

install(DIRECTORY worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)

install(DIRECTORY media/
  DESTINATION share/${PROJECT_NAME}/media
)

ament_package()
