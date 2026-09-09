import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityTurtlePub(Node):

    def __init__(self):
        super().__init__('velocity_turtle_pub')

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.vel = 0.0
        self.timer_ = self.create_timer(0.5, self.publish_velocity)

    def publish_velocity(self):
        msg = Twist()

        if self.vel <= 1.2:
            msg.linear.x = self.vel
            self.publisher_.publish(msg)
            self.get_logger().info(f'Velocidad enviada: {self.vel:.1f} m/s')
            self.vel = round(self.vel + 0.1, 1)
        else:
            msg.linear.x = 0.0
            self.publisher_.publish(msg)
            self.get_logger().info('Velocidad maxima alcanzada (1.2 m/s). Tortuga deteniéndose.')
            self.timer_.cancel() 


def main(args=None):
    rclpy.init(args=args)
    node = VelocityTurtlePub()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()