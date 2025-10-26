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