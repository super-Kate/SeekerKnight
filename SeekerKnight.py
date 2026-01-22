import arcade

from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
    UIBoxLayout,
    UILabel
)

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SPRITE_SCALING = 1.0

VIEWPORT_MARGIN = 220

CAMERA_SPEED = 0.1
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 15

PLAYING_FIELD_WIDTH = SCREEN_WIDTH - 300
PLAYING_FIELD_HEIGHT = SCREEN_HEIGHT - 300
CELL_SIZE = 64

door1_start, door1_end = 576, 768
door2_start, door2_end = 1088, 1280
door3_start, door3_end = 1536, 1728

TEX_RED_BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")

background_hall = arcade.Sprite("sprites/first_hall.png", scale=1)
second_hall = arcade.Sprite("sprites/second_hall.png", scale=1)
hall_map = "map_files/dungeon.tmx"
room_1 = arcade.Sprite("sprites/room_1.png", scale=1)
room_2_map = "map_files/room_2.tmx"
room_3 = arcade.Sprite("sprites/room_3.png", scale=1)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        bg_scale = 1.2
        self.bg_sprite = arcade.Sprite("sprites/mainmenu_bg.png", scale=bg_scale)
        self.bg_sprite.center_x = 1000
        self.bg_sprite.center_y = 600
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.bg_sprite)
        self.ui = UIManager()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.add(self.box_layout)
        self.ui.add(self.anchor_layout)

        button_play = self.box_layout.add(
            UITextureButton(
                text="Играть",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
            )
        )

        @button_play.event("on_click")
        def on_click(event):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        button_exit = self.box_layout.add(
            UITextureButton(
                text="Выйти",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
            )
        )

        @button_exit.event("on_click")
        def on_click(event):
            self.window.close()

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear(color=arcade.uicolor.BLACK)
        self.sprite_list.draw()
        self.ui.draw()


class Room:
    def __init__(self, background, map_name):
        self.wall_list = arcade.SpriteList()
        self.background = background
        self.map_name = map_name


def setup_room_0():
    room = Room(background_hall, hall_map)
    return room

def setup_room_1():
    room = Room(room_1, hall_map)
    return room

def setup_room_2():
    room = Room(room_3, room_2_map)
    return room

def setup_room_3():
    room = Room(room_3, hall_map)
    return room

def setup_room_4():
    room = Room(second_hall, hall_map)
    return room

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.keys_picked = 0
        self.current_room = 0
        self.e_pressed = False
        self.rooms = None
        self.player_list = None
        self.wall_list = None
        self.room2_key_picked = False
        self.key_list = arcade.SpriteList()
        h = SCREEN_HEIGHT - 200

        self.player_sprite = None
        self.physics_engine = None
        self.keys_display = arcade.Text(
            f"keys: {self.keys_picked}",
            x=10,
            y=1200,
            color=arcade.csscolor.WHITE,
            font_size=20,
        )
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.camera_sprites.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

    def setup(self):
        self.player_sprite = arcade.Sprite("sprites/player_idle.PNG", scale=1.0)
        self.player_sprite.center_x = CELL_SIZE * 1 + (CELL_SIZE / 2)
        self.player_sprite.center_y = CELL_SIZE * 2 + (CELL_SIZE / 2)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.key = arcade.Sprite("sprites/key.png", scale=1)

        self.rooms = []
        room = setup_room_0()
        self.rooms.append(room)

        room = setup_room_1()
        self.rooms.append(room)
        room = setup_room_2()
        self.rooms.append(room)
        room = setup_room_3()
        self.rooms.append(room)
        room = setup_room_4()
        self.rooms.append(room)
        self.current_room = 0

        self.current_map = self.rooms[self.current_room].map_name
        self.tile_map = arcade.load_tilemap(self.current_map, scaling=1.0)
        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.collision_list = self.tile_map.sprite_lists["collision"]

        self.current_background_list = arcade.SpriteList()
        self.current_background = self.rooms[self.current_room].background
        self.current_background.center_x = self.tile_map.width * self.tile_map.tile_width / 2
        self.current_background.center_y = self.tile_map.height * self.tile_map.tile_height / 2
        self.current_background_list.append(self.current_background)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.collision_list)
        self.background_color = arcade.color.BLUE_YONDER

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()

        self.current_background_list.draw()
        self.wall_list.draw()
        self.key_list.draw()
        self.player_list.draw()
        self.key_list.draw()
        with self.camera_gui.activate():
            self.keys_display.text = f"Keys: {self.keys_picked}"
            self.keys_display.draw()

        self.camera_shake.update_camera()
        self.camera_shake.readjust_camera()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        elif key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.E:
            self.e_pressed = True
        elif key == arcade.key.R:
            self.move_back()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.E:
            self.e_pressed = False

    def on_update(self, delta_time):
        self.physics_engine.update()
        if self.current_room == 0:
            if self.e_pressed:
                if door1_start <= self.player_sprite.center_x <= door1_end:
                    self.load_room(1)
                elif door2_start <= self.player_sprite.center_x <= door2_end:
                    self.load_room(2)
                    self.place_key(2)
                elif door3_start <= self.player_sprite.center_x <= door3_end:
                    self.load_room(3)
            elif self.player_sprite.center_x > 1831:
                self.load_room(4)
        elif self.current_room == 1:
            if self.player_sprite.center_x < 89:
                self.load_room(0)
        elif self.current_room == 2:
            if self.player_sprite.center_x < 89:
                self.load_room(0)
            keys_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.key_list)
            for key in keys_hit_list:
                key.remove_from_sprite_lists()
                self.keys_picked += 1
                self.room2_key_picked = True
        elif self.current_room == 3:
            if self.player_sprite.center_x < 89:
                self.load_room(0)
        elif self.current_room == 4:
            if self.e_pressed:
                pass
            elif self.player_sprite.center_x < 89:
                self.load_room(0)

        self.camera_shake.update(delta_time)
        self.scroll_to_player()

    def place_key(self, level):
        if level == 2 and self.room2_key_picked == False:
            self.key.center_x = 1760
            self.key.center_y = 480
            self.key_list.append(self.key)


    def move_back(self):
        self.player_sprite.center_x = CELL_SIZE * 1 + (CELL_SIZE / 2)
        self.player_sprite.center_y = CELL_SIZE * 2 + (CELL_SIZE / 2)

    def load_room(self, room_index):
        self.current_room = room_index

        self.current_map = self.rooms[self.current_room].map_name
        self.tile_map = arcade.load_tilemap(self.current_map, scaling=1.0)

        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.collision_list = self.tile_map.sprite_lists["collision"]

        self.current_background_list.clear()
        self.current_background = self.rooms[self.current_room].background
        self.current_background.center_x = self.tile_map.width * self.tile_map.tile_width / 2
        self.current_background.center_y = self.tile_map.height * self.tile_map.tile_height / 2
        self.current_background_list.append(self.current_background)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.collision_list)

        self.player_sprite.center_x = CELL_SIZE * 2 + (CELL_SIZE / 2)
        self.player_sprite.center_y = CELL_SIZE * 2 + (CELL_SIZE / 2)

    def scroll_to_player(self):
        position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position,
            position,
            CAMERA_SPEED,
        )

SCREEN_WIDTH1 = 600
SCREEN_HEIGHT1 = 600
GRID_SIZE = 3
TILE_SIZE = SCREEN_WIDTH1 // GRID_SIZE


class SlidePuzzle(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH1, SCREEN_HEIGHT1, "Puzzle")
        
        self.board = []
        self.tiles = []
        self.selected_tile = None
        
        self.setup()

    def setup(self):
       numbers = list(range(1, GRID_SIZE * GRID_SIZE + 1))
       random.shuffle(numbers)
       self.board = []
       index = 0
       for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            row.append(numbers[index])
            index += 1
            self.board.append(row)

        self.tiles = arcade.SpriteList()
        self.create_tiles()
    
    def create_tiles(self):
        images = ["01.jpg", '02.jpg', '03.jpg', '04.jpg', '05.jpg', '06.jpg', '07.jpg', '08.jpg', '09.jpg']
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile_value = self.board[row][col]
                ch = random.choice(images)
                tile = arcade.Sprite(ch, scale=0.8)
                images.remove(ch)

                tile.center_x = col * TILE_SIZE + TILE_SIZE // 2
                tile.center_y = SCREEN_HEIGHT1 - (row * TILE_SIZE + TILE_SIZE // 2)

                tile.properties = {
                    'value': tile_value,
                    'grid_pos': (row, col),
                    'selected': False
                }
                
                self.tiles.append(tile)

    def on_draw(self):
        for i in range(GRID_SIZE + 1):
            arcade.draw_line(
                i * TILE_SIZE, 0,
                i * TILE_SIZE, SCREEN_HEIGHT1,
                arcade.color.BLACK, 2
            )
            arcade.draw_line(
                0, i * TILE_SIZE,
                SCREEN_WIDTH1, i * TILE_SIZE,
                arcade.color.BLACK, 2
            )
        
        self.tiles.draw()
            

    def on_mouse_press(self, x, y, button):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        
        col = x // TILE_SIZE
        row = (SCREEN_HEIGHT1 - y) // TILE_SIZE
        
        clicked_tile = None
        for tile in self.tiles:
            if tile.properties['grid_pos'] == (row, col):
                clicked_tile = tile
                break
        
        if not clicked_tile:
            return
        
        if self.selected_tile is None:
            self.selected_tile = clicked_tile
            clicked_tile.properties['selected'] = True
        else:
            if self.can_swap(self.selected_tile, clicked_tile):
                self.swap_tiles(self.selected_tile, clicked_tile)
                if self.check_win():
                    print("Поздравляем! Вы собрали пазл!")

            self.selected_tile.properties['selected'] = False
            clicked_tile.properties['selected'] = False
            self.selected_tile = None
    
    def can_swap(self, tile1, tile2):
        row1, col1 = tile1.properties['grid_pos']
        row2, col2 = tile2.properties['grid_pos']
        
        return (abs(row1 - row2) == 1 and col1 == col2) or \
               (abs(col1 - col2) == 1 and row1 == row2)
    
    def swap_tiles(self, tile1, tile2):
        row1, col1 = tile1.properties['grid_pos']
        row2, col2 = tile2.properties['grid_pos']
        
        self.board[row1][col1], self.board[row2][col2] = \
            self.board[row2][col2], self.board[row1][col1]
        
        tile1.center_x, tile2.center_x = tile2.center_x, tile1.center_x
        tile1.center_y, tile2.center_y = tile2.center_y, tile1.center_y
        
        tile1.properties['grid_pos'], tile2.properties['grid_pos'] = \
            tile2.properties['grid_pos'], tile1.properties['grid_pos']
    
    def check_win(self):
        pass

    
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.ui = UIManager()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.add(self.box_layout)
        self.ui.add(self.anchor_layout)

        self.game_view = game_view
        self.label = UILabel(text="Пауза",
                             font_size=40,
                             text_color=arcade.color.WHITE,
                             width=200,
                             align="center")
        self.box_layout.add(self.label)
        button_back = self.box_layout.add(
            UITextureButton(
                text="Вернуться в игру",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
            )
        )
        button_menu = self.box_layout.add(
            UITextureButton(
                text="В меню",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
            )
        )

        @button_back.event("on_click")
        def on_click(event):
            self.window.show_view(self.game_view)

        @button_menu.event("on_click")
        def on_click(event):
            self.window.show_view(MenuView())

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        self.clear(color=arcade.uicolor.BLACK)
        self.ui.draw()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, title="SeekerKnight")
    window.show_view(MenuView())
    window.set_fullscreen(True)
    arcade.run()


if __name__ == "__main__":
    main()