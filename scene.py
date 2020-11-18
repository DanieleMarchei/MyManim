from os import write
from manim import *
import numpy as np
from my_config import *
from tangle import *
from rna import *

config['pixel_height'] = 720
config['pixel_width'] = 1280
config['frame_rate'] = 30

config["background_color"] = palette["bg"]

class SquareToCircle(Scene):
    def construct(self):

        text = Tex('Hello world')

        self.play(Write(text))
        self.wait()

        square = Square()
        square.flip(RIGHT)
        square.rotate(- 3 * TAU / 8)

        self.play(Transform(text, square))
        self.wait()
        
        circle = Circle()
        
        self.play(Transform(square, circle))

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

class FactorTangle(Scene):
    def construct(self):

        #TODO: Add text to indicate which part of the screen is representing

        edge_col = [RED, PURPLE_C, BLUE, YELLOW]

        size = 2
        runtime = 1

        f = Tangle("1,3 2,4' 4,2' 1',3'", size = size)
        f.set_edge_color("1,3", edge_col[0])
        f.set_edge_color("2,4'", edge_col[1])
        f.set_edge_color("4,2'", edge_col[2])
        f.set_edge_color("1',3'", edge_col[3])

        self.play(ShowCreation(f))

        tangle_to_factorize = Tex('Tangle to factorize').scale(0.7)
        tangle_to_factorize.next_to(f, 4 * UP)

        self.play(Write(tangle_to_factorize, run_time = runtime))

        tangle_type = Tex('Mixed type').scale(0.6)
        tangle_type.next_to(tangle_to_factorize, DOWN)
        self.play(Write(tangle_type, run_time = runtime))

        current_operation = Tex('Current Operation').scale(0.7)
        current_operation.next_to(f, 4 * UP + 4 * LEFT)

        self.play(Write(current_operation, run_time = runtime))

        operation = Tex('Removing $T_2$').scale(0.6)
        operation.next_to(current_operation, DOWN)
        self.play(Write(operation, run_time = runtime))


        empty = EmptyTangle(4, size = size)
        empty.shift(3.5 * LEFT)
        t2 = Tangle.get_prime_tangle("T2", 4, size = size)
        t2.next_to(empty, DOWN)

        g = Group(empty, t2)

        self.play(ShowCreation(g))
        
        self.play(PutUnderTangle(t2, empty, put_next_to=False))

        edges = ["1,3", "1',2'", "2,4'", "4,3'"]
        cols = [edge_col[0], edge_col[3], edge_col[1], edge_col[2]]
        for i, edge in enumerate(edges):
            e = empty.add_edge(edge)
            self.play(ShowCreation(e))
            e = empty.get_edge(edge)
            if i == 0:
                self.play(ApplyMethod(e.set_color, cols[i]))
            if i == 1:
                e1 = t2.get_edge_attached_to("1")
                e2 = t2.get_edge_attached_to("2")
                g_ = Group(e, e1, e2)
                self.play(ApplyMethod(g_.set_color, cols[i]))
            if i == 2:
                e1 = t2.get_edge_attached_to("4")
                g_ = Group(e, e1)
                self.play(ApplyMethod(g_.set_color, cols[i]))
            if i == 3:
                e1 = t2.get_edge_attached_to("3")
                g_ = Group(e, e1)
                self.play(ApplyMethod(g_.set_color, cols[i]))

        r1 = Tangle(" ".join(edges), size = size)
        r1.set_edge_color("1,3", edge_col[0])        
        r1.set_edge_color("2,4'", edge_col[1])      
        r1.set_edge_color("4,3'", edge_col[2])    
        r1.set_edge_color("1',2'", edge_col[3])    

        self.play(
            FadeOutAndShift(g, RIGHT),
            TransformTangle(f, r1)
        )

        factors_queue = Tex('Factors Queue').scale(0.7)
        factors_queue.next_to(f, 4 * UP + 3 * RIGHT)

        self.play(Write(factors_queue, run_time = runtime))

        tex1 = Tex('$T_2$')
        queue = Queue(tex1)
        queue.next_to(r1, 4 * RIGHT)
        self.play(Write(tex1))
        #-------------------------------------

        tangle_type_new = Tex('Ends with a U tangle').scale(0.6)
        tangle_type_new.next_to(tangle_to_factorize, DOWN)

        self.play(ReplacementTransform(tangle_type, tangle_type_new, run_time = runtime))

        tangle_type = tangle_type_new

        operation_new = Tex('Removing $U_1$').scale(0.6)
        operation_new.next_to(current_operation, DOWN)

        self.play(ReplacementTransform(operation, operation_new, run_time = runtime))

        operation = operation_new

        empty = EmptyTangle(4, size = size)
        empty.shift(3.5 * LEFT)

        u1 = Tangle.get_prime_tangle("U1", 4, size = size)
        u1.next_to(empty, DOWN)

        g = Group(empty, u1)

        self.play(ShowCreation(g))
        self.play(PutUnderTangle(u1, empty, put_next_to=False))

        e_ = u1.get_edge("1',2'")
        self.play(ApplyMethod(e_.set_color, edge_col[3]))

        edges = ["1,1'", "3,2'", "2,4'", "4,3'"]
        for i, edge in enumerate(edges):
            e = empty.add_edge(edge)
            self.play(ShowCreation(e))
            if i == 1:
                e1 = empty.get_edge_attached_to("1")
                e2 = empty.get_edge_attached_to("3")
                e3 = u1.get_edge("1,2")
                g_ = Group(e1, e2, e3)
                self.play(ApplyMethod(g_.set_color, edge_col[0]))
            if i == 2:
                e1 = empty.get_edge("2,4'")
                e2 = u1.get_edge("4,4'")
                g_ = Group(e1, e2)
                self.play(ApplyMethod(g_.set_color, edge_col[1]))
            if i == 3:
                e1 = empty.get_edge("4,3'")
                e2 = u1.get_edge("3,3'")
                g_ = Group(e1, e2)
                self.play(ApplyMethod(g_.set_color, edge_col[2]))

        r2 = Tangle(" ".join(edges), size = size)
        r2.set_edge_color("1,1'", edge_col[0])        
        r2.set_edge_color("2,4'", edge_col[1])      
        r2.set_edge_color("3,2'", edge_col[0])    
        r2.set_edge_color("4,3'", edge_col[2]) 

        self.play(
            FadeOutAndShift(g, RIGHT),
            TransformTangle(r1, r2)
        )

        tex2 = Tex('$U_1$')
        self.play(ApplyMethod(queue.shift,  0.5 * RIGHT))
        tex2.next_to(queue, LEFT / 2)
        queue.add(tex2)
        self.play(Write(tex2))

        e = r2.get_edge("3,2'")
        self.play(ApplyMethod(e.set_color, edge_col[3]))    


        #-------------------------------------

        tangle_type_new = Tex('T-tangle').scale(0.6)
        tangle_type_new.next_to(tangle_to_factorize, DOWN)

        self.play(ReplacementTransform(tangle_type, tangle_type_new, run_time = runtime))

        tangle_type = tangle_type_new

        operation_new = Tex('Removing $T_3$').scale(0.6)
        operation_new.next_to(current_operation, DOWN)

        self.play(ReplacementTransform(operation, operation_new, run_time = runtime))

        operation = operation_new

        r_t3 = Tangle("1,1' 2,3' 3,2' 4,4'", size = size)
        r_t3.set_edge_color("2,3'", edge_col[1])
        r_t3.set_edge_color("4,4'", edge_col[2])
        r_t3.set_edge_color("1,1'", edge_col[0])
        r_t3.set_edge_color("3,2'", edge_col[3])

        self.play(TransformTangle(r2, r_t3))

        tex3 = Tex('$T_3$')
        self.play(ApplyMethod(queue.shift,  0.5 * RIGHT))
        tex3.next_to(queue, LEFT / 2)
        queue.add(tex3)
        self.play(Write(tex3))

        operation_new = Tex('Removing $T_2$').scale(0.6)
        operation_new.next_to(current_operation, DOWN)

        self.play(ReplacementTransform(operation, operation_new, run_time = runtime))

        operation = operation_new

        i_n = Tangle.get_prime_tangle("In", 4, size = size)
        i_n.set_edge_color("1,1'", edge_col[0])
        i_n.set_edge_color("2,2'", edge_col[1])
        i_n.set_edge_color("3,3'", edge_col[3])
        i_n.set_edge_color("4,4'", edge_col[2])

        self.play(TransformTangle(r_t3, i_n))

        tex4 = Tex('$T_2$', size = size)
        self.play(ApplyMethod(queue.shift,  0.5 * RIGHT))
        tex4.next_to(queue, LEFT / 2)
        queue.add(tex4)
        self.play(Write(tex4))

        tangle_type_new = Tex('Identity').scale(0.6)
        tangle_type_new.next_to(tangle_to_factorize, DOWN)

        self.play(ReplacementTransform(tangle_type, tangle_type_new, run_time = runtime))

        operation_new = Tex('Done').scale(0.6)
        operation_new.next_to(current_operation, DOWN)

        self.play(ReplacementTransform(operation, operation_new, run_time = runtime))

        self.play(ShowPassingFlashAround(queue))

        self.wait()

class MovingTest(Scene):
    def construct(self):
        rna = Rna("AGCUCUUAGCUACGAGGCUGCUA")
        self.play(Write(rna))

        rna.start_updater() 
        self.wait(20)

