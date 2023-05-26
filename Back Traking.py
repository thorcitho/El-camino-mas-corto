import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Button, TextBox

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
        
        all_paths = find_all_paths(start_point, end_point)
        if all_paths:
            shortest_path = find_shortest_path(all_paths)
            if shortest_path:
                for i in range(len(shortest_path) - 1):
                    draw_line_and_calculate_distance(shortest_path[i], shortest_path[i+1])
        
        plt.show()

# Función para encontrar todos los caminos posibles entre dos puntos utilizando backtracking
def find_all_paths(start, end):
    visited = set()
    paths = []
    current_path = [start]
    
    backtrack(start, end, visited, paths, current_path)
    
    return paths

def backtrack(current_point, end, visited, paths, current_path):
    if current_point == end:
        paths.append(current_path.copy())
        return
    
    visited.add(current_point)
    
    for neighbor in get_neighbors(current_point):
        if neighbor not in visited:
            current_path.append(neighbor)
            backtrack(neighbor, end, visited, paths, current_path)
            current_path.pop()
    
    visited.remove(current_point)

# Función para obtener los vecinos de un punto
def get_neighbors(point):
    neighbors = set()
    for (point1, point2) in distances.keys():
        if point1 == point:
            neighbors.add(point2)
        elif point2 == point:
            neighbors.add(point1)
    return neighbors

# Función para encontrar el camino más corto entre varios caminos
def find_shortest_path(paths):
    shortest_path = None
    shortest_distance = float('inf')
    
    for path in paths:
        distance = calculate_total_distance(path)
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_path = path
    
    return shortest_path

# Función para calcular la distancia total de un camino
def calculate_total_distance(path):
    total_distance = 0
    
    for i in range(len(path) - 1):
        point1 = path[i]
        point2 = path[i+1]
        if (point1, point2) in distances:
            total_distance += distances[(point1, point2)]
    
    return total_distance

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
