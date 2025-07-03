from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Window dimensions
WIDTH, HEIGHT = 500, 650

# Catcher properties
c_width = 150
c_height = 10
catch_x = (WIDTH - c_width) // 2
catch_y = 50
speed = 20

# Diamond properties
dSize = 20
d_x = random.randint(50, WIDTH - 50)
d_y = HEIGHT - 50
diamond_speed = 2
diamond_falling = True

# Game state
score = 0
game_over = False
paused = False

# Buttons
size_button = 30
def draw_button(x, y, color, shape) :
    glColor3f(*color)
    glBegin(GL_LINES)
    if shape == "left":
        glVertex2f(x, y)
        glVertex2f(x + size_button, y + size_button // 2)
        glVertex2f(x, y + size_button)
        glVertex2f(x + size_button, y + size_button // 2)
    elif shape == "pause":
        glVertex2f(x, y)
        glVertex2f(x, y + size_button)
        glVertex2f(x + size_button, y)
        glVertex2f(x + size_button, y + size_button)
    elif shape == "exit":
        glVertex2f(x, y)
        glVertex2f(x + size_button, y + size_button)
        glVertex2f(x + size_button, y)
        glVertex2f(x, y + size_button)
    glEnd()

def draw_catcher() :
    glColor3f(1, 1, 1) if not game_over else glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(catch_x, catch_y)
    glVertex2f(catch_x + c_width, catch_y)
    glVertex2f(catch_x, catch_y)
    glVertex2f(catch_x + c_width // 4, catch_y + c_height)
    glVertex2f(catch_x + c_width, catch_y)
    glVertex2f(catch_x + 3 * c_width // 4, catch_y + c_height)
    glVertex2f(catch_x + c_width // 4, catch_y + c_height)
    glVertex2f(catch_x + 3 * c_width // 4, catch_y + c_height)
    glEnd()

def draw_diamond() :
    glColor3f(1, 1, 0)
    glBegin(GL_LINES)
    glVertex2f(d_x, d_y)
    glVertex2f(d_x + dSize // 2, d_y + dSize // 2)
    glVertex2f(d_x + dSize // 2, d_y + dSize // 2)
    glVertex2f(d_x, d_y + dSize)
    glVertex2f(d_x, d_y + dSize)
    glVertex2f(d_x - dSize // 2, d_y + dSize // 2)
    glVertex2f(d_x - dSize // 2, d_y + dSize // 2)
    glVertex2f(d_x, d_y)
    glEnd()

def has_collided() :
    return (d_x > catch_x and d_x < catch_x + c_width and
            d_y <= catch_y + c_height)

def update(value) :
    global d_y, d_x, diamond_falling, score, game_over
    if not paused and not game_over:
        d_y -= diamond_speed
        if d_y <= 0:
            game_over = True
        if has_collided():
            score += 1
            d_x = random.randint(50, WIDTH - 50)
            d_y = HEIGHT - 50
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def display() :
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher()
    draw_diamond()
    draw_button(20, HEIGHT - 50, (0, 1, 1), "left")
    draw_button(WIDTH // 2 - 10, HEIGHT - 50, (1, 0.7, 0), "pause")
    draw_button(WIDTH - 50, HEIGHT - 50, (1, 0, 0), "exit")
    glutSwapBuffers()

def keyboard(key, x, y) :
    global catch_x, paused, game_over, d_x, d_y, score
    if key == b'a' and catch_x > 0:
        catch_x -= speed
    elif key == b'd' and catch_x < WIDTH - c_width:
        catch_x += speed
    elif key == b'r':  # Restart
        game_over = False
        score = 0
        d_x = random.randint(50, WIDTH - 50)
        d_y = HEIGHT - 50
    elif key == b'p':  # Pause
        paused = not paused
    elif key == b'q':  # Quit
        print(f"Goodbye! Final Score: {score}")
        glutLeaveMainLoop()

def mouse(button, state, x, y) :
    global paused, game_over, score, d_x, d_y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 20 <= x <= 50 and HEIGHT - 50 <= y <= HEIGHT - 20:
            game_over = False
            score = 0
            d_x = random.randint(50, WIDTH - 50)
            d_y = HEIGHT - 50
        elif WIDTH // 2 - 10 <= x <= WIDTH // 2 + 20 and HEIGHT - 50 <= y <= HEIGHT - 20:
            paused = not paused
        elif WIDTH - 50 <= x <= WIDTH - 20 and HEIGHT - 50 <= y <= HEIGHT - 20:
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()

def main() :
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Catch the Diamonds!")
    glClearColor(0, 0, 0, 1)
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(16, update, 0)
    glutMainLoop()

if __name__ == "__main__" :
    main()



