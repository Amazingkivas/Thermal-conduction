from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 1, 1)  # Белый цвет фона
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical')
        label = Label(text="This is the first screen")
        button = Button(text="Go to Second Screen", on_press=self.switch_screen)

        layout.add_widget(label)
        layout.add_widget(button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def switch_screen(self, *args):
        self.manager.current = 'second'


class SecondScreen(Screen):
    param1: float
    param2: float
    param3: float
    plot_type: str

    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        super().__init__()
        self.param1 = 0
        self.param2 = 0
        self.param3 = 0
        self.plot_type = "plus"

        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        label = Label(text="This is the second screen", size_hint=(None, None), size=(200, 50), color=[0, 0, 0, 1])
        button = Button(text="Go to First Screen", on_press=self.switch_screen,
                        size_hint=(None, None), size=(200, 50), color=[0, 0, 0, 1])

        # Основной макет приложения
        layout = BoxLayout(orientation='horizontal', padding=10, spacing=5)
        vertical_box = BoxLayout(orientation='vertical', spacing=5)

        # Поля для ввода параметров
        parameter1 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='Parameter 1')
        parameter2 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='Parameter 2')
        parameter3 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='Parameter 3')

        # Таблица для отображения данных x от y
        self.table_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, row_default_height=40)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.scroll_view = ScrollView(size_hint=(0.4, 1), do_scroll_y=True, do_scroll_x=False,
                                      scroll_type=['bars'], bar_width='15dp')
        self.scroll_view.add_widget(self.table_layout)

        # Виджет Graph для отображения графика
        self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=10,
                           y_grid_label=True, x_grid_label=True,
                           padding=10, xlog=False, ylog=False,
                           x_grid=True, y_grid=True, xmin=-100, xmax=100,
                           ymin=-100, ymax=100, size_hint=(1, 0.8), width=400)

        # Обработчик события ввода параметров
        def on_text(instance, value):
            try:
                self.param1 = float(parameter1.text)
                self.param2 = float(parameter2.text)
                self.param3 = float(parameter3.text)

                current_plot = self.graph.plots[0] if self.graph.plots else None

                x_values = [x for x in range(-100, 101)]  # Значения x от -100 до 100
                y_values = [self.param1 * x ** 2 + self.param2 * x + self.param3 for x in x_values]  # Функция x^2

                # Проверка наличия графика перед удалением
                if self.graph.plots:
                    self.graph.remove_plot(self.graph.plots[0])

                plot_color = [1, 0, 0, 1]

                # Построение графика
                plot = MeshLinePlot(color=plot_color)
                plot.points = list(zip(x_values, y_values))
                self.graph.add_plot(plot)

                self.add_table_data(x_values, y_values)

            except ValueError:
                pass

        parameter1.bind(text=on_text)
        parameter2.bind(text=on_text)
        parameter3.bind(text=on_text)

        switch_button = Button(text='Переключить график', size_hint=(None, None), size=(200, 50))
        switch_button.bind(on_press=self.switch_graph)

        # Добавление виджетов на макет
        grid = GridLayout(cols=3)
        vertical_box.add_widget(label)
        vertical_box.add_widget(button)
        vertical_box.add_widget(parameter1)
        vertical_box.add_widget(parameter2)
        vertical_box.add_widget(parameter3)
        vertical_box.add_widget(switch_button)
        vertical_box.add_widget(self.graph)
        layout.add_widget(vertical_box)
        grid.add_widget(self.scroll_view)
        layout.add_widget(grid)
        self.add_widget(layout)

    def switch_graph(self, instance):

        current_plot = self.graph.plots[0] if self.graph.plots else None

        x_values = [x for x in range(-100, 101)]  # Значения x от -100 до 100

        if self.plot_type == "minus":
            y_values = [self.param1 * x ** 2 + self.param2 * x + self.param3 for x in x_values]  # Функция x^2
            plot_color = [1, 0, 0, 1]
            self.plot_type = "plus"
        else:
            y_values = [-self.param1 * x ** 2 + self.param2 * x + self.param3 for x in x_values]  # Функция x^2
            plot_color = [0, 1, 0, 1]
            self.plot_type = "minus"

        # Проверка наличия графика перед удалением
        if self.graph.plots:
            self.graph.remove_plot(self.graph.plots[0])

        # Построение графика
        plot = MeshLinePlot(color=plot_color)
        plot.points = list(zip(x_values, y_values))
        self.graph.add_plot(plot)

    def add_table_data(self, x_values, y_values):
        # Добавление данных в таблицу
        self.table_layout.clear_widgets(children=self.table_layout.children[:3])
        for value in ['№ узла', 'X', 'Y']:
            cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
            cell.bind(size=self.draw_border_2)
            self.table_layout.add_widget(cell)
        num = 0
        for x, y in zip(x_values, y_values):
            num += 1
            for value in [num, x, y]:
                cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
                cell.bind(size=self.draw_border_2)
                self.table_layout.add_widget(cell)

    def draw_border_1(self, instance, size):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0, 0, 1)
            instance.rect = Rectangle(size=instance.size, pos=instance.pos)
        instance.bind(size=self._update_rect, pos=self._update_rect)

    def draw_border_2(self, instance, size):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(1, 1, 1, 1)
            instance.rect = Rectangle(size=instance.size, pos=instance.pos)
        instance.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def switch_screen(self, *args):
        self.manager.current = 'first'


class ParameterInputApp(App):
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def switch_screen(self, *args):
        self.manager.current = 'first'

    def build(self):
        screen_manager = ScreenManager()

        first_screen = FirstScreen(name='first')
        second_screen = SecondScreen(name='second')

        screen_manager.add_widget(first_screen)
        screen_manager.add_widget(second_screen)

        return screen_manager

if __name__ == '__main__':
    ParameterInputApp().run()
