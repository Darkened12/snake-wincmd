import random


class ScreenObject:
    """Represents a character on the screen"""
    def __init__(self, character, screen_size, x_pos, y_pos):
        self._screen_size = screen_size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self._char = character

    def __eq__(self, other):
        return self.y_pos == other.y_pos and self.x_pos == other.x_pos and self.character == other.character

    @staticmethod
    def check_value(value):
        if type(value) == int:
            return value
        else:
            raise ValueError('Value must be an integer')

    def get_position(self):
        return [self.y_pos, self.x_pos]

    @property
    def position(self):
        return self.get_position()

    @position.setter
    def position(self, values):
        self.y_pos = values[0]
        self.x_pos = values[1]

    @property
    def character(self):
        return self._char

    @property
    def screen_size(self):
        """Should be a screen.Size object"""
        return self._screen_size

    def set_random_position(self, objs_to_not_collide_with=None):
        """objs_to_not_collide_with must be a list of ScreenObject objects.
        Generates a random position without conflicting with other ScreenObject objects"""
        if objs_to_not_collide_with is None:
            objs_to_not_collide_with = []

        objs_x_pos = [obj.x_pos for obj in objs_to_not_collide_with]
        objs_y_pos = [obj.y_pos for obj in objs_to_not_collide_with]

        while True:
            x_pos = random.randrange(0, self._screen_size.width)
            if x_pos not in objs_x_pos:
                break

        while True:
            y_pos = random.randrange(0, self._screen_size.height)
            if y_pos not in objs_y_pos:
                break

        self.y_pos = y_pos
        self.x_pos = x_pos

    def collided_with(self, screen_obj):
        if self.get_position() == screen_obj.get_position():
            return True
        else:
            return False

    def _is_out_of_screen(self):
        """Complicated way to check whether a object is out of screen or not then flips its position if it is"""
        if self.y_pos >= self._screen_size.height:
            self.y_pos -= self._screen_size.height
        elif self.y_pos < 0:
            self.y_pos += self._screen_size.height

        if self.x_pos >= self._screen_size.width:
            self.x_pos -= self._screen_size.width
        elif self.x_pos < 0:
            self.x_pos += self._screen_size.width

    def move(self, up=0, down=0, left=0, right=0):
        """The most important method. Moves the object across the screen without going outside of height and width"""
        self.y_pos = self.y_pos - up
        self.y_pos = self.y_pos + down
        self.x_pos = self.x_pos - left
        self.x_pos = self.x_pos + right

        self._is_out_of_screen()
