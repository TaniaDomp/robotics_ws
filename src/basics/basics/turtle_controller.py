#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist

#Este nodo se suscribe al topico /joystick_raw para recibir las lecturas del joystick en un mensaje Int32MultiArray.
#Se encarga de hacer la conversion de las unidades a velocidad linear y angular, publica estas en un mensaje Twist por 
#medio del topico /turtle1/cmd_vel.
class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        # Parametros de calibracion (se eligieron de acuerdo a lo observado en el serial monitor de arduino)
        self.CENTER_X = 1870
        self.CENTER_Y = 1804
        self.DEAD_ZONE = 250   # Zona muerta de +-250 alrededor del centro
        self.ADC_MAX = 4095

        # Limites de las velocidades
        self.MAX_LIN_VEL = 2.0  # m/s
        self.MAX_ANG_VEL = 2.0  # rad/s

        # Suscriptor al topico /joystick_raw
        self.subscription_ = self.create_subscription(Int32MultiArray, '/joystick_raw', self.joy_callback,10)

        # Publicador para /turtle1/cmd_vel
        self.cmd_vel_pub_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def calcular_velocidad_proporcional(self, raw_val, centro):
        #Aplica la zona muerta y realiza el control proporcional escalado en [-1.0, 1.0]
        diferencia = raw_val - centro

        # Posicion neutral: si el valor esta a 250 de la poisicion centro se define velocidad 0.0
        if abs(diferencia) <= self.DEAD_ZONE:
            return 0.0

        # Escala la lectura entre 0.0 y 1.0 (o -1.0) desde el borde de la zona muerta, 
        # garantizando una aceleración suave sin saltos al salir del punto neutro.
        if diferencia > 0:
            rango_util = self.ADC_MAX - centro - self.DEAD_ZONE
            normalizado = (diferencia - self.DEAD_ZONE) / rango_util
        else:
            rango_util = centro - self.DEAD_ZONE
            normalizado = (diferencia + self.DEAD_ZONE) / rango_util

        # Garantiza un rango estricto entre -1.0 y 1.0
        return max(-1.0, min(1.0, normalizado))

    def joy_callback(self, msg):
        #Recibe los mensajes
        if len(msg.data) < 2:
            return

        raw_x = msg.data[0]
        raw_y = msg.data[1]

        # Calcular los factores de escala proporcional [-1.0, 1.0]
        prop_x = self.calcular_velocidad_proporcional(raw_x, self.CENTER_X)
        prop_y = self.calcular_velocidad_proporcional(raw_y, self.CENTER_Y)

        # Construccion Twist
        # Eje Y: Avance y retroceso (velocidad lineal)
        # Eje X: Rotacion (velocidad angular)
        twist = Twist()
        twist.linear.x = prop_y * self.MAX_LIN_VEL
        twist.angular.z = prop_x * self.MAX_ANG_VEL

        self.cmd_vel_pub_.publish(twist)
        self.get_logger().info(f'Lineal: {twist.linear.x:.2f} m/s | Angular: {twist.angular.z:.2f} rad/s')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()