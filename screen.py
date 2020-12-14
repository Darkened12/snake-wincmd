import os
import time


class Size:
    def __init__(self, size):
        self.height = size[0]
        self.width = size[1]


class Screen:
    """High level class to show stuff on the screen"""
    def __init__(self, height, width, refresh_rate=0):
        self._objs = []
        self._height = height
        self._width = width
        self._refresh_rate = refresh_rate

    def __add__(self, screen_obj):
        """Easier way to add objects to Screen"""
        def error(obj):
            raise ValueError(f'There is already an object with (y={obj.y_pos}, x={obj.x_pos}) position!')

        if type(screen_obj) == list:
            self._objs.extend([obj if not self._exists(obj) else error(obj) for obj in screen_obj])
        elif not self._exists(screen_obj):
            self._objs.append(screen_obj)
        else:
            error(screen_obj)

    def __sub__(self, screen_obj):
        """Easier way to remove objects from Screen"""
        if self._exists(screen_obj):
            self._objs.remove(screen_obj)
        else:
            raise ValueError("There isn't an object in this position!")

    @staticmethod
    def cls():
        """Clear the Windows command line output"""
        os.system('cls')

    @property
    def screen_objs(self):
        return self._objs

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def size(self):
        return Size([self._height, self._width])

    @property
    def refresh_rate(self):
        return self._refresh_rate

    def _exists(self, screen_obj):
        for obj in self.screen_objs:
            if obj == screen_obj:
                return True
        else:
            return False

    def add_screen_objs(self, screen_obj):
        self.__add__(screen_obj)

    def remove_screen_obj(self, screen_obj):
        self.__sub__(screen_obj)

    def flush_screen(self):
        self._objs = []

    def _get_blank_screen(self):
        """The root part of the entire system! here we build a 2D list representing a screen"""
        lines = [" " for n in range(self.width)]
        screen = [lines.copy() for n in range(self.height)]
        return screen

    def get_screen(self):
        """Adds all ScreenObject's and returns a printable string representation"""
        self.cls()
        screen = self._get_blank_screen()

        # Checking if there are objects with equal positions
        for obj in self.screen_objs:
            try:
                screen[obj.y_pos][obj.x_pos] = obj.character
            except IndexError:
                raise IndexError(f'Wrong Screen position (x={obj.x_pos}, y={obj.y_pos}) for object "{obj.character}"')

        result = ""
        for line in screen:
            string = "".join(line)
            string += "\n"
            result += string
        return result

    def get_raw_screen(self):
        """Same as Screen.get_screen() but returns a 2D list instead"""
        self.cls()
        screen = self._get_blank_screen()
        for obj in self.screen_objs:
            screen[obj.y_pos][obj.x_pos] = obj.character
        return screen

    def print_screen(self):
        """The high level Screen.get_screen() method with print() and time.sleep() already implemented"""
        print(self.get_screen())
        time.sleep(self._refresh_rate)
