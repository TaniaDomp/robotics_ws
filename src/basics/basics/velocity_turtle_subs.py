import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

#Este nodo recime mensajes Twist por medio del topico /turtle1/cmd_vel
class VelocityTurtleSubs(Node):

    def __init__(self):
        super().__init__('velocity_turtle_subscriber')
        #Nos suscribimos al topico y se indica que cada que llega un mensaje se llama a velocity_callback
        self.subscription_ = self.create_subscription(
            Twist,
            '/turtle1/cmd_vel',
            self.velocity_callback,
            10
        )
        self.get_logger().info('Suscriptor listo. Esperando mensajes...')

    #Se ejecuta cada que llega un mensaje
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