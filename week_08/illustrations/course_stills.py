"""Static CST4714 worked-example diagrams. No animation is authored.
Render: manim -s -r 2240,960 --disable_caching --media_dir <build> course_stills.py OwnershipStill IndexEvidenceStill RecoveryStill DocumentGrowthStill
The diagrams show relationships between values in the teaching fixture.
"""
from manim import *
config.frame_width=16
config.frame_height=48/7
config.background_color='#FCFCFA'
INK='#111827';BLUE='#214AE8';MUTED='#64748B';RULE='#CBD5E1';GREEN='#17745B'
def label(s,x,y,size=32,color=INK,bold=False,mono=False):
 v=Text(s,font='Menlo' if mono else 'Helvetica Neue',font_size=size,color=color,weight=BOLD if bold else NORMAL,line_spacing=1.15)
 if v.width>15.1:v.scale_to_fit_width(15.1)
 return v.move_to([x,y,0])
def box(scene,x,y,w,h,title,lines):
 scene.add(Rectangle(width=w,height=h,color=RULE,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([x,y,0]));v=label(title,x,y+h/2-.42,30,BLUE,True)
 if v.width>w-.35:v.scale_to_fit_width(w-.35)
 scene.add(v)
 for i,s in enumerate(lines):
  v=label(s,x,y+h/2-1.08-i*.55,28)
  if v.width>w-.35:v.scale_to_fit_width(w-.35)
  scene.add(v)
def arrow(scene,x1,y1,x2,y2):scene.add(Arrow([x1,y1,0],[x2,y2,0],buff=.12,color=BLUE,stroke_width=4))
class OwnershipStill(Scene):
 def construct(self):
  self.add(label('One table. Two actors. Different visible rows.',0,2.96,38,bold=True))
  box(self,-5.2,.3,4.8,3.55,'Stored rows',['1, 2  → resident_101_lab','3, 4  → resident_102_lab','Nothing is deleted.'])
  box(self,0,.3,4.2,3.55,'SELECT policy',['owner_role','equals','current_user'])
  box(self,5.3,.3,4.8,3.55,'Returned IDs',['Resident 101 → 1, 2','Resident 102 → 3, 4','Same SELECT text.'])
  arrow(self,-2.75,.3,-2.1,.3);arrow(self,2.1,.3,2.85,.3)
  self.add(label('Resident 101 asking for ticket 3 receives zero rows.',0,-2.35,34,GREEN,True));self.add(label('Object privileges and this row policy are separate checks.',0,-3.0,29,MUTED))
class IndexEvidenceStill(Scene):
 def construct(self):
  self.add(label('Compare the answer before comparing the work.',0,2.96,38,bold=True))
  box(self,-5.2,.25,4.6,3.5,'Question',['status = open','newest opened_at first','tie: ticket_id descending'])
  box(self,0,.25,4.6,3.5,'Same ordered IDs',['1011','1007','1001'])
  box(self,5.2,.25,4.6,3.5,'Then inspect the plan',['scan + sort work','rows and buffers','index size + write cost'])
  arrow(self,-2.9,.25,-2.3,.25);arrow(self,2.3,.25,2.9,.25)
  self.add(label('CSV inspection predicts the answer, not the PostgreSQL plan.',0,-2.4,32,GREEN,True));self.add(label('Twelve rows can make a sequential scan a reasonable choice.',0,-3.0,29,MUTED))
class RecoveryStill(Scene):
 def construct(self):
  self.add(label('An artifact becomes evidence through a separate restore.',0,2.96,36,bold=True))
  box(self,-5.2,.3,4.6,3.5,'Source database',['3 users','3 tickets','5 events'])
  box(self,0,.3,4.6,3.5,'Custom-format dump',['pg_dump','retained bytes','not a running database'])
  box(self,5.2,.3,4.6,3.5,'Separate restore',['pg_restore','known values match','invalid status rejected'])
  arrow(self,-2.9,.3,-2.3,.3);arrow(self,2.3,.3,2.9,.3)
  self.add(label('Counts + relationships + known values + behavior',0,-2.35,34,GREEN,True));self.add(label('Do not restore a practice artifact over the source database.',0,-3.0,29,MUTED))
class DocumentGrowthStill(Scene):
 def construct(self):
  self.add(label('A useful preview does not replace the complete history.',0,2.96,37,bold=True))
  box(self,-5.2,.25,4.6,3.6,'Authoritative user',['user_id: 103','display_name:','Requester 103'])
  box(self,0,.25,4.6,3.6,'Ticket page',['ticket_id: 1003','requester_id: 103','preview: 5007, 5006'])
  box(self,5.2,.25,4.6,3.6,'Event → new state',['5005 → open','5006 → in_progress','5007 → resolved'])
  arrow(self,-2.3,.6,-2.9,.6);arrow(self,2.9,.6,2.3,.6)
  self.add(label('Reference the current name; define how the preview refreshes.',0,-2.4,31,GREEN,True));self.add(label('Later design discussion: today’s lab keeps all three events in both designs.',0,-3.0,27,MUTED))
