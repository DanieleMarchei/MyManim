from scenes import *
from manim import *
import numpy as np
from my_config import *
from tangle import *
from rna import *
import pickle as pkl

config['pixel_height'] = 1080
config['pixel_width'] = 1920
config['frame_rate'] = 60

config["background_color"] = palette["bg"]

class TitleScreen(SlideScene):
    def construct(self):
        title = "A factorization algorithm\\\\for the Brauer Monoid"
        speaker_name = "Daniele Marchei"
        supervisor_name = "Emanuela Merelli"
        logo = "imgs/unicam.png"
        date = "18/11/2020"

        title = Tex(title, color = BLUE).scale(1.1).shift(2.5*UP)
        speaker_name = Tex(speaker_name).scale(0.7).next_to(title, 2*DOWN)
        date = Tex(date).scale(0.5).next_to(speaker_name, DOWN)

        supervisor = Tex(r'\textbf{Supervisor}').scale(0.5).move_to(DOWN)
        supervisor_name = Tex(supervisor_name).scale(0.7).next_to(supervisor, DOWN)


        texts = VGroup(title, speaker_name, date, supervisor, supervisor_name)

        t1a = Tangle.get_prime_tangle("T1", 4, size = 2, color = DARK_GRAY).next_to(title, 3 * LEFT)
        t1b = Tangle.get_prime_tangle("U1", 4, size = 2, color = DARK_GRAY).next_to(title, 3 * RIGHT)
        t2a = Tangle.get_prime_tangle("T2", 4, size = 2, color = DARK_GRAY).next_to(t1a, 2 * DOWN)
        t2b = Tangle.get_prime_tangle("U2", 4, size = 2, color = DARK_GRAY).next_to(t1b, 2 * DOWN)
        t3a = Tangle.get_prime_tangle("T3", 4, size = 2, color = DARK_GRAY).next_to(t2a, 2 * DOWN)
        t3b = Tangle.get_prime_tangle("U3", 4, size = 2, color = DARK_GRAY).next_to(t2b, 2 * DOWN)

        self.add(t1a, t1b, t2a, t2b, t3a, t3b)

        logo = ImageMobject(logo).next_to(supervisor_name, DOWN)
        self.play(Write(texts))
        self.play(FadeInFrom(logo, DOWN))


        self.wait()

class FactorTangle(SlideScene):
    def construct(self):

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

class RnaFolding(SlideScene):
    def construct(self):
        rna = Rna("AGCUCUUAGCUACGAGGCUGCUA")
        self.play(Write(rna))

        self.comment("Start Updater Fold")

        rna.start_updater() 
        self.wait(10)

        self.comment("Stop Updater Fold")

        rna.stop_updater()
        self.wait()
        rna.set_state("stretch")

        self.comment("Start Updater Stretch")

        rna.start_updater() 
        self.wait(10)

        self.comment("Stop Updater Stretch")

        rna.stop_updater()

        self.wait()

        self.play(ApplyMethod(rna.move_to, ORIGIN))
        self.wait()

        simple = rna.get_simple()
        print(simple)

        with open("rna.obj", "wb") as rna_file:
            pkl.dump(simple, rna_file)

class RnaToFinger(SlideScene):
    def construct(self):
        with open("rna.obj", "rb") as rna_file:
            rnaString, bonds = pkl.load(rna_file)
        
        rna = SimpleRna(rnaString, bonds)
        rna.move_to(ORIGIN)
        self.add(rna)

        delete_unbonded = AnimationGroup(*[ShrinkToCenter(nuc) for nuc in rna.nucleotides if not nuc.bonded_with])
        self.play(delete_unbonded)
        self.wait()
        
        dot_bonded = []
        dots = VGroup()
        for nuc in rna.nucleotides:
            if nuc.bonded_with:
                d = Dot(nuc.get_center())
                dots.add(d)
                dot_bonded.append(ReplacementTransform(nuc, d)) 

        self.play(*dot_bonded)
        self.wait()
        
        to_delete = [0,-1,-2,-3]
        lines = AnimationGroup(*[FadeOut(rna.lines[i]) for i in to_delete])
        self.play(lines)
        self.wait()

        # Create finger diagram
        finger1 = FingerDiagram(bonds)
        finger1.move_to(rna)
        for i,dot in enumerate(finger1.dots):
            dot.move_to(dots.submobjects[i])
        
        self.remove(rna)
        self.add(finger1)

        finger2 = FingerDiagram(bonds)
        finger2.move_to(finger1)
        # Oh well...
        self.clear()
        self.play(ReplacementTransform(finger1,finger2))
        self.wait()

        with open("finger.obj", "wb") as finger_file:
            pkl.dump(bonds, finger_file)

class FingerToTangle(SlideScene):
    def construct(self):
        with open("finger.obj", "rb") as finger_file:
            bonds = pkl.load(finger_file)
        
        finger = FingerDiagram(bonds)
        finger.move_to(ORIGIN)
        self.add(finger)

        arrow = Arrow(RIGHT * 5, UP * 3 + RIGHT, color = BLUE, path_arc = TAU / 4).scale(0.5)
        self.play(ShowCreation(arrow))
        self.wait()
        self.play(Uncreate(arrow))
        self.wait()

        dots1 = VGroup(*finger.dots[:len(bonds)])
        dots2 = VGroup(*finger.dots[len(bonds):])

        brace1 = Brace(dots1)
        t1 = brace1.get_text("Bottom").scale(0.7)
        brace2 = Brace(dots2)
        t2 = brace2.get_text("Top").scale(0.7)

        self.play(
            FadeInFrom(brace1, LEFT),
            FadeInFrom(t1, LEFT)
        )

        self.wait()

        self.play(
            ReplacementTransform(brace1, brace2),
            ReplacementTransform(t1, t2)
        )

        self.wait()

        self.play(
            FadeOutAndShift(brace2, RIGHT),
            FadeOutAndShift(t2, RIGHT)
        )

        self.wait()

        colors = [RED, BLUE, GREEN, PURPLE, YELLOW]
        apply_colors = []
        for bond,col in zip(finger.bond_lines, colors):
            apply = ApplyMethod(bond.set_color, col)
            apply_colors.append(apply)

        self.play(*apply_colors)
        self.wait()

        paths = []
        k = len(bonds) - 1
        for dot in finger.dots[len(bonds):]:
            arc = ArcBetweenPoints(dot.get_center(), finger.dots[k].get_center() + 2 * UP)
            move_along = MoveAlongPath(dot, arc, run_time = 2)
            paths.append(move_along)
            k -= 1
        
        finger.moving = True
        self.play(*paths)
        finger.moving = False
        self.wait()

        self.play(ApplyMethod(finger.move_to, ORIGIN))
        self.wait()

        lines = VGroup(*finger.lines)
        self.play(FadeOut(lines))
        self.wait()


        texs = VGroup()
        copy_top = finger.dots[len(bonds):].copy()
        copy_top.reverse()
        for i,dot in enumerate(copy_top):
            t = Tex(str(i+1)).next_to(dot, 0.5 * UP).scale(0.7)
            texs.add(t)

        for i,dot in enumerate(finger.dots[:len(bonds)]):
            t = Tex(str(i+1)+ "'").next_to(dot, 0.5 * DOWN).scale(0.7)
            texs.add(t)

        self.play(Write(texs))
        self.wait()

class Test(SlideScene):
    def construct(self):
        s = Dot()
        arc = ArcBetweenPoints(ORIGIN, UR)
        self.play(ShowCreation(s))
        self.play(MoveAlongPath(s, arc))
        self.wait()


class FullScene(SceneWithTimeStamps):
    def construct(self):
        TitleScreen(self).construct()
        self.clear()
        FactorTangle(self).construct()
        self.clear()
        RnaFolding(self).construct()
        self.clear()
        RnaToFinger(self).construct()
        self.clear()
        FingerToTangle(self).construct()
        self.clear()