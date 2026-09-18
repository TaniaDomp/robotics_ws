import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

#Este nodo recibe los mensajes del topico /analog, lee los mensajes (tipo Int32) e imprime en pantalla el valor 
class AnalogSubscriber(Node):
    def __init__(self):
        super().__init__('analog_subscriber')
        #Se hace la suscripcion
        self.subscription_ = self.create_subscription(Int32, '/analog', self.analog_callback, 10)
        self.get_logger().info('Esperando datos')

    #Imprime los valores en pantalla
    def analog_callback(self, msg):
        valor = msg.data
        self.get_logger().info(f'ADC = {valor}')

def main(args=None):
    rclpy.init(args=args)
    node = AnalogSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
