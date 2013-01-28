
:position:
  :title:
  :role:
  :type:
  :points:
  :key:
  :image:
  :warning:
  :error:


:transition:
  :title:
  :type:
  :from:
  :to:
  :opportunity:
  :key:
  :counter:
  :image:
  :video:
  :warning:
    what injuries to watch out for
  :error:
    common errors


:submission:
  :title:
  :type:
  :from:
  :opportunity:
  :key:

  :counter:
  :image:
  :video:
  :warning:
    what injuries to watch out for
  :error:

Draw from other "maps" of BJJ
-----------------------------

* http://mattsdailyjournal.files.wordpress.com/2012/03/jiu-jitsu-univ-mindmap.jpg


Countermove
-----------

It's useful to know both the opportunity that makes a move possible,
and a countermove that will block it.  These relate directly to 
what you need to control your opponent, to prevent them from
being able to make a given countermove.  

Countermove should be described in terms of

* where the countermove "leads to", i.e. it could itself be a 
  transition to a new position, or an actual submission.  In those
  cases I just need a link to that says that move can counter this
  move.
* control: "opportunity" is all about controlling some key part of
  the opponent's body (legs, hips, torso, shoulders, head, arms, 
  hands) so you can act on them while preventing them from countering
  effectively.  You want to understand what each control is for, e.g.
  to prevent them from posting, or to stop them from turning to take
  your back.

Seems like countermoves divide into two types:

* "neutralizer": blocks your move without transitioning to a new
  position
* "countermove": actually a transition (or even a submission)
  that takes you to a new position.  


How to handle variations?  For the moment I can just pile it on
one page.  Later I can try to sort them out in a nice interface.


Simple interface proposal
-------------------------

* plan to use this via mobile device on the mat.
* minimize typing, aim for just clicking on touch screen.
  But how to achieve this?  Could pose a challenge screen,
  where you think through your answer without typing anything,
  then jump to an answers screen where you see the answer(s)
  (and possibly score which one(s) you got right).

Screens

* "you are in position X: what can you do?"
* "you want to do X: how exactly do you do it?"
* "opponent is doing such-and-such: what do you do?"

Could use "adventure"-style role-playing game FSA to string
these together in a plausible flow.

Could tie this to warmups that exercise a specific move,
e.g. "triangle" hip raises.

Position screen
...............

Purpose: to build awareness of all the possible moves and dangers
in a given position.

some random variables to make it less predictable and more useful as
mental exercise for sparring:

* your role in the position: D vs. A
* whether to ask you what you can do vs. what to watch out for from
  your opponent
* prompt you with possible variations (e.g. posts his arm) vs. keep
  it generic.  The former tests understanding of specific key opportunities,
  whereas the latter tests understanding all your options.
* whether to segue to a specific transition or submission from this
  list.

Transition or submission screen
...............................

Purpose: to practice a given move either on the mat or in your mind

random vars:

* your role: making the move vs. resisting or countering it.
* whether to ask you the sequence of moves or the keys to success.
* possible variations: 

Easiest path for moving this forward
....................................

* focus right now on running this in its current form
  (as a CherryPy server) and adding content (on laptop),
  but *access* it from smartphone or ipad.

* later explore generating static pages using something
  like Pelican, which you could view directly on smartphone
  even offline.

