import matplotlib.pyplot as plt
import math

from matplotlib.widgets import Button
from matplotlib.widgets import TextBox

# Cargar la imagen de fondo
background_img = plt.imread('imagen.jpg')

# Definir los puntos fijos con nombres y coordenadas
points = {
    'esquisesqui': (725, 205),
    'puertaposgrado': (1146, 463),
    'puertaestadio': (874, 289),
    'puertaprincipal': (784, 289),
    'piscina': (1074, 633),
    'esceducacionfisica': (947, 668),
    'servisocial': (890, 753),
    'puntocar': (787, 775),
    'escenfermeria': (764, 670),
    'escodontologia': (632, 711),
    'auditorio': (727, 794),
    'escsistemas': (622, 938),
    'escelectronica': (587, 790),
    'esccivil': (560, 912),
    'puertacamal': (409, 887),
    'mediocaminocamal': (626, 583),
    'escmecanica': (586, 853),
    'educacionyestadio': (726, 437),
    'puertaeducacion': (702, 313)
    
}

# Crear una figura y configurar el evento de clic del mouse
fig, ax = plt.subplots()

# Mostrar la imagen de fondo
ax.imshow(background_img, extent=[0, 2000, 0, 1500])

# Agregar los puntos fijos a la gráfica
for point_name, (x, y) in points.items():
    plt.plot(x, y, 'ro')
    plt.text(x, y, point_name, fontsize=10, ha='center', va='bottom')

# Unir los puntos y calcular la distancia entre ellos
line_color = 'c'
distances = {}

def draw_line_and_calculate_distance(point1, point2):
    x1, y1 = points[point1]
    x2, y2 = points[point2]
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    distances[(point1, point2)] = distance
    distances[(point2, point1)] = distance  # Duplicar la distancia en la dirección opuesta
    
    plt.plot([x1, x2], [y1, y2], color=line_color)
    plt.text((x1 + x2) / 2, (y1 + y2) / 2, f'{distance:.2f}', fontsize=8, ha='center', va='bottom')

draw_line_and_calculate_distance('puertaposgrado', 'puertaestadio')
draw_line_and_calculate_distance('puertaestadio', 'puertaprincipal')
draw_line_and_calculate_distance('puertaprincipal', 'esquisesqui')
draw_line_and_calculate_distance('esquisesqui', 'puertaeducacion')
draw_line_and_calculate_distance('puertaposgrado', 'piscina')
draw_line_and_calculate_distance('piscina', 'esceducacionfisica')
draw_line_and_calculate_distance('esceducacionfisica', 'servisocial')
draw_line_and_calculate_distance('servisocial', 'puntocar')
draw_line_and_calculate_distance('puntocar', 'auditorio')
draw_line_and_calculate_distance('puntocar', 'escenfermeria')
draw_line_and_calculate_distance('auditorio', 'escsistemas')
draw_line_and_calculate_distance('escenfermeria', 'escodontologia')
draw_line_and_calculate_distance('escodontologia', 'escelectronica')
draw_line_and_calculate_distance('escelectronica', 'escmecanica')
draw_line_and_calculate_distance('escmecanica', 'esccivil')
draw_line_and_calculate_distance('escmecanica', 'escsistemas')
draw_line_and_calculate_distance('esccivil', 'puertacamal')
draw_line_and_calculate_distance('puertacamal', 'mediocaminocamal')
draw_line_and_calculate_distance('mediocaminocamal', 'puertaeducacion')
draw_line_and_calculate_distance('puertaeducacion', 'educacionyestadio')
draw_line_and_calculate_distance('educacionyestadio', 'escenfermeria')
draw_line_and_calculate_distance('puertaprincipal', 'educacionyestadio')

# Función para encontrar el punto más cercano al punto actual
def find_closest_point(current_point, unvisited_points):
    closest_point = None
    min_distance = math.inf
    
    for point in unvisited_points:
        distance = distances.get((current_point, point), math.inf)
        if distance < min_distance:
            closest_point = point
            min_distance = distance
    
    return closest_point

# Función para encontrar el camino más corto utilizando el algoritmo goloso
def find_shortest_path(start, end):
    unvisited_points = set(points.keys())
    unvisited_points.remove(start)
    
    current_point = start
    path = [current_point]
    
    while current_point != end:
        next_point = find_closest_point(current_point, unvisited_points)
        if next_point is None:
            break  # No se encontró un punto válido, salir del bucle
        
        path.append(next_point)
        unvisited_points.remove(next_point)
        current_point = next_point
    
    return path

# Función para manejar el evento de clic del botón "viaje"
def button_clicked(event):
    start_point = textbox_start.text.strip().lower()
    end_point = textbox_end.text.strip().lower()
    
    if start_point in points and end_point in points:
        plt.figure()
        ax = plt.gca()
        ax.imshow(background_img, extent=[0, 2000, 0, 1500])
        for point_name, (x, y) in points.items():
            plt.plot(x, y, 'ro')
            plt.text(x, y, point_name, fontsize=10, ha='center', va='bottom')
        
        shortest_path = find_shortest_path(start_point, end_point)
        if shortest_path:
            for i in range(len(shortest_path) - 1):
                draw_line_and_calculate_distance(shortest_path[i], shortest_path[i+1])
        
        plt.show()

# Crear el botón y los cuadros de texto
button_ax = plt.axes([0.7, 0.05, 0.1, 0.05])
button = Button(button_ax, 'Viaje')
button.on_clicked(button_clicked)

textbox_start_ax = plt.axes([0.1, 0.05, 0.15, 0.05])
textbox_start = TextBox(textbox_start_ax, 'Inicio', initial='')
textbox_end_ax = plt.axes([0.3, 0.05, 0.15, 0.05])
textbox_end = TextBox(textbox_end_ax, 'Fin', initial='')

# Mostrar el gráfico
plt.show()

# Imprimir las distancias calculadas
for (point1, point2), distance in distances.items():
    print(f'Distancia entre {point1} y {point2}: {distance:.2f}')
