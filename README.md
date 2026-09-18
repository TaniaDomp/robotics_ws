

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
[P3_LEDB.webm](https://github.com/user-attachments/assets/a1a76d7f-2f34-4a60-b12b-6d33891f764c)

## Potenciómetro

### Descripción breve

Lectura y monitoreo de datos analógicos obtenidos desde una ESP32 a través de una interfaz serial en ROS 2 (datos de un potenciómetro), publicando las lecturas del convertidor ADC en un tópico para ser leídas por un nodo suscriptor.

Modificaciones realizadas

* Se empleó el tipo de mensaje `std_msgs/msg/Int32` para procesar y publicar los valores enteros leídos del puerto analógico.

* El nodo `analog_serial_pub.py` se configuró para leer de forma continua (cada 0.01 segundos) la entrada serial desde la ESP32 a través de `/dev/ttyUSB0` a 115200 baudios, decodificar el texto, validar que sea un valor numérico e insertarlo en la trama de ROS2.

* El nodo `analog_subscriber.py` se implementó para recibir las lecturas del ADC e imprimirlas directamente en la terminal en tiempo real.

* Se utilizó la librería `pyserial` para la comunicación y lectura de los caracteres provenientes de la tarjeta de desarrollo.

### Funcionamiento

* **Tópico utilizado:** `/analog`

* **Tipo de mensaje:** `std_msgs/msg/Int32`

* **Publicador / Puente (analog_serial_pub.py):** Captura la lectura del puerto serie enviada por la ESP32, la convierte a un número entero y la publica en el tópico `/analog`.

* **Suscriptor (analog_subscriber.py):** Se suscribe al tópico `/analog`, escucha las lecturas entrantes del ADC y despliega en pantalla los valores numéricos correspondientes.

### Comandos utilizados

```bash
# Terminal 1: Lanzar el nodo puente de comunicación serial
ros2 run basics analog_serial_pub

# Terminal 2: Lanzar el nodo publicador para parpadeo del LED
ros2 run basics analog_subs
```

### Problemas encontrados y soluciones
**Problema:** Cuando se trató de subir el código no se mostraban los datos.

**Solución:** Se desconectó y se volvió a conectar la tarjeta.

### Video de funcionamiento
[P3_POT.webm](https://github.com/user-attachments/assets/82b04d8d-143f-44ff-bdab-3fcfb24dc4fe)

## Tarea: Control Proporcional de Turtlesim mediante Joystick HW-504 y ESP32

### Descripción breve

Desarrollo e integración de un sistema en ROS2 para manipular la velocidad lineal y angular del simulador Turtlesim en tiempo real, empleando un joystick HW-504 conectado a una ESP32 mediante comunicación Serial USB.

### Modificaciones y desarrollos realizados

* Se programó la ESP32 en Arduino para realizar la lectura del joystick (ADC de 12 bits) y transmitirlos en formato `xValue \t yValue`.
* Se implementó un nodo publicador en Python para leer de manera continua el puerto serie (`/dev/ttyUSB0`), extraer las lecturas y publicarlas en ROS2.
* Se diseñó un nodo controlador que ajusta los valores del joystick aplicando filtrado por zona muerta y escalando los valores, convirtiendo las lecturas en comandos de velocidad.

### Justificación Técnica de Parámetros de Control

* **Valores del Centro (`CENTER_X = 1870`, `CENTER_Y = 1804`):** Se determinó que los valores neutros son $1870$ para el eje X y $1804$ para el eje Y por medio de la observación de los datos en el monitor serial de arduino.

* **Zona Muerta (`DEAD_ZONE = ±250`):** Por medio de investigación (y observando el comportamiento de los valores en el monitor serial) se definió un margen de $\pm 250$ unidades alrededor de cada centro.

* **Límites de Velocidad Máxima (`MAX_LIN_VEL = 2.0 m/s`, `MAX_ANG_VEL = 2.0 rad/s`):** Se establecieron en $2.0$ para asegurar una respuesta fluida dentro de Turtlesim ($11 \times 11$ metros). Con valores mayores la tortuga choca con las paredes demasiado rápido, mientras que con valores menores no se aprecia la aceleración.

* **Control Proporcional fuera de la Zona Muerta:** Para evitar cambios bruscos de velocidad (escalones) al salir de la zona muerta, la función *calcular_velocidad_proporcional* mapea el recorrido restante hasta los extremos ($0$ y $4095$) para que la velocidad inicie de forma continua en $0.0$ justo al cruzar el límite de la zona muerta y alcance suavemente el $100\%$ ($\pm 1.0$) al llegar al tope físico.

### Funcionamiento de los nodos y arquitectura

* **Publicador Serial (`turtlejoy_pub.py`):**
  * **Nombre del nodo:** `turtlejoy_pub`
  * **Tópico publicado:** `/joystick_raw`
  * **Tipo de mensaje:** `std_msgs/msg/Int32MultiArray`
  * **Función:** Lee la trama serie enviada por la ESP32 a 115200 baudios, separa los valores numéricos mediante tabuladores y publica un arreglo de 2 enteros `[raw_x, raw_y]`.

* **Controlador de Movimiento (`turtle_controller.py`):**
  * **Nombre del nodo:** `turtle_controller`
  * **Tópicos:** Subscrito a `/joystick_raw` | Publica en `/turtle1/cmd_vel`
  * **Tipos de mensajes:** `std_msgs/msg/Int32MultiArray` y `geometry_msgs/msg/Twist`
  * **Función:** Recibe las lecturas del ADC ($0$ a $4095$), descuenta el desplazamiento del centro mecánico, aplica la tolerancia de la zona muerta y calcula de forma proporcional el porcentaje de inclinación. Asigna el eje Y a la velocidad lineal `linear.x` (adelante/atrás) y el eje X a la velocidad angular `angular.z` (izquierda/derecha).

* **Simulador Gráfico (`turtlesim_node`):**
  * **Nombre del nodo:** `turtlesim`
  * **Tópico suscrito:** `/turtle1/cmd_vel`
  * **Tipo de mensaje:** `geometry_msgs/msg/Twist`
  * **Función:** Recibe las velocidades vectoriales y ejecuta los movimientos físicos de la tortuga en la ventana gráfica.

### Comandos utilizados

Para ejecutar los programas en terminales separadas:

```bash
# Terminal 1: Lanzar la interfaz gráfica de Turtlesim
ros2 run turtlesim turtlesim_node

# Terminal 2: Lanzar el nodo publicador del puerto serie
ros2 run basics turtlejoy_pub

# Terminal 3: Lanzar el nodo controlador del movimiento
ros2 run basics turtle_controller
```

Para el monitoreo de los nodos:

```bash
# Monitorear la lectura proveniente de la ESP32
ros2 topic echo /joystick_raw

# Monitorear las velocidades enviadas a la tortuga
ros2 topic echo /turtle1/cmd_vel

# Ver el grafo de los nodos
ros2 run rqt_graph rqt_graph
```
### Problemas encontrados y soluciones
**Problema:** No se tenia muy claro como se tomaban los ejes físicos.

**Solución:** Se revisó documentación del joystick.

### Video de funcionamiento
https://github.com/user-attachments/assets/b42c2fd0-30c9-4c64-bce6-83f3adb0693a



