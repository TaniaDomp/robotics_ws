import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

#Este nodo manda los mensajes, estos son de tipo Float32 
#y se mandan por el topico /velocity
class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('velocity_publisher')
        self.publisher_ = self.create_publisher(Float32,'/velocity',10)
        #Inicia el valor de la velocidad
        self.Vel = 0.0
        #indica que el mensaje se publica cada 0.5s (manda a llamar al metodo
        #publish_velocity)
        self.timer_ = self.create_timer(0.5,self.publish_velocity)

    def publish_velocity(self):
        #Prepara el mensaje
        msg = Float32()
        msg.data = self.Vel
        # Envia el mensaje al topico
        self.publisher_.publish(msg)
        self.get_logger().info(f'Vel = {self.Vel:.1f}')

        #Se hace un bucle, cuando Vel llega a 1.5 se reincia a 0
        if self.Vel < 1.5:
            self.Vel = round(self.Vel + 0.1, 1)
        else:
            self.Vel = 0.0

#Establece la configuracion necesaria para ROS (igual que en el subscriber)
def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()