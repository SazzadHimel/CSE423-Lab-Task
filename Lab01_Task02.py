from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

ball_size = 10
points = []
paused = False
blink = False
time_count = 0
Width, Height = 500, 500

class Point:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)


def convert_coordinate(x,y):
    global Width, Height
    a = x - (Width/2)
    b = (Height/2) - y 
    return a, b


def keyboardListener(key, x, y):
    global paused
    if key==b' ':
        if paused:
            paused = False
        else:
            paused = True

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    if key==GLUT_KEY_UP and not paused:
        for p in points:
            if p.dx < 50:
                p.dx += 0.1
                p.dy += 0.1
    elif key== GLUT_KEY_DOWN and not paused:
        for p in points:
            if p.dx > 0:
                p.dy -= 0.1
                p.dx -= 0.1
    
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global blink

    if button==GLUT_LEFT_BUTTON and state == GLUT_DOWN and not paused:
        if blink:
            blink = False
        else:
            blink = True
        
    if button==GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not paused:
        a, b = convert_coordinate(x,y)

        for p in range(random.randint(2, 20)):
            points.append(Point(a, b))

        glutPostRedisplay()

    glutPostRedisplay()


def display():
    global time_count
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200,	0, 0, 0,	0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    glPointSize(ball_size)
    glBegin(GL_POINTS)
    for p in points:
        if blink:
            if time_count < 2000:
                glColor3f(0,0,0)
            elif time_count < 4000:
                glColor3f(p.color[0], p.color[1], p.color[2])
            else:
                time_count = -1
            
            time_count += 1
        else:
            glColor3f(p.color[0], p.color[1], p.color[2])
        glVertex2f(p.x, p.y)
    glEnd()
    
    glutSwapBuffers()


def animate():
    if not paused:
        
        for p in points:
            p.x += p.dx
            p.y += p.dy

            if p.x > Width/2 or p.x < -Width/2:
                p.dx *= -1
            if p.y > Height/2 or p.y < -Height/2:
                p.dy *= -1
                
        glutPostRedisplay()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(100,	1,	1,	1000)


glutInit()
glutInitWindowSize(Width, Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b" Designed Box")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()
