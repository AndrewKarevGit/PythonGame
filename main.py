from tkinter import *
import math
import time
import music
import random


# ----- START WINDOW -----


def create_start_window():
    global NAME, POINTS, LEVEL
    NAME = None
    POINTS = 0
    LEVEL = 1
    # Window settings
    music.start_window()
    root.title('DungeonMaster')
    root.geometry('480x480')
    root.iconphoto(True, hero_img)
    start_window_bg.place(x=0, y=0)

    # Name Input
    name_input.insert(0, "Name...")
    name_input.place(x=100, y=175, width=285)

    # Start Button
    goto_level1_btn.place(x=150, y=240, width=185)
    cheat_btn.place(x=172, y=70, width=48)


# ----- GAME OVER WINDOW -----


def create_game_over_window():
    # Window Settings
    music.end_window()
    root.title('DungeonMaster')
    root.geometry('480x480')

    game_over_window_bg.place(x=0, y=0)
    game_over_window_points.place(x=150, y=175, width=185)
    game_over_window_score.place(x=150, y=215, width=185)
    restart_btn.place(x=150, y=260, width=185)
    gg_with_name.place(x=240, y=450, width=240)


# ----- LEVEL N WINDOW -----


def create_level_n_window(current_level):
    root.bind("<KeyPress>", key_pressed)

    global master, portal, name, level, holes, enemies, life, is_life
    battlefield.delete("all")

    if LEVEL == 1:
        music.beginner()
        battlefield.config(bg='#FFF1D0')
    elif LEVEL == 11:
        music.stop()
        music.intermediate()
        battlefield.config(bg='#FFFD82')
    elif LEVEL == 21:
        music.stop()
        music.hard()
        battlefield.config(bg='#F4B393')

    name.place(x=0, y=0)
    level.place(x=241, y=0)

    battlefield.place(x=0, y=49)

    # Spawn
    spawn_pos = (random.randint(0, N_X - 1) * STEP,
                 random.randint(0, N_Y - 1) * STEP)
    spawn = battlefield.create_image(spawn_pos[0], spawn_pos[1],
                                     image=spawn_img, anchor="nw")
    portal_pos = (random.randint(0, N_X - 1) * STEP,
                  random.randint(0, N_Y - 1) * STEP)
    portal = battlefield.create_image(portal_pos[0], portal_pos[1],
                                      image=portal_img, anchor="nw")
    master_pos = spawn_pos
    master = battlefield.create_image(master_pos[0], master_pos[1],
                                      image=master_img, anchor="nw")

    is_life = random.choice((True, False))
    if is_life:
        life_pos = (random.randint(0, N_X - 1) * STEP,
                    random.randint(0, N_Y - 1) * STEP)
        while life_pos == spawn_pos:
            life_pos = (random.randint(0, N_X - 1) * STEP,
                        random.randint(0, N_Y - 1) * STEP)
        while life_pos == portal_pos:
            life_pos = (random.randint(0, N_X - 1) * STEP,
                        random.randint(0, N_Y - 1) * STEP)
        life = battlefield.create_image((life_pos[0], life_pos[1]),
                                        image=life_img, anchor='nw')

    enemies = []
    enemies_num = math.floor(LEVEL / 2)
    for _ in range(enemies_num):
        enemy_pos = (random.randint(0, N_X - 1) * STEP,
                     random.randint(0, N_Y - 1) * STEP)
        while enemy_pos == spawn_pos:
            enemy_pos = (random.randint(0, N_X - 1) * STEP,
                         random.randint(0, N_Y - 1) * STEP)

        if LEVEL < 6:
            enemy_type = 'default'
        elif LEVEL < 11:
            enemy_type = random.choice(('default', 'peaceful'))
        else:
            enemy_type = random.choice(('default', 'teleport', 'peaceful'))

        if enemy_type == 'default':
            skin = enemy_default_img
        elif enemy_type == 'teleport':
            skin = enemy_teleport_img
        else:
            skin = enemy_peaceful_img
        enemy = battlefield.create_image((enemy_pos[0], enemy_pos[1]),
                                         image=skin, anchor='nw')
        enemies.append((enemy, enemy_type))

    holes = []
    holes_num = math.floor(LEVEL / 3)
    for _ in range(holes_num):
        hole_pos = (random.randint(0, N_X - 1) * STEP,
                    random.randint(0, N_Y - 1) * STEP)
        while hole_pos == spawn_pos:
            hole_pos = (random.randint(0, N_X - 1) * STEP,
                        random.randint(0, N_Y - 1) * STEP)
        while hole_pos == portal_pos:
            hole_pos = (random.randint(0, N_X - 1) * STEP,
                        random.randint(0, N_Y - 1) * STEP)
        hole = battlefield.create_image((hole_pos[0], hole_pos[1]),
                                        image=hole_img, anchor='nw')
        holes.append(hole)

    while level == LEVEL:
        time.sleep(1)
        if len(enemies) > 0:
            for e in enemies:
                direction = 'Up'
                if battlefield.coords(master)[0] < battlefield.coords(e[0])[0]:
                    direction = 'Left'
                elif battlefield.coords(master)[0] > battlefield.coords(e[0])[0]:
                    direction = 'Right'
                elif battlefield.coords(master)[1] < battlefield.coords(e[0])[1]:
                    direction = 'Down'
                move_wrap(e, direction)


# ----- END ----

def clean():
    battlefield.delete('all')
    name.place_forget()
    level.place_forget()


def do_nothing():
    pass


def check_move():
    global POINTS, LEVEL, SCORE, NAME, with_life, master
    if battlefield.coords(master) == battlefield.coords(portal):
        POINTS += LEVEL * 10
        if SCORE < POINTS:
            SCORE = POINTS
        LEVEL += 1
        clean()
        goto_level_n()

    if is_life and battlefield.coords(master) == battlefield.coords(life):
        with_life = True
        battlefield.delete(life)
        POINTS += 10
        if SCORE < POINTS:
            SCORE = POINTS
        name.config(text=f'{NAME}: {POINTS}')
        battlefield.itemconfig(master, image=master_with_life_img)

    enemies_to_delete = []
    for h in holes:
        if battlefield.coords(master) == battlefield.coords(h) and not CHEAT:
            root.bind("<KeyPress>", do_nothing())
            goto_game_over()
        for e in enemies:
            if battlefield.coords(e[0]) == battlefield.coords(h):
                enemies_to_delete.append(e)
                POINTS += 10
                if SCORE < POINTS:
                    SCORE = POINTS
                name.config(text=f'{NAME}: {POINTS}')
    for e in enemies:
        if battlefield.coords(master) == battlefield.coords(e[0]) and not CHEAT:
            if with_life:
                with_life = False
                battlefield.itemconfig(master, image=master_img)
                enemies_to_delete.append(e)
            else:
                root.bind("<KeyPress>", do_nothing())
                goto_game_over()

    if len(enemies_to_delete) > 0:
        for e in enemies_to_delete:
            battlefield.delete(e[0])
            enemies.remove(e)


def move_wrap(obj, move):
    x1, y1 = battlefield.coords(obj)[:2]
    new_x = x1 + move[0]
    new_y = y1 + move[1]

    if new_x < 0:
        new_x = N_X * STEP + new_x
    elif new_x > N_X * (STEP - 1):
        new_x = 0

    if new_y < 0:
        new_y = N_Y * STEP + new_y
    elif new_y > N_Y * (STEP - 1):
        new_y = 0

    battlefield.move(obj, new_x - x1, new_y - y1)


def enemy_default_step(e):
    if (battlefield.coords(master)[0] == battlefield.coords(e)[0] and
            battlefield.coords(master)[1] == battlefield.coords(e)[1]):
        direction = (0, 0)
    elif battlefield.coords(master)[0] == battlefield.coords(e)[0]:
        if battlefield.coords(master)[1] < battlefield.coords(e)[1]:
            direction = (0, -STEP)
        else:
            direction = (0, STEP)
    elif battlefield.coords(master)[1] == battlefield.coords(e)[1]:
        if battlefield.coords(master)[0] < battlefield.coords(e)[0]:
            direction = (-STEP, 0)
        else:
            direction = (STEP, 0)
    elif battlefield.coords(master)[0] < battlefield.coords(e)[0]:
        direction = (-STEP, 0)
    elif battlefield.coords(master)[0] > battlefield.coords(e)[0]:
        direction = (STEP, 0)
    elif battlefield.coords(master)[1] < battlefield.coords(e)[1]:
        direction = (0, -STEP)
    else:
        direction = (0, STEP)
    move_wrap(e, direction)


def enemy_peaceful_step(e):
    move_wrap(e, random.choice([(STEP, 0), (-STEP, 0), (0, STEP), (0, -STEP)]))


def enemy_teleport_step(e):
    battlefield.coords(e, random.randint(0, N_X - 1) * STEP,
                       random.randint(0, N_Y - 1) * STEP)


def enemies_step():
    for e in enemies:
        if e[1] == 'default':
            enemy_default_step(e[0])
        elif e[1] == 'peaceful':
            enemy_peaceful_step(e[0])
        else:
            enemy_teleport_step(e[0])
    check_move()


def key_pressed(event):
    if event.keysym == 'space':
        goto_game_over()
    if event.keysym == 'Up':
        move_wrap(master, (0, -STEP))
        enemies_step()
    if event.keysym == 'Down':
        move_wrap(master, (0, +STEP))
        enemies_step()
    if event.keysym == 'Left':
        move_wrap(master, (-STEP, 0))
        enemies_step()
    if event.keysym == 'Right':
        move_wrap(master, (+STEP, 0))
        enemies_step()


def name_input_validate(entry_text):
    return True if len(entry_text) <= 7 else False


def goto_level_n():
    global NAME
    NAME = name_input.get()
    level.config(text=f"Level: {LEVEL}")
    name.config(text=f'{NAME}: {POINTS}')
    start_window_bg.place_forget()
    name_input.place_forget()
    goto_level1_btn.place_forget()
    cheat_btn.place_forget()
    create_level_n_window(LEVEL)


def goto_game_over():
    clean()
    game_over_window_points.config(text=f'Points: {POINTS}')
    game_over_window_score.config(text=f'Score: {SCORE}')
    gg_with_name.config(text=f'Good game, {NAME}!')
    create_game_over_window()


def goto_start_window():
    game_over_window_bg.place_forget()
    game_over_window_points.place_forget()
    game_over_window_score.place_forget()
    gg_with_name.place_forget()
    restart_btn.place_forget()
    music.stop()
    create_start_window()


def cheat_on():
    global clicks, CHEAT
    clicks += 1
    if clicks == 3:
        CHEAT = True


root = Tk()

# ----- IMAGES -----
hero_img = PhotoImage(file="img/hero.png")
start_window_bg_img = PhotoImage(file="img/start_window_bg.png")
start_btn_bg_img = PhotoImage(file="img/start_btn_bg.png")
restart_btn_bg_img = PhotoImage(file="img/restart_btn_bg.png")
spawn_img = PhotoImage(file="img/spawn.png")
portal_img = PhotoImage(file="img/portal.png")
master_img = PhotoImage(file="img/master.png")
enemy_default_img = PhotoImage(file="img/enemy_default.png")
enemy_peaceful_img = PhotoImage(file="img/enemy_peaceful.png")
enemy_teleport_img = PhotoImage(file="img/enemy_teleport.png")
hole_img = PhotoImage(file="img/hole.png")
cheat_hole_img = PhotoImage(file="img/cheat_hole.png")
life_img = PhotoImage(file="img/life.png")
master_with_life_img = PhotoImage(file="img/master_with_life.png")

# ----- DATA -----
NAME = None
SCORE = 0
POINTS = 0
LEVEL = 1

N_X = 10
N_Y = 9
STEP = 48

CHEAT = False
clicks = 0

with_life = False

battlefield = Canvas(root, bg='white', width=480, height=480 - 48)

# Start Window
start_window_bg = Label(root, image=start_window_bg_img)
validator = (root.register(name_input_validate), '%P')

name_input = Entry(root,
                   font=('Impact', 32),
                   bd=0,
                   fg='black',
                   validate="key",
                   validatecommand=validator,
                   justify='center')

goto_level1_btn = Button(root,
                         bg='white',
                         bd=0,
                         image=start_btn_bg_img,
                         command=goto_level_n)

cheat_btn = Button(root,
                   bg='white',
                   bd=0,
                   image=cheat_hole_img,
                   command=cheat_on)

# Game Over Window
game_over_window_bg = Label(root, image=start_window_bg_img)

game_over_window_points = Label(root,
                                font=('Impact', 24),
                                bd=0,
                                bg='white',
                                fg='black',
                                text=f'Points: {POINTS}',
                                width=200)

game_over_window_score = Label(root,
                               font=('Impact', 24),
                               bd=0,
                               bg='white',
                               fg='black',
                               text=f'Score: {SCORE}',
                               width=200)

gg_with_name = Label(root,
                     font=('Impact', 16),
                     bd=0,
                     bg='white',
                     fg='black',
                     text=f'Good game, {NAME}!',
                     width=200)

restart_btn = Button(root,
                     bg='white',
                     bd=0,
                     image=restart_btn_bg_img,
                     command=goto_start_window)

img = PhotoImage()

name = Label(root,
             image=img,
             font=('Impact', 32),
             bd=0,
             bg='black',
             fg='white',
             text=f'{NAME}: {POINTS}',
             compound=LEFT,
             width=240,
             height=STEP)

level = Label(root,
              image=img,
              font=('Impact', 32),
              bd=0,
              bg='black',
              fg='white',
              text=f'Level {LEVEL}',
              compound=RIGHT,
              width=240,
              height=STEP)

create_start_window()
root.mainloop()
