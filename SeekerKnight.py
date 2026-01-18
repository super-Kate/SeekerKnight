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
TEX_RED_BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
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
        self.ui.draw()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = None
        self.wall_list = None
        self.background_list = arcade.SpriteList()
        self.background_sprite = arcade.Sprite("sprites/first_hall.png", scale=1)
        self.background_sprite.center_x = 1920 / 2
        self.background_sprite.center_y = 1024 / 2
        self.background_list.append(self.background_sprite)
        map_name = "map_files/dungeon.tmx"
        self.tile_map = arcade.load_tilemap(map_name, scaling=1.0)

        self.player_sprite = None
        self.physics_engine = None
        self.camera_sprites = arcade.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.camera_sprites.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.collision_list = self.tile_map.sprite_lists["collision"]
        self.player_sprite = arcade.Sprite(
            "sprites/player_idle.PNG",
            scale=1.0,
        )
        self.player_sprite.center_x = CELL_SIZE * 1 + (CELL_SIZE / 2)
        self.player_sprite.center_y = CELL_SIZE * 2 + (CELL_SIZE / 2)
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.collision_list)
        self.physics_engine.disable_multi_jump()
        self.background_color = arcade.color.BLUE_YONDER

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.camera_shake.update_camera()
        self.camera_sprites.use()
        self.wall_list.draw()
        self.player_list.draw()

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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.camera_shake.update(delta_time)
        self.scroll_to_player()



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