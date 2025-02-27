from OpenGL.GL import *
from OpenGL.GLUT import *
import random

direction = 0
night = True
drop = []

def draw_points(x, y):
    
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def drawHome():
    
    glBegin(GL_LINES)
    # x-axis Wall
    glVertex2f(100, 200)
    glVertex2f(500, 200)
    glVertex2f(200, 500)
    glVertex2f(500, 500)
    
    # Y -axis Wall
    glVertex2f(100, 200)
    glVertex2f(100, 500)
    glVertex2f(500, 200)
    glVertex2f(500, 500)
    
    # x axis window 1
    glVertex2f(120, 350)
    glVertex2f(220, 350)
    glVertex2f(120, 450)
    glVertex2f(220, 450)
    
    # y axis window 1
    glVertex2f(120, 350)
    glVertex2f(120, 450)
    glVertex2f(220, 350)
    glVertex2f(220, 450)
    
    # x axis window 2
    glVertex2f(370, 350)
    glVertex2f(470, 350)
    glVertex2f(370, 450)
    glVertex2f(470, 450)
    
    # y axis window 2
    glVertex2f(370, 350)
    glVertex2f(370, 450)
    glVertex2f(470, 350)
    glVertex2f(470, 450)
    
    # x axis door
    glVertex2f(250, 400)
    glVertex2f(350, 400)
    glVertex2f(250, 220)
    glVertex2f(350, 220)
    
    # y axis door
    glVertex2f(250, 220)
    glVertex2f(250, 400)
    glVertex2f(350, 220)
    glVertex2f(350, 400)
    
    glEnd()
    
def drawRain(x, y):
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(0, 1, 1)
    glVertex2f(x, y)
    glVertex2f(x, y + 18)
    glEnd()
    
    
def drawTriangle():
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 1)
    glVertex2f(50, 500)
    glVertex2f(550, 500)
    glVertex2f(300, 650)
    glEnd()
    

def iterate():
    glViewport(0, 0, 600, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 600, 0, 800, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def animate(value):
    global direction
    for i in range(len(drop)):

        drop[i][1] -= 5
        drop[i][0] += direction * 0.1
        
        if drop[i][1] < 0:
            drop[i][1] = 600 + random.randint(10, 100)
            drop[i][0] = random.randint(0, 800)
        
    glutPostRedisplay()
    glutTimerFunc(10, animate, 0)

def special_key_pressed(key, x, y):
    
    global direction, night
    if key == GLUT_KEY_RIGHT:
        direction = 50
    elif key == GLUT_KEY_LEFT:
        direction = -50
    elif key == GLUT_KEY_DOWN:
        day_night()

def special_key_released(key, x, y):
    global direction
    if key in (GLUT_KEY_LEFT, GLUT_KEY_RIGHT):
        direction = 0

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(0, 0, 1)
    draw_points(250, 350)
    drawHome()
    glColor3f(0, 1, 0)
    drawTriangle()
    for raindrop in drop:
        drawRain(raindrop[0], raindrop[1])
    glutSwapBuffers()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    
def day_night():
    global night
    night = not night
    if night:
        glClearColor(0, 0, 0, 1)
    else:
        glClearColor(1, 1, 1, 1)
        
    glutPostRedisplay()

def display():
    global night
    if night:
        glClearColor(0, 0, 0, 1)
    else:
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        
    for raindrop in drop:
        drawRain(raindrop[0], raindrop[1])
        
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(600, 700)
glutCreateWindow(b"Rainfall On House")
glutDisplayFunc(showScreen)
glutSpecialFunc(special_key_pressed)
glutSpecialUpFunc(special_key_released)
init()

for i in range(150):
    x = random.randint(0, 1200)
    y = random.randint(0, 1200)
    drop.append([x, y])
    
glutTimerFunc(10, animate, 0)
glutMainLoop()

