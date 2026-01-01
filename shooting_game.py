from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


window_width = 1000
window_height = 600

length_tile = 100 
num_tile = 14
half_field = (num_tile * length_tile) // 2 

wide_angle = 120

agent = {
    "pos": [0.0, 0.0, 0.0],
    "angle": 0.0,
}

display_state = {
    "mode": "third",               
    "eye": [0, 500, 500],
}


bullets = []  
oppoents = []         

max_num_opponents = 5


curr_game_stats = {
    "running": True,
    "health": 5,
    "score": 0,
    "missed": 0,
}


auto_play = {
    "enabled": False,
    "spin_steps": 0,
    "ready": True,
}

view_tweaks = {
    "gun_view": False,
    "follow_offset": [-100.0, 0.0, 60.0],
}

cheat_marker = {
    "cheat": False,
}


speed_bullet = 10
opponent_speed = 0.05
normal_step_size = 20
cheating_step_size = 50
turning_step_size = 5

max_wasted_bullet = 10



def calc_eulc_distance(a,b):
    return math.sqrt(a * a + b * b)


def is_player_inside(x, y):
    if  -half_field <= x <= half_field and -half_field <= y <= half_field:
        return True
    return False    
    


def spawn_opponent():
    while True:
        x_coor = random.randint(-650, 650)
        y_coor = random.randint(-650, 650)
        temp = max(abs(x_coor), abs(y_coor))

        if temp > 150:
            return {
                "pos": [float(x_coor), float(y_coor), 0.0],
                "scale": 1.0,
                "del": 0.005,
            }


def spawn_initial_wave():
    oppoents[:] = [] # i am clearing all initial enemies
    for i in range(max_num_opponents):
        temp = spawn_opponent()
        oppoents.append(temp) # i am spawning new enemies


def reset_game():
    bullets[:] = []
    curr_game_stats["running"] = True
    curr_game_stats["health"] = 5
    curr_game_stats["score"] = 0
    curr_game_stats["missed"] = 0

    agent["pos"][:] = [0, 0, 0]
    agent["angle"] = 0

    display_state["mode"] = "third"
    display_state["eye"][:] = [0, 500, 500]

    auto_play["enabled"] = False
    auto_play["spin_steps"] = 0
    auto_play["ready"] = True

    view_tweaks["gun_view"] = False
    view_tweaks["follow_offset"][:] = [-100, 0, 60]

    cheat_marker["cheat"] = False

    spawn_initial_wave()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()


    gluOrtho2D(0, window_width, 0, window_height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_floor_pattern():
    glBegin(GL_QUADS)
    for r in range(num_tile):
        for c in range(num_tile):
            if (r+c) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            #calc bottom left corner
            left = (r - num_tile // 2) * length_tile
            bottom = (c - num_tile // 2) * length_tile

            #calc right and top
            right = left + length_tile
            top = bottom + length_tile

            glVertex3f(left, bottom, 0) #bottom left
            glVertex3f(right, bottom, 0) #bottom right
            glVertex3f(right, top, 0) #top right
            glVertex3f(left, top, 0) #top left

    glEnd()


def draw_bounderies():
    dist = half_field
    h = 121

    colors = [
        (0.014, 1, 0.98),
        (0, 0, 1.),
        (1, 1, 1),
        (0, 1, 0),
    ]

    #wall defined using direction coordinate
    corners = [
        [(-1, -1), (1, -1), (1, -1), (-1, -1)],
        [(1, -1), (1, 1), (1, 1), (1, -1)],
        [(1, 1), (-1, 1), (-1, 1), (1, 1)],
        [(-1, 1), (-1, -1), (-1, -1), (-1, 1)],
    ]

    for i in range(4):
        glBegin(GL_QUADS)
        glColor3f(*colors[i])
        for i, (d_x, d_y) in enumerate(corners[i]):
            wx = d_x * dist
            wy = d_y * dist
            if i >= 2:
                wz = h
            else:
                wz = 0
            glVertex3f(wx, wy, wz)
        glEnd()




def draw_agent():
    glPushMatrix()

    px, py, pz = agent["pos"]
    glTranslatef(px, py, pz)
    glRotatef(agent["angle"], 0, 0, 1)

    if not curr_game_stats["running"]:
        glRotatef(90, 0, 1, 0) #lying down 

    # waist down
    glColor3f(0.0, 0.0, 1.0)
    glTranslatef(0, -20, -100)
    glRotatef(90, 0, 1, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10)

    glTranslatef(0, -80, 0)
    gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10)

    # body
    glColor3f(0.095, 0.350, 0.095)
    glTranslatef(0, 40, -30)
    glutSolidCube(80)

    # gun
    glColor3f(0.6, 0.6, 0.6)
    glTranslatef(0, 0, 40)
    glTranslatef(30, 0, -90)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 20, 5, 120, 10, 10)

    # arms
    glColor3f(1.0, 0.88, 0.65)
    glTranslatef(0, -25, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)

    glTranslatef(0, 50, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)

    # head
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(40, -25, -25)
    gluSphere(gluNewQuadric(), 30, 10, 10)

    glPopMatrix()


def draw_bullets():
    glColor3f(1, 0, 0)
    for b in bullets:
        x, y, z = b["pos"]
        glPushMatrix()
        glTranslatef(x, y, z)
        glutSolidCube(10)
        glPopMatrix()


def draw_opponents(opponent):
    x, y, z = opponent["pos"]
    s = opponent["scale"]

    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(s, s, s)

    # body
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 40, 20, 20)
    glPopMatrix()

    # head
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 80)
    gluSphere(gluNewQuadric(), 30, 20, 20)
    glPopMatrix()

    glPopMatrix()



def set_viewing_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(wide_angle, 1.25, 0.1, 1500) #aspect_ratio, near clipping plane, far clipping plane
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    if display_state["mode"] != "third":
        r = math.radians(agent["angle"]) # agent angle to radians
        base_dir = [-math.cos(r), -math.sin(r)]  # forward x direction, forward y direction

        forward_offset = 45 #move camera forward
        side_offset = 28 #move camera sideways
        up_offset = 39 #move camera upwards

        p_x, p_y, p_z = agent["pos"]
        cam_x = p_x + side_offset * math.sin(r) - forward_offset * math.cos(r) 
        cam_y = p_y - side_offset * math.cos(r) - forward_offset * math.sin(r) 
        cam_z = p_z + up_offset

        if auto_play["enabled"] and view_tweaks["gun_view"]: #gun_view
            x_view = cam_x + base_dir[0] * 95
            y_view = cam_y + base_dir[1] * 95
            z_view = cam_z
        elif auto_play["enabled"]: #head_view
            off = view_tweaks["follow_offset"]
            cam_x = off[0] + 150
            cam_y = off[1]
            cam_z = p_z + off[2] - 10
            x_view, y_view, z_view = p_x, p_y, p_z
        else:
            x_view = cam_x + base_dir[0] * 100
            y_view = cam_y + base_dir[1] * 100
            z_view = cam_z

        gluLookAt(cam_x, cam_y, cam_z, x_view, y_view, z_view, 0, 0, 1)

    else:
        ex, ey, ez = display_state["eye"]
        gluLookAt(ex, ey, ez, 0, 0, 0, 0, 0, 1)




def update_opponents():
    if not curr_game_stats["running"]:
        return

    px, py, pz = agent["pos"]

    for enemy in oppoents[:]:
        ex, ey, ez = enemy["pos"]
        vx = px - ex
        vy = py - ey
        dist = calc_eulc_distance(vx, vy)

        if dist > 1e-3:
            step = opponent_speed / dist
            enemy["pos"][0] += vx * step
            enemy["pos"][1] += vy * step

        enemy["scale"] += enemy["del"]
        if enemy["scale"] < 0.8 or enemy["scale"] > 1.2: #the del vaiable reverses pulsating direction
            enemy["del"] *= -1

        hit_box = 100.0
        #collision with player
        if (
            abs(px - enemy["pos"][0]) < hit_box
            and abs(py - enemy["pos"][1]) < hit_box
            and abs(pz - enemy["pos"][2]) < hit_box
        ):
            oppoents.remove(enemy)

            if cheat_marker["cheat"]:
                oppoents.append(spawn_opponent())
                continue

            if curr_game_stats["health"] > 0:
                curr_game_stats["health"] -= 1
                oppoents.append(spawn_opponent())
            else:
                curr_game_stats["running"] = False
                oppoents[:] = []
            break


def update_bullets():
    if not bullets: #if out of ammo
        return

    still_in_view = [] #active bullets  
    for b in bullets:
        pos = b["pos"]
        d = b["dir"]
        pos[0] += d[0] * speed_bullet
        pos[1] += d[1] * speed_bullet
        pos[2] += d[2] * speed_bullet

        if abs(pos[0]) >= 600 or abs(pos[1]) >= 600: #check if the bullet is in arena
            if cheat_marker["cheat"] and oppoents:
                closest = min(
                    oppoents,
                    key=lambda e: (
                        (e["pos"][0] - pos[0]) ** 2
                        + (e["pos"][1] - pos[1]) ** 2
                        + (e["pos"][2] - pos[2]) ** 2
                    ),
                )
                curr_game_stats["score"] += 1
                oppoents.remove(closest)
                oppoents.append(spawn_opponent())
            else:
                curr_game_stats["missed"] += 1
            continue

        still_in_view.append(b)

    bullets[:] = still_in_view

    if (not cheat_marker["cheat"]) and (curr_game_stats["missed"] >= max_wasted_bullet or curr_game_stats["health"] == 0):
        curr_game_stats["running"] = False
        oppoents[:] = []


def opponent_hits():
    if not bullets or not oppoents:
        return

    if cheat_marker["cheat"]:
        base_range = 60
    else:
        base_range = 30

    r2 = base_range * base_range

    survivors = []
    for b in bullets:
        b_x, b_y, b_z = b["pos"]
        struck = False
        for enemy in oppoents[:]:
            ex, ey, ez = enemy["pos"]
            dx = b_x - ex
            dy = b_y - ey
            dz = b_z - ez
            if dx * dx + dy * dy + dz * dz < r2:
                curr_game_stats["score"] += 1
                oppoents.remove(enemy)
                oppoents.append(spawn_opponent())
                struck = True
                break
        if not struck:
            survivors.append(b)

    bullets[:] = survivors


def update_cheating_mode():
    if auto_play["enabled"] == False or curr_game_stats["running"] == False:
        return

    agent["angle"] = (agent["angle"] + 1) % 360
    auto_play["spin_steps"] += 1

    if auto_play["spin_steps"] >= 30:
        auto_play["spin_steps"] = 0
        auto_play["ready"] = True

    if auto_play["ready"] == False:
        return

    rad = math.radians(agent["angle"])
    gun_forward = 140
    gun_side = 50
    gun_height = 10

    p_x, p_y, p_z = agent["pos"]
    dir_aimed = [-math.cos(rad), -math.sin(rad)]

    gun_x = p_x + gun_side * math.sin(rad) + dir_aimed[0] * gun_forward
    gun_y = p_y - gun_side * math.cos(rad) + dir_aimed[1] * gun_forward
    gun_z = p_z + gun_height

    for opponent in oppoents:
        e_x, e_y, e_z = opponent["pos"]
        d_x = e_x - gun_x
        d_y = e_y - gun_y
        d_z = e_z - gun_z

        horiz = calc_eulc_distance(d_x, d_y)
        if horiz == 0:
            continue

        align = (d_x * dir_aimed[0] + d_y * dir_aimed[1]) / horiz
        if align > 0.99:
            total = math.sqrt(d_x * d_x + d_y * d_y + d_z * d_z)
            fire_dir = [d_x / total, d_y / total, d_z / total]
            bullets.append({"pos": [gun_x, gun_y, gun_z], "dir": fire_dir})
            auto_play["ready"] = False
            break


def idle():
    update_bullets()
    opponent_hits()
    update_opponents()
    update_cheating_mode()
    glutPostRedisplay()

def keyboardListener(key, x, y):

    if auto_play["enabled"]:
        speed = cheating_step_size
    else:
        speed = normal_step_size

    if curr_game_stats["running"]:
        if key == b"w":
            ang = math.radians(agent["angle"])
            d_x = -math.cos(ang) * speed
            d_y = -math.sin(ang) * speed
            n_x = agent["pos"][0] + d_x
            n_y = agent["pos"][1] + d_y
            if is_player_inside(n_x, n_y):
                agent["pos"][0] = n_x
                agent["pos"][1] = n_y
                if (
                    display_state["mode"] == "first"
                    and auto_play["enabled"]
                    and not view_tweaks["gun_view"]
                ):
                    view_tweaks["follow_offset"][0] += d_x
                    view_tweaks["follow_offset"][1] += d_y

        elif key == b"s":
            ang = math.radians(agent["angle"])
            d_x = math.cos(ang) * speed
            d_y = math.sin(ang) * speed
            n_x = agent["pos"][0] + d_x
            n_y = agent["pos"][1] + d_y
            if is_player_inside(n_x, n_y):
                agent["pos"][0] = n_x
                agent["pos"][1] = n_y
                if (
                    display_state["mode"] == "first"
                    and auto_play["enabled"]
                    and not view_tweaks["gun_view"]
                ):
                    view_tweaks["follow_offset"][0] += d_x
                    view_tweaks["follow_offset"][1] += d_y

        elif key == b"a" and auto_play["enabled"] == False:
            agent["angle"] += turning_step_size

        elif key == b"d" and auto_play["enabled"] == False:
            agent["angle"] -= turning_step_size

        elif key == b"c":
            auto_play["enabled"] = not auto_play["enabled"]
            cheat_marker["cheat"] = auto_play["enabled"]
            if not auto_play["enabled"]:
                view_tweaks["gun_view"] = False

        elif key == b"v":
            if display_state["mode"] == "first" and auto_play["enabled"]:
                view_tweaks["gun_view"] = not view_tweaks["gun_view"]

    elif key == b"r":
        reset_game()


def specialKeyListener(key, x, y):
    if not curr_game_stats["running"]:
        return

    step = 3.0
    if key == GLUT_KEY_UP:
        display_state["eye"][1] += step
    elif key == GLUT_KEY_DOWN:
        display_state["eye"][1] -= step
    elif key == GLUT_KEY_LEFT:
        display_state["eye"][0] -= step
    elif key == GLUT_KEY_RIGHT:
        display_state["eye"][0] += step


def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and curr_game_stats["running"]:
        ang = math.radians(agent["angle"])
        dir_x = -math.cos(ang)
        dir_y = -math.sin(ang)

        gun_length = 140
        gun_side = 50
        gun_up = 10

        p_x, p_y, p_z = agent["pos"]
        s_x = p_x + gun_side * math.sin(ang) + dir_x * gun_length
        s_y = p_y - gun_side * math.cos(ang) + dir_y * gun_length
        s_z = p_z + gun_up

        bullets.append({"pos": [s_x, s_y, s_z], "dir": [dir_x, dir_y, 0.0]})

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and curr_game_stats["running"] == True:
        display_state["mode"] = "first" if display_state["mode"] == "third" else "third"



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, window_width, window_height)

    set_viewing_camera()

    draw_floor_pattern()
    draw_bounderies()

    if curr_game_stats["running"]:
        draw_text(10, 450, "health: %d" % curr_game_stats["health"])
        draw_text(10, 430, "score: %d" % curr_game_stats["score"])
        draw_text(10, 410, "missed: %d" % curr_game_stats["missed"])
    else:
        draw_text(10, 450, "game over! score: %d" % curr_game_stats["score"])
        draw_text(10, 430, 'press "r" to restart')

    draw_agent()
    draw_bullets()
    for opponent in oppoents:
        draw_opponents(opponent)

    glutSwapBuffers()



def main():
    reset_game()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D Bullet Frenzy")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()


