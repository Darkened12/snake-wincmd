from screen_object import ScreenObject


class Snake:
    """Represents a snake using ScreeObject objects"""
    def __init__(self, head):
        self._screen_size = head.screen_size
        self._last_direction = 'right'
        self._parts = [head,
                       ScreenObject(head.character, self._screen_size, head.x_pos - 1, head.y_pos),
                       ScreenObject(head.character, self._screen_size, head.x_pos - 2, head.y_pos)]

    def get_all_parts(self):
        return self._parts

    @property
    def head(self):
        return self._parts[0]

    def add_part(self, screen):
        """This method needs a better implementation since I couldn't find a easier way to do this.
        Since the main code won't show on the screen right away all snake parts before reorganizing them, I just used
        ScreenObject.set_random_position() to avoid position conflicts. But this is a terrible implementation"""
        self._parts.append(ScreenObject(self.head.character,
                                        y_pos=0,
                                        x_pos=0,
                                        screen_size=self._screen_size))

        self._parts[-1].set_random_position(objs_to_not_collide_with=screen.screen_objs)
        screen + self._parts[-1]

    def is_opposite(self, direction):
        """Preventing the snake from colliding with itself"""
        if direction == 'up' and self._last_direction == 'down':
            return 'down'
        elif direction == 'down' and self._last_direction == 'up':
            return 'up'
        elif direction == 'right' and self._last_direction == 'left':
            return 'left'
        elif direction == 'left' and self._last_direction == 'right':
            return 'right'
        else:
            return direction

    def move(self, direction):
        """Works almost like ScreenObject.move()"""

        direction = self.is_opposite(direction)
        self._last_direction = direction

        # Here we move all parts but the head forward
        last_position = self.head.position
        for part in self._parts[1:]:
            old_position = part.position
            part.position = last_position
            last_position = old_position

        if direction == 'up':
            self.head.move(up=1)
        elif direction == 'down':
            self.head.move(down=1)
        elif direction == 'left':
            self.head.move(left=1)
        elif direction == 'right':
            self.head.move(right=1)

        # Checks if the head has collided with its parts
        for part in self._parts[1:]:
            if part.collided_with(self.head):
                raise CollisionError

    def collided_with(self, screen_obj):
        return self.head.collided_with(screen_obj)


class CollisionError(Exception):
    pass
