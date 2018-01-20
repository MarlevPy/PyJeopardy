from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty

Builder.load_file('widgets.kv')


class AddPointsPopup(Popup):
    pass


class AnswerButton(ButtonBehavior, Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'media/answer.png'

    def on_press(self):
        current_screen = App.get_running_app().screen_manager.current
        answer_screen = '-'.join(current_screen.split('-')[:2]) + '-answer'
        App.get_running_app().screen_manager.current = answer_screen


class AnswerScreen(Screen):
    answer = StringProperty()
    answer_description = StringProperty()
    title = StringProperty()
    category = StringProperty()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = '{category}-{point}-answer'.format(
            category=self.category, point=self.point)
        self.app = App.get_running_app()


class AnswerLayout(AnchorLayout):
    pass


class BackButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'media/back.png'

    def on_press(self):
        App.get_running_app().screen_manager.current = 'board_screen'


class BackLayout(AnchorLayout):
    pass


class BaseLayout(FloatLayout):
    pass


class BoardScreen(Screen):
    point = NumericProperty()


class CategoryGrid(GridLayout):
    pass


class GridLabelButton(Button):
    font_color = StringProperty()
    category = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '[color={font_color}][b]{category}[/b][/color]'.format(
            category=self.category, font_color=self.font_color)


class GridButton(Button):
    category = StringProperty()
    point = NumericProperty()
    font_color = StringProperty()
    pushed = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '[color={font_color}][b]{point}[/b][/color]'.format(
            point=self.point, font_color=self.font_color)
        self.pushed = False
        self.id = '{category}.{point}'.format(
            category=self.category, point=self.point)


class HeaderLayout(AnchorLayout):
    pass


class MainLayout(BoxLayout):
    pass


class PlayerLabel(Label):
    pass


class PlayersScoreLayout(BoxLayout):
    player = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        Clock.schedule_interval(self.update_points, 1)

    def update_points(self, _dt):
        self.ids.score_label.text = str(self.player.points)


class PopupBackButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_press(self):
        self.app.add_points_popup.dismiss()
        self.app.screen_manager.current = 'board_screen'


class PopupBaseLayout(BoxLayout):
    pass


class PopupButtonLayout(BoxLayout):
    pass


class PopupCloseButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_press(self):
        self.app.add_points_popup.dismiss()


class PopupPlayerContent(BoxLayout):
    player = ObjectProperty()
    points = StringProperty()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        Clock.schedule_interval(self.set_answer_point, 0.5)

    def set_answer_point(self, _dt):
        self.point = self.app.screen_manager.current_screen.point

    def add_points(self, player, point):
        player.points += point
        self.ids.score_label.text = str(self.player.points)

    def sub_points(self, player, point):
        player.points -= point
        self.ids.score_label.text = str(self.player.points)


class PopupPlayerLayout(BoxLayout):
    pass


class QABox(BoxLayout):
    pass


class QAImage(Image):
    pass


class QALayout(AnchorLayout):
    pass


class QuestionLabel(Label):
    question_text = StringProperty()
    font_color = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_color = '561f60'
        self.markup = True

    def on_size(self, *_unused):
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


class AnswerLabel(QuestionLabel):
    pass


class QuestionScreen(Screen):
    question_text = StringProperty()
    title = StringProperty()
    category = StringProperty()
    point = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = '{category}-{point}-question'.format(
            category=self.category, point=self.point)
        self.app = App.get_running_app()


class ScoreLayout(BoxLayout):
    pass


class ScoreLabel(Label):
    pass


class SetPointsButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'media/set_points.png'


class WallpaperImage(Image):
    pass
