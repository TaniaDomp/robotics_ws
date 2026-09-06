import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

#Este nodo recibe los mensajes, estos son de tipo Float32 
#y se mandan por el topico /velocity
class VelocitySubscriber(Node):
    #Se crea el nodo y se hace la suscripcion
    def __init__(self):
        super().__init__('velocity_subscriber')
        self.subscription_ = self.create_subscription(Float32,'/velocity',self.velocity_callback,10)

    #Se ejecuta cada que llega un mensaje, imprime en pantalla el contenido
    #con un decimal
    def velocity_callback(self, msg):
        Velocity = msg.data
        self.get_logger().info(f'Vel = {Velocity:.1f} m/s')

#Establece la configuracion necesaria para ROS
def main(args = None):
    # Inicia las comunicaciones 
    rclpy.init(args=args)
    #crea al nodo
    node = VelocitySubscriber()
    #indica que el nodo se queda trabajando hasta que se indique que debe detenerse
    rclpy.spin(node)
    #destruye el nodo y cierra la comunicacion
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()