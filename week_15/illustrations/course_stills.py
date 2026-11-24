"""Editable static Manim diagrams for CST4714 weeks11–15.
Run: manim -s -r 2240,960 --disable_caching --media_dir build course_stills.py Grain Recovery RepeatImport VersionGuard Populations
These are teaching diagrams of the supplied fixture, not screenshots or performance measurements.
"""
from manim import *
config.frame_width=16;config.frame_height=48/7;config.background_color='#FCFCFA'
INK='#111827';BLUE='#214AE8';GREY='#64748B';RULE='#CBD5E1';GREEN='#17745B';AMBER='#A34C18'
def text(scene,value,x,y,size=32,color=INK,bold=False,width=None):
 o=Text(value,font='Helvetica Neue',font_size=size,color=color,weight=BOLD if bold else NORMAL)
 if width and o.width>width:o.scale_to_fit_width(width)
 o.move_to([x,y,0]);scene.add(o);return o
def arrow(scene,x1,y1,x2,y2,color=BLUE):scene.add(Arrow([x1,y1,0],[x2,y2,0],buff=.1,color=color,stroke_width=4,max_tip_length_to_length_ratio=.18))
def rule(scene,y):scene.add(Line([-7.4,y,0],[7.4,y,0],color=RULE))
class Grain(Scene):
 def construct(self):
  text(self,'A ticket row and an event row count different things',0,2.95,36,bold=True)
  text(self,'Active tickets',-4,2.1,32,BLUE,True);text(self,'After default $unwind',4,2.1,32,BLUE,True)
  for j,(a,b) in enumerate([('1001 · 2 events','1001 · assigned'),('1002 · 1 event','1001 · created'),('1004 · empty array','1002 · created')]):
   y=1.15-j*.85;text(self,a,-4,y,32);text(self,b,4,y,32)
  arrow(self,-1,0.3,1,0.3)
  text(self,'1004 emits no event row',4,-1.55,29,AMBER)
  rule(self,-2.15);text(self,'3 ticket rows ≠ 3 event rows',0,-2.65,38,bold=True)
class Recovery(Scene):
 def construct(self):
  text(self,'An independent artifact lets us recover an earlier value',0,2.95,34,bold=True)
  for x,title,lines in [(-5.1,'Atlas source',['5 tickets','1004: Broken bench slat']), (0,'Saved Extended JSON',['5 saved documents','1004: Broken bench slat']), (5.1,'Separate Atlas target',['5 tickets','1004: wrong subject'])]:
   text(self,title,x,1.95,30,BLUE,True,width=4.65)
   text(self,lines[0],x,.95,32)
   text(self,lines[1],x,.15,26,AMBER if x==5.1 else INK,width=4.65)
  arrow(self,-2.75,.85,-2.25,.85);arrow(self,2.35,.85,2.85,.85)
  text(self,'Keep source unchanged',-5.1,-1.0,26,GREY,width=4.6)
  text(self,'Repair 1004 from this copy',0,-1.0,28,GREEN,width=4.7)
  arrow(self,1.8,-1.6,5.0,-1.6,GREEN)
  rule(self,-2.15);text(self,'Count passes. Compare IDs, types, and complete values.',0,-2.7,32,bold=True)
class RepeatImport(Scene):
 def construct(self):
  text(self,'A stable source ID makes a repeated import repeatable',0,2.95,34,bold=True)
  for x,label,count in [(-5.2,'Empty target','0'),(0,'After first import','75'),(5.2,'After second import','75')]:
   text(self,label,x,1.9,30,BLUE,True,width=4.8);text(self,count,x,.5,78,bold=True)
  arrow(self,-3.45,.5,-1.55,.5);arrow(self,1.7,.5,3.5,.5)
  text(self,'Key: cveID → SQL cve_id',0,-1.15,34)
  rule(self,-2.0);text(self,'Do not reset before the repeat. Check fields as well as counts.',0,-2.65,31,bold=True)
class VersionGuard(Scene):
 def construct(self):
  text(self,'A delayed older state must not replace a newer state',0,2.95,34,bold=True)
  text(self,'Delivery order for ticket 1008',0,2.05,29,GREY)
  for x,v in [(-5.2,'17'),(-1.75,'17 again'),(1.75,'18'),(5.2,'16 late')]:text(self,v,x,1.1,35,BLUE,True)
  arrow(self,-4.1,1.1,-3,1.1);arrow(self,-.6,1.1,.7,1.1);arrow(self,2.65,1.1,3.8,1.1)
  text(self,'Guard enabled',-4.0,-.2,32,BLUE,True);text(self,'Guard disabled',4.0,-.2,32,AMBER,True)
  text(self,'closed · version 18',-4,-1.1,38,GREEN,True);text(self,'open · version 16',4,-1.1,38,AMBER,True)
  rule(self,-2.0);text(self,'This model uses complete-state events and one ordered version per ticket.',0,-2.65,28)
class Populations(Scene):
 def construct(self):
  text(self,'The active backlog includes an unassigned ticket',0,2.95,36,bold=True)
  text(self,'All active ticket IDs',-4.8,2.0,30,BLUE,True);text(self,'1, 3, 4',-4.8,.95,52,bold=True)
  text(self,'Assigned',.3,2.0,30,BLUE,True);text(self,'1, 4',.3,.95,48,bold=True)
  text(self,'Unassigned',5.3,2.0,30,AMBER,True);text(self,'3',5.3,.95,48,bold=True)
  arrow(self,-2.8,.9,-1.5,.9);text(self,'+',2.8,.95,40,GREY)
  text(self,'Staff report: Agent 201 = 1, Agent 202 = 1, Agent 203 = 0',0,-.5,31)
  rule(self,-1.55);text(self,'3 active = 2 assigned active + 1 unassigned active',0,-2.25,35,bold=True)
  text(self,'Zero matched tickets is not a missing staff row.',0,-2.95,28,GREY)
