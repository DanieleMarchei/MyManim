from manim import *
import numpy as np


class Nucleotide(VGroup):

    CONFIG = {
        "padding" : 0.05
    }

    def __init__(self, letter : chr):
        self.letter = str(letter).upper()
        self.tex = Tex(letter).scale(0.5)
        self.circle = Circle(color = WHITE, stroke_width = 1)
        self.circle.surround(self.tex)
        self.circle.set_fill(BLACK, opacity= 1)
        VGroup.__init__(self, self.circle, self.tex)

        self.diameter = 2 * np.linalg.norm(self.circle.get_center() - self.circle.get_bottom()) + self.padding

        self.bonded_with = None
    
    def set_bond(self, other):
        self.bonded_with = other

        color = None
        bond_type = self.letter + other.letter
        if bond_type in ["AU", "UA"]:
            color = GREEN
        elif bond_type in ["CG", "GC"]:
            color = RED
        elif bond_type in ["UG", "GU"]:
            color = BLUE

        self.tex.set_color(BLACK)
        self.circle.set_fill(color, opacity= 1)

class Rna(VGroup):

    CONFIG = {
        "gamma" : 0.005,
    }

    def rnaUpdater(self, mobject, dt):
        if not self.can_update:
            return

        base = mobject.letter
        s = np.zeros((3,))

        p = mobject.get_center()
        adj = self.get_neigh(mobject)

        for n in self.submobjects:
            v = n.get_center() - p
            if n in adj:
                # if the adjs are far apart, bring them closer
                if np.linalg.norm(v) >= 2 * mobject.diameter:
                    s += v
                if np.linalg.norm(v) <= mobject.diameter:
                    s -= v
            else:
                # if other nucleotides are too close, push them afar
                if np.linalg.norm(v) < mobject.diameter:
                    s -= v

        
        forbidden = self.get_neigh(mobject,3)
        
        #if the nucleotide is not bonded
        if mobject.bonded_with == None:
            for b in self.attracted_by[base]:
                for a in self.basis[b]:
                    if a in forbidden:
                        continue
                
                    if a.bonded_with != None:
                        continue
                    
                    v = a.get_center() - p
                    
                    #if one possible bonding is far, bring it closer
                    if np.linalg.norm(v) > mobject.diameter:
                        s += 0.5 * v
                    else:
                        #else, bond with it
                        mobject.set_bond(a)
                        a.set_bond(mobject)
        
        #if it is bonded
        if mobject.bonded_with != None:
            a = mobject.bonded_with
            v = a.get_center() - p
            #the bond HAVE to be very clese
            if np.linalg.norm(v) >= mobject.diameter:
                s += 5 * v
            else:
                s -= v

        for b in self.repelled_by[base]:
            for r in self.basis[b]:
                v = r.get_center() - p
                if np.linalg.norm(v) <= 1:
                    s -= v

        s *= self.gamma
        mobject.shift(s)


    def lineUpdater(self, mobject, dt):
        if not self.can_update:
            return

        a,b = self.line_attached_to[mobject]
        mobject.set_start_and_end_attrs(a.get_center(), b.get_center())
        mobject.generate_points()

    def center_rna(self, rna, dt):
        if not self.can_update:
            return
        p = self.get_center()
        o = ORIGIN
        v = o - p
        self.shift(v * dt)

    def __init__(self, rnaString : str, point = 5 * LEFT, closeness = 2, **kwargs):

        texs = []
        self.basis = {
            "A" : [],
            "C" : [],
            "G" : [],
            "U" : []
        }

        self.attracted_by = {
            "A" : ["U"],
            "C" : ["G"],
            "G" : ["C", "U"],
            "U" : ["A", "G"]
        }

        self.repelled_by = {
            "A" : ["G", "C", "A"],
            "C" : ["C", "U", "A"],
            "G" : ["A", "G"],
            "U" : ["U", "C"],
        }

        self.can_update = False

        for x, t in enumerate(rnaString):
            pos = np.zeros(3,)
            pos[0] = x / closeness
            pos[1] = np.sin(pos[0])
            pos += point
            tex = Nucleotide(t)
            tex.move_to(pos)
            tex.add_updater(self.rnaUpdater)
            self.basis[t.upper()].append(tex)

            texs.append(tex)


        self.line_attached_to = {}

        mobjects = []
        for i, tex in enumerate(texs):
            neigh = []
            if i > 0:
                neigh.append(texs[i - 1])

            if i < len(texs) - 1:
                neigh.append(texs[i + 1])

            lines = []
            for n in neigh:
                line = Line(tex.get_center(), n.get_center())
                line.set_stroke(width = 1)
                line.add_updater(self.lineUpdater)
                self.line_attached_to[line] = [tex, n]
                lines.append(line)

            mobjects = list_update(mobjects, lines + neigh)
        
        VGroup.__init__(self, *mobjects, **kwargs)

        self.add_updater(self.center_rna)

    def get_neigh(self, tex, distance = 1):
        N = len(self.submobjects) - 1
        index = None

        for i,t in enumerate(self.submobjects):
            if t == tex:
                index = i
                break
        
        neigh = []
        for i in range(distance):
            if index - i > 0:
                neigh.append(self.submobjects[index - i - 1])

            if index + i < N:
                neigh.append(self.submobjects[index + i + 1])

        return neigh

    def start_updater(self):
        self.can_update = True
    
    def stop_updater(self):
        self.can_update = False