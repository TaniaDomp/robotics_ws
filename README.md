# Práctica: Publicador y Suscriptor de Velocidad en ROS 2

**Autor:** Tania Ariadna Dominguez Palma

## Práctica 1
### Descripción breve
En esta actividad aprendimos a conectar dos nodos en ROS 2 mediante un tópico, implementando un nodo **Publicador** (*Publisher*) y un nodo **Suscriptor** (*Subscriber*).

### Funcionamiento
* **Tópico utilizado:** `/velocity`
* **Tipo de mensaje:** `std_msgs/msg/Float32`

* **Publicador (`velocity_publisher.py`):** Genera y empaqueta un valor de velocidad de tipo `Float32`. Muestra en la terminal el dato que envía y actualiza el valor periódicamente a través de un *timer*.
* **Suscriptor (`velocity_subscriber.py`):** Se conecta al tópico `/velocity`, recibe los mensajes emitidos por el publicador y muestra la velocidad en la terminal.

### Comandos utilizados
Para compilar el paquete y configurar el entorno:
```bash
colcon build
```

Para ejecutar los nodos:

```bash
# Terminal 1: Ejecutar el publicador
ros2 run basics velocity_publisher

# Terminal 2: Ejecutar el suscriptor
ros2 run basics velocity_subscriber
```

### Problemas encontrados
**Problema**: Al intentar ejecutar los comandos *ros2 run basics ...*, la terminal no me reconocia el paquete.

**Solucion**: Se agrego la fuente del espacio de trabajo *(source ~/robotics_ws/install/setup.bash)* al archivo *~/.bashrc* para que las variables de entorno se carguen automaticamente en cada nueva terminal.

### Video de funcionamiento
[Practica1.webm](https://github.com/user-attachments/assets/8090ebe5-1510-48a8-be96-2a1aed5ae069)


## Práctica 2

### Descripción breve

Integración y control de velocidad en el simulador gráfico Turtlesim mediante nodos modificados de publicación y suscripción para observar el movimiento real de la tortuga en pantalla.

Modificaciones realizadas

* Se adaptaron los scripts para utilizar el tipo de mensaje geometry_msgs/msg/Twist.

* El nodo velocity_turtle_pub.py se modificó para incrementar la velocidad lineal linear.x de 0.0 a 1.2 m/s en pasos de 0.1 m/s cada medio segundo.

* Al alcanzar los 1.2 m/s, el publicador manda velocidad 0.0 para detener a la tortuga y cancela su temporizador.

* Se agregó la dependencia <exec_depend>geometry_msgs</exec_depend> en package.xml y se registraron los comandos ejecutables en setup.py.

### Funcionamiento

* **Tópico utilizado:** `/turtle1/cmd_vel`

* **Tipo de mensaje:** `geometry_msgs/msg/Twist`

* **Publicador (velocity_turtle_pub.py):** Transmite las órdenes de movimiento en el eje X directamente al tópico de la tortuga.

* **Suscriptor (velocity_turtle_subs.py):** Escucha las órdenes transmitidas a la tortuga y despliega en la terminal el valor actual de velocidad recibida.

### Comandos utilizados

Para compilar y preparar el entorno:
```bash
colcon build
```

Para ejecutar la simulación simultánea (en terminales separadas):

```bash
# Terminal 1: Lanzar Turtlesim
ros2 run turtlesim turtlesim_node

# Terminal 2: Lanzar el suscriptor
ros2 run basics velocity_turtle_subs

# Terminal 3: Lanzar el publicador
ros2 run basics velocity_turtle_pub
```

### Problemas encontrados y soluciones

**Problema:** Ocurrió un error de importación (Traceback) al intentar ejecutar el suscriptor debido a residuos de compilación previa.

**Solución:** Se limpiaron los directorios de compilación con rm *-rf build/ install/ log/* y se recompiló el paquete con *colcon build*.

### Video de funcionamiento
[Practica2.webm](https://github.com/user-attachments/assets/e990a258-1449-4a30-b8ef-914a696dae70)

## Práctica 3
## Led blink
### Descripción breve

Integración y comunicación entre ROS 2 y una tarjeta ESP32 mediante puerto serie para el control de parpadeo de un LED, utilizando un nodo publicador de estados y un nodo puente (bridge) de comunicación serial.

Modificaciones realizadas

* Se implementó el tipo de mensaje `std_msgs/msg/Int32` para transmitir los estados de encendido (1) y apagado (0).

* El nodo `led_blink.py` se diseñó para alternar el estado del LED (0 o 1) mediante un temporizador configurado a cada 1.0 segundo.

* El nodo `serial_bridge.py` se configuró para suscribirse al tópico del LED y enviar las órdenes en formato de texto (`b'1\n'` / `b'0\n'`) a través del puerto serie (`/dev/ttyUSB0` a 115200 baudios).

* Se incluyó la librería `pyserial` para la gestión de la interfaz de puerto serie en el nodo puente.

### Funcionamiento

* **Tópico utilizado:** `/led_command`

* **Tipo de mensaje:** `std_msgs/msg/Int32`

* **Publicador (led_blink.py):** Genera y conmuta el estado lógico (1 para encendido, 0 para apagado) cada segundo y lo transmite al tópico.

* **Suscriptor / Puente (serial_bridge.py):** Escucha el tópico `/led_command` y retransmite las órdenes recibidas de ROS2 hacia la ESP32 a través de la conexión serial.

### Comandos utilizados

Para ejecutar en dos terminales separadas:

```bash
# Terminal 1: Lanzar el nodo puente de comunicación serial
ros2 run basics serial_bridge

# Terminal 2: Lanzar el nodo publicador para parpadeo del LED
ros2 run basics led_blink
```
### Problemas encontrados y soluciones

**Problema:** Cuando se trató de subir el código a la tarjeta aparecia un error de permisos.

**Solución:** Se ejecutó el comando *sudo chmod 777 /dev/ttyUSB0* para establecer la conexión.

### Video de funcionamiento

