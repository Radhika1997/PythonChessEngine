import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
Window.size = (800, 600)
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import NumericProperty


class TilePanel(Button):

    def __init__(self, **kwargs):
        super(TilePanel, self).__init__(**kwargs)
        self.size = ['10dp', '10dp']
        self.background_normal = ""

    def set_color(self, red, green, blue, alpha):
        self.background_color = [red, green, blue, alpha]

    def set_id(self, index):
        self.id = str(index)
        self.text = str(index)

    def get_color(self):
        return self.background_color


class GameLayout(GridLayout):

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.cols = 8
        self.rows = 8
        tile_panels = list()

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

        for tile_panel in tile_panels:
            self.add_widget(tile_panel)


class MainScreen(Screen):
    pass


class GameScreen(Screen):
    ratio = NumericProperty(1 / 1)

    def __init__(self, **kw):
        super(GameScreen, self).__init__(**kw)
        self.name = 'game'

    def apply_ratio(self, child):
        child.size_hint = None, None
        child.pos_hint = {"center_x": .5, "center_y": .5}
        w, h = self.size
        h -= 40
        h2 = w * self.ratio
        if h2 > self.height:
            w = h / self.ratio
        else:
            h = h2
        child.size = w, h


class ScreenManagement(ScreenManager):
    pass


class Table(App):

    def btn_exit(self):
        exit(0)

