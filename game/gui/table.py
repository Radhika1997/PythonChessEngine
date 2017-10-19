import kivy
from game.board import Board
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
Window.size = (800, 600)
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import NumericProperty


class TilePanel(Button):
    ratio = NumericProperty(1 / 1)
    default_path = "game/images/pieces/"

    def __init__(self, **kwargs):
        super(TilePanel, self).__init__(**kwargs)
        self.size = ['10dp', '10dp']
        self.background_normal = ""

    def set_color(self, red, green, blue, alpha):
        self.background_color = [red, green, blue, alpha]

    def set_id(self, index):
        self.id = str(index)
        # self.text = str(index)

    def set_image(self, path):
        self.add_widget(Image(source=self.default_path + path))

    def get_color(self):
        return self.background_color

    def apply_ratio(self):
        for child in self.children:

            child.x = self.x
            child.y = self.y
            print
            child.size_hint = 0.5, 0.5
            child.pos_hint = {"center_x": .5, "center_y": .5}
            w, h = self.size
            h -= 40
            h2 = w * self.ratio
            if h2 > self.height:
                w = h / self.ratio
            else:
                h = h2
            child.size = w, h


class GameLayout(GridLayout):
    ratio = NumericProperty(1 / 1)
    board = None

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.cols = 8
        self.rows = 8
        self.id = 'gl'
        tile_panels = list()
        self.board = Board(0)

        for i in range(0,64):
            tile_panels.append(TilePanel())
            tile_panels[i].set_id(i)
            if i<8:
                if i%2 == 0:
                    tile_panels[i].set_color(0.466, 0.345, 0.156, 1)
                else:
                    tile_panels[i].set_color(0.976, 0.749, 0.407, 1)
            else:
                if tile_panels[i-8].get_color() == [0.466, 0.345, 0.156, 1]:
                    tile_panels[i].set_color(0.976, 0.749, 0.407, 1)
                else:
                    tile_panels[i].set_color(0.466, 0.345, 0.156, 1)

            if self.board.get_tile(i).is_tile_occupied():
                path = self.board.get_tile(i).get_pieces().set_path(
                    self.board.get_tile(i).get_pieces().get_piece_alliance(),
                    self.board.get_tile(i).get_pieces().get_piece_type())
                tile_panels[i].set_image(path)

        for tile_panel in tile_panels:
            self.add_widget(tile_panel)

    def apply_ratio(self):
        for child in self.children:
            child.apply_ratio()


class MainScreen(Screen):
    pass


class GameScreen(Screen):
    ratio = NumericProperty(1 / 1)

    def __init__(self, **kw):
        super(GameScreen, self).__init__(**kw)
        self.name = 'game'
        Clock.schedule_interval(self.my_callback, 3)

    def apply_ratio(self, child):
        child.size_hint = None, None
        child.pos_hint = {"center_x": .5, "center_y": .5}
        w, h = self.size
        h2 = w * self.ratio
        if h2 > self.height:
            w = h / self.ratio
        else:
            h = h2
        child.size = w, h
        child.apply_ratio()

    def my_callback(self,dt):
        for childs in self.children:
            for child in childs.children:
                if child.id == 'gl':
                    self.apply_ratio(child)


class ScreenManagement(ScreenManager):
    pass


class Table(App):

    def btn_exit(self):
        exit(0)

