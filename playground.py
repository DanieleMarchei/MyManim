from PIL import Image
from manim import *
import numpy as np
from my_config import *
import sys
from tangle import *
from rna import *
from scenes import *

config['pixel_height'] = 1080
config['pixel_width'] = 1920
config['frame_rate'] = 60

config["background_color"] = palette["bg"]

class TimeStampTest(SlideScene):
    def construct(self):
        square = Square()
        anim = ShowCreation(square)
        self.play(anim)

        circle = Circle()
        anim = ReplacementTransform(square, circle)
        self.play(anim)
        self.wait()

class TangleConstruct(Scene):
     def construct(self):

        point = 2 * UP + 2 * LEFT
        size = 4

        In = Tangle.get_prime_tangle("I", 4, size = size, point = point)
        In.set_edge_color("1,1'", RED)
        self.play(ShowCreation(In), run_time = 2)
        e = In.get_edge("1,1'")
        self.play(WiggleOutThenIn(e, scale_value = 1.2))
        e = In.add_edge("1,2'")
        self.play(ShowCreation(e))

        self.wait()

        tangle = Tangle("1,3 2,4' 4,2' 1',3'", size = size, point = point)
        tangle.set_edge_color("1,3", RED)
        self.play(ReplacementTransform(In, tangle))
        
        u1 = Tangle.get_prime_tangle("U1", 4, size = size, point = point)
        self.play(ReplacementTransform(tangle, u1))

        u2 = Tangle.get_prime_tangle("U2", 4, size = size, point = point)
        self.play(ReplacementTransform(u1, u2))

        t1 = Tangle.get_prime_tangle("T1", 4, size = size, point = point)
        self.play(ReplacementTransform(u2, t1))

        t2 = Tangle.get_prime_tangle("T2", 4, size = size, point = point)
        self.play(ReplacementTransform(t1, t2))

class TangleEmpty(Scene):
     def construct(self):

        empty = EmptyTangle(4)
        self.play(ShowCreation(empty))

        e = empty.add_edge("1,2'")
        self.play(ShowCreation(e))

        e = empty.get_edge_attached_to("2'")
        self.play(WiggleOutThenIn(e))

class TangleTransformation(Scene):
    def construct(self):

        size = 3

        In = Tangle.get_prime_tangle("I", 4, size = size)
        self.play(ShowCreation(In))
        u = Tangle("1,3 2,4' 4,2' 1',3'", size = size)
        u.move_to(In)

        self.play(TransformTangle(In, u))


        self.play(ApplyMethod(u.shift, 2 * UP + 2 * LEFT))

        empty = EmptyTangle(4, size = size)
        empty.shift(DOWN)
        
        self.play(ShowCreation(empty))

        self.play(PutUnderTangle(empty, u))

        self.wait(3)

class MergeTangles(Scene):
    def construct(self):
        u1 = Tangle.get_prime_tangle("U1", 4)
        u2 = Tangle.get_prime_tangle("U2", 4)
        u2.next_to(u1, DOWN)

        self.add(u1)
        self.add(u2)

        self.play(PutUnderTangle(u2, u1))

        g = Group(u1,u2)

        r = Tangle("1,2 3,1' 4,4' 2',3'")

        self.play(
            FadeOutAndShift(g, RIGHT),
            FadeInFrom(r, LEFT)
        )
        self.wait()

class RnaMovingTest(Scene):
    def construct(self):
        rna = Rna("AGCUCUUAGCUACGAGGCUGCUA")
        self.play(Write(rna))

        rna.start_updater() 
        self.wait(20)