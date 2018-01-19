#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.config import Config

kivy.require('1.10.0')
Config.set('graphics', 'fullscreen', 'auto')

PLAYERS = ('Lag 1', 'Lag 2', 'Lag 3')

# TODO: Add path for question image and answer image to JEOPARDY_DICT

JEOPARDY_DICT = {
    'Nyårskunskap': {
        10: {'title': 'Nyårscuisine',
             'question': 'God mat hör nyårsafton till.\n\nDet är inte alltid lätt att förstå orden som används i kokböcker och recept. Men vad heter det med ett finare ord när man sjuder någonting i vätska?',
             'answer_label': 'Pochera',
             'answer_text': 'Pochera kommer från franska ordet poche, som betyder ficka.'},
        20: {'title': 'Nyårstradition',
             'question': 'Nyårsafton är omgärdat av traditioner.\n\nEn tradition som sänds på SVT varje nyår vid klockslaget är när en svensk kändis läser upp dikten Nyårsklockan (Ring klocka, ring?)\nVar i Sverige utförs denna tradition?',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
        30: {'title': 'Nyårsdrink',
             'question': 'Question Nyår 30',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
        40: {'title': 'Nyårsväder',
             'question': 'Question Nyår 40',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
        50: {'title': 'Nyårskunskap',
             'question': 'Question Nyår 50',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
    },
    'Lek på allvar': {
        10: {'title': 'Lek på allvar',
             'question': 'Question Lek 10',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
        20: {'title': 'Lek på allvar',
             'question': 'Question Lek 20',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
        30: {'title': 'Lek på allvar',
             'question': 'Question Lek 30',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
        40: {'title': 'Lek på allvar',
             'question': 'Question Lek 40',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
        50: {'title': 'Lek på allvar',
             'question': 'Question Lek 50',
             'answer_label': 'LABEL',
             'answer_text': 'TEXT'},
    },
    '2017': {
        10: {'title': '2017',
             'question': 'Question 2017 10',
             'answer_label': 'Answer 2017 10',
             'answer_text': 'TEXT'},
        20: {'title': '2017',
             'question': 'Question 2017 20',
             'answer_label': 'Answer 2017 20',
             'answer_text': 'TEXT'},
        30: {'title': '2017',
             'question': 'Question 2017 30',
             'answer_label': 'Answer 2017 30',
             'answer_text': 'TEXT'},
        40: {'title': '2017',
             'question': 'Question 2017 40',
             'answer_label': 'Answer 2017 40',
             'answer_text': 'TEXT'},
        50: {'title': '2017',
             'question': 'Question 2017 50',
             'answer_label': 'Answer 2017 50',
             'answer_text': 'TEXT'}
    }}


class Player(object):

    def __init__(self, name=None, points=None):
        self.name = name
        self.points = points

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def set_name(self, name):
        self.name = name
        return self.name

    def set_points(self, points, operation):
        if operation == "+":
            self.points += points
        elif operation == "-":
            self.points -= points
        return self.points

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Player: {}, Points: {}>".format(self.name, self.points)


class BaseLayout(FloatLayout):
    pass


class WallpaperImage(Image):
    pass


class BoardScreen(Screen):
    point = NumericProperty()


class MainLayout(BoxLayout):
    pass


class ScoreLayout(BoxLayout):
    pass


class ScoreLabel(Label):
    pass


class PlayerLabel(Label):
    pass


class CategoryGrid(GridLayout):
    pass


class QALayout(AnchorLayout):
    pass


class QABox(BoxLayout):
    pass


class QAImage(Image):
    pass


class HeaderLayout(AnchorLayout):
    pass


class BackLayout(AnchorLayout):
    pass


class AnswerLayout(AnchorLayout):
    pass


class QuestionScreen(Screen):
    question_text = StringProperty()
    title = StringProperty()
    category = StringProperty()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

        self.name = '{category}-{point}-question'.format(
            category=self.category, point=self.point)
        self.app = App.get_running_app()


class QuestionLabel(Label):
    question_text = StringProperty()
    font_color = StringProperty()

    def __init__(self, **kwargs):
        super(QuestionLabel, self).__init__(**kwargs)
        self.font_color = '561f60'
        self.markup = True

    def on_size(self, *args):
        self.canvas.before.clear()
        boarder_size = 5
        with self.canvas.before:
            Color(0, 0, 0, 0.7)
            Rectangle(pos=(self.pos[0] - boarder_size,
                           self.pos[1] - boarder_size),
                      size=(self.size[0] + 2 * boarder_size,
                            self.size[1] + 2 * boarder_size))
            Color(1, 0.75, 0.29, 0.9)
            Rectangle(pos=self.pos, size=self.size)


class AnswerButton(ButtonBehavior, Image):

    def __init__(self, **kwargs):
        super(AnswerButton, self).__init__(**kwargs)
        self.source = 'media/answer.png'

    def on_press(self):
        current_screen = App.get_running_app().screen_manager.current
        answer_screen = '-'.join(current_screen.split('-')[:2]) + '-answer'
        App.get_running_app().screen_manager.current = answer_screen


class SetPointsButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(SetPointsButton, self).__init__(**kwargs)
        self.source = 'media/set_points.png'


class AnswerScreen(Screen):
    answer_label = StringProperty()
    answer_text = StringProperty()
    title = StringProperty()
    category = StringProperty()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super(AnswerScreen, self).__init__(**kwargs)

        self.name = '{category}-{point}-answer'.format(
            category=self.category, point=self.point)
        self.app = App.get_running_app()


class AnswerLabel(QuestionLabel):
    def __init__(self, **kwargs):
        super(AnswerLabel, self).__init__(**kwargs)


class BackButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BackButton, self).__init__(**kwargs)
        self.source = 'media/back.png'

    def on_press(self):
        App.get_running_app().screen_manager.current = 'board_screen'


class GridLabelButton(Button):
    font_color = StringProperty()
    category = StringProperty()

    def __init__(self, **kwargs):
        super(GridLabelButton, self).__init__(**kwargs)
        self.text = '[color={font_color}][b]{category}[/b][/color]'.format(
                    category=self.category, font_color=self.font_color)


class GridButton(Button):
    category = StringProperty()
    point = NumericProperty()
    font_color = StringProperty()
    pushed = BooleanProperty()

    def __init__(self, **kwargs):
        super(GridButton, self).__init__(**kwargs)
        self.text = '[color={font_color}][b]{point}[/b][/color]'.format(
                    point=self.point, font_color=self.font_color)
        self.pushed = False
        self.id = '{category}.{point}'.format(category=self.category, point=self.point)


class PlayersScoreLayout(BoxLayout):
    player = ObjectProperty()

    def __init__(self, **kwargs):
        super(PlayersScoreLayout, self).__init__(**kwargs)
        self.app = App.get_running_app()
        Clock.schedule_interval(self.update_points, 1)

    def update_points(self, dt):
        self.ids.score_label.text = str(self.player.get_points())


class AddPointsPopup(Popup):
    pass


class MainApp(App):
    POINTS = JEOPARDY_DICT[next(iter(JEOPARDY_DICT.keys()))].keys()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.players = list()
        self.screen_manager = ObjectProperty()
        self.add_points_popup = ObjectProperty()

    def go_to_question(self, instance):
        if not instance.pushed:
            instance.background_color = (1, 1, 1, 0.1)
            instance.pushed = True

        screen_name = instance.id.split(".")[0] + "-" + instance.id.split(".")[1] + "-question"

        self.screen_manager.current = screen_name

    def close_popup(self, instance):
        self.add_points_popup.dismiss()

    def build(self):
        self.screen_manager = self.root.ids.screen_manager
        self.screen_manager.transition = NoTransition()

        self.create_players()
        self.build_score_layout()
        self.build_category_grid()
        self.build_question_screens()
        self.build_answer_screens()
        self.build_add_points_popup()

    def create_players(self):
        for player in PLAYERS:
            self.players.append(Player(name=player, points=0))

    def build_score_layout(self):
        for player in self.players:
            self.root.ids.score_layout.add_widget(PlayersScoreLayout(player=player, id=player.get_name()))

    def build_category_grid(self):
        for category in JEOPARDY_DICT.keys():
            self.root.ids.category_grid.add_widget(GridLabelButton(
                category=category))

        for point in self.POINTS:
            for category in JEOPARDY_DICT.keys():
                grid_button = GridButton(category=category, point=point)
                grid_button.bind(on_press=self.go_to_question)
                self.root.ids.category_grid.add_widget(grid_button)

    def build_question_screens(self):
        for category in JEOPARDY_DICT.keys():
            for point in self.POINTS:
                JEOPARDY_DICT[category][point]['question_screen'] = QuestionScreen(
                    question_text=JEOPARDY_DICT[category][point]['question'],
                    title=JEOPARDY_DICT[category][point]['title'],
                    category=category, point=point)
                self.screen_manager.add_widget(JEOPARDY_DICT[category][point]['question_screen'])

    def build_answer_screens(self):
        for category in JEOPARDY_DICT.keys():
            for point in self.POINTS:
                JEOPARDY_DICT[category][point]['answer_screen'] = AnswerScreen(
                    answer_label=JEOPARDY_DICT[category][point]['answer_label'],
                    answer_text=JEOPARDY_DICT[category][point]['answer_text'],
                    title=JEOPARDY_DICT[category][point]['title'],
                    category=category, point=point)
                self.screen_manager.add_widget(JEOPARDY_DICT[category][point]['answer_screen'])

    def build_add_points_popup(self):
        popup_player_layout = PopupPlayerLayout()

        for player in self.players:
            popup_player_content = PopupPlayerContent(player=player)
            popup_player_layout.add_widget(popup_player_content)

        popup_layout = PopupBaseLayout()
        popup_layout.add_widget(popup_player_layout)
        popup_layout.add_widget(PopupButtonLayout())

        self.add_points_popup = AddPointsPopup(content=popup_layout)


class PopupBaseLayout(BoxLayout):
    pass


class PopupPlayerLayout(BoxLayout):
    pass


class PopupButtonLayout(BoxLayout):
    pass


class PopupCloseButton(Button):
    def __init__(self, **kwargs):
        super(PopupCloseButton, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_press(self):
        self.app.add_points_popup.dismiss()


class PopupBackButton(Button):

    def __init__(self, **kwargs):
        super(PopupBackButton, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_press(self):
        self.app.add_points_popup.dismiss()
        self.app.screen_manager.current = 'board_screen'


class PopupPlayerContent(BoxLayout):
    player = ObjectProperty()
    points = StringProperty()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super(PopupPlayerContent, self).__init__(**kwargs)
        self.app = App.get_running_app()
        Clock.schedule_interval(self.set_answer_point, 0.5)

    def set_answer_point(self, dt):
        self.point = self.app.screen_manager.current_screen.point

    def add_points(self, player, point):
        player.set_points(point, "+")
        self.ids.score_label.text = str(self.player.get_points())

    def sub_points(self, player, point):
        player.set_points(point, "-")
        self.ids.score_label.text = str(self.player.get_points())


if __name__ == '__main__':
    MainApp().run()
