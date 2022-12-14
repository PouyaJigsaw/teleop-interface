import math
from textwrap import fill
from tkinter import *
import numpy
import threading
import random
from playsound import playsound
from event import *

#------Canvas Position ---- #
big_canvas_info = {
    "x": 1500,
    "y": 600,
    "width": 150,
    "height": 150,
    "endup_angle": numpy.deg2rad(-90),
    "endleft_angle": numpy.deg2rad(-240),
    "endright_angle": numpy.deg2rad(60),
    "outline_color": "SpringGreen3",
    "outline_width": 5,
    "color": "green",
    "active": True
}
small_canvas_info = {
    "x": 430,
    "y": 250,
    "width": 50,
    "height": 50,
    "endup_angle": numpy.deg2rad(-90),
    "endleft_angle": numpy.deg2rad(-240),
    "endright_angle": numpy.deg2rad(60),
    "outline_color": "SpringGreen3",
    "outline_width": 2,
    "color": "green",
    "active": False


}
bar_canvas_info_main = {
    "x": 560,
    "y": 70,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 50/100,
    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "blue",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 0.7,
    "progress_step": 0.5,
    "active": True

}
bar_canvas_info1 = {
    "x": 560,
    "y": 30,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 20/100,
    "line_thresholdpercent": 60/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 1.3,
    "progress_step": 10,
    "active": False

}
bar_canvas_info2 = {
    "x": 560,
    "y": 60,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 40/100,
    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 0.2,
    "progress_step": 0.5,
    "active": False

}
bar_canvas_info3 = {
    "x": 560,
    "y": 90,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 25/100,
    "line_thresholdpercent": 50/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 0.7,
    "progress_step": 2,
    "active": False

}
timer_canvas_info = {
    "x": 1700,
    "y": 30,
    "width": 150,
    "height": 50,
    "color": "red",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}
task_canvas_info = {
    "x": 1600,
    "y": 30,
    "width": 150,
    "height": 50,
    "color": "green",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}
score_canvas_info = {
    "x": 1500,
    "y": 30,
    "width": 150,
    "height": 50,
    "color": "blue",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}


score_events = {
    "time_punish": 200,
    "step_error": 10,
    "error_push": 5,
    "threshold_cross": 50,
    "step_error_danger": 20,
    "threshold_cross_danger": 100

}

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

        
    def change_args(self, *args):
        self.args = args

class BaseCanvas():
    def __init__(self, r, info_dict):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.active = info_dict["active"]
        self.offset = 10
        
        self.canvas = Canvas(r, bg=r.cget('bg'), width=self.width+self.offset, height=self.height+self.offset)
        _x = self.x if self.active else 5000
        self.canvas.place(x = _x , y = self.y , width= self.width+self.offset, height= self.height+self.offset)

    def enable(self):
        self.active = True
        self.canvas.place(x = self.x , y = self.y , width= self.width+self.offset, height= self.height+self.offset) 

    def disable(self):
        self.active = False
        self.canvas.place(x = 5000 , y = self.y , width= self.width+self.offset, height= self.height+self.offset)

class CursorCanvas(BaseCanvas):
    def __init__(self, r, info_dict):
        super().__init__(r,info_dict)
        self.a_up = info_dict["endup_angle"]
        self.a_left = info_dict["endleft_angle"]
        self.a_right = info_dict["endright_angle"]
        self.outline_color = info_dict["outline_color"]
        self.color = info_dict["color"]
        self.outline_width = info_dict["outline_width"]

        self.angle_diff = 1

        cursor_endpoints = self.create_arrowpoints()
        self.canvas.create_polygon(cursor_endpoints, outline=self.outline_color, fill=self.color, width=self.outline_width)

    def create_arrowpoints(self):
    
        center_x = self.width/2
        center_y = self.height/2
    
        length = self.width /2


        endup_x = center_x + length * math.cos(self.a_up)
        endup_y = center_y + length * math.sin(self.a_up)

        endleft_x = center_x + length * math.cos(self.a_left)
        endleft_y = center_y + length * math.sin(self.a_left)

        endright_x = center_x + length * math.cos(self.a_right)
        endright_y = center_y + length * math.sin(self.a_right)

        points = [endup_x, endup_y, endleft_x, endleft_y, center_x, center_x,  endright_x, endright_y]
    
    
        return points

    def rotate(self, string):

        if string == "right":
            self.a_up += numpy.deg2rad(self.angle_diff)
            self.a_left += numpy.deg2rad(self.angle_diff)
            self.a_right += numpy.deg2rad(self.angle_diff)
        elif string == "left":
            self.a_up -= numpy.deg2rad(self.angle_diff)
            self.a_left -= numpy.deg2rad(self.angle_diff)
            self.a_right -= numpy.deg2rad(self.angle_diff)
        
        new_cursor_endpoints = self.create_arrowpoints()
        self.canvas.delete('all')
        self.canvas.create_polygon(new_cursor_endpoints, outline=self.outline, fill=self.fill, width=self.outline_width)

class BarCanvas(BaseCanvas): 
    danger_mode = None
    def __init__(self, r, info_dict, danger):
        super().__init__(r,info_dict)
        self.bar_percent = info_dict["bar_defaultpercent"]
        self.bar_defaultpercent = self.bar_percent
        self.tag_bar = "bar"
        self.tag_line = "line"
        self.outline_color = info_dict["outline_color"]
        self.bar_color = info_dict["color"]
        self.line_color = info_dict["line_color"]
        self.outline_width = info_dict["outline_width"]
        self.line_width = info_dict["line_width"]
        self.line_thresholdpercent = info_dict["line_thresholdpercent"]
        self.repeat_moving = None
        self.active = info_dict["active"]
        self.secondary_task = RepeatedTimer(random.randint(1,10), self.random_movement)
        self.move_interval= info_dict["move_interval"]
        self.progress_step = info_dict["progress_step"]
        self.canvas.create_rectangle(2,2, self.width, self.height, fill=r.cget('bg'), outline=self.outline_color, width=self.outline_width)
        self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
        self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width*self.line_thresholdpercent,self.height, fill=self.line_color, width=self.outline_width, tags=self.tag_line)
        self.passed = False
        self.is_danger = danger
        self.red_mode = False
    
    
    def move_bar(self,string):   
        #just to prevent danger bars being active while normal is active (and vice versa) 
        if (self.is_danger and BarCanvas.danger_mode) or (not self.is_danger and not BarCanvas.danger_mode):
            
            self.canvas.delete(self.tag_bar,self.tag_line)
            if string == "left" and self.bar_percent > 0: self.bar_percent -= self.progress_step / 100
            elif string == "right" and self.bar_percent < 100: self.bar_percent += self.progress_step / 100
            
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
            self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width * self.line_thresholdpercent,self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)

            self.colorchange_check()
            self.canvas.tag_raise(self.tag_line,self.tag_bar)
    
    def colorchange_check(self):     
        #check to see the time the bar has passed the threshold 
        if not self.passed and self.bar_percent > self.line_thresholdpercent:
            self.passed = True
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill="yellow", tags=self.tag_bar)
            self.canvas.create_line(self.width * self.line_thresholdpercent, 0, self.width * self.line_thresholdpercent, self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)
            if self.is_danger: post_event("yellow_mode", self) 
            
        #if the bar moves backward it may get less than the threshold 
        if self.passed and self.bar_percent < self.line_thresholdpercent:
            self.passed = False
            return
        
        # check to see if the user ignored and the bar is just keep going 
        elif self.passed and self.bar_percent > self.line_thresholdpercent + self.progress_step/100:
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill="red", tags=self.tag_bar)
            self.canvas.create_line(self.width * self.line_thresholdpercent, 0, self.width * self.line_thresholdpercent, self.height, fill="blue", width=self.line_width, tags=self.tag_line)
            if self.red_mode:
                post_event("step_error_danger") if self.is_danger else post_event("step_error")
                post_event("red_mode", self)
            else:
                post_event("threshold_cross_danger") if self.is_danger else post_event("threshold_cross")
                if self.danger_mode: post_event("red_init_mode", self)
                self.red_mode = True
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/error.wav")
                    
        
    def reset_button(self):
        if self.passed == False:
            post_event("error_push")
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/error.wav")
            return
        else:
            self.passed = False
            self.red_mode = False
            
            if not self.is_danger:
                self.bar_percent = self.bar_defaultpercent
            else:
                self.bar_percent = random.randint(20, self.line_thresholdpercent * 100) / 100
            
            self.canvas.delete(self.tag_bar,self.tag_line)
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
            self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width*self.line_thresholdpercent,self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)

            playsound("/home/pouya/catkin_ws/src/test/src/sounds/beep.wav") 
    def reset(self):
        self.passed = False
        self.bar_percent = self.bar_defaultpercent
        self.canvas.delete(self.tag_bar,self.tag_line)
        self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
        self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width*self.line_thresholdpercent,self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)  
    def move_bar_repeat(self, string, interval):
        if self.repeat_moving is not None:
            self.repeat_moving.stop()
            self.repeat_moving.change_args(string)
            self.repeat_moving.start()
        else:
            self.repeat_moving = RepeatedTimer(interval, self.move_bar, string)  
    def random_movement(self):
        r = random.randint(0,3)
        if r > 2:
            self.move_bar_repeat("left", self.move_interval)
        else:
            self.move_bar_repeat("right", self.move_interval)

class TimerCanvas(BaseCanvas):
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.seconds = '00'
        self.minutes = '00'
        self.text = self.minutes + ":" + self.seconds
        self.countdown = None
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
    def start(self):
        self.countdown = RepeatedTimer(1, self.plus)
    def stop(self):
        self.countdown.stop()
    def plus(self):
        sec = self.seconds
        sec = int(sec)
        min = self.minutes
        min = int(min)
        sec += 1
        if sec == 60:
            sec = 0
            min += 1
        if min == 10:
            post_event("time_punish")
        self.seconds = str(sec) if sec >= 10 else '0' + str(sec) 
        self.minutes = str(min) if min >= 10 else '0' + str(min)
        self.text = self.minutes + ":" + self.seconds
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
    
class TaskCanvas(BaseCanvas):
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.text = '0'
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        self.fsm = None
    def add_fsm(self, fsm):
        self.fsm = fsm
    def plus(self):
        c = int(self.text)
        c += 1
        if c  > 10: return
        if c == 3:
            self.fsm.s12()
        elif c == 5:
            self.fsm.s23()
        elif c == 7:
            self.fsm.s34()
        elif c == 9:
            if self.fsm.is_s5:
                self.fsm.s57()
            elif self.fsm.is_s6:
                self.fsm.s67()
        elif c == 10:
            self.fsm.s78()

        self.text = str(c)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        
class ScoreCanvas(BaseCanvas):  
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.text = "0"
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        
        subscribe("time_punish", self.add_score)
        
        subscribe("step_error", self.add_score)
        subscribe("step_error_danger", self.add_score)
        
        subscribe("threshold_cross", self.add_score)
        subscribe("threshold_cross_danger", self.add_score)   
    def add_score(self, event_type):
        score = self.text
        score = int(score)
        score += score_events[event_type]
        self.text = str(score)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
    def subtract_score(self, event_type):
        score = self.text
        score = int(score)
        score += score_events[event_type]
        self.text = str(score)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
