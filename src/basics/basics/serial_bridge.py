import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial

#Este nodo recibe mensajes Int32 del topico /led_command, los imprime en pantalla y los envia a la ESP32
#por medio de una conexion serial
class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')
        #Suscripcion al topico y creacion de la conexion
        self.subscription_ = self.create_subscription(Int32, '/led_command', self.led_callback,10)
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        self.get_logger().info('Esperando mensajes')

    #Impresion de los mensajes y envio a la ESP32
    def led_callback(self, msg):
        if msg.data == 1:
            self.serial_.write(b'1\n')
            self.get_logger().info('ROS 2 -> Serial: 1')

        elif msg.data == 0:
            self.serial_.write(b'0\n')
            self.get_logger().info('ROS 2 -> Serial: 0')


def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    rclpy.spin(node)
    node.serial_.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
