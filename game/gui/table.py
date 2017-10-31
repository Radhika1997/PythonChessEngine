from alliance import Alliance
from game.board import Board
from game.move import MoveCreator
from game.move_status import Status
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from game.engine.minimax import MiniMax
Window.size = (800, 600)
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import NumericProperty

# TODO undo, restart, alliance issues, game over issues, flip board
source_tile = None
board = Board(0)
destination_tile = None
human_moved_piece = None
source_color = None
destination_color = None
mode = 0
whiteAI = None
blackAI = None
tile_panels = list()
alliance = Alliance.WHITE


def redraw():
    for i in range(0, 64):
        tile_panels[i].clear_widgets()
        if board.get_tile(i).is_tile_occupied():
            path = board.get_tile(i).get_pieces().set_path(
                board.get_tile(i).get_pieces().get_piece_alliance(),
                board.get_tile(i).get_pieces().get_piece_type())
            tile_panels[i].set_image(path)


def AIvsAI(turn):
    if turn == 0:
        if white():
            AIvsAI(1)
        print 'White AI lost'
    else:
        if black():
            AIvsAI(0)
        print 'Black AI lost'


def white():
    global board, whiteAI
    new_board = whiteAI.update()
    if board == new_board:
        return False
    else:
        board = new_board
        redraw()
        return True


def black():
    global board, blackAI
    new_board = blackAI.update()
    if board == new_board:
        return False
    else:
        board = new_board
        redraw()
        return True


class Notify:

    def __init__(self):
        pass

    # TODO adding dialog box and create thread
    def update(self):
        global board
        if not board.get_current_player().is_checkmate() and \
           not board.get_current_player().is_stalemate():
            minimax = MiniMax(2)
            best_move = minimax.execute(board)
            transition = board.get_current_player().make_move(best_move)
            new_board = transition.get_transition_board()
            move_log.add_move(best_move)
            player = new_board.get_current_player()
            print new_board.get_tile(best_move.get_destination_coordinate()).get_pieces().get_chess_coordinate(best_move.string()) + \
                player.get_player_checks()
            return new_board
        else:
            print 'Game ends'
            return board


class MoveLog:

    moves = list()

    def __init__(self):
        pass

    def add_move(self, move):
        self.moves.append(move)

    def size(self):
        return len(self.moves)

    def clear(self):
        self.moves = list()

    def remove_move(self, val):
        if val is int():
            del self.moves[val]
        else:
            for move in self.moves:
                if val.equals(move):
                    self.moves.remove(val.equals(move))
                    break


move_log = MoveLog()


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
        global source_tile, destination_tile, human_moved_piece, source_color, \
            destination_color, mode, board, tile_panels, alliance
        if mode == 0:
            if source_tile is None:
                source_tile = board.get_tile(int(self.id))
                human_moved_piece = source_tile.get_pieces()
                if human_moved_piece is None:
                    source_tile = None
                else:
                    source_color = self.background_color
                    self.set_color(0.074, 0.467, 0.156, 1)

                if destination_color is not None:
                    tile_panels[destination_tile.get_tile_coordinate()].set_color(destination_color[0],
                                                                                  destination_color[1],
                                                                                  destination_color[2],
                                                                                  destination_color[3])
                    destination_color = None
                    destination_tile = None

            else:
                destination_tile = board.get_tile(int(self.id))
                destination_coordinate = destination_tile.get_tile_coordinate()
                destination_color = self.get_color()
                if alliance == human_moved_piece.get_piece_alliance():
                    move = MoveCreator().create_move(board,
                                                     source_tile.get_tile_coordinate(),
                                                     destination_coordinate)
                    transition = board.get_current_player().make_move(move)
                    # print transition.get_move_status()
                    if transition.get_move_status() == Status.DONE:
                        board = transition.get_transition_board()
                        if not board.get_tile(source_tile.get_tile_coordinate()).is_tile_occupied():
                            redraw()
                            global move_log
                            move_log.add_move(move)
                            player = board.get_current_player()
                            print board.get_tile(destination_coordinate).get_pieces().get_chess_coordinate(move.string()) + \
                                player.get_player_checks()
                            if alliance == Alliance.WHITE:
                                alliance = Alliance.BLACK
                            else:
                                alliance = Alliance.WHITE
                    else:
                        self.set_color(0.686, 0.109, 0.109, 1)

                else:
                    self.set_color(0.686, 0.109, 0.109, 1)
                tile_panels[source_tile.get_tile_coordinate()].set_color(source_color[0],
                                                                         source_color[1],
                                                                         source_color[2],
                                                                         source_color[3])
                source_tile = None
                human_moved_piece = None
                source_color = None

        elif mode == 1:
            if source_tile is None:
                source_tile = board.get_tile(int(self.id))
                human_moved_piece = source_tile.get_pieces()
                if human_moved_piece is None:
                    source_tile = None
                else:
                    source_color = self.background_color
                    self.set_color(0.074, 0.467, 0.156, 1)

                if destination_color is not None:
                    tile_panels[destination_tile.get_tile_coordinate()].set_color(destination_color[0],
                                                                                  destination_color[1],
                                                                                  destination_color[2],
                                                                                  destination_color[3])
                    destination_color = None
                    destination_tile = None

            else:
                destination_tile = board.get_tile(int(self.id))
                destination_coordinate = destination_tile.get_tile_coordinate()
                destination_color = self.get_color()
                if alliance == human_moved_piece.get_piece_alliance():
                    move = MoveCreator().create_move(board,
                                                     source_tile.get_tile_coordinate(),
                                                     destination_coordinate)
                    transition = board.get_current_player().make_move(move)
                    # print transition.get_move_status()
                    if transition.get_move_status() == Status.DONE:
                        board = transition.get_transition_board()
                        if not board.get_tile(source_tile.get_tile_coordinate()).is_tile_occupied():
                            redraw()
                            global move_log
                            move_log.add_move(move)
                            player = board.get_current_player()
                            print board.get_tile(destination_coordinate).get_pieces().get_chess_coordinate(move.string()) + \
                                player.get_player_checks()
                            global blackAI
                            ai_board = blackAI.update()
                            board = ai_board
                            redraw()
                    else:
                        self.set_color(0.686, 0.109, 0.109, 1)

                else:
                    self.set_color(0.686, 0.109, 0.109, 1)
                tile_panels[source_tile.get_tile_coordinate()].set_color(source_color[0],
                                                                         source_color[1],
                                                                         source_color[2],
                                                                         source_color[3])
                source_tile = None
                human_moved_piece = None
                source_color = None

        elif mode == 2:
            if source_tile is None:
                source_tile = board.get_tile(int(self.id))
                human_moved_piece = source_tile.get_pieces()
                if human_moved_piece is None:
                    source_tile = None
                else:
                    source_color = self.background_color
                    self.set_color(0.074, 0.467, 0.156, 1)

                if destination_color is not None:
                    tile_panels[destination_tile.get_tile_coordinate()].set_color(destination_color[0],
                                                                                  destination_color[1],
                                                                                  destination_color[2],
                                                                                  destination_color[3])
                    destination_color = None
                    destination_tile = None

            else:
                destination_tile = board.get_tile(int(self.id))
                destination_coordinate = destination_tile.get_tile_coordinate()
                destination_color = self.get_color()
                if alliance == human_moved_piece.get_piece_alliance():
                    move = MoveCreator().create_move(board,
                                                     source_tile.get_tile_coordinate(),
                                                     destination_coordinate)
                    transition = board.get_current_player().make_move(move)
                    # print transition.get_move_status()
                    if transition.get_move_status() == Status.DONE:
                        board = transition.get_transition_board()
                        if not board.get_tile(source_tile.get_tile_coordinate()).is_tile_occupied():
                            redraw()
                            global move_log
                            move_log.add_move(move)
                            player = board.get_current_player()
                            print board.get_tile(destination_coordinate).get_pieces().get_chess_coordinate(move.string()) + \
                                player.get_player_checks()
                            global whiteAI
                            ai_board = whiteAI.update()
                            board = ai_board
                            redraw()

                    else:
                        self.set_color(0.686, 0.109, 0.109, 1)
                else:
                    self.set_color(0.686, 0.109, 0.109, 1)
                tile_panels[source_tile.get_tile_coordinate()].set_color(source_color[0],
                                                                         source_color[1],
                                                                         source_color[2],
                                                                         source_color[3])
                source_tile = None
                human_moved_piece = None
                source_color = None
        else:
            AIvsAI(0)


class GameLayout(GridLayout):
    ratio = NumericProperty(1 / 1)
    board = None
    tile_panels = list()

    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.cols = 8
        self.rows = 8
        self.id = 'gl'
        global board, tile_panels
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
        tile_panels = self.tile_panels

    def apply_ratio(self):
        for child in self.children:
            child.apply_ratio()


class MainScreenButton(Button):

    mode = 0

    def __init__(self, **kwargs):
        super(MainScreenButton, self).__init__(**kwargs)
        self.size = ['150dp', '48dp']
        self.text = kwargs['text']
        self.mode = kwargs['mode']

    def on_release(self):
        global mode, blackAI, whiteAI, board
        mode = self.mode
        if mode == 0:
            blackAI = None
            whiteAI = None
        elif mode == 1:
            blackAI = Notify()
            whiteAI = None
        elif mode == 2:
            global alliance
            alliance = Alliance.BLACK
            blackAI = None
            whiteAI = Notify()
            ai_board = whiteAI.update()
            board = ai_board
            redraw()
        else:
            whiteAI = Notify()
            blackAI = Notify()

        self.parent.change_screen()


class MainScreenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreenLayout, self).__init__(**kwargs)
        self.id = 'ms'
        self.orientation = 'vertical'
        btn1 = MainScreenButton(text='Start Player vs Player', mode=0)
        btn2 = MainScreenButton(text='Start White Player vs AI', mode=1)
        btn3 = MainScreenButton(text='Start AI vs Black Player', mode=2)
        btn4 = MainScreenButton(text='Start AI vs AI', mode=3)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(btn3)
        self.add_widget(btn4)

    def change_screen(self):
        self.parent.change_screen()


class MainScreen(Screen):

    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)
        self.name = 'start'
        main = MainScreenLayout()
        self.add_widget(main)

    def change_screen(self):
        self.parent.current = 'game'


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
