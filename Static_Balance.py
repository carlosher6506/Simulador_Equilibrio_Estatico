import pygame
import math

# Configuraciones iniciales
WIDTH, HEIGHT = 1350, 840
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 71, 125)

# Inicializar Pygame
pygame.init()
# Cargar imagen personalizada
image_path = "../Static balance simulator/Images/Block.png"

body_image = pygame.image.load(image_path)

# Redimensionar la imagen (opcional)
body_image = pygame.transform.scale(body_image, (520, 450))

# Parámetros del sistema físico
weight = 100  # Peso del cuerpo (N)
g = 9.81  # Aceleración gravitatoria (m/s^2)
theta1, theta2 = 10, 10  # Ángulos iniciales en grados

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
    
    body_x = (T2 * math.cos(math.radians(theta2)) * anchor1_x + 
              T1 * math.cos(math.radians(theta1)) * anchor2_x) / denominator
    
    body_y = anchor_y + T1 * math.sin(math.radians(theta1))
    return int(body_x), int(body_y)

# Función para dibujar la escena
def draw_scene(screen, weight, theta1, theta2):
    screen.fill(WHITE)
    
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
    image_rect = body_image.get_rect(center=(body_x, body_y))
    
    # Dibujar las cuerdas
    pygame.draw.line(screen, BLACK, (anchor1_x, anchor_y), (body_x, body_y), 2)
    pygame.draw.line(screen, BLACK, (anchor2_x, anchor_y), (body_x, body_y), 2)
    
    # Dibujar el cuerpo (imagen)
    screen.blit(body_image, image_rect)
    
    # Dibujar puntos de anclaje
    pygame.draw.circle(screen, GREEN, (anchor1_x, anchor_y), 10)
    pygame.draw.circle(screen, GREEN, (anchor2_x, anchor_y), 10)
    
    # Mostrar tensiones y ángulos cerca de las cuerdas
    font = pygame.font.SysFont(None, 24)
    text_T1 = font.render(f"T1: {T11:.2f} N", True, BLACK)
    text_T2 = font.render(f"T2: {T22:.2f} N", True, BLACK)
    text_theta1 = font.render(f"θ1: {theta1:.1f}°", True, BLACK)
    text_theta2 = font.render(f"θ2: {theta2:.1f}°", True, BLACK)
    text_weight = font.render(f"{weight:.0f} N", True, BLACK)
    
    screen.blit(text_T1, ((anchor1_x + body_x) // 2 - 50, (anchor_y + body_y) // 2))
    screen.blit(text_T2, ((anchor2_x + body_x) // 2 + 20, (anchor_y + body_y) // 2))
    screen.blit(text_theta1, (anchor1_x - 50, anchor_y - 30))
    screen.blit(text_theta2, (anchor2_x + 20, anchor_y - 30))
    screen.blit(text_weight, (body_x - 30, body_y + 30))
    
    pygame.draw.rect(screen, BLUE, (0, 0, 1440, 45))
    
    pygame.draw.rect(screen, (BLUE), pygame.Rect(22, 520, 440, 300))
    pygame.draw.rect(screen, (WHITE), pygame.Rect(30, 530, 422, 280))
    text_weight11 = font.render(f'Peso = {text_weight}', pygame.Rect(160, 600, 200, 32), BLACK)
        #draw_text(screen, f'Tensión 1 = {text_T1:.2f}', pygame.Rect(1160, 650, 200, 32), BLACK)
        #draw_text(screen, f'Tensión 2 = {text_T2:.2f}', pygame.Rect(1160, 700, 200, 32), BLACK)

# Función principal que controla la ejecución
def main():
    global weight, theta1, theta2, dragging, drag_start_x, drag_start_y, start_weight, start_theta1, start_theta2
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Simulador de Cuerpos en Equilibrio")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Comenzar el arrastre
                dragging = True
                drag_start_x, drag_start_y = pygame.mouse.get_pos()
                
                # Coordenadas de los puntos de anclaje
                anchor1_x = WIDTH // 4
                anchor2_x = 3 * WIDTH // 4
                anchor_y = HEIGHT // 4
                
                # Calcular la posición del cuerpo
                body_x, body_y = calculate_body_position(anchor1_x, anchor2_x, anchor_y, calculate_tensions(weight, theta1, theta2)[0], calculate_tensions(weight, theta1, theta2)[1], theta1, theta2)
                
                # Definir el rectángulo de la imagen del cuerpo
                image_rect = body_image.get_rect(center=(body_x, body_y))
                
                # Verificar si el clic fue cerca del cuerpo
                if image_rect.collidepoint(drag_start_x, drag_start_y):
                    start_weight = weight
                    start_theta1 = theta1
                    start_theta2 = theta2

            elif event.type == pygame.MOUSEBUTTONUP:
                # Terminar el arrastre
                dragging = False
                
            elif event.type == pygame.MOUSEMOTION and dragging:
                # Obtener la posición actual del ratón
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Calcular el cambio en la posición del ratón
                delta_x = mouse_x - drag_start_x
                delta_y = mouse_y - drag_start_y
                
                # Ajustar el peso en función del movimiento del ratón
                if image_rect.collidepoint(drag_start_x, drag_start_y):
                    weight = max(0, start_weight + delta_y // 2)  # Cambiar peso en función del movimiento vertical
            
            # Manejo de teclas para ajustar los ángulos
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                theta1 = max(1, theta1 - 1)
            if keys[pygame.K_RIGHT]:
                theta1 = min(179, theta1 + 1)
            if keys[pygame.K_UP]:
                theta2 = max(1, theta2 - 1)
            if keys[pygame.K_DOWN]:
                theta2 = min(179, theta2 + 1)
        
        # Asegurar que los ángulos estén en el rango correcto
        theta1 = max(1, min(theta1, 179))
        theta2 = max(1, min(theta2, 179))
        
        # Dibujar la escena con el cuerpo y las cuerdas ajustadas
        draw_scene(screen, weight, theta1, theta2)
        
        # Actualizar la pantalla
        pygame.display.flip()
        
        # Establecer la velocidad de actualización (FPS)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
