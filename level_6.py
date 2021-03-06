# -----------------------------------------------------------------------------------
from pico2d import *
import framework
import game
import level_6
import level_7
# -----------------------------------------------------------------------------------
from jumper import Jumper
from obstacle import Spike, Saw, Flag

# -----------------------------------------------------------------------------------
name = "level_6"
# -----------------------------------------------------------------------------------
jumper, spike, saw, flag = None, None, None, None
level, blink, sign, font = None, None, None, None
falling_state = True
# -----------------------------------------------------------------------------------


def create_world():
    global jumper, spike, saw, flag, level, blink, sign, font

    # game class import
    jumper = Jumper()
    spike = Spike()
    saw = Saw()
    flag = Flag()

    # game image load
    level = load_image("resource/image/levels/level_6.png")
    blink = load_image("resource/image/objects/blink.png")
    sign = load_image("resource/image/objects/sign.png")
    font = load_font("resource/font/overwatch.TTF", 25)

    # game initialize
    game.jumping = 0
    game.flying = 0
    game.movement = 0
    game.seta = 90
    game.key = False
    game.gravity_stage = False
    game.height = 0
    game.x, game.y = 50, 244
    game.jump_x, game.jump_y = 12, 23
    game.gck, game.gak = 90, 270
    game.sign_x, game.sign_y = 310, 196
    game.min_x, game.max_x = 0, 1000
    game.min_wall, game.max_wall = 40, 40

    # class initialize
    if falling_state is True:
        jumper.x, jumper.y = 50, 470
        game.key = False
    if falling_state is False:
        jumper.x, jumper.y = 50, 244
        game.key = True

    flag.x, flag.y = 555, 197
    spike.x, spike.y = 503, 105
    spike.box_x, spike.box_y = 393, 10
    jumper.state = Jumper.STANDRIGHT
    jumper.life = 1


def enter():
    create_world()
    framework.reset_time()


def exit():
    pass


def pause():
    pass


def resume():
    pass


# -----------------------------------------------------------------------------------

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            framework.quit()
        if game.key:
            if jumper.life == 1:
                if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                    game.jumping = 1

                if game.jumping == 0:
                    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                        jumper.state = jumper.RUNRIGHT
                    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                        jumper.state = jumper.RUNLEFT
                    if (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
                        jumper.state = jumper.STANDRIGHT
                    if (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
                        jumper.state = jumper.STANDLEFT

                if game.jumping == 1:
                    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                        game.movement = 1

                    if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                        game.movement = 2

                    if jumper.state == jumper.RUNRIGHT or jumper.state == jumper.STANDRIGHT:
                        jumper.state = jumper.JUMPRIGHT

                    if jumper.state == jumper.RUNLEFT or jumper.state == jumper.STANDLEFT:
                        jumper.state = jumper.JUMPLEFT

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            jumper.y += 2

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            jumper.y -= 2


def update(frame_time):
    # update ----------------------------------
    jumper.update(frame_time)
    saw.update(frame_time)
    logic(frame_time)
    height(frame_time)
    wall(frame_time)
    collision(frame_time)
    change_level(frame_time)
    # -----------------------------------------
    update_canvas()


def draw(frame_time):
    clear_canvas()
    # draw objects ----------------------------
    level.draw(game.back_x, game.back_y)
    sign.draw(game.sign_x, game.sign_y)
    saw.draw()
    flag.draw()
    jumper.draw()
    text(frame_time)
    # draw bounding box -----------------------
    # jumper.draw_bb()
    # spike.draw_bb()
    # saw.draw_bb_1()
    # saw.draw_bb_2()
    # saw.draw_bb_3()
    # saw.draw_bb_4()
    # saw.draw_bb_5()
    # saw.draw_bb_6()
    # -----------------------------------------
    update_canvas()


# -----------------------------------------------------------------------------------

def logic(frame_time):
    global falling_state

    if jumper.x > 150 and jumper.x < 265 \
            or jumper.x > 380 and jumper.x < 510 \
            or jumper.x > 580 and jumper.x < 705 \
            or jumper.x > 775 and jumper.x < 900:
        if jumper.state == Jumper.RUNRIGHT:
            jumper.state = Jumper.STANDRIGHT
            game.jumping = 1
            jumper.state = Jumper.JUMPRIGHT

        if jumper.state == Jumper.RUNLEFT:
            jumper.state = Jumper.STANDLEFT
            game.jumping = 1
            jumper.state = Jumper.JUMPLEFT

    if jumper.y > 245 and falling_state:
        jumper.y -= 9

    if jumper.y <= 245 and falling_state:
        jumper.y = 244
        game.key = True
        falling_state = False

    if jumper.state == Jumper.JUMPRIGHT:
        jumper.y += 2
        if jumper.x > 150:
            game.gck = 110
        if jumper.x > 380:
            game.jump_y = 33

    if jumper.state == Jumper.JUMPLEFT:
        jumper.y += 2
        if jumper.x < 270:
            game.gak = 250

        if jumper.x > 270:
            game.gak = 270
            game.jump_y = 23

    if jumper.x >= flag.x:
        game.checkpoint = True

# -----------------------------------------------------------------------------------


def height(frame_time):
    if jumper.x < 150:
        game.height = 0

    if jumper.y <= 140:
        if jumper.x > 105:
            if jumper.x < 270:
                game.height = 140 - game.y

    elif jumper.y > 140:
        if jumper.x > 150:
            if jumper.x < 270:
                game.height = 140 - game.y

    if jumper.x > 270:
        if jumper.x < 380:
            game.height = 199 - game.y

    if jumper.x > 380:
        if jumper.x < 510:
            game.height = 140 - game.y

    if jumper.x > 510:
        if jumper.x < 580:
            game.height = 199 - game.y

    if jumper.x > 580:
        if jumper.x < 705:
            game.height = 140 - game.y

    if jumper.x > 705:
        if jumper.x < 775:
            game.height = 199 - game.y

    if jumper.x > 775:
        if jumper.x < 900:
            game.height = 140 - game.y

    if jumper.x > 900:
        game.height = 199 - game.y

    if game.height == 140 - game.y:
        jumper.y -= 2

# -----------------------------------------------------------------------------------


def wall(frame_time):
    if jumper.x < 960:
        game.max_wall = 40

    if jumper.x >= 960:
        game.max_wall = 0


# -----------------------------------------------------------------------------------

def text(frame_time):
    # text for player :)
    font.draw(395, 12, "SPINNING  SAW  IS  MY  FAVORITE", (255, 255, 255))
    print(jumper.y)
    if jumper.x > game.sign_x - 20:
        if jumper.x < game.sign_x + 20:
            if jumper.y == 199:
                font.draw(200, 270, "STEP ON JUMPING PLATFORMS", (255, 255, 255))
                font.draw(240, 240, "TO", (255, 255, 255))
                font.draw(268, 240, "JUMP HIGHER", (255, 50, 50))


# -----------------------------------------------------------------------------------

def collision(frame_time):
    if collide(jumper, spike) or collide_1(jumper, saw) or collide_2(jumper, saw) or collide_3(jumper, saw) \
            or collide_4(jumper, saw) or collide_5(jumper, saw) or collide_6(jumper, saw):
        game.reset = True
        framework.push_state(level_6)
        if game.checkpoint:
            jumper.x = flag.x
            jumper.y = flag.y + 2


# -----------------------------------------------------------------------------------

def change_level(frame_time):
    if game.reset:
        blink.draw(game.back_x, game.back_y)
        game.temp += 1

    if game.temp > 2:
        game.reset = False

    if jumper.x >= game.max_x:
        game.checkpoint = False
        framework.push_state(level_7)


# -----------------------------------------------------------------------------------

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True


def collide_1(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb_1()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True


def collide_2(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb_2()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True


def collide_3(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb_3()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True


def collide_4(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb_4()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True


def collide_5(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb_5()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True


def collide_6(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb_6()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True

# -----------------------------------------------------------------------------------


