from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

WIDTH  = 500
HEIGHT = 750

class ABCD:
    def __init__(self, x, y, w, h, speed):
        self.x, self.y, self.w, self.h, self.speed = x, y, w, h, speed
        self.color = (random.uniform(0.3, 1), random.uniform(0.3, 1), random.uniform(0.3, 1))
    
    def collides_with(self, other):
        return (self.x < other.x + other.w and self.x + self.w > other.x and self.y < other.y + other.h and self.y + self.h > other.y)
    
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
    def move_right(self):
        if self.x + self.w < WIDTH:
            self.x += self.speed
    def move_down(self):
        self.y -= self.speed

    def increase_speed(self):
        self.speed += 0.05

catcher = ABCD(200, 0, 100, 20, 20) 
diamond = ABCD(random.randint(0, WIDTH-30), HEIGHT-90, 30, 50, 0.8)
collision = True
play = True
score = 0
game_over = False

def draw_catcher(obj):
    global collision
    glPointSize(2)

    if not collision:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_POINTS)
    # bottom line
    drawline(obj.x + 10, obj.y + 4, obj.x + obj.w - 10, obj.y + 4)

    # right line
    drawline(obj.x + obj.w - 10, obj.y + 4, obj.x + obj.w, obj.y + obj.h)

    # top line
    drawline(obj.x, obj.y + obj.h, obj.x + obj.w, obj.y + obj.h)

    # left line
    drawline(obj.x, obj.y + obj.h, obj.x + 10, obj.y + 4)
    glEnd()

def draw_diamond(obj):
    
    glColor3f(obj.color[0], obj.color[1], obj.color[2])
    glPointSize(2)
    glBegin(GL_POINTS)
    
    # upper left line
    drawline(obj.x, obj.y + obj.h//2, obj.x + obj.w//2, obj.y + obj.h)

    # upper right line
    drawline(obj.x + obj.w, obj.y + obj.h//2, obj.x + obj.w//2, obj.y + obj.h)
    
    # lower left line
    drawline(obj.x + obj.w//2, obj.y, obj.x, obj.y + obj.h//2)

    # lower right line
    drawline(obj.x + obj.w//2, obj.y, obj.x + obj.w, obj.y + obj.h//2)

    glEnd()

def draw_restart_button():
    
    glColor3f(0.0, 0.5, 0.5)
    
    glPointSize(3)
    
    glBegin(GL_POINTS)
    
    drawline(10, 710, 30, 740)
    drawline(10, 710, 60, 710)
    drawline(10, 710, 30, 680)

    glEnd()

def draw_pause_or_play_button():
    glPointSize(3)
    glBegin(GL_POINTS)
    
    if not play:
        glColor3f(0.0, 1.0, 0.0)
        drawline(225, 740, 225, 680)
        drawline(225, 740, 275, 710)
        drawline(225, 680, 275, 710)
        
    elif play and collision:
        glColor3f(1.0, 0.74, 0.0)
        drawline(240, 740, 240, 680)
        drawline(260, 740, 260, 680)
        
    else:
        pass

    glEnd()

def draw_close_button():
    
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(3)
    glBegin(GL_POINTS)
    
    drawline(440, 740, 490, 680)
    drawline(440, 680, 490, 740)

    glEnd()

# MIDPOINT LINE ALGORITHM START

def draw_points(x, y, zone):
    if zone == 0:
        glVertex2f(x, y)
    elif zone == 1:
        glVertex2f(y, x)
    elif zone == 2:
        glVertex2f(-y, x)
    elif zone == 3:
        glVertex2f(-x, y)
    elif zone == 4:
        glVertex2f(-x, -y)
    elif zone == 5:
        glVertex2f(-y, -x)
    elif zone == 6:
        glVertex2f(y, -x)
    elif zone == 7:
        glVertex2f(x, -y)

def midpoint_line(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    dE = 2*dy
    dNE = 2*(dy - dx)
    x = x1
    y = y1
    
    draw_points(x, y, zone)
    
    while x < x2:
        if d < 0:
            d = d + dE
            x = x + 1
        else:
            d = d + dNE
            x = x + 1
            y = y + 1
        draw_points(x, y, zone)
    
    return x1, y1, x2, y2

def convert_to_zone0(x1, y1, x2, y2, zone):
    
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2

def convert_from_zone0(x1, y1, zone):
    
    if zone == 0:
        return x1, y1
    elif zone == 1:
        return y1, x1
    elif zone == 2:
        return -y1, x1
    elif zone == 3:
        return -x1, y1
    elif zone == 4:
        return -x1, -y1
    elif zone == 5:
        return -y1, -x1
    elif zone == 6:
        return y1, -x1
    elif zone == 7:
        return x1, -y1

def check_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx > 0:
            if dy >= 0:
                return 0
            else:
                return 7
        else:
            if dy >= 0:
                return 3
            else:
                return 4
    else:
        if dx > 0:
            if dy >= 0:
                return 1
            else:
                return 6
        else:
            if dy >= 0:
                return 2
            else:
                return 5

def drawline(x1, y1, x2, y2):
    zone = check_zone(x1, y1, x2, y2)
    
    x1, y1, x2, y2 = convert_to_zone0(x1, y1, x2, y2, zone)
    
    midpoint_line(x1, y1, x2, y2, zone)


def initialize():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def check_collision():
    global score, diamond, collision, play, game_over

    if catcher.collides_with(diamond):
        score += 1
        speed = diamond.speed
        diamond = ABCD(random.randint(0, WIDTH-30), HEIGHT-120, 30, 50, speed)
        diamond.increase_speed()
        print("Score: ", score)
    else:
        if diamond.y + diamond.h < 0:
            collision = False
            if not game_over:
                print("Game Over! Score: ", score)  
            game_over = True

def show_screen():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_restart_button()
    draw_pause_or_play_button()
    draw_close_button()
    
    draw_catcher(catcher)
    draw_diamond(diamond)

    glutSwapBuffers()

def keyboard_special_keys(key, _, __):
    
    if play and collision:
        if key == GLUT_KEY_LEFT:
            catcher.move_left()
        elif key == GLUT_KEY_RIGHT:
            catcher.move_right()

    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global play, score, catcher, diamond, collision, game_over

    mx, my = x, HEIGHT - y

    if button==GLUT_LEFT_BUTTON and state == GLUT_UP:
        if mx >= 0 and mx <= 60 and my >= 680 and my <= 740:
            score = 0
            catcher = ABCD(200, 0, 100, 20, 20)
            diamond = ABCD(random.randint(0, WIDTH-30), HEIGHT-90, 30, 50, 0.8)
            play = True
            collision = True
            print("Starting over!")
            game_over = False
        elif mx >= 225 and mx <= 275 and my >= 680 and my <= 740:
            if play:
                play = False
            else:
                play = True
        elif mx >= 440 and mx <= 500 and my >= 680 and my <= 740:
            print("Goodbye! Score: ", score)
            glutLeaveMainLoop()

    glutPostRedisplay()

def animation():
    
    if play:
        if diamond.y < 20:
            check_collision()

        diamond.move_down()

    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Catch the Diamonds!")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)

glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()