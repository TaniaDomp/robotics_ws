# Práctica: Publicador y Suscriptor de Velocidad en ROS 2

**Autor:** Tania Ariadna Dominguez Palma

## Descripción breve
En esta actividad aprendimos a conectar dos nodos en ROS 2 mediante un tópico, implementando un nodo **Publicador** (*Publisher*) y un nodo **Suscriptor** (*Subscriber*).

## Funcionamiento
* **Tópico utilizado:** `/velocity`
* **Tipo de mensaje:** `std_msgs/msg/Float32`

* **Publicador (`velocity_publisher.py`):** Genera y empaqueta un valor de velocidad de tipo `Float32`. Muestra en la terminal el dato que envía y actualiza el valor periódicamente a través de un *timer*.
* **Suscriptor (`velocity_subscriber.py`):** Se conecta al tópico `/velocity`, recibe los mensajes emitidos por el publicador y muestra la velocidad en la terminal.

## Comandos utilizados
Para compilar el paquete y configurar el entorno:
```bash
colcon build
source install/setup.bash
```

Para ejecutar los nodos:

```bash
# Terminal 1: Ejecutar el publicador
ros2 run basics velocity_publisher

# Terminal 2: Ejecutar el suscriptor
ros2 run basics velocity_subscriber
```

## Comandos utilizados
**Problema**: Al intentar ejecutar los comandos *ros2 run basics ...*, la terminal no me reconocia el paquete.

**Solucion**: Se agrego la fuente del espacio de trabajo (source ~/robotics_ws/install/setup.bash) al archivo ~/.bashrc para que las variables de entorno se carguen automaticamente en cada nueva terminal.