from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        # 1. Nodo del simulador Turtlesim
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),

        # 2. Nodo publicador del Joystick / ESP32
        Node(
            package='basics',
            executable='turtlejoy_pub',
            name='turtlejoy_pub',
            output='screen'
        ),

        # 3. Nodo controlador de movimiento
        Node(
            package='basics',
            executable='turtle_controller',
            name='turtle_controller',
            output='screen'
        ),

    ])