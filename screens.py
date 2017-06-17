from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import random


class MainMenu(Screen):

    @staticmethod
    def door_assignment():
        """
        Allow items to be randomly assigned to a specific door
        """
        doors = ['door-money.png', 'door-goat.png', 'door-trash.png']

        GameScreen.door1_reveal = random.choice(doors)
        doors.remove(GameScreen.door1_reveal)
        GameScreen.door2_reveal = random.choice(doors)
        doors.remove(GameScreen.door2_reveal)
        GameScreen.door3_reveal = random.choice(doors)
        doors.remove(GameScreen.door3_reveal)


class Settings(Screen):
    pass


class InstructionsScreen(Screen):
    pass


class GameScreen(Screen):
    door1_counter = 0
    door2_counter = 0
    door3_counter = 0

    door1_reveal = None
    door2_reveal = None
    door3_reveal = None

    score = 0
    winner = 'WINNER'
    win_message = 'CONGRATS YOU HAVE WON!!!'
    loser = 'SORRY'
    loss_message = 'BETTER LUCK NEXT TIME!!!'

    def make_selection(self, num):
        """
        Reveal items behind doors based off of selection
        :param num: indicate which door is being selected
        """
        other_doors = None
        if num is 1:
            other_doors = [str(2), str(3)]
        elif num is 2:
            other_doors = [str(1), str(3)]
        elif num is 3:
            other_doors = [str(1), str(2)]

        reveal = str(random.choice(other_doors))
        other_doors.remove(reveal)
        third_door = random.choice(other_doors)
        other_doors.remove(third_door)

        main_door = getattr(self, 'door' + str(num) + '_counter')
        door_second = getattr(self, 'door' + reveal + '_counter')
        door_third = getattr(self, 'door' + third_door + '_counter')
        main_door_reveal = getattr(self, 'door'+str(num)+'_reveal')

        if (main_door is 0 and door_second is 0
                and door_third is 0):
            self.ids['door'+reveal].source = \
                getattr(self, 'door'+reveal+'_reveal')
            self.ids['button'+reveal].disabled = True
            inc = getattr(self, 'door' + str(num) + '_counter')
            setattr(self, 'door' + str(num) + '_counter', inc + 1)
        elif main_door is 1 and door_second is 0 and door_third is 0:
            for i in range(1, 4, 1):
                self.ids['door' + str(i)].source = \
                    getattr(self, 'door' + str(i) + '_reveal')
                self.ids['button'+str(i)].disabled = True
            if main_door_reveal in ['door-money.png']:
                self.win_popup()
            else:
                self.lose_popup()
        elif main_door is 0 and (door_second is 1 or door_third is 1):
            for i in range(1, 4, 1):
                self.ids['door' + str(i)].source = \
                    getattr(self, 'door' + str(i) + '_reveal')
                self.ids['button'+str(i)].disabled = True
            if main_door_reveal in ['door-money.png']:
                self.win_popup()
            else:
                self.lose_popup()

    def win(self):
        """
        Increase the total score when user selects doors with "best" item
        """
        self.score += 1
        self.ids['score'].text = 'SCORE: ' + str(self.score)

    def exit_game(self):
        """
        Exit game to main menu, reset doors and its counter, re-enable
        buttons, and set score back to 0 (frontend and backend)
        """
        for i in range(1, 4, 1):
            self.ids['door' + str(i)].source = \
                'door_closed.jpg'
            self.ids['button' + str(i)].disabled = False
            setattr(self, 'door'+str(i)+'_counter', 0)
        self.manager.current = 'MainMenu'
        self.ids['score'].text = 'SCORE: 0'
        self.score = 0

    def next_round(self):
        """
        Have game continue to next round, reset doors and its counter,
        re-enable buttons, return to game-screen, and initate random door
        selection for new game round
        """
        for i in range(1, 4, 1):
            self.ids['door' + str(i)].source = \
                'door_closed.jpg'
            self.ids['button' + str(i)].disabled = False
            setattr(self, 'door'+str(i)+'_counter', 0)
        self.win()
        self.manager.current = 'GameScreen'
        MainMenu.door_assignment()

    def restart_game(self):
        """
        Have user restart game, reset doors and its counter,
        re-enable buttons, return to game-screen, and initate random door
        selection for new game
        """
        for i in range(1, 4, 1):
            self.ids['door' + str(i)].source = \
                'door_closed.jpg'
            self.ids['button' + str(i)].disabled = False
            setattr(self, 'door'+str(i)+'_counter', 0)
        self.ids['score'].text = 'SCORE: 0'
        self.score = 0
        MainMenu.door_assignment()

    def win_popup(self):
        """
        Function called on to initiate a winner popup when user wins round
        and contain two buttons that allows user to continue to next round
        or exit game to main menu
        """
        content = BoxLayout(orientation='vertical')
        message_label = Label(text=self.win_message)
        button_layer = BoxLayout(orientation='horizontal')
        dismiss_button = Button(text='QUIT', size_hint=(1, 1))
        next_button = Button(id='next', text='NEXT ROUND', size_hint=(1, 1))
        button_layer.add_widget(dismiss_button)
        button_layer.add_widget(next_button)
        content.add_widget(message_label)
        content.add_widget(button_layer)
        popup = Popup(title=self.winner,
                      content=content, size_hint=(0.3, 0.25))
        dismiss_button.bind(on_release=(lambda a: self.exit_game()),
                            on_press=popup.dismiss)
        next_button.bind(on_release=(lambda a: self.next_round()),
                         on_press=popup.dismiss)
        popup.open()

    def lose_popup(self):
        """
        Function called on to initiate a loss popup when user loses round
        and contain two buttons that allows user to continue to try again
        or to exit game to main menu
        """
        content = BoxLayout(orientation='vertical')
        message_label = Label(text=self.loss_message)
        button_layer = BoxLayout(orientation='horizontal')
        dismiss_button = Button(text='QUIT', size_hint=(1, 1))
        next_button = Button(id='try_again', text='TRY AGAIN', size_hint=(1,
                                                                          1))
        button_layer.add_widget(dismiss_button)
        button_layer.add_widget(next_button)
        content.add_widget(message_label)
        content.add_widget(button_layer)
        popup = Popup(title=self.loser, content=content,
                      size_hint=(0.3, 0.25))
        dismiss_button.bind(on_release=(lambda a: self.exit_game()),
                            on_press=popup.dismiss)
        next_button.bind(on_release=(lambda a: self.restart_game()),
                         on_press=popup.dismiss)
        popup.open()
