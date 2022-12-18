import japanize_kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.metrics import dp

Window.size = (480, 480)

class HelloWorldApp(App):
    def build(self):
        self.root = FloatLayout()

        self.label = Label(size_hint = (None, None))
        self.label.bind(size = self.label.setter('text_size'))
        self.label.text = 'ハローワールド'
        self.label.font_size = dp(18)
        # self.label.bold = False
        # self.label.italic = False
        self.label.color = (1, 1, 1, 1)
        self.label.pos = (dp(0), dp(480-48))
        self.label.size = (dp(480), dp(48))
        self.label.halign = "left"
        self.label.valign = "middle"
        self.root.add_widget(self.label)

        return self.root

if __name__ == '__main__':
    HelloWorldApp().run()