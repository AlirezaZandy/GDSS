from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.factory import Factory as F
from kivy.core.window import Window
from kivy.lang.builder import Builder
import os
import random
import tkinter
from tkinter import filedialog
from sympy import false, true

## Kivy Code

Builder.load_string('''
#: import ew kivy.uix.effectwidget
<GoButton@Button>:
    name:None
    background_color: 0,0,0,0
    canvas:
        Color:
            hsv: 0,0,1
            a: 0 if self.state == 'normal' else 1
        Rectangle:
            size: (32,32)
            pos: (self.pos[0]+self.size[0]/2.0) - 32/2.0, (self.pos[1]+self.size[1]/2.0) - 32/2.0
            source: "icons/{}.png".format(self.name)
    on_press: self.background_color = (0.5,0.5,0.5,0.5)
    on_release: self.background_color = (0,0,0,0)

<TogButton@ToggleButton>:
    name:None
    background_color: 0,0,0,0
    canvas:
        Color:
            hsv: 0,0,1
            a: 0.3 if self.state == 'normal' else 1
        Rectangle:
            size: (20,20) 
            pos: (self.pos[0]+self.size[0]/2.0) - 20/2.0, (self.pos[1]+self.size[1]/2.0) - 20/2.0
            source: "icons/{}.png".format(self.name)
            
            

# Main Layout
<Pictuer>:
    EffectWidget:
        id: mono
        bnw: False
        effects:[ew.MonochromeEffect()] if self.bnw  else []
        Image:
            id: imageView
            source: "defualt.png"
            allow_stretch: False
            nocache: True
            mipmap: False
    FloatLayout:
        size_hint: None ,None
        size: root.width, 30
        pos_hint:{"center_x":0.5,"y":0}
        FloatLayout:
            canvas:
                Color:
                    rgba: 0, 0, 0, 0.5
                Rectangle:
                    size: self.size
                    pos: self.pos
        BoxLayout:
            pos_hint:{"center_x":0.5,"center_y":0.5}
            size_hint: None, None
            size: 300, 32
            orientation: 'horizontal'
            TogButton:
                name:"exit"
                on_press: app.close_application()
                # back to the perv screen
            TogButton:
                name:"info"
                on_press: root.ids.filename.visible = not root.ids.filename.visible
            TogButton:
                name:"folder"
                on_press: root.rest_catalog(), root.next_image()
            TogButton:
                name:"sound"
                # beeper
            TogButton:
                name:"over"
                # always on top
            TogButton:
                name:"bnw"
                on_press: root.ids.mono.bnw = not root.ids.mono.bnw
                # pictuer adjustment
            TogButton:
                name:"timer"
                on_press: root.ids.timer.visible = not root.ids.timer.visible
    GoButton:
        name:"next"
        size_hint: None, None
        size: 64, root.height
        pos_hint:{"right":1, "center_y":0.5}
        on_release: root.next_image()
        on_press: root.remaining = root.total
    GoButton:
        name:"prev"
        size_hint: None, None
        size: 64, root.height
        pos_hint:{"left":0, "center_y":0.5}
        on_release: root.prev_image()
        on_press: root.remaining = root.total
    ToggleButton:
        size_hint: None, None
        size: root.width/5, root.height/5
        pos_hint:{"center_x":0.5, "center_y":0.5}
        on_press: root.start_stop()
        background_color: 0,0,0,0
        canvas:
            Color:
                hsv: 0,0,1
                a: 1 if self.state == 'normal' else 0
            Rectangle:
                size: (128,128)
                pos: (self.pos[0]+self.size[0]/2.0) - 128/2.0, (self.pos[1]+self.size[1]/2.0) - 128/2.0
                source: "icons/p_paused.png"

    Label:
        id: timer
        visible: False
        opacity: 1 if self.visible else 0
        text:'{:.0f}:{:.0f}'.format((root.remaining // 60),(root.remaining % 60))
        size_hint: None, None
        size: 50, 50
        pos_hint:{"right":0.98, "top":0.98}
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 0.5
            Ellipse:
                pos: self.pos
                size: self.size
    Label:
        id: filename
        visible: False
        opacity: 1 if self.visible else 0
        text:'{}'.format(root.ids.filename.text)
        size_hint: None, None
        size: root.width, 32
        pos_hint:{"center_x":0.5, "top":1}
''')

## Kivy Code

# time_sec=300

Window.size = (700/1.5, 700)
Window.borderless = false



class Pictuer(FloatLayout):

    active = F.BooleanProperty(False)
    remaining = F.NumericProperty(0)

    def img_cataloge(self, dirs):
    
        img_path_list = []
        for root, subdir, files in os.walk(dirs, topdown=True):
            for file_name in files:
                if file_name.lower().endswith((".jpg",".jpeg",".png")):
                    img_path_list.append(os.path.join(root, file_name))
        random.shuffle(img_path_list)
        return img_path_list

    def __init__(self, total, **kwargs):

        super(Pictuer, self).__init__()
        self.total = total
        self.img_li = self.get_path()
        self.img_id = -1
        Clock.schedule_interval(self.call_back, 0.1)
    
    def rest_catalog(self):

        self.img_li = self.get_path()
    
    def get_path(self):
        
        root = tkinter.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        open_file = filedialog.askdirectory()
        test_var = str(open_file).replace('/','\\')
        return self.img_cataloge(test_var)

    def img_gen(self):

        img = self.img_li[self.img_id]
        self.ids.imageView.source = img
        img_tag = img.split("\\")[-1]
        self.ids.filename.text= img_tag 

    def next_image(self):

        try:
            self.img_id += 1
            self.img_gen()
        except IndexError:
            self.img_id = 0
            self.img_gen()

        # print(self.ids.imageView.source)

    def prev_image(self):

        if self.img_id <= 0:
            pass
        else:
            self.img_id -= 1
            self.img_gen()

        # print(self.ids.imageView.source)

    def start_stop(self):

        self.active = not self.active

    def call_back(self, dt):

        if not self.active:
            return
        if self.remaining <= dt:
            self.next_image()
            self.remaining = self.total
        else:
            self.remaining -= dt


class MyApp(App):
    
    time_sec = input("enter in sec:   ")

    def build(self):

        return Pictuer(total=self.time_sec)

    def close_application(self):

        App.get_running_app().stop()
        Window.close()


if __name__ == "__main__":
    MyApp().run()
