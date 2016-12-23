# -----------------------------------------------------------------------------------
from pico2d import *
import framework

# -----------------------------------------------------------------------------------
from runner import Runner

# -----------------------------------------------------------------------------------
name = "gameMain"
# -----------------------------------------------------------------------------------
runner = None
# -----------------------------------------------------------------------------------


def create_world():
    global runner
    runner = Runner()


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
RIGHTSTAND = 0
LEFTSTAND = 1
RIGHT = 2
LEFT = 3


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            framework.quit()

        # 조작
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            runner.state = RIGHT
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            runner.state = LEFT
        if (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            runner.state = RIGHTSTAND
            #runner.right_frame = 0
        if (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            runner.state = LEFTSTAND
            #runner.left_frame = 0


def update(frame_time):
    runner.update(frame_time)
    update_canvas()

def draw(frame_time):
    clear_canvas()
    runner.draw()
    update_canvas()

# -----------------------------------------------------------------------------------



