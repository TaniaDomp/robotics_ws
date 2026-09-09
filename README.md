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
