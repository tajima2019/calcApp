from kivy.app import App
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
import enum
import re
import math



import japanize_kivy

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')


class MethodType(enum.IntEnum):
    No = 0
    Plus = 1
    Minus = 2
    Times = 3
    Divide = 4
    Equal = 5


class CalculateWidget(Widget):
    text = StringProperty()
    signMode = False
    dot = False
    const = False

    e = 1.6021766 * 10 ** -19
    mu = 1.2566370 * 10 ** -6
    G = 6.6743015 * 10 ** -11
    g = 9.80665
    NA = 6.0221407 * 10 ** 23
    P0 = 101325
    k = 1.380649 * 10 ** -23
    h = 6.62607015 * 10 ** -34
    c = 2.99792458 * 10 ** 8
    rydR = 1.0973731 * 10 ** 7
    R = 8.3144626
    pi = 3.1415926

    str_C_lst = ["e", "μ0", "G", "g", "NA", "P0", "k", "h", "c", "R∞", "R", "π"]
    int_C_lst = [e, mu, G, g, NA, P0, k, h, c, rydR, R, pi]

    def __init__(self, **kwargs):
        super(CalculateWidget, self).__init__(**kwargs)
        self.text = '0'
        self.method_type = MethodType.No.value

    def press_number(self, instance):
        if self.dot and instance.text == ".":
            return

        if instance.text == ".":
            self.dot = True

        if self.const and instance.text in self.str_C_lst:
            return

        if instance.text in self.str_C_lst:
            self.const = True

        self.method_type = MethodType.No.value
        self.change_display(instance.text)

    def change_display(self, number):
        if self.text == "0":
            self.text = number
        else:
            self.text += number

    def clear_all(self):
        self.text = "0"
        self.method_type = 0
        self.dot = False
        self.const = False

    def call_method(self, _method_type):
        self.dot = False
        if self.method_type != MethodType.No.value:
            return
        if _method_type == MethodType.Plus.value:
            self.method_type = _method_type
            self.text += "＋"
        elif _method_type == MethodType.Minus.value:
            self.method_type = _method_type
            self.text += "－"
        elif _method_type == MethodType.Times.value:
            self.method_type = _method_type
            self.text += "×"
        elif _method_type == MethodType.Divide.value:
            self.method_type = _method_type
            self.text += "÷"
        elif _method_type == MethodType.Equal.value:
            self.method_type = _method_type
            self.equal()

    def equal(self):
        lst = self.text
        num_lst = re.split(r'[＋－×÷]', lst)
        cal_lst = []
        result = ""
        for e in lst:
            if e == "＋":
                cal_lst.append("+")
            if e == "－":
                cal_lst.append("-")
            if e == "×":
                cal_lst.append("*")
            if e == "÷":
                cal_lst.append("/")

        cal_lst.append("")
        sign_lst = []
        for n, c in zip(num_lst, cal_lst):

            if n in self.str_C_lst:
                index = self.str_C_lst.index(n)
                n = str(self.int_C_lst[index])
            sign_lst.append(self.sign(n))
            result += n
            result += c
        value = eval(result)

        if self.signMode:
            min_n = min(sign_lst)
            print("min_n", min_n)
            value = self.sig_round(value, min_n)

        self.text = str(value)
        self.method_type = MethodType.No.value

    def switch_click(self, switchObject, switchValue): # 掛け算の時でしか有効数字をONにできない
        if switchValue:
            self.signMode = True
        else:
            self.signMode = False

    def sign(self, _n):
        c = 0
        isZero = True

        for e in _n:
            if e == ".":
                continue
            if isZero:
                if e == "0":
                    isZero = True
                else:
                    isZero = False
                    c += 1
            else:
                c += 1
        print("c",c)
        print("_n", _n)
        return c

    def sig_round(self, x, digit):
        x_order = int(math.log10(abs(x)))
        return round(x / 10 ** (x_order - digit + 1)) * 10 ** (x_order - digit + 1)


class CalculatorApp(App):
    def __init__(self, **kwargs):
        super(CalculatorApp, self).__init__(**kwargs)
        self.title = 'calculator'


if __name__ == '__main__':
    CalculatorApp().run()

