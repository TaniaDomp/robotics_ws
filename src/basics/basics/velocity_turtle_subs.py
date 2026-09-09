import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityTurtleSubs(Node):

    def __init__(self):
        super().__init__('velocity_turtle_subscriber')
        
        self.subscription_ = self.create_subscription(
            Twist,
            '/turtle1/cmd_vel',
            self.velocity_callback,
            10
        )
        self.get_logger().info('Suscriptor listo. Esperando mensajes...')

    def velocity_callback(self, msg):
        velocidad_x = msg.linear.x
        self.get_logger().info(f'Velocidad recibida: {velocidad_x:.1f} m/s')


def main(args=None):
    rclpy.init(args=args)
    node = VelocityTurtleSubs()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()