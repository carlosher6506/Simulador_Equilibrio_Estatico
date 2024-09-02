import pygame
import math

# Configuraciones iniciales
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Inicializar Pygame
pygame.init()

# Parámetros del sistema físico
weight = 100  # Peso del cuerpo (N)
g = 9.81  # Aceleración gravitatoria (m/s^2)
theta1, theta2 = 45, 45  # Ángulos iniciales en grados

# Función para calcular las tensiones
def calculate_tensions(weight, theta1, theta2):
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    
    T2 = weight * math.sin(theta1_rad) / math.sin(theta1_rad + theta2_rad)
    T1 = weight * math.sin(theta2_rad) / math.sin(theta1_rad + theta2_rad)
    
    return T1, T2

# Función para calcular la posición del cuerpo
def calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2):
    body_x = (T2 * math.cos(math.radians(theta2)) * anchor1_x + 
              T1 * math.cos(math.radians(theta1)) * anchor2_x) / (T1 * math.cos(math.radians(theta1)) + T2 * math.cos(math.radians(theta2)))
    
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
    
    # Calcular la posición del cuerpo
    body_x, body_y = calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2)
    
    # Dibujar las cuerdas
    pygame.draw.line(screen, BLACK, (anchor1_x, anchor_y), (body_x, body_y), 2)
    pygame.draw.line(screen, BLACK, (anchor2_x, anchor_y), (body_x, body_y), 2)
    
    # Dibujar el cuerpo
    pygame.draw.circle(screen, RED, (body_x, body_y), 20)
    
    # Dibujar puntos de anclaje
    pygame.draw.circle(screen, GREEN, (anchor1_x, anchor_y), 10)
    pygame.draw.circle(screen, GREEN, (anchor2_x, anchor_y), 10)
    
    # Mostrar tensiones y ángulos cerca de las cuerdas
    font = pygame.font.SysFont(None, 24)
    text_T1 = font.render(f"T1: {T1:.3f} N", True, BLACK)
    text_T2 = font.render(f"T2: {T2:.3f} N", True, BLACK)
    text_theta1 = font.render(f"θ1: {theta1:.2f}°", True, BLACK)
    text_theta2 = font.render(f"θ2: {theta2:.2f}°", True, BLACK)
    text_weight = font.render(f"{weight:.3f} N", True, BLACK)
    
    screen.blit(text_T1, ((anchor1_x + body_x) // 2 - 50, (anchor_y + body_y) // 2))
    screen.blit(text_T2, ((anchor2_x + body_x) // 2 + 20, (anchor_y + body_y) // 2))
    screen.blit(text_theta1, (anchor1_x - 50, anchor_y - 30))
    screen.blit(text_theta2, (anchor2_x + 20, anchor_y - 30))
    screen.blit(text_weight, (body_x - 30, body_y + 30))

# Función principal que controla la ejecución
def main():
    global weight, theta1, theta2
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Cuerpos en Equilibrio")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    weight += 10
                elif event.key == pygame.K_DOWN:
                    weight -= 10
                elif event.key == pygame.K_LEFT:
                    theta1 -= 5
                    theta2 += 5
                elif event.key == pygame.K_RIGHT:
                    theta1 += 5
                    theta2 -= 5
        
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

# Ejecutar solo si este archivo se ejecuta como un script
if __name__ == "__main__":
    main()