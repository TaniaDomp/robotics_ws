import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import serial

#Este nodo lee los datos de la ESP32 y los transforma para mandarlos en un arreglo de dos Int32 (primero manda el del ejex 
#y luego el del y), manda estos mensajes en el topico /joystick_raw
class JoySerialPublisher(Node):
    def __init__(self):
        super().__init__('turtlejoy_pub')

        #Creacion del topico
        self.publisher_ = self.create_publisher(Int32MultiArray, '/joystick_raw', 10)

        # Conexion al puerto serie
        try:
            self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            self.get_logger().info('ESP32 conectada exitosamente en /dev/ttyUSB0')
        except serial.SerialException as e:
            self.get_logger().error(f'Error al abrir el puerto serie: {e}')

        # Se establece un temporizador a ~50 Hz
        self.timer_ = self.create_timer(0.02, self.read_serial_and_publish)

    def read_serial_and_publish(self):
        if hasattr(self, 'serial_') and self.serial_.in_waiting > 0:
            try:
                linea = self.serial_.readline().decode('utf-8').strip()
                # Parseo usando el tabulador '\t' 
                partes = linea.split('\t')
                if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                    raw_x = int(partes[0])
                    raw_y = int(partes[1])
                    #Construccion del mensaje
                    msg = Int32MultiArray()
                    msg.data = [raw_x, raw_y]
                    self.publisher_.publish(msg)
            except (ValueError, UnicodeDecodeError) as e:
                self.get_logger().warn(f'Linea con formato no valido: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = JoySerialPublisher()
    rclpy.spin(node)
    if hasattr(node, 'serial_') and node.serial_.is_open: #Para evitar bloqueo del puerto
        node.serial_.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()