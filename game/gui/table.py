import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.actionbar import ActionBar
from kivy.core.window import Window
Window.size = (800, 600)
from kivy.uix.widget import Widget


class Action(ActionBar):
    pass


class Table(App):

    def build(self):
        return Action()

    def btn_exit(self):
        exit(0)

