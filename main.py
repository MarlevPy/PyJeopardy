# Kivy imports
from kivy import require
from kivy.app import App
from kivy.uix.screenmanager import NoTransition
from kivy.properties import NumericProperty, ObjectProperty
from kivy.config import Config

# Local imports
from widgets import PlayersScoreLayout, GridLabelButton, GridButton,\
    QuestionScreen, AnswerScreen, PopupPlayerLayout, PopupPlayerContent,\
    PopupBaseLayout, PopupButtonLayout, AddPointsPopup

# 3rd party imports
try:
    import simplejson as json
except ImportError:
    import json

require('1.10.0')
Config.set('graphics', 'fullscreen', 'auto')

# Tuple with name for all the players in the game
PLAYERS = ('Lag 1', 'Lag 2', 'Lag 3')

# Load the data for the game including categories, questions, answers and points
with open('jeopardy.json', 'r', encoding='utf-8') as json_file:
    JEOPARDY_DATA = json.load(json_file)

# Assumes that first
POINTS = JEOPARDY_DATA[next(iter(JEOPARDY_DATA.keys()))].keys()


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
    point = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.players = list()
        self.screen_manager = ObjectProperty()
        self.add_points_popup = ObjectProperty()

    def go_to_question(self, instance):
        """
        Called when choosing question from the main grid.
        :param instance:    Name and reference to the object instance
                            of the button being pressed.
        :return: None
        """
        # Change background color for questions that have been opened
        if not instance.pushed:
            instance.background_color = (1, 1, 1, 0.1)
            instance.pushed = True

        # From question button instance, get screen name
        screen_name = \
            instance.id.split(".")[0] + "-" + \
            instance.id.split(".")[1] + "-question"

        # Change screen
        self.screen_manager.current = screen_name

    def build(self):
        """
        Initializes the application by building the widget instances
        :return: None
        """
        self.screen_manager = self.root.ids.screen_manager
        self.screen_manager.transition = NoTransition()

        self.create_players()
        self.build_score_layout()
        self.build_category_grid()
        self.build_question_and_answer_screens()
        self.build_add_points_popup()

    def create_players(self):
        """
        Instantiates all players in the PLAYERS tuple and add those to
        the list attribute [players] in the app.
        :return: None
        """
        for player in PLAYERS:
            self.players.append(Player(name=player, points=0))

    def build_score_layout(self):
        """
        Instantiates the top layout of the main screen
        that shows the player scores.
        :return: None
        """
        for player in self.players:
            self.root.ids.score_layout.add_widget(PlayersScoreLayout(
                player=player, id=player.name))

    def build_category_grid(self):
        """
        Instantiates the main grid that shows the question cateqories
        and its corresponding question buttons.
        Gathers data from JEOPARDY_DATA.
        :return: None
        """
        # First row that holds the category labels as buttons.
        for category in JEOPARDY_DATA.keys():
            self.root.ids.category_grid.add_widget(GridLabelButton(
                category=category))

        # Rest of the rows that holds a button for each question.
        for point in POINTS:
            for category in JEOPARDY_DATA.keys():
                grid_button = GridButton(category=category, point=int(point))
                grid_button.bind(on_press=self.go_to_question)
                self.root.ids.category_grid.add_widget(grid_button)

    def build_question_and_answer_screens(self):
        """
        Instantiates the main question and answer screens and
        add those to the screen manager.
        :return: None
        """
        for category in JEOPARDY_DATA.keys():
            for point in POINTS:
                # Build Question Screens
                JEOPARDY_DATA[category][point]['question_screen'] = QuestionScreen(
                    question_text=JEOPARDY_DATA[category][point]['question'],
                    title=JEOPARDY_DATA[category][point]['title'],
                    category=category, point=int(point))
                self.screen_manager.add_widget(
                    JEOPARDY_DATA[category][point]['question_screen'])
                # Build Answer Screens
                JEOPARDY_DATA[category][point]['answer_screen'] = AnswerScreen(
                    answer=JEOPARDY_DATA[category][point]['answer'],
                    answer_description=JEOPARDY_DATA[category][point]['answer_description'],
                    title=JEOPARDY_DATA[category][point]['title'],
                    category=category, point=int(point))
                self.screen_manager.add_widget(
                    JEOPARDY_DATA[category][point]['answer_screen'])

    def build_add_points_popup(self):
        """
        Instantiates the popup that is used to add points after
        each answer.
        :return: None
        """
        popup_player_layout = PopupPlayerLayout()

        for player in self.players:
            popup_player_content = PopupPlayerContent(player=player)
            popup_player_layout.add_widget(popup_player_content)

        popup_layout = PopupBaseLayout()
        popup_layout.add_widget(popup_player_layout)
        popup_layout.add_widget(PopupButtonLayout())

        self.add_points_popup = AddPointsPopup(content=popup_layout)


if __name__ == '__main__':
    MainApp().run()
