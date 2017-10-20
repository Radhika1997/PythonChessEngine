import kivy
from game.board import Board
from game.move import MoveCreator
from game.move_status import Status
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
Window.size = (800, 600)
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import NumericProperty

source_tile = -1
board = Board(0)
destination_tile = -1
human_moved_piece = None
source_color = None
destination_color = None


class TilePanel(Button):
    ratio = NumericProperty(1 / 1)
    default_path = "game/images/pieces/"
    path = ""

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

    # TODO work on on_press method for better interaction

    def on_release(self):
        global source_tile, destination_tile, human_moved_piece, source_color, destination_color
        if source_tile == -1:
            source_tile = self.parent.board.get_tile(int(self.id))
            human_moved_piece = source_tile.get_pieces()
            if human_moved_piece is None:
                source_tile = -1
            else:
                source_color = self.background_color
                self.set_color(0.074, 0.467, 0.156, 1)

            if destination_color is not None:
                self.parent.tile_panels[destination_tile.get_tile_coordinate()].set_color(destination_color[0],
                                                                                          destination_color[1],
                                                                                          destination_color[2],
                                                                                          destination_color[3])
                destination_color = None
                destination_tile = None

        else:
            destination_tile = self.parent.board.get_tile(int(self.id))
            destination_coordinate = destination_tile.get_tile_coordinate()
            destination_color = self.get_color()
            move = MoveCreator().create_move(self.parent.board,
                                             source_tile.get_tile_coordinate(),
                                             destination_coordinate)
            transition = self.parent.board.get_current_player().make_move(move)
            if transition.get_move_status() == Status.DONE:
                self.parent.board = transition.get_transition_board()
                if not self.parent.board.get_tile(source_tile.get_tile_coordinate()).is_tile_occupied():
                    path = self.parent.board.get_tile(destination_coordinate).get_pieces().set_path(
                        self.parent.board.get_tile(destination_coordinate).get_pieces().get_piece_alliance(),
                        self.parent.board.get_tile(destination_coordinate).get_pieces().get_piece_type())
                    self.set_image(path)
                    self.parent.tile_panels[source_tile.get_tile_coordinate()].clear_widgets()

            else:
                self.set_color(0.686, 0.109, 0.109, 1)
            self.parent.tile_panels[source_tile.get_tile_coordinate()].set_color(source_color[0],
                                                                                 source_color[1],
                                                                                 source_color[2],
                                                                                 source_color[3])
            source_tile = -1
            human_moved_piece = None
            source_color = None


class GameLayout(GridLayout):
    ratio = NumericProperty(1 / 1)
    board = None
    tile_panels = list()

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.cols = 8
        self.rows = 8
        self.id = 'gl'
        global board
        self.board = board

        for i in range(0,64):
            self.tile_panels.append(TilePanel())
            self.tile_panels[i].set_id(i)
            if i<8:
                if i%2 == 0:
                    self.tile_panels[i].set_color(0.466, 0.345, 0.156, 1)
                else:
                    self.tile_panels[i].set_color(0.976, 0.749, 0.407, 1)
            else:
                if self.tile_panels[i-8].get_color() == [0.466, 0.345, 0.156, 1]:
                    self.tile_panels[i].set_color(0.976, 0.749, 0.407, 1)
                else:
                    self.tile_panels[i].set_color(0.466, 0.345, 0.156, 1)

            if self.board.get_tile(i).is_tile_occupied():
                path = self.board.get_tile(i).get_pieces().set_path(
                    self.board.get_tile(i).get_pieces().get_piece_alliance(),
                    self.board.get_tile(i).get_pieces().get_piece_type())
                self.tile_panels[i].set_image(path)

        for tile_panel in self.tile_panels:
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
        Clock.schedule_interval(self.my_callback, 0.01)

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
        for child in self.children:
            for every_child in child.children:
                if every_child.id == 'gl':
                    self.apply_ratio(every_child)


class ScreenManagement(ScreenManager):
    pass


class Table(App):

    def btn_exit(self):
        exit(0)

