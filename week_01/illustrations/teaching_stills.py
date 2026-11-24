"""Static Manim diagrams. Render with manim -s -r 2240,1000.

These still diagrams use self.add. Worked example
values come from the Metro Support fixture, except the explicitly labeled tie.
"""
from manim import *
config.frame_width=16
config.frame_height=50/7
config.background_color='#FCFCFA'
INK='#111827'; MUTED='#475569'; ORANGE='#BF3E05'; BLUE='#214AE8'; GREEN='#17745B'; RULE='#CBD5E1'
def label(scene,s,x,y,size=32,color=INK,bold=False):
    t=Text(s,font='Helvetica Neue',font_size=size,color=color,weight=BOLD if bold else NORMAL,line_spacing=1.1)
    t.move_to([x,y,0]);scene.add(t);return t
def panel(scene,title,body,x,y,width=4.4,height=3.4,color=BLUE):
    r=Rectangle(width=width,height=height,color=RULE,fill_color=WHITE,fill_opacity=1,stroke_width=2).move_to([x,y,0]);scene.add(r)
    label(scene,title,x,y+height/2-.55,30,color,True)
    body_text=label(scene,body,x,y-.25,30)
    if body_text.width > width-.28: body_text.scale_to_fit_width(width-.28)
def arrow(scene,x,y,x2,y2,color=ORANGE):scene.add(Arrow([x,y,0],[x2,y2,0],buff=.12,color=color,stroke_width=5))

class StoredAndDisplayed(Scene):
    def construct(self):
        panel(self,'Stored tickets','1001  open\n1003  resolved\n1004  new\n1009  new',-5.4,.25)
        panel(self,'Keep active','1001  open\n1004  new\n1009  new',0,.25)
        panel(self,'Require an agent','1001\nAgent 201',5.4,.25)
        arrow(self,-3.1,.25,-2.3,.25);arrow(self,2.3,.25,3.1,.25)
        label(self,'The stored table stays unchanged while the query builds its result.',0,-2.65,34,ORANGE,True)

class JoinGrain(Scene):
    def construct(self):
        panel(self,'One ticket','ticket_id  1003\nLow water pressure',-5.35,.6,height=2.9)
        panel(self,'Event / new_status','5005  open\n5006  in_progress\n5007  resolved',0,.6,height=2.9)
        panel(self,'Three joined rows','1003 + 5005\n1003 + 5006\n1003 + 5007',5.35,.6,height=2.9)
        arrow(self,-3.05,.6,-2.25,.6);arrow(self,2.25,.6,3.05,.6)
        label(self,'COUNT(*) on this join = 3     Distinct ticket IDs = 1',0,-1.9,35,ORANGE,True)
        label(self,'One output row is one ticket-event pair.',0,-2.65,32)

class SafeMigration(Scene):
    def construct(self):
        panel(self,'Add the field','source_channel\nNULL allowed',-5.35,.3)
        panel(self,'Preserve history','Existing 12 rows\nbecome unknown',0,.3)
        panel(self,'Set the contract','Allowed values\n+ NOT NULL\n+ future default',5.35,.3)
        arrow(self,-3.05,.3,-2.25,.3);arrow(self,2.25,.3,3.05,.3)
        label(self,'Rehearse inside BEGIN / ROLLBACK; verify before the committed run.',0,-2.6,32,ORANGE,True)

class ConstraintTruth(Scene):
    def construct(self):
        label(self,"CHECK (priority IN ('low', 'medium', 'high', 'urgent'))",0,2.6,31,ORANGE,True)
        panel(self,'high','Expression: TRUE\nCHECK accepts',-5.35,.25,height=2.7,color=GREEN)
        panel(self,'extreme','Expression: FALSE\nCHECK rejects',0,.25,height=2.7,color=ORANGE)
        panel(self,'NULL','Expression: UNKNOWN\nCHECK alone accepts',5.35,.25,height=2.7,color=BLUE)
        label(self,'A separate NOT NULL rule rejects a missing priority.',0,-2.3,36,ORANGE,True)
        label(self,'The supplied tickets table already declares priority NOT NULL.',0,-2.95,29,MUTED)

class LatestEventRule(Scene):
    def construct(self):
        label(self,'Illustrative tie: both events have exactly the same time',0,2.65,34,ORANGE,True)
        panel(self,'Event 7001','ticket 1001\n2026-02-15 12:00 UTC',-4,.55,width=6.4,height=2.8)
        panel(self,'Event 7002','ticket 1001\n2026-02-15 12:00 UTC',4,.55,width=6.4,height=2.8)
        label(self,'ORDER BY event_at DESC, event_id DESC',0,-1.6,35,BLUE,True)
        label(self,'7002 receives rn = 1.  The stated tie rule makes the result repeatable.',0,-2.5,31)

class WaitingWriter(Scene):
    def construct(self):
        panel(self,'Session A','Writes high / open\nUncommitted\nHolds the row lock',-5.35,.25)
        panel(self,'Ordinary reader','Sees medium / open\nCommitted values\nCan finish its read',0,.25,color=GREEN)
        panel(self,'Session B','Wants in_progress\nSame ticket 1004\nWaits for A',5.35,.25,color=ORANGE)
        label(self,'A rolls back: medium / in_progress     A commits: high / in_progress',0,-2.6,31,ORANGE,True)
