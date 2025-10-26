# gazebo_sfm_plugin

## 简要介绍

本仓库为gazebo_sfm_plugin based on Ubuntu22.04-ros2-humble and gazebo classic version

其中代码基本上来自https://github.com/robotics-upo/lightsfm的头文件以及https://github.com/robotics-upo/gazebo_sfm_plugin的galactic分支

## 使用方法

```bash
# 进入src所在的文件夹
colcon build
# 执行以下代码进行测试（注意需要使用到gazebo的自带模型）
ros2 launch gazebo_sfm_plugin cafe_ros2.launch.py
```

若没有gazebo的自带模型：

```bash
git clone https://github.com/osrf/gazebo_models ~/.gazebo/models
```

## 仓库代码内容

其中对gazebo_sfm_plugin的CMakeLists.txt以及package.xml做出如下修改：

```python
# CMakeLists.txt

# 手动查找lightsfm（因为它是头文件库）
# find_path(LIGHTSFM_INCLUDE_DIRS
#   NAMES sfm.hpp
#   PATHS /usr/local/include /opt/ros/${ROS_DISTRO}/include ${CMAKE_INSTALL_PREFIX}/include
#   PATH_SUFFIXES lightsfm
# )

set(LIGHTSFM_INCLUDE_DIRS ../lightsfm/include)
include_directories(${LIGHTSFM_INCLUDE_DIRS})

message(STATUS "Using lightsfm from: ${LIGHTSFM_INCLUDE_DIRS}")
```

```python
# package.xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>gazebo_sfm_plugin</name>
  <version>1.0.0</version>
  <description>The gazebo_sfm_plugin package</description>

  <maintainer email="noeperez@upo.es">Noé Pérez-Higueras</maintainer>
  <license>BSD</license>
  <url type="repository">https://github.com/robotics-upo/gazebo_sfm_plugin</url>
  <author>Noé Pérez</author>

  <buildtool_depend>ament_cmake</buildtool_depend>
  
  <!-- 修复依赖项：使用ROS2包名 -->
  <depend>rclcpp</depend>
  <depend>gazebo_ros</depend>
  <depend>geometry_msgs</depend>
  <depend>std_msgs</depend>

  <!-- lightsfm依赖需要特殊处理 -->
  <build_depend>lightsfm</build_depend>

  <export>
    <build_type>ament_cmake</build_type>
    <gazebo_ros plugin_path="${prefix}/lib" gazebo_media_path="${prefix}/share/${PROJECT_NAME}" />
  </export>
</package>
```

然后修改gazebo_sfm_plugin/launch/cafe_ros2.launch.py以及gazebo_sfm_plugin/worlds/cafe3.world如下：

```python
#gazebo_sfm_plugin/launch/cafe_ros2.launch.py
#!/usr/bin/env python3

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
import os

def generate_launch_description():
    # 获取包路径
    pkg_share = get_package_share_directory('gazebo_sfm_plugin')
    
    # 世界文件路径
    world_path = os.path.join(pkg_share, 'worlds', 'cafe3.world')
    
    # 插件路径
    plugin_path = os.path.join(pkg_share, 'lib')
    
    # 模型路径
    model_path = os.path.join(pkg_share, 'media', 'models')
    home_model_path = os.path.expanduser('~/.gazebo/models')
    
    # 检查文件是否存在
    if not os.path.exists(world_path):
        print(f"错误: 世界文件不存在: {world_path}")
        return LaunchDescription()
    
    print(f"使用世界文件: {world_path}")
    print(f"插件路径: {plugin_path}")
    print(f"模型路径: {model_path}")
    
    # 设置环境变量
    env_vars = {
        'GAZEBO_PLUGIN_PATH': plugin_path,
        'GAZEBO_MODEL_PATH': f"{model_path}:{home_model_path}",
    }
    
    return LaunchDescription([
        # 设置环境变量
        SetEnvironmentVariable(
            name='GAZEBO_PLUGIN_PATH',
            value=env_vars['GAZEBO_PLUGIN_PATH']
        ),
        
        SetEnvironmentVariable(
            name='GAZEBO_MODEL_PATH', 
            value=env_vars['GAZEBO_MODEL_PATH']
        ),
        
        # 直接启动 gazebo（包含服务器和客户端）
        ExecuteProcess(
            cmd=[
                'gazebo',  # 使用 gazebo 命令而不是 gzserver/gzclient
                '--verbose',
                world_path
            ],
            output='screen',
            shell=False
        ),
    ])
```

```
#gazebo_sfm_plugin/worlds/cafe3.world
其中的所有actot都修改为普通的dae
  <skin>
    <filename>walk.dae</filename> 
    <scale>1.0</scale>
  </skin>
  <animation name="walking">
    <filename>walk.dae</filename> 
    <scale>1.000000</scale>
    <interpolate_x>true</interpolate_x>
  </animation>
```

