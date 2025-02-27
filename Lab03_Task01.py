from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500

circles = []
Shooter_Point = 250
Shooter_Width = 40
Shooter_Redius = 15
Bullet_Point = 45
Bullet_Speed = 5
Bullet_Missed_Counter = 0
Game_over = False

current_time = 0
collision_time = 0
current_speed = 0.5

Circle, Bullet, Pause = False, False, False
Score = 0
Play = True


# ---------- MIDPOINT LINE DRAWING ALGORITHM START -----------

def drawLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                drawLine_0(x0, y0, x1, y1, 0)
            else:
                drawLine_0(x0, -y0, x1, -y1, 7)
        else:
            if dy >= 0:
                drawLine_0(-x0, y0, -x1, y1, 3)
            else:
                drawLine_0(-x0, -y0, -x1, -y1, 4)
    else:
        if dx >= 0:
            if dy >= 0:
                drawLine_0(y0, x0, y1, x1, 1)
            else:
                drawLine_0(y0, -x0, y1, -x1, 6)
        else:
            if dy >= 0:
                drawLine_0(-y0, x0, -y1, x1, 2)
            else:
                drawLine_0(-y0, -x0, -y1, -x1, 5)

def drawLine_0(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    delE = 2 * dy
    delNE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x0
    y = y0
    while x < x1:
        draw8way(x, y, zone)
        if d < 0:
            d += delE
            x += 1
        else:
            draw8way(x, y, zone)
            d += delNE
            x += 1
            y += 1

def draw8way(x, y, zone):
    if zone == 0:
        draw_points(x, y)
    if zone == 1:
        draw_points(y, x)
    if zone == 2:
        draw_points(-y, x)
    if zone == 3:
        draw_points(-x, y)
    if zone == 4:
        draw_points(-x, -y)
    if zone == 5:
        draw_points(-y, -x)
    if zone == 6:
        draw_points(y, -x)
    if zone == 7:
        draw_points(x, -y)
        
def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# ------------ MIDPOINT LINE DRAWING ALGORITHM END ------------

# ------------ MIDPOINT CIRCLE DRAWING ALGORITHM START ------------


def drawCircle(x1, y1, r):
    x = r
    d = 5 + 4 * x
    y = 0

    while x >= y:
        draw8way_cir(x, y, x1, y1)
        if d > 0: # For North
            d += 4 * (-2 * x + 2 * y + 5)
            x -= 1
            y += 1
        else:  # For North-West
            d += 4 * (2 * y + 2)
            y += 1


def draw8way_cir(x, y, a, b):
    draw_point(x+a, y+b)
    draw_point(y+a, x+b)
    draw_point(-y+a, x+b)
    draw_point(-x+a, y+b)
    draw_point(-x+a, -y+b)
    draw_point(-y+a, -x+b)
    draw_point(y+a, -x+b)
    draw_point(x+a, -y+b)

def draw_point(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# ------------ MIDPOINT CIRCLE DRAWING ALGORITHM END ------------

# ------------ DRAW RESTART BUTTON ------------

def draw_restart_button():
    glColor3f(0.0, 0.5, 0.5)
    glPointSize(5)
    drawLine(10, 470, 60, 470)
    drawLine(10, 470, 30, 490)
    drawLine(10, 470, 30, 450)

# ------------ DRAW PLAY PAUSE BUTTON ------------

def draw_pause_or_play_button():
    global Play
    glPointSize(5)
    if Play:
        glColor3f(1.0, 0.74, 0.0)
        drawLine(240, 450, 240, 490)
        drawLine(260, 450, 260, 490)
    elif not Play:
        glColor3f(0.0, 1.0, 0.0)
        drawLine(240, 450, 240, 490)
        drawLine(240, 490, 280, 470)
        drawLine(240, 450, 280, 470)

# ------------ DRAW CLOSE BUTTON ------------

def draw_close_button():
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(5)
    drawLine(450, 450, 490, 490)
    drawLine(450, 490, 490, 450)
    
# ------------ DRAW SHOOTER ------------

def draw_Shooter():
    global Shooter_Point, Shooter_Width, Shooter_Redius
    x = Shooter_Point
    y = Shooter_Width
    z = Shooter_Redius
    glColor3f(1, 1, 1)
    drawCircle(x, y - z, z)

def Animate(value):
    global Bullet_Missed_Counter, circles, Shooter_Point, Shooter_Width, Shooter_Redius, Bullet_Point, Circle, Score, Pause, current_time, collision_time, Play

    if not Pause and Play:
        if random.random() < 0.02:
            Cir_X = random.randint(25, 472)
            Cir_Y = 420
            Cir_R = random.randint(22, 25)
            circles.append([Cir_X, Cir_Y, Cir_R])

        for k in circles:
            k[1] -= current_speed

        for k in circles:
            if Shooter_Point - 25 <= k[0] <= Shooter_Point + Shooter_Width and k[1] <= 25:
                Pause = True
                print('Collision with Shooter, Game Over! Score:', Score)
                circles = []
                glutPostRedisplay()
                return
            
            elif 15 == k[1]:
                Pause = True
                print('Collision with Boundary, Game Over! Score:', Score)
                circles = []
                glutPostRedisplay()
                return

    glutPostRedisplay()
    glutTimerFunc(15, Animate, 0)

def BulletAnimate(value):
    global Bullet_Point, Bullet, Bullet_Missed_Counter, Pause, circles, Game_over

    if Bullet:
        Bullet_Point += Bullet_Speed
        
        if Bullet_Point > 420:
            Bullet_Missed_Counter += 1
            Bullet = False
            Bullet_Point = 45

    if Bullet_Missed_Counter == 3 and not Game_over:
        circles = []
        Bullet = False
        print("Game Over! Your Score:", Score)
        Pause = True
        Game_over = True
        glutPostRedisplay()
        return 
    
    glutPostRedisplay()
    glutTimerFunc(15, BulletAnimate, 0)
    

def KeyboardSpecialKeys(key, _, __):
    global Shooter_Point, Shooter_Width, Play, Pause
    if Play and not Pause:
        if key == GLUT_KEY_LEFT:
            if Shooter_Point - 10 >= 10:
                Shooter_Point -= 10

        elif key == GLUT_KEY_RIGHT:
            if Shooter_Point + Shooter_Width + 10 <= W_Width + 10:
                Shooter_Point += 10
            
    glutPostRedisplay()


def MouseListener(button, state, x, y):
    global Circle, Bullet, Bullet_Point, Pause, Play, circle_x, circle_y, Score, circles, Bullet_Missed_Counter, current_time, current_speed, collision_time

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        circle_X = x
        circle_Y = y
        
        if 50 <= circle_X and 50 <= circle_Y and not Bullet and Play:
            Bullet = True
            glutTimerFunc(0, BulletAnimate, 0)
            
        if 0 <= circle_X <= 50 and 0 <= circle_Y <= 50:
            print('Starting over!!!')
            circles = []
            circle_x= random.choice([10, 490])
            circle_y = 440
            Circle = True
            Score = 0
            Bullet_Missed_Counter = 0
            Pause = False
            current_time = 0
            current_speed = 0.5
            collision_time = 0


        if 200 <= circle_X <= 300 and 0 <= circle_Y <= 50:
            if not Play:
                Play = True
                print('Game Paused!')
            else:
                Play = False
                print('Game Resumed!')

        if 400 <= circle_X <= 500 and 0 <= circle_Y <= 50:
            print('Goodbye! Score:', Score)
            glutLeaveMainLoop()

        glutPostRedisplay()


def display():
    global Shooter_Point, Shooter_Width, Bullet_Point, Bullet_Missed_Counter, Bullet, Score, Pause, circles
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 500, 0.0, 500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Drawing the buttons
    draw_restart_button()
    draw_pause_or_play_button()
    draw_close_button()
    
    # Drawing the circles
    glColor3f(1, 0, 1)
    for i in circles:
        drawCircle(i[0], i[1], i[2])
        
    if Bullet:
        drawCircle(Shooter_Point, Bullet_Point, 3)
    
    # Drawing the shooter
    draw_Shooter()
    
    for point in circles:
        if Bullet and abs(Bullet_Point-point[1]) < point[2] and abs(Shooter_Point-point[0]) < Shooter_Width/2:
            circles.remove(point)
            Bullet = False
            Score += 1
            print('Score:', Score)
            Bullet_Point = 45
            
    glutSwapBuffers()


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Bubble Shooter Game!")

glutMouseFunc(MouseListener)
glutSpecialFunc(KeyboardSpecialKeys)
glutDisplayFunc(display)
glutTimerFunc(0, Animate, 0)
glutTimerFunc(0, BulletAnimate, 0)

glutMainLoop()
