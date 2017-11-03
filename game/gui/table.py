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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from game.engine.minimax import MiniMax
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty

Window.size = (800, 600)

# TODO game over issues
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
flipped = False
alliance = Alliance.WHITE


def redraw():
    for i in range(0, 64):
        tile_panels[i].clear_widgets()
    draw_board(1)


def draw_board(val):
    normal = [56, 57, 58, 59, 60, 61, 62, 63,
              48, 49, 50, 51, 52, 53, 54, 55,
              40, 41, 42, 43, 44, 45, 46, 47,
              32, 33, 34, 35, 36, 37, 38, 39,
              24, 25, 26, 27, 28, 29, 30, 31,
              16, 17, 18, 19, 20, 21, 22, 23,
              8, 9, 10, 11, 12, 13, 14, 15,
              0, 1, 2, 3, 4, 5, 6, 7]
    flip = [0, 1, 2, 3, 4, 5, 6, 7,
            8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 21, 22, 23,
            24, 25, 26, 27, 28, 29, 30, 31,
            32, 33, 34, 35, 36, 37, 38, 39,
            40, 41, 42, 43, 44, 45, 46, 47,
            48, 49, 50, 51, 52, 53, 54, 55,
            56, 57, 58, 59, 60, 61, 62, 63]
    global flipped
    for i in range(0, 64):
        if not flipped:
            tile_panels[i].set_id(normal[i])
            dark = (0.466, 0.345, 0.156, 1)
            light = (0.976, 0.749, 0.407, 1)
            if val == 0:
                if i < 8:
                    if i % 2 == 0:
                        tile_panels[i].set_color(light[0], light[1], light[2], light[3])
                    else:
                        tile_panels[i].set_color(dark[0], dark[1], dark[2], dark[3])
                else:
                    if tile_panels[i - 8].get_color() == [light[0], light[1], light[2], light[3]]:
                        tile_panels[i].set_color(dark[0], dark[1], dark[2], dark[3])
                    else:
                        tile_panels[i].set_color(light[0], light[1], light[2], light[3])

            if board.get_tile(i).is_tile_occupied():
                path = board.get_tile(i).get_pieces().set_path(
                    board.get_tile(i).get_pieces().get_piece_alliance(),
                    board.get_tile(i).get_pieces().get_piece_type())
                tile_panels[normal[i]].set_image(path)
        else:
            tile_panels[i].set_id(flip[i])
            dark = (0.466, 0.345, 0.156, 1)
            light = (0.976, 0.749, 0.407, 1)
            if val == 0:
                if i < 8:
                    if i % 2 == 0:
                        tile_panels[i].set_color(dark[0], dark[1], dark[2], dark[3])
                    else:
                        tile_panels[i].set_color(light[0], light[1], light[2], light[3])
                else:
                    if tile_panels[i - 8].get_color() == [dark[0], dark[1], dark[2], dark[3]]:
                        tile_panels[i].set_color(light[0], light[1], light[2], light[3])
                    else:
                        tile_panels[i].set_color(dark[0], dark[1], dark[2], dark[3])

            if board.get_tile(i).is_tile_occupied():
                path = board.get_tile(i).get_pieces().set_path(
                    board.get_tile(i).get_pieces().get_piece_alliance(),
                    board.get_tile(i).get_pieces().get_piece_type())
                tile_panels[flip[i]].set_image(path)


# TODO apply threading to calculate in background and notify in foreground only when calculation is done
# noinspection PyPep8Naming
def AIvsAI(turn):
    while (not board.get_current_player().is_checkmate() and
           not board.get_current_player().is_stalemate()):
        if turn == 0:
            white()
            turn = 1
            print 'White AI lost'
        else:
            black()
            turn = 0
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


def restart():
    global board, tile_panels
    board = Board(0)
    for i in range(0, 64):
        tile_panels[i].clear_widgets()
    draw_board(0)


def exit_button(argument):
    exit(0)


def dialog_box(title, message):
    content = BoxLayout(orientation='vertical')
    content.add_widget(Label(text=message))
    content.add_widget(Label(text=''))
    btn1 = Button(text='Home', size=(40, 40))
    btn2 = Button(text='Exit', size=(40, 40))
    layout = BoxLayout()
    layout.add_widget(btn1)
    layout.add_widget(btn2)
    content.add_widget(layout)
    popup = Popup(title=title, content=content,
                  auto_dismiss=False, size=(100, 40))
    btn1.bind(on_release=popup.dismiss)
    btn2.bind(on_release=exit_button)
    popup.open()


class Notify:
    def __init__(self):
        pass

    # TODO adding dialog box and create thread
    @staticmethod
    def update():
        global board
        if not board.get_current_player().is_checkmate() and \
                not board.get_current_player().is_stalemate():
            minimax = MiniMax(2)
            best_move = minimax.execute(board)
            transition = board.get_current_player().make_move(best_move)
            new_board = transition.get_transition_board()
            move_log.add_move(best_move)
            player = new_board.get_current_player()
            print new_board.get_tile(best_move.get_destination_coordinate()). \
                get_pieces().get_chess_coordinate(best_move.string()) + \
                player.get_player_checks()
            if player.get_player_checks() == "#":
                dialog_box('Game Over!', 'You are in Checkmate')
            return new_board
        else:
            dialog_box('Game Over!', 'AI is in Checkmate')
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


class BoardLog:
    board_log = list()
    length = None
    current = None

    def __init__(self):
        self.current = -1
        self.length = 0

    def add(self, new_board):
        if self.current == self.length - 1:
            self.board_log.append(new_board)
            self.current += 1
            self.length += 1
        else:
            for i in range(self.current + 1, self.length):
                self.remove()
            self.board_log.append(new_board)
            self.current += 1
            self.length = self.current + 1

    def remove(self):
        del self.board_log[-1]

    def undo(self):
        self.current -= 1
        global board
        if self.current < 0:
            self.current = -1
        else:
            board = self.board_log[self.current]
            redraw()

    def redo(self):
        self.current += 1
        global board
        if self.current < self.length:
            board = self.board_log[self.current]
            redraw()
        else:
            self.current = self.length - 1


board_log = BoardLog()


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
                    for i in range(64):
                        if int(tile_panels[i].id) == destination_tile.get_tile_coordinate():
                            tile_panels[i].set_color(destination_color[0],
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
                            global move_log, board_log
                            move_log.add_move(move)
                            board_log.add(board)
                            player = board.get_current_player()
                            print board.get_tile(destination_coordinate).get_pieces(). \
                                get_chess_coordinate(move.string()) + \
                                player.get_player_checks()
                            if alliance == Alliance.WHITE:
                                alliance = Alliance.BLACK
                                if player.get_player_checks() == "#":
                                    dialog_box('Game Over!', 'Black Player is in Checkmate')
                            else:
                                alliance = Alliance.WHITE
                                if player.get_player_checks() == "#":
                                    dialog_box('Game Over!', 'White Player is in Checkmate')
                    else:
                        self.set_color(0.686, 0.109, 0.109, 1)

                else:
                    self.set_color(0.686, 0.109, 0.109, 1)
                for i in range(64):
                    if int(tile_panels[i].id) == source_tile.get_tile_coordinate():
                        tile_panels[i].set_color(source_color[0],
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
                    for i in range(64):
                        if int(tile_panels[i].id) == destination_tile.get_tile_coordinate():
                            tile_panels[i].set_color(destination_color[0],
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
                            global move_log, board_log
                            move_log.add_move(move)
                            player = board.get_current_player()
                            print board.get_tile(destination_coordinate).get_pieces(). \
                                get_chess_coordinate(move.string()) + \
                                player.get_player_checks()
                            global blackAI
                            ai_board = blackAI.update()
                            board = ai_board
                            redraw()
                            board_log.add(board)
                    else:
                        self.set_color(0.686, 0.109, 0.109, 1)

                else:
                    self.set_color(0.686, 0.109, 0.109, 1)
                for i in range(64):
                    if int(tile_panels[i].id) == source_tile.get_tile_coordinate():
                        tile_panels[i].set_color(source_color[0],
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
                    for i in range(64):
                        if int(tile_panels[i].id) == destination_tile.get_tile_coordinate():
                            tile_panels[i].set_color(destination_color[0],
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
                            global move_log, board_log
                            move_log.add_move(move)
                            player = board.get_current_player()
                            print board.get_tile(destination_coordinate).get_pieces(). \
                                get_chess_coordinate(move.string()) + \
                                player.get_player_checks()
                            global whiteAI
                            ai_board = whiteAI.update()
                            board = ai_board
                            redraw()
                            board_log.add(board)

                    else:
                        self.set_color(0.686, 0.109, 0.109, 1)
                else:
                    self.set_color(0.686, 0.109, 0.109, 1)
                for i in range(64):
                    if int(tile_panels[i].id) == source_tile.get_tile_coordinate():
                        tile_panels[i].set_color(source_color[0],
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

        for i in range(0, 64):
            tile_panels.append(TilePanel())
        draw_board(0)
        for tile_panel in tile_panels:
            self.add_widget(tile_panel)

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
        global mode, blackAI, whiteAI, board, board_log
        mode = self.mode
        # restart()
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
            # Clock.schedule_interval(self.AIcallback, 3)
        board_log.add(board)
        self.parent.change_screen()

    # noinspection PyPep8Naming
    @staticmethod
    def AIcallback(dt):
        white()


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

    def my_callback(self, dt):
        for child in self.children:
            for every_child in child.children:
                if every_child.id == 'gl':
                    self.apply_ratio(every_child)


class ScreenManagement(ScreenManager):
    pass


class Table(App):

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.title = "PCE"

    @staticmethod
    def btn_exit():
        exit(0)

    @staticmethod
    def restart():
        global board, board_log
        print 'Game restarts'
        board = Board(0)
        board_log = BoardLog()
        redraw()

    @staticmethod
    def undo():
        global board_log, mode, alliance
        board_log.undo()
        if mode == 0:
            if alliance == Alliance.WHITE:
                alliance = Alliance.BLACK
            else:
                alliance = Alliance.WHITE

    @staticmethod
    def redo():
        global board_log, mode, alliance
        board_log.redo()
        if mode == 0:
            if alliance == Alliance.WHITE:
                alliance = Alliance.BLACK
            else:
                alliance = Alliance.WHITE

    @staticmethod
    def flip():
        global flipped
        if flipped is True:
            flipped = False
        else:
            flipped = True
        restart()
