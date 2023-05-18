# Actividad Opcional

1 punto Extra

- Primera Convocatoria 10/02/2023

Desarrollar el algoritmo de A Star. En los apuntes clase se explica el funcionamiento del algoritmo A* para encontrar el camino más corto entre dos puntos. En la carpeta *act_opt/src* se puede encontrar una aplicación para ello.

- *main.py* es el punto de entrada y el script que debe ejecutarse para poner en funcionamiento la aplicación y poder probar el algoritmo.

- *app.py* es la parte encargada de gestionar el main loop. Al iniciarse crea un objeto de tipo *Maze* que representa al laberinto. Inicializa todos los recursos, crea un par de coordenadas (con sus respectivas imágenes), y crea un objeto de tipo *PathFinder* con el laberinto anterior y una heurística determinada. En la parte de procesamiento de entradas, responde al click izquierdo del ratón, el primer click determina la coordenada origen (verde), el segundo click determina la coordenada destino (rojo) y llama al *Pathfinder* para calcular el camino más corto. El render primero pinta la imagen de fondo del laberinto, luego el camino si lo hubiera, y luego las coordenadas de origen/destino.

- *maze.py* representa al laberinto, se carga desde disco a partir de una imagen bmp, internamente contiene una lista de dos dimensiones, donde para cada (fila, columna) guarda un 0 si el suelo es pisable, y un 1 si es una pared. Tiene un zoom para hacer la imagen más grande de 1 pixel por coordenada, y provee varias funciones helper para consultar datos sobre el laberinto, como su tamaño, si una coordenada es pisable, conversiones entre pixeles y coordenadas de laberinto,...

- *pathfinder.py* contiene el código necesario para el algoritmo A*, y se invoca a su método *calc_path* cuando se quiere calcular un camino. También contiene todas las funciones heurísticas habituales. La función *return_path* es la que realiza el backtracking para revertir el camino una vez encontrado.

- *node.py* es el objeto usado para cada nodo del algoritmo A*, donde cada nodo tiene una posición en el laberinto, un padre y unos costes.

En la clase *PathFinder* adjunta se incluye el prototipo de la función *calc_path*, que debe implementar el algoritmo A*. Este algoritmo debe usar la clase *Node* (para cada nodo que se recorre) definida en el mismo fichero como apoyo, y al final del algoritmo estos nodos tendrán cada uno el padre desde el que fueron alcanzados. De esta manera, la función ya implementada *return_path* será capaz de determinar el camino, una vez se cumpla la condición de salida (haber llegado al final). También se proveen tres funciones para distintas heurísticas, se puede usar libremente cualquiera de ellas.

Se provee también de toda la infraestructura para cargar el fichero del laberinto, y construirlo como una lista bidimensional (que se deberá usar para conocer el entorno, por filas, columnas), donde el primer nivel son las filas y luego las columnas. En cada punto del laberinto se tiene un 0 si esa baldosa es transitable, o un 1 si es una pared. Al clickar sobre el mapa una vez, se determina el punto de salida, y otro click determina el punto de finalización, y en ese momento se llama a la función para calcular el camino más corto.

Se deben adjuntar todos los ficheros que formen parte de la solución.