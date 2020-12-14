import msvcrt
import time
from threading import Thread
from screen_object import ScreenObject
from screen import Screen
from snake import Snake, CollisionError


# global variables
user_input = b'd'
refresh_rate = 0.1


SCREEN_HEIGHT = 15
SCREEN_WIDTH = 20


def intro():
    choice = ''
    while choice != 'play':
        Screen.cls()
        choice = input("""Hello! Ready to play Snake?
Control the snake with WASD. Any other key you press will quit the game!

Note: will should not run this in Pycharm! Run in cmd.exe!

Type "play" to start playing or "quit" to quit!
:> """)
        if choice == 'quit':
            Screen.cls()
            return
    return set_difficulty()


def set_difficulty():
    global refresh_rate
    choice = ''
    while choice not in ['easy', 'medium', 'hard']:
        Screen.cls()
        choice = input('Now set the difficulty: "easy", "medium" or "hard":\n:> ')

        if choice == 'easy':
            refresh_rate = 0.5
        elif choice == 'medium':
            refresh_rate = 0.3
        elif choice == 'hard':
            refresh_rate = 0.1
        elif choice == 'quit':
            Screen.cls()
            return

    Screen.cls()
    return run()


def get_user_input():
    """Runs in the background and stores the user input in a global variable"""
    global user_input
    while True:
        user_input = msvcrt.getch()
        if user_input not in [b'a', b's', b'd', b'w']:
            break
        time.sleep(0.1)


def main():
    screen = Screen(height=SCREEN_HEIGHT, width=SCREEN_WIDTH, refresh_rate=refresh_rate)

    # positioning the snake in the middle of the screen
    snake = Snake(ScreenObject(x_pos=int(screen.size.width / 2), y_pos=int(screen.size.height / 2), character='°',
                               screen_size=screen.size))
    food = ScreenObject(character='¤', x_pos=0, y_pos=0, screen_size=screen.size)
    food.set_random_position(objs_to_not_collide_with=snake.get_all_parts())

    screen + snake.get_all_parts()
    screen + food

    screen.print_screen()
    while True:
        try:
            if user_input == b'a':
                snake.move('left')
            elif user_input == b'd':
                snake.move('right')
            elif user_input == b'w':
                snake.move('up')
            elif user_input == b's':
                snake.move('down')
            else:
                screen.cls()
                break
        except CollisionError:
            Screen.cls()
            print("Oops! you lost! \n Starting again....")
            time.sleep(3)
            main()

        screen.print_screen()

        if snake.collided_with(food) and food in screen.screen_objs:
            snake.add_part(screen)
            food.set_random_position(objs_to_not_collide_with=snake.get_all_parts())


def run():
    Thread(target=main).start()
    Thread(target=get_user_input).start()


if __name__ == '__main__':
    intro()
