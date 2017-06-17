from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import FallOutTransition
from screens import MainMenu, GameScreen


kv = Builder.load_file('MontyFrontend.kv')
LabelBase.register(name='Aller', fn_regular='Aller_Rg.ttf')


class ScreenApp(App):

    def build(self):
        self.manager = ScreenManager(transition=FallOutTransition())
        self.manager.add_widget(MainMenu(name='MainMenu'))
        self.manager.add_widget(GameScreen(name='GameScreen'))

        return self.manager


if __name__ == '__main__':
    ScreenApp().run()
