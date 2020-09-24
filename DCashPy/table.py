from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string(
"""
<TableButton>:
    canvas.before:
        Color:
            rgba: 0.9,0.9,0.9,1
        Line:
            width: 0.5
            rectangle: self.x, self.y, self.width, self.height
"""
)

class TableButton(Button):
    pass

