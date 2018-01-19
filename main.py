#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
import json

from kivy import require
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition
from kivy.properties import NumericProperty, ObjectProperty
from kivy.config import Config

from widgets import PlayersScoreLayout, GridLabelButton, GridButton,\
    QuestionScreen, AnswerScreen, PopupPlayerLayout, PopupPlayerContent,\
    PopupBaseLayout, PopupButtonLayout, AddPointsPopup

require('1.10.0')
Config.set('graphics', 'fullscreen', 'auto')

PLAYERS = ('Lag 1', 'Lag 2', 'Lag 3')

with open('jeopardy.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)


class Player(object):

    def __init__(self, name=None, points=None):
        self._name = name
        self._points = points

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Player: {}, Points: {}>".format(self._name, self._points)


class MainApp(App):
    POINTS = data[next(iter(data.keys()))].keys()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.players = list()
        self.screen_manager = ObjectProperty()
        self.add_points_popup = ObjectProperty()

    def go_to_question(self, instance):
        if not instance.pushed:
            instance.background_color = (1, 1, 1, 0.1)
            instance.pushed = True

        screen_name = \
            instance.id.split(".")[0] + "-" + \
            instance.id.split(".")[1] + "-question"

        self.screen_manager.current = screen_name

    def close_popup(self, _instance):
        self.add_points_popup.dismiss()

    def build(self):
        self.screen_manager = self.root.ids.screen_manager
        self.screen_manager.transition = NoTransition()
        self.create_players()
        self.build_score_layout()
        self.build_category_grid()
        self.build_question_screens()
        self.build_add_points_popup()

    def create_players(self):
        for player in PLAYERS:
            self.players.append(Player(name=player, points=0))

    def build_score_layout(self):
        for player in self.players:
            self.root.ids.score_layout.add_widget(PlayersScoreLayout(
                player=player, id=player.name))

    def build_category_grid(self):
        for category in data.keys():
            self.root.ids.category_grid.add_widget(GridLabelButton(
                category=category))

        for point in self.POINTS:
            for category in data.keys():
                grid_button = GridButton(category=category, point=int(point))
                grid_button.bind(on_press=self.go_to_question)
                self.root.ids.category_grid.add_widget(grid_button)

    def build_question_screens(self):
        for category in data.keys():
            for point in self.POINTS:
                # Build Question Screens
                data[category][point]['question_screen'] = QuestionScreen(
                    question_text=data[category][point]['question'],
                    title=data[category][point]['title'],
                    category=category, point=int(point))
                self.screen_manager.add_widget(
                    data[category][point]['question_screen'])
                # Build Answer Screens
                data[category][point]['answer_screen'] = AnswerScreen(
                    answer_label=data[category][point]['answer_label'],
                    answer_text=data[category][point]['answer_text'],
                    title=data[category][point]['title'],
                    category=category, point=int(point))
                self.screen_manager.add_widget(
                    data[category][point]['answer_screen'])

    def build_add_points_popup(self):
        popup_player_layout = PopupPlayerLayout()

        for player in self.players:
            popup_player_content = PopupPlayerContent(player=player)
            popup_player_layout.add_widget(popup_player_content)

        popup_layout = PopupBaseLayout()
        popup_layout.add_widget(popup_player_layout)
        popup_layout.add_widget(PopupButtonLayout())

        self.add_points_popup = AddPointsPopup(content=popup_layout)


if __name__ == '__main__':
    Builder.load_file('widgets.kv')

    MainApp().run()
