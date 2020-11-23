import enum
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

    def fold(self, mobject, dt):
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
                        #yeah I know, cuncurrency is hard
                        if a.bonded_with != None:
                            continue
                        #else, bond with it
                        mobject.set_bond(a)
                        a.set_bond(mobject)
                        m_i = self.get_index_of(mobject)
                        a_i = self.get_index_of(a)
                        sign = 1 if m_i > a_i else -1
                        arc = Line(mobject.get_center(), a.get_center(), path_arc = sign * TAU / 2)
                        self.arc_attached_to[arc] = (mobject, a)
                        arc.add_updater(self.bondUpdater)
                        self.add_to_back(arc)
        
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

    def stretch(self, mobject, dt):
        i = self.get_index_of(mobject)
        objective_point = self.point + 0.35*RIGHT*i
        s = objective_point - mobject.get_center()
        s = s * self.gamma * 2
        mobject.shift(s)

    def rnaUpdater(self, mobject, dt):
        if not self.can_update:
            return
        
        if self.state == "fold":
            self.fold(mobject, dt)
        elif self.state == "stretch":
            self.stretch(mobject, dt)

    def lineUpdater(self, mobject, dt):
        if not self.can_update:
            return

        a,b = self.line_attached_to[mobject]
        mobject.set_start_and_end_attrs(a.get_center(), b.get_center())
        mobject.generate_points()
    
    def bondUpdater(self, mobject, dt):
        if not self.can_update:
            return

        a,b = self.arc_attached_to[mobject]

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
        
        self.state = "fold"
        self.rnaString = rnaString
        self.n_nucletides = len(rnaString)
        self.point = point

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
        self.arc_attached_to = {}

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

        #this is a very ugly hack
        mobjects[-2], mobjects[-3] = mobjects[-3], mobjects[-2]
        mobjects[-1], mobjects[-2] = mobjects[-2], mobjects[-1]

        self.nucleotides = [t for t in mobjects if isinstance(t, Nucleotide)]
        self.neighs = {}
        self.indexes = {}
        
        VGroup.__init__(self, *mobjects, **kwargs)

        self.add_updater(self.center_rna)

    def get_index_of(self, obj):
        if obj in self.indexes:
            return self.indexes[obj]
        for i,t in enumerate(self.nucleotides):
            if t == obj:
                self.indexes[obj] = i
                return i

    def get_neigh(self, tex, distance = 1):
        if (tex, distance) in self.neighs:
            return self.neighs[(tex, distance)]

        N = len(self.nucleotides) - 1
        index = self.get_index_of(tex)
        
        neigh = []
        for i in range(distance):
            if index - i > 0:
                neigh.append(self.nucleotides[index - i - 1])

            if index + i < N:
                neigh.append(self.nucleotides[index + i + 1])

        self.neighs[(tex, distance)] = neigh

        return neigh

    def start_updater(self):
        self.can_update = True
    
    def stop_updater(self):
        self.can_update = False
    
    def set_state(self, state):
        self.state = state

    def get_simple(self):
        bonds = []
        for nucleotide in self.nucleotides:
            if nucleotide.bonded_with:
                i,j = self.get_index_of(nucleotide), self.get_index_of(nucleotide.bonded_with)
                if (i,j) not in bonds and (j,i) not in bonds:
                    bonds.append((i,j))
        return (self.rnaString, bonds)

class SimpleRna(VGroup):

    def lineUpdater(self, mobject, dt):
        if not self.can_update:
            return

        a,b = self.line_attached_to[mobject]
        mobject.set_start_and_end_attrs(a.get_center(), b.get_center())
        mobject.generate_points()
    
    def bondUpdater(self, mobject, dt):
        if not self.can_update:
            return

        a,b = self.arc_attached_to[mobject]

        mobject.set_start_and_end_attrs(a.get_center(), b.get_center())
        mobject.generate_points()

    def __init__(self, rnaString, bonds, point = 5 * LEFT):
        VGroup.__init__(self)

        self.rnaString = rnaString
        self.bonds = bonds
        self.point = point
        self.can_update = False

        self.indexes = {}

        self.nucleotides = []
        for i,n in enumerate(rnaString):
            nuc = Nucleotide(n)
            nuc.move_to(self.point + 0.35*RIGHT*i)
            self.nucleotides.append(nuc)
        


        self.bond_lines = []
        self.arc_attached_to = {}
        for bond in bonds:
            i,j = bond
            a,b = self.nucleotides[i], self.nucleotides[j]
            a.set_bond(b)
            b.set_bond(a)
            line = Line(a.get_center(), b.get_center(), path_arc = - TAU / 2)
            line.add_updater(self.bondUpdater)
            self.arc_attached_to[line] = (a,b)
            self.bond_lines.append(line)

        self.lines = []
        self.line_attached_to = {}
        for i,v in enumerate(self.nucleotides):
            if i == len(self.nucleotides) - 1:
                break
            
            a,b = self.nucleotides[i], self.nucleotides[i+1]
            line = Line(a.get_center(), b.get_center(), width = 1)
            line.add_updater(self.lineUpdater)
            self.line_attached_to[line] = (a,b)
            self.lines.append(line)
        
        self.add(*self.lines)
        self.add(*self.bond_lines)
        self.add(*self.nucleotides)

    def start_updater(self):
        self.can_update = True
    
    def stop_updater(self):
        self.can_update = False

class FingerDiagram(VGroup):

    def lineUpdater(self, mobject, dt):
        if not self.can_update:
            return
        
        a,b = self.line_attached_to[mobject]
        mobject.set_start_and_end_attrs(a.get_center(), b.get_center())
        mobject.generate_points()
    
    def bondUpdater(self, mobject, dt):
        if not self.can_update:
            return

        a,b = self.arc_attached_to[mobject]

        if self.moving:
            i,j = 0,0
            i = self.dots.index(a)
            j = self.dots.index(b)
            l = len(self.bonds)
            is_top_or_bottom = i > l and j > l or i < l and j < l
            if not is_top_or_bottom:
                mobject.set_path_arc(mobject.path_arc + dt * 1.5)

        mobject.set_start_and_end_attrs(a.get_center(), b.get_center())
        mobject.generate_points()


    def __init__(self, bonds, point = 5 * LEFT):
        VGroup.__init__(self)

        self.can_update = True
        self.moving = False

        d = {}
        flattened = [x for b in bonds for x in b]
        flattened = sorted(flattened)
        for i,v in enumerate(flattened):
            d[v] = i

        self.bonds = {}
        for bond in bonds:
            a = d[bond[0]]
            b = d[bond[1]]
            self.bonds[a] = b
        
        self.dots = []
        for i in range(len(flattened)):
            dot = Dot(point + 0.8*RIGHT*i)
            self.dots.append(dot)

        self.bond_lines = []
        self.arc_attached_to = {}
        for bond in self.bonds.items():
            i,j = bond
            a,b = self.dots[i], self.dots[j]
            line = Line(a.get_center(), b.get_center(), path_arc = - TAU / 2)
            self.arc_attached_to[line] = (a,b)
            line.add_updater(self.bondUpdater)
            self.bond_lines.append(line)

        self.lines = []
        self.line_attached_to = {}
        for i,v in enumerate(self.dots):
            if i == len(self.dots) - 1:
                break
            
            a,b = self.dots[i], self.dots[i+1]
            line = Line(a.get_center(), b.get_center(), width = 1)
            self.line_attached_to[line] = (a,b)
            line.add_updater(self.lineUpdater)
            self.lines.append(line)
        
        self.add(*self.lines)
        self.add(*self.bond_lines)
        self.add(*self.dots)
        

    def start_updater(self):
        self.can_update = True
    
    def stop_updater(self):
        self.can_update = False