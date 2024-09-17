import pygame
import math
import os

# Configuraciones iniciales
WIDTH, HEIGHT = 1350, 880
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 71, 125)

# Inicializar Pygame
pygame.init()

# Cargar imágenes
rotacion_image_path = 'C:/Users/carli/Documents/7to Semestre/INGENIERIA DEL SOFTWARE II/Static balance simulator/Simulador_Equilibrio_Estatico/Giro.png'
peso_image_path = 'C:/Users/carli/Documents/7to Semestre/INGENIERIA DEL SOFTWARE II/Static balance simulator/Simulador_Equilibrio_Estatico/Peso.png'
polea_image_path = 'C:/Users/carli/Documents/7to Semestre/INGENIERIA DEL SOFTWARE II/Static balance simulator/Simulador_Equilibrio_Estatico/Poleas2.png'
rope_image_path = 'C:/Users/carli/Documents/7to Semestre/INGENIERIA DEL SOFTWARE II/Static balance simulator/Simulador_Equilibrio_Estatico/1.png'
fondo_image_path = 'C:/Users/carli/Documents/7to Semestre/INGENIERIA DEL SOFTWARE II/Static balance simulator/Simulador_Equilibrio_Estatico/Fondo3.png'

# Cargar imágenes
rotacion_image = pygame.image.load(os.path.abspath(rotacion_image_path))
peso_image = pygame.image.load(os.path.abspath(peso_image_path))
polea_image = pygame.image.load(os.path.abspath(polea_image_path))
rope_image = pygame.image.load(os.path.abspath(rope_image_path))
fondo_image = pygame.image.load(os.path.abspath(fondo_image_path))

# Redimensionar imágenes (si es necesario)
peso_image = pygame.transform.scale(peso_image, (520, 450))
polea_image = pygame.transform.scale(polea_image, (200, 140))
rotacion_image = pygame.transform.scale(rotacion_image, (90, 70))
rope_image = pygame.transform.scale(rope_image,(420,420))



# Parámetros del sistema físico
weight = 100  
g = 9.81  
theta1, theta2 = 45, 45  
k = 50 

# Variables para manejar el arrastre del ratón
dragging = False
drag_start_x = 0
drag_start_y = 0
start_weight = weight
start_theta1 = theta1
start_theta2 = theta2

def solution(weight, theta1, theta2):
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    T22 = weight / (math.sin(theta2_rad) + math.cos(theta2_rad) * math.tan(theta1_rad))
    T11 = weight / (math.sin(theta1_rad) + math.cos(theta1_rad) * math.tan(theta2_rad))
    
    return T11, T22

# Función para calcular las tensiones
def calculate_tensions(weight, theta1, theta2):
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    
    denominator = math.sin(theta1_rad + theta2_rad)
    
    if denominator == 0:
        return 0, 0  # Para evitar la división por cero
    
    T2 = weight * math.sin(theta1_rad) / denominator
    T1 = weight * math.sin(theta2_rad) / denominator
    
    return T1, T2

# Función para calcular la posición del cuerpo
def calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2):
    denominator = (T1 * math.cos(math.radians(theta1)) + T2 * math.cos(math.radians(theta2)))
    
    if denominator == 0:
        return anchor1_x, anchor_y  # Evitar la división por cero, devolver una posición por defecto
    body_x = (T2 * math.cos(math.radians(theta2)) * anchor1_x + T1 * math.cos(math.radians(theta1)) * anchor2_x) / denominator
    body_y = anchor_y + T1 * math.sin(math.radians(theta1))
    return int(body_x), int(body_y)

def conversor(Kg):
    return Kg * 9.81

# Función para dibujar la escena
def draw_scene(screen, weight, theta1, theta2, result_conversion, conversor_visible):

    screen.fill(WHITE)
    
    mass = weight / g
    
    # Coordenadas de los puntos de anclaje
    anchor1_x = WIDTH // 4
    anchor2_x = 3 * WIDTH // 4
    anchor_y = HEIGHT // 4
    
    # Calcular las tensiones
    T1, T2 = calculate_tensions(weight, theta1, theta2)
    T11, T22 = solution(weight, theta1, theta2)
    
    # Calcular la posición del cuerpo
    body_x, body_y = calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2)
    
    # Definir el rectángulo de la imagen del cuerpo
    body_image_rect = peso_image.get_rect(center=(body_x, body_y))
    
    # Definir rectángulos de las imágenes de las poleas
    polea_image_rect1 = polea_image.get_rect(center=(anchor1_x, anchor_y - 22))
    polea_image_rect2 = polea_image.get_rect(center=(anchor2_x, anchor_y - 22))
    
    #Definir el fondo del simulaodr
    fondo_image_rect = fondo_image.get_rect(center = (anchor1_x + 335, anchor_y + 340))
    
    # Dibujar el soporte por encima de las poleas
    screen.blit(fondo_image, fondo_image_rect)
    
    # Rotar la imagen de rotación en el lado de theta1
    rotated_rotacion_image1 = pygame.transform.rotate(rotacion_image, theta1)
    rotacion_image_rect1 = rotated_rotacion_image1.get_rect(center=(anchor1_x, anchor_y + 20))
    
    # Rotar la imagen de rotación en el lado de theta2
    rotated_rotacion_image2 = pygame.transform.rotate(rotacion_image, theta2)
    rotacion_image_rect2 = rotated_rotacion_image2.get_rect(center=(anchor2_x, anchor_y + 20))
    
    # Dibujar las imágenes de giro rotadas para theta1 y theta2
    screen.blit(rotated_rotacion_image1, rotacion_image_rect1)
    screen.blit(rotated_rotacion_image2, rotacion_image_rect2)
    
    # Dibujar las cuerdas después de las imágenes de giro
    draw_rope(screen, (anchor1_x, anchor_y), (body_x, body_y), rope_image)
    draw_rope(screen, (anchor2_x, anchor_y), (body_x, body_y), rope_image)
    
    # Dibujar las imágenes 
    screen.blit(polea_image, polea_image_rect1)
    screen.blit(polea_image, polea_image_rect2)
    
    # Dibujar el cuerpo (imagen) por encima de la cuerda
    screen.blit(peso_image, body_image_rect)
    
    font_large = pygame.font.SysFont(None, 40)
    font = pygame.font.SysFont(None, 24)
    
    # Mostrar tensiones y ángulos cerca de las cuerdas
    text_T1 = font.render(f"T1: {T11:.2f} N", True, BLACK)
    text_T2 = font.render(f"T2: {T22:.2f} N", True, BLACK)
    text_theta1 = font.render(f"θ1: {theta1:.1f}°", True, BLACK)
    text_theta2 = font.render(f"θ2: {theta2:.1f}°", True, BLACK)
    text_weight = font.render(f"{weight:.0f} N", True, BLACK)
    text_mass = font.render(f"{mass:.2f} kg", True, BLACK) 
    
    screen.blit(text_T1, ((anchor1_x + body_x) // 2 - 50, (anchor_y + body_y) // 2))
    screen.blit(text_T2, ((anchor2_x + body_x) // 2 + 20, (anchor_y + body_y) // 2))
    screen.blit(text_theta1, (anchor1_x - 50, anchor_y - 30))
    screen.blit(text_theta2, (anchor2_x + 20, anchor_y - 30))
    screen.blit(text_weight, (body_x - 30, body_y + 30))
    screen.blit(text_mass, (body_x - 30, body_y + 50)) 
    
    pygame.draw.rect(screen, BLUE, (0, 0, 1440, 45))
    pygame.draw.rect(screen, BLUE, pygame.Rect(0, 812, 1440, 65))
    pygame.draw.rect(screen, WHITE, pygame.Rect(9, 818, 1420, 55))
    
    if conversor_visible:
        
        pygame.draw.rect(screen, BLUE, pygame.Rect(0, 580, 440, 235))
        pygame.draw.rect(screen, WHITE, pygame.Rect(7, 590, 422, 215))
        
        conversion_text = font_large .render(f"{result_conversion:.2f} N", True, BLACK)
        screen.blit(conversion_text, (145, 730))
        
        texto_Title = font_large.render('Conversor de Kg a N', True, BLACK)
        screen.blit(texto_Title, (70,600))
        
        btn_function_color = pygame.Color('black')
        btn_function = pygame.Rect(65, 680, 300, 40)
        pygame.draw.rect(screen, btn_function_color, btn_function)
        
        input_1 = pygame.Rect(65, 630, 300, 45)
        color_inactive = pygame.Color(BLACK)
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        pygame.draw.rect(screen, color, input_1, 2)
        
        texto = font_large.render('Convertir', True, WHITE)
        screen.blit(texto, (155, 685))
    
    BtnConversor = pygame.Rect(40, 826, 180, 40)
    pygame.draw.rect(screen, BLUE, BtnConversor)
    texto2 = font_large.render('Conversor', True, WHITE)
    screen.blit(texto2, (58, 835))

    
def draw_rope(screen, start, end, rope_image):
    # Calcular la distancia y el ángulo entre los puntos
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    length = math.hypot(dx, dy)

    # Escalar la imagen de la cuerda al largo necesario
    scaled_rope = pygame.transform.scale(rope_image, (int(length), rope_image.get_height()))
    
    # Rotar la imagen de la cuerda
    rotated_rope = pygame.transform.rotate(scaled_rope, math.degrees(-angle))

    # Calcular la posición para dibujar la cuerda rotada
    rope_rect = rotated_rope.get_rect()
    rope_rect.center = (start[0] + dx/2, start[1] + dy/2)

    # Dibujar la cuerda
    screen.blit(rotated_rope, rope_rect)

# Función principal que controla la ejecución
def main():
    global weight, theta1, theta2, dragging, drag_start_x, drag_start_y, start_weight, start_theta1, start_theta2, k
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Simulador de Cuerpos en Equilibrio")
    clock = pygame.time.Clock()
    
    running = True
    active = False
    conversor_visible = False  # Conversor oculto por defecto
    text = '50'
    result_conversion = 0
    body_image_rect = None
    
    # Definir el botón y el input aquí
    btn_function = pygame.Rect(65, 680, 300, 40)
    input_1 = pygame.Rect(65, 630, 300, 45)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_function.collidepoint(event.pos) and conversor_visible:
                    try:
                        k = float(text)  # Convertir el texto ingresado a un número
                        result_conversion = conversor(k)  # Calcular el resultado
                    except ValueError:
                        print("Ingrese un valor numérico válido")
                        
                BtnConversor = pygame.Rect(40, 826, 180, 40)
                if BtnConversor.collidepoint(event.pos):
                    conversor_visible = not conversor_visible  # Alternar la visibilidad del conversor
                            
                dragging = True
                drag_start_x, drag_start_y = pygame.mouse.get_pos()
                
                anchor1_x = WIDTH // 4
                anchor2_x = 3 * WIDTH // 4
                anchor_y = HEIGHT // 4

                body_x, body_y = calculate_body_position(anchor1_x, anchor2_x, anchor_y, calculate_tensions(weight, theta1, theta2)[0], calculate_tensions(weight, theta1, theta2)[1], theta1, theta2)

                body_image_rect = peso_image.get_rect(center=(body_x, body_y))

                if body_image_rect.collidepoint(drag_start_x, drag_start_y):
                    start_weight = weight
                    start_theta1 = theta1
                    start_theta2 = theta2
                
                # Verificar si se hizo clic en el input
                input_1 = pygame.Rect(65, 630, 300, 45)
                if input_1.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                    
                if input_1.collidepoint(event.pos) and conversor_visible:
                    active = True
                else:
                    active = False

            elif event.type == pygame.MOUSEBUTTONUP:
                # Terminar el arrastre
                dragging = False
                
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                delta_x = mouse_x - drag_start_x
                delta_y = mouse_y - drag_start_y
                
                if body_image_rect and body_image_rect.collidepoint(drag_start_x, drag_start_y):
                    weight = max(0, start_weight + delta_y // 2) 
            
            # Manejo de teclas para ajustar los ángulos
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            k = float(text)
                            result_conversion = conversor(k)
                        except ValueError:
                            print("Ingrese un valor numérico válido")
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                theta1 = max(1, theta1 - 1)
            if keys[pygame.K_RIGHT]:
                theta1 = min(90, theta1 + 1)
            if keys[pygame.K_UP]:
                theta2 = max(1, theta2 - 1)
            if keys[pygame.K_DOWN]:
                theta2 = min(90, theta2 + 1)
        
        # Asegurar que los ángulos estén en el rango correcto
        theta1 = max(1, min(theta1, 90))
        theta2 = max(1, min(theta2, 90))
        
        # Dibujar la escena
        draw_scene(screen, weight, theta1, theta2, result_conversion, conversor_visible)
        
        if conversor_visible:
        # Dibujar el input con el texto ingresado
            font = pygame.font.SysFont(None, 24)
            input_1 = pygame.Rect(65, 630, 300, 45)
            color_inactive = pygame.Color(BLACK)
            color_active = pygame.Color('dodgerblue2')
            color = color_active if active else color_inactive
            pygame.draw.rect(screen, color, input_1, 2)
            texto = font.render(text, True, BLACK)
            screen.blit(texto, (input_1.x + 5, input_1.y + 5))
        
        pygame.display.flip()
        
        # Establecer la velocidad de actualización (FPS)
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()