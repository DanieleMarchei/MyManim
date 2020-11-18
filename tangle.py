from manim import *
import numpy as np

class AbsTangle(Group):
    CONFIG = {
        "dot_radius": 0.08,
        "stroke_width": 0,
        "color": WHITE,
        "scale" : 0.5,
        "point" : ORIGIN,
        "size" : 1
    }

    

    def __init__(self, **kwargs):
        self.edges = {}
        Group.__init__(self, **kwargs)

    def set_edge_color(self, name, value):
        e = self.get_edge(name)
        if e is None:
            raise(Exception("Edge is None"))
        e.set_color(value)
    
    def get_edge(self, name):

        a, b = self.build_inv(name)[0]
        

        p1 = self.submobjects[a]
        p2 = self.submobjects[b]
        e = self.edges[(a,b)]

        return Group(p1,p2,e)

    def add_edge(self, name, **kwargs):
        a, b = self.build_inv(name)[0]
        p1 = self.submobjects[a]
        p2 = self.submobjects[b]


        e = None
        if a % 2 != b % 2:
            e = Line(p1.get_arc_center(),p2.get_arc_center(), **kwargs)
        else:
            if a % 2 != 0:
                e = ArcBetweenPoints(p1.get_arc_center(),p2.get_arc_center(), angle= - TAU / 4, **kwargs)
            else:
                e = ArcBetweenPoints(p1.get_arc_center(),p2.get_arc_center(), **kwargs)
        self.add(e)

        self.edges[(a,b)] = e

        return e
    
    def build_inv(self, tangle_inv):
        '''
        tangle_inv example : 1,1' 2,2' 3,4, 5,3' 4',5'
        '''
        str_pairs = tangle_inv.split(" ")
        pairs = []
        for s in str_pairs:
            str_a, str_b = s.split(",")
            a, b = None, None
            if "'" in str_a:
                _a = int(str_a[0])
                a = 2*_a - 1
            else:
                _a = int(str_a)
                a = 2*_a - 2
            if "'" in str_b:
                _b = int(str_b[0])
                b = 2*_b - 1
            else:
                _b = int(str_b)
                b = 2*_b - 2
            
            pairs.append((a, b))
        
        return pairs

    def get_edge_attached_to(self, dot):
        a = self.build_inv(dot + ",1'")[0][0]
        b = None
        for k in self.edges.keys():
            if a in k:
                a,b = k
                break
        
        p1 = self.submobjects[a]
        p2 = self.submobjects[b]
        e = self.edges[(a,b)]

        return Group(p1,p2,e)
    
    def get_edges(self):
        edges = []
        for edge in self.submobjects:
            if isinstance(edge, ArcBetweenPoints) or isinstance(edge, Line):
                edges.append(edge)
        return edges
    
    def get_dots(self):
        dots = []
        for dot in self.submobjects:
            if isinstance(dot, Dot):
                dots.append(dot)
        return dots
    
    def get_texs(self):
        texs = []
        for tex in self.submobjects:
            if isinstance(tex, Tex):
                texs.append(tex)
        return texs

class Tangle(AbsTangle):

    def get_prime_tangle(name : str, N : int, **kwargs):
        inv = " ".join([f"{a+1},{a+1}'" for a in range(N)])
        if name == "I":
            pass
        elif name.startswith("U"):
            i = int(name[1])
            assert(1 <= i < N)
            inv = inv.replace(f"{i}'", "#")
            inv = inv.replace(f"{i+1},", "^," )
            inv = inv.replace("#", str(i + 1))
            inv = inv.replace("^", str(i) + "'" )
        elif name.startswith("T"):
            i = int(name[1])
            assert(1 <= i < N)
            inv = inv.replace(f"{i}'", "#")
            inv = inv.replace(f"{i+1}'", "^" )
            inv = inv.replace("#", str(i + 1) + "'")
            inv = inv.replace("^", str(i) + "'")
        return Tangle(inv, **kwargs)

    def __init__(self, str_inv, **kwargs):

        AbsTangle.__init__(self, **kwargs)
        self.inv = str_inv
        self.tuple_inv = self.build_inv(str_inv)
        self.N = len(self.tuple_inv)
        dot = Dot(**kwargs)
        doti = Dot(**kwargs).next_to(dot, direction = self.size * 2 * DOWN)
        dots = [dot, doti]
        for i in range(len(self.tuple_inv) - 1):
            _dot = Dot(**kwargs).next_to(dot, self.size * RIGHT)
            _doti = Dot(**kwargs).next_to(doti, self.size * RIGHT)
            
            dots.extend([_dot, _doti])
            
            dot = _dot
            doti = _doti


        texs = []
        num = 1
        for i,v in enumerate(dots):
            if i % 2 == 0:
                texs.append(Tex(str(num), **kwargs).next_to(v,.5 * UP).scale(self.scale))
            else:
                texs.append(Tex(str(num) + "'", **kwargs).next_to(v,.5 * DOWN).scale(self.scale))
                num += 1
        
        arcs = []
        for a,b in self.tuple_inv:
            p1, p2 = dots[a].get_arc_center(), dots[b].get_arc_center()
            e = None
            if a % 2 != b % 2:
                e = Line(p1,p2, **kwargs)
            else:
                if a % 2 != 0:
                    e = ArcBetweenPoints(p1,p2, angle= - TAU / 4, **kwargs)
                else:
                    e = ArcBetweenPoints(p1,p2, **kwargs)
            arcs.append(e)
            self.edges[(a,b)] = e
        
        objs = dots + arcs + texs
        self.add(*(objs))
        self.move_to(self.point)


    
    def __str__(self) -> str:
        return self.inv

class EmptyTangle(AbsTangle):

    def __init__(self, N, **kwargs):
        AbsTangle.__init__(self, **kwargs)
        self.N = N
        dot = Dot(**kwargs)
        doti = Dot(**kwargs).next_to(dot, direction = self.size * 2 * DOWN)
        dots = [dot, doti]
        for i in range(N - 1):
            _dot = Dot(**kwargs).next_to(dot, self.size * RIGHT)
            _doti = Dot(**kwargs).next_to(doti, self.size * RIGHT)
            
            dots.extend([_dot, _doti])
            
            dot = _dot
            doti = _doti
        
        texs = []
        num = 1
        for i,v in enumerate(dots):
            if i % 2 == 0:
                texs.append(Tex(str(num), **kwargs).next_to(v,.5 * UP).scale(self.scale))
            else:
                texs.append(Tex(str(num) + "'", **kwargs).next_to(v,.5 * DOWN).scale(self.scale))
                num += 1
        
        objs = dots + texs

        self.add(*(objs))
        self.move_to(self.point)


class TransformTangle(AnimationGroup):
    def __init__(self, tangle, target, **kwargs):
        
        N_m = len(tangle.submobjects)
        N_t = len(target.submobjects)
        assert(N_m == N_t)

        animations = []

        m_edges = tangle.get_edges()
        t_edges = target.get_edges()
        
        for e_m, e_t in zip(m_edges, t_edges):
            animations.append(ReplacementTransform(e_m, e_t, **kwargs))
        
        m_dots = tangle.get_dots()
        t_dots = target.get_dots()

        for d_m, d_t in zip(m_dots, t_dots):
            animations.append(ReplacementTransform(d_m, d_t, **kwargs))
        
        m_texs = tangle.get_texs()
        t_texs = target.get_texs()

        for t_m, t_t in zip(m_texs, t_texs):
            animations.append(ReplacementTransform(t_m, t_t, **kwargs))
        
        AnimationGroup.__init__(self, *animations, **kwargs)

class PutUnderTangle(AnimationGroup):
    def __init__(self, tangle, target, put_next_to = True, **kwargs):
        top_texs = [t for t in tangle.get_texs() if "'" not in t.tex_string]
        bottom_texs_target = [t for t in target.get_texs() if "'" in t.tex_string]

        tangle_animations = []
        amount = np.abs(target.get_bottom()[1] - target.get_dots()[1].get_arc_center()[1])

        if put_next_to:
            tangle_animations.append(ApplyMethod(tangle.next_to, target, DOWN, **kwargs))
        tangle_animations.append(ApplyMethod(tangle.shift, 2 * amount * UP + UP * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, **kwargs))

        tex_animations = []
        for tex in bottom_texs_target:
            tex_animations.append(ApplyMethod(tex.set_opacity, 0, **kwargs))
        
        for tex in top_texs:
            tex_animations.append(ApplyMethod(tex.set_opacity, 0, **kwargs))
        
        succession = Succession(*tangle_animations)
        group = AnimationGroup(*tex_animations)
        animations = [succession, group]
        AnimationGroup.__init__(self, *animations, **kwargs)

class Queue(Mobject):
    def __init__(self, mobject, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.add(mobject)
    
    def add(self, mobject):
        '''
        Enqueue the mobjects into the Queue. The first element of the input list will be the first element of the Queue.
        '''
        if self is mobject:
            raise ValueError("Mobject cannot contain self")
        self.submobjects = list_update(mobject, self.submobjects)
        return self
    
    def isempty(self):
        return len(self.submobjects) == 0