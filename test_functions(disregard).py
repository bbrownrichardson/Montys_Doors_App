from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import random


def door_assignment():
    doors = ['door-money.png', 'door-goat.png', 'door-trash.png']

    door1_reveal = random.choice(doors)
    doors.remove(door1_reveal)
    door2_reveal = random.choice(doors)
    doors.remove(door2_reveal)
    door3_reveal = random.choice(doors)
    doors.remove(door3_reveal)

    doors = ['door-money.png', 'door-goat.png', 'door-trash.png']

    return door1_reveal, door2_reveal, door3_reveal
# print door_assignment()


def popups(self, results, message, button_next, up_next):
    content = BoxLayout(orientation='vertical')
    message_label = Label(text=message)
    button_layer = BoxLayout(orientation='horizontal')
    dismiss_button = Button(text='QUIT', size_hint=(1, 1))
    next_button = Button(text=button_next, size_hint=(1, 1))
    button_layer.add_widget(dismiss_button)
    button_layer.add_widget(next_button)
    content.add_widget(message_label)
    content.add_widget(button_layer)
    popup = Popup(title=results, content=content, size_hint=(0.3,
                                                             0.25))
    dismiss_button.bind(on_release=(lambda a: self.exit_game()), on_press=
    popup.dismiss)
    next_button.bind(on_release=(lambda a: up_next), on_press=
    popup.dismiss)
    popup.open()

                win = getattr(GameScreen, 'winner')
                message = getattr(GameScreen, 'win_message')
                button_nxt = 'NEXT ROUND'
                next_screen = self.next_round()
                self.popups(win, message, button_nxt, next_screen)

    def make_selection(num):
        other_doors = None
        if str(num) is 1:
            other_doors = [2, 3]
        elif str(num) is 2:
            other_doors = [1, 3]
        elif str(num) is 3:
            other_doors = [1, 2]

        reveal = str(random.choice(other_doors))

        temp_other_doors = other_doors
        second_door = random.choice(other_doors)
        other_doors.remove(second_door)
        third_door = random.choice(other_doors)
        other_doors.remove(third_door)
        other_doors = temp_other_doors

        main_door = getattr(GameScreen, 'door' + num + '_counter')
        door_second = getattr(GameScreen, 'door' + second_door + '_counter')
        door_third = getattr(GameScreen, 'door' + third_door + '_counter')
        main_door_reveal = getattr(GameScreen, 'door'+num+'_reveal')

        if (main_door is 0 and door_second is 0
                and door_third is 0):
            self.ids['door'+reveal].source = \
                getattr(GameScreen, 'door'+reveal+'_reveal')
            self.ids['button'+reveal].disabled = True
            inc = getattr(GameScreen, 'door' + num + '_counter')
            setattr(GameScreen, 'door' + num + '_counter', inc + 1)
        elif(main_door is 1 and door_second is 0
             and door_third is 0):
            for i in range(1,4,1):
                self.ids['door'+ str(i)].source = \
                    getattr(GameScreen, 'door' + str(i) + '_reveal')
                self.ids['button'+str(i)].disabled = True
            if main_door_reveal in ['door-money.png']:
                self.win_popup()
            else:
                self.lose_popup()
        elif(main_door is 0 and (door_second is 1
            or door_third is 1)):
            for i in range(1,4,1):
                self.ids['door'+ str(i)].source = \
                    getattr(GameScreen, 'door' + str(i) + '_reveal')
                self.ids['button'+str(i)].disabled = True
            if main_door_reveal in ['door-money.png']:
                self.win_popup()
            else:
                self.lose_popup()