import math
import win32api
import win32.lib.win32con as win32con
import time
import random

from Engine import *
from Input import *

right = True
last = right
def GetCoinPos():
    global last, right
    new = random.randint(0, 100) >= 30
    right = (not right) if new else last
    last = right
    if not right:
        return (random.randint(-45, -15), random.randint(3, 18))
    if right:
        return (random.randint(15, 45), random.randint(3, 18))


player = Quad((-30,10), 3, 6, 0, "# ")
ground = Quad((50, -20), 35, 20, 0, ". ")
ground2 = Quad((-50, -20), 35, 20, 0, ". ")
wall = Quad((-80, 30), 15, 60, 0, ". ")
wall2 = Quad((80, 30), 15, 60, 0, ". ")
coin = Circle(GetCoinPos(), 2, "@ ")
coins = [coin]
score = 0
cur_gravity = 0
frame = 0
gb = time.time()

#-- settings --#
gravity = 5
max_speed = 50
acceleration = 28
turning_power = 100
deceleration = 0.1
jump_power = 2.25
horizontal_jump_power = 18
total_time = 5
time_per_coin = 1.75

res = (50, 30)
#-- settings --#

walls = [wall, wall2]
grounds = [ground, ground2]
collisions = walls+grounds
speed = 0

def main(dt, f):
    if f == 0:
        global cur_gravity, player, coin, score, coins, gb, tl, speed
    if f%10 == 0:
        tl = gb - time.time() + total_time

        if player.c[1] < -50 or tl <= 0:
            return 0

    #--layers--
    players = [player]
    everything = walls+grounds+players+coins
    #--layers--

    if KeyDown("A"):
        speed -= acceleration*dt
        if speed < -max_speed:
            speed += abs(speed)-max_speed
    elif speed < 0 and KeyDown("D"):
        speed += turning_power*dt
    if KeyDown("D"):
        speed += acceleration*dt
        if speed > max_speed:
            speed -= (speed-max_speed)
    elif speed > 0 and KeyDown("A"):
        speed -= turning_power*dt
    if not (KeyDown("A") or KeyDown("D")):
        speed = speed + (0 - speed) * (1 - deceleration ** dt)

    side_move = player.move(speed*dt, 0, collisions)
    player = side_move[0]
    if side_move[1]:
        speed = 0

    next_grav_move = player.move(0, cur_gravity-0.1, grounds)
    grounded = next_grav_move[1]
    if not grounded:
        player = next_grav_move[0]
        cur_gravity -= gravity*dt
    elif player.bl[1] >= next_grav_move[2].tl[1]:
        dis = -(player.br[1] - next_grav_move[2].tr[1])
        player = player.move(0, dis, [])[0]
        cur_gravity = 0

    if KeyDown("SPACE") and grounded:
        if KeyDown("A"):
            speed -= horizontal_jump_power
        if KeyDown("D"):
            speed += horizontal_jump_power
        cur_gravity = jump_power
        player = player.move(0, cur_gravity, [])[0]
        
    if coin.check_rect_collision([player]):
        gb += time_per_coin
        score += 1
        win32api.MessageBeep(win32con.MB_ICONERROR)
        coin = Circle(GetCoinPos(), 2, "@ ")
        coins = [coin]
    
    cp = player.c
    Render(res, (100, 50), everything, cp, 50, [f"Score: {score}", f"Time: {int(tl)}", f"FPS: {int(1/(dt+0.0001))}"])

st = time.time()
et = time.time()
dt = 0

while 1:
    st = time.time()
    game = main(dt, frame)
    if game == 0:
        break
    et = time.time()
    dt = et-st
    frame += 1

print("\n\n")
print("Game over!")
print(f"Score: {score}")
hs = int(open("hs.txt", "r").read())
if score > hs:
    print("New highscore!")
    hs = open("hs.txt", "w").write(str(score))
else:
    print(f"Highscore: {hs}")

input()

