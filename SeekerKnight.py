import arcade

from pyglet.graphics import Batch
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
    UIView,
    UIBoxLayout,
    UILabel
)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
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
            self.window.show_view(GameView())

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

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)


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