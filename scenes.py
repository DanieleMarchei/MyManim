from PIL import Image
from manim import *
import numpy as np
from my_config import *
import sys
from tangle import *
from rna import *

config['pixel_height'] = 1080
config['pixel_width'] = 1920
config['frame_rate'] = 60

config["background_color"] = palette["bg"]


class SceneWithTimeStamps(Scene):
    def setup(self):
        self.time_elapsed = 0
        file_name = sys.argv[1].replace(".py", "")
        quality_folder = f"{config['pixel_height']}p{config['frame_rate']}"

        path = f"media/videos/{file_name}/{quality_folder}/{self}.txt"
        self.timestamps_file = open(path, "w")

    def play(self, *args, **kwargs):
        for anim in args:
            self.time_elapsed += self.get_run_time([anim])
            time_ms = int(self.time_elapsed * 1000)
            self.timestamps_file.write(f"{time_ms} {anim}\n")

        Scene.play(self, *args, **kwargs)
    
    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None):
        self.time_elapsed += duration
        duration_str = "Wait " + str(duration)
        time_ms = int(self.time_elapsed * 1000)
        self.timestamps_file.write(f"{time_ms} {duration_str}\n")

        Scene.wait(self, duration, stop_condition)

    def clear(self):
        Scene.clear(self)

    def remove(self, *mobjects):
        Scene.remove(self, *mobjects)

    def comment(self, text):
        self.timestamps_file.write(f"# {text}\n")

class SlideScene(Scene):

    def __init__(self, caller = None, renderer=None, **kwargs):

        self.caller = caller
        self.comment(self)

        Scene.__init__(self, renderer, **kwargs)

    def add(self, *mobjects):
        if self.caller:
            self.caller.add(*mobjects)
        else:
            Scene.add(self, *mobjects)

    def play(self, *args, **kwargs):
        if self.caller:
            self.caller.play(*args, **kwargs)
        else:
            Scene.play(self, *args, **kwargs)
    
    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None):
        if self.caller:
            self.caller.wait(duration, stop_condition)
        else:
            Scene.wait(self, duration, stop_condition)
    
    def clear(self):
        if self.caller:
            self.caller.clear()
        else:
            Scene.clear(self)

    def remove(self, *mobjects):
        if self.caller:
            self.caller.remove(*mobjects)
        else:
            Scene.remove(*mobjects)

    def comment(self, text):
        if self.caller:
            self.caller.comment(self)