"""Static Manim teaching illustrations for CST4714 Week 10.

Render with Manim Community 0.22:
  manim -s -r 2240,960 --disable_caching --media_dir <build> week10_stills.py \
    ArrayMatchStill RepeatedSetStill ExpectedStateStill FilterProjectSortStill
Only self.add is used. No animation or movie is authored.
Values come from the Week 10 notebook and its six-ticket fixture.
"""
from manim import *

config.frame_width = 16
config.frame_height = 48 / 7
config.background_color = "#FCFCFA"
BG = "#FCFCFA"
INK = "#111827"
BLUE = "#214AE8"
MUTED = "#64748B"
RULE = "#CBD5E1"
PALE = "#F1F5F9"
GREEN = "#17745B"
AMBER = "#A34C18"
SANS = "Helvetica Neue"
MONO = "Menlo"


def t(s, size=34, color=INK, bold=False, mono=False):
    return Text(s, font=MONO if mono else SANS, font_size=size,
                color=color, weight=BOLD if bold else NORMAL, line_spacing=1.1)


def put(scene, s, x, y, size=34, color=INK, bold=False, mono=False):
    v=t(s,size,color,bold,mono).move_to([x,y,0]); scene.add(v); return v


def line(scene, a, b, color=RULE, width=2):
    v=Line([*a,0],[*b,0],color=color,stroke_width=width);scene.add(v);return v


def arrow(scene,a,b,color=BLUE):
    v=Arrow([*a,0],[*b,0],buff=.08,color=color,stroke_width=4,max_tip_length_to_length_ratio=.16);scene.add(v);return v


def event(scene, x, y, eid, kind, role):
    box=Rectangle(width=6.3,height=1.3,color=RULE,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([x,y,0]);scene.add(box)
    put(scene,str(eid),x-2.25,y,31,MUTED,mono=True)
    put(scene,kind,x-.15,y,33,BLUE if kind=='created' else INK,mono=True)
    put(scene,role,x+2.05,y,33,AMBER if role=='agent' else INK,mono=True)


class ArrayMatchStill(Scene):
    def construct(self):
        # Both lanes display the same two actual events, never invented records.
        for x in [-4,4]:
            put(self,"Ticket 1001 events",x,2.9,32,MUTED)
            put(self,"event_id",x-2.25,2.25,26,MUTED,mono=True)
            put(self,"type",x-.15,2.25,26,MUTED,mono=True)
            put(self,"actor_role",x+2.05,2.25,26,MUTED,mono=True)
            event(self,x,1.25,5001,'created','resident')
            event(self,x,-.3,5002,'assigned','agent')
        line(self,(0,3.1),(0,-3.1))
        # Across-element path visibly connects the two relevant values.
        line(self,(-4.8,.85),(-3.5,.85),BLUE,5)
        line(self,(-2.45,-.7),(-1.45,-.7),AMBER,5)
        line(self,(-4.15,.8),(-4.15,.5),BLUE,4)
        line(self,(-4.15,.5),(-7.45,.5),BLUE,4)
        line(self,(-7.45,.5),(-7.45,-1.3),BLUE,4)
        arrow(self,(-7.45,-1.3),(-4.6,-1.57),BLUE)
        arrow(self,(-1.95,-.95),(-3.1,-1.5),AMBER)
        put(self,"Separate dotted conditions",-4,-1.97,34,bold=True)
        put(self,"Both values occur somewhere",-4,-2.62,30)
        put(self,"Ticket matches",-4,-3.04,32,GREEN,True)
        # The right lane tests each intact event as a unit.
        for y in [1.25,-.3]:
            line(self,(.58,y+.55),(.58,y-.55),AMBER,4)
            line(self,(.58,y+.55),(.82,y+.55),AMBER,4)
            line(self,(.58,y-.55),(.82,y-.55),AMBER,4)
            put(self,"×",7.55,y,40,AMBER,True)
        put(self,"$elemMatch",4,-1.97,34,bold=True,mono=True)
        put(self,"No event contains both values",4,-2.62,30)
        put(self,"Ticket does not match",4,-3.04,32,AMBER,True)


def document(scene,x,y,status,assignee,emphasis=False):
    # A document silhouette keeps the state concrete without representing storage internals.
    w=4.35;h=2.65
    pts=[[-w/2,-h/2,0],[w/2,-h/2,0],[w/2,h/2-.36,0],[w/2-.36,h/2,0],[-w/2,h/2,0]]
    shape=Polygon(*pts,color=BLUE if emphasis else RULE,stroke_width=3,fill_color=WHITE,fill_opacity=1).move_to([x,y,0]);scene.add(shape)
    put(scene,"ticket_id 1099",x,y+.87,29,MUTED,mono=True)
    put(scene,"status",x,y+.3,26,MUTED,mono=True)
    put(scene,status,x,y-.18,31,BLUE if emphasis else INK,True,True)
    put(scene,assignee,x,y-.88,27,MUTED,mono=True)


class RepeatedSetStill(Scene):
    def construct(self):
        put(self,'$set  status = "in_progress", assignee_id = 202',0,2.95,34,mono=True)
        for x,label in [(-5.3,'Before'),(0,'After first update'),(5.3,'After the repeat')]:
            put(self,label,x,2.15,30,bold=True)
        document(self,-5.3,.38,'new','assignee_id absent')
        document(self,0,.38,'in_progress','assignee_id 202',True)
        document(self,5.3,.38,'in_progress','assignee_id 202',True)
        arrow(self,(-3.0,.38),(-2.35,.38))
        arrow(self,(2.35,.38),(3.0,.38))
        put(self,'matched 1',0,-1.5,33,INK,mono=True)
        put(self,'modified 1',0,-2.07,33,GREEN,True,True)
        put(self,'matched 1',5.3,-1.5,33,INK,mono=True)
        put(self,'modified 0',5.3,-2.07,33,AMBER,True,True)
        put(self,'No reset\nbetween updates',-5.3,-1.84,32,MUTED)
        line(self,(-7.5,-2.55),(7.5,-2.55))
        put(self,'The second filter still matches. The requested values are already stored.',0,-3.03,32)


class ExpectedStateStill(Scene):
    def construct(self):
        put(self,'Expected-state update on test ticket 1099',0,2.95,34,MUTED)
        document(self,-5.1,.45,'in_progress','assignee_id 202',True)
        put(self,'Stored document',-5.1,2.15,32,bold=True)
        put(self,'Filter also requires',.65,2.15,32,bold=True)
        put(self,'status = "new"',.65,1.5,34,mono=True)
        # Gate bars separate a permitted identity match from a failed state requirement.
        line(self,(-1.65,-1.0),(-1.65,1.0),BLUE,6)
        line(self,(-1.35,-1.0),(-1.35,1.0),BLUE,6)
        arrow(self,(-2.75,.45),(-1.85,.45))
        put(self,'×',.65,.45,70,AMBER,True)
        put(self,'State does\nnot match',.65,-.68,30,AMBER,True)
        line(self,(2.95,.45),(4.05,.45),RULE,4)
        put(self,'Requested change',5.4,2.15,32,bold=True)
        put(self,'status =',5.4,1.47,31,MUTED,mono=True)
        put(self,'"resolved"',5.4,.84,34,MUTED,mono=True)
        put(self,'No write',5.4,-.38,38,AMBER,True)
        put(self,'matched 0     modified 0',0,-1.83,36,INK,True,True)
        line(self,(-7.5,-2.42),(7.5,-2.42))
        put(self,'Status stays in_progress. Reload the document before deciding what to do next.',0,-2.96,30)


class FilterProjectSortStill(Scene):
    def construct(self):
        # Trace exactly three real fixture documents. Priority remains stored;
        # the projection hides it only in the returned result.
        put(self,'Filter chooses documents. Projection chooses fields. Sort orders results.',0,3.02,31,bold=True)
        put(self,'Three selected tickets from the six-ticket fixture; other fields are omitted here.',0,2.53,27,MUTED)
        columns=[(-5.7,4.0,'Before'),(-1.45,3.95,'1  Filter'),(2.4,3.2,'2  Project'),(5.95,3.2,'3  Sort')]
        for x,w,label in columns:
            put(self,label,x,1.92,31,BLUE if label!='Before' else INK,True)
        arrow(self,(-4.45,1.92),(-2.88,1.92))
        arrow(self,(-.30,1.92),(1.03,1.92))
        arrow(self,(3.65,1.92),(4.80,1.92))
        for x,label in [(-5.7,'ticket_id / status / priority'),(-1.45,'Keep active tickets'),(2.4,'Return two fields'),(5.95,'Descending ticket_id')]:
            v=t(label,23,MUTED)
            v.scale_to_fit_width(min(v.width,3.85 if x<0 else 3.1))
            v.move_to([x,1.38,0]);self.add(v)

        def card(x,y,w,tid,status,priority=None):
            box=RoundedRectangle(width=w,height=.73,corner_radius=.08,color=RULE,stroke_width=2,
                                 fill_color=WHITE,fill_opacity=1).move_to([x,y,0]);self.add(box)
            main=t(f'{tid}  {status}',23,INK,mono=True)
            main.scale_to_fit_width(min(main.width,w-.28))
            main.move_to([x,y+(.13 if priority is not None else 0),0]);self.add(main)
            if priority is not None:put(self,f'priority: {priority}',x,y-.19,20,MUTED,mono=True)

        rows=[(1001,'open','high',.68),(1003,'resolved','urgent',-.22),(1006,'in_progress','medium',-1.12)]
        for tid,status,priority,y in rows:card(-5.7,y,4.0,tid,status,priority)
        for tid,status,priority,y in rows:
            if status!='resolved':card(-1.45,y,3.95,tid,status,priority)
        put(self,'1003 is excluded',-1.45,-.22,24,AMBER)
        card(2.4,.68,3.2,1001,'open');card(2.4,-1.12,3.2,1006,'in_progress')
        card(5.95,.68,3.2,1006,'in_progress');card(5.95,-1.12,3.2,1001,'open')
        put(self,'Same documents',2.4,-.22,23,MUTED)
        put(self,'Same fields',5.95,-.22,23,MUTED)
        line(self,(-7.7,-1.60),(7.55,-1.60))
        put(self,'Selected IDs:\n1001, 1003, 1006',-5.7,-2.25,22,MUTED,mono=True)
        put(self,'{"status": {"$in":\n["new", "open",\n"in_progress"]}}',-1.45,-2.25,20,INK,mono=True)
        put(self,'{"_id": 0,\n"ticket_id": 1,\n"status": 1}',2.4,-2.25,20,INK,mono=True)
        put(self,'.sort(\n"ticket_id", -1\n)',5.95,-2.25,20,INK,mono=True)
        put(self,'These are conceptual steps. The stored documents are unchanged.',0,-3.08,26,bold=True)
