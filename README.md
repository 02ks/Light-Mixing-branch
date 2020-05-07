# LightMixing
**Note: This ReadMe was updated toward the end of the year. It is mostly a update to help those who will work on this project after us. Much of our code can look very complicated, but at the core they simply are of two things: a function, or code to make sure that function runs without issue**

Installation:

Light Mixing requires:
  - kivy
  - python
  - Pidev (Can be found on the DPEA github; typically part of the setup for kivy; ask Mr. Harlow for clarification)
  - Light Mixing (at least hardware to run code on)

Trouble Shooting:

- Firstly, make sure you are not editing the main repository. That code should remain unchanged until new working version. Instead, edit Light Mixing Branch, a respository that can be found through Alex's github (IncrediblyOriginalUsername)
- If you are having problems with our code (i.e. it's not working correctly when run on Light Mixing), feel free to double check with the code on the official Light Mixing repository on github. Some of our code on Light Mixing branch is still in development (Especially code like that of the color picker) and it is typically buggy.
- When working with the actual physical project various issues can occur. If one of the lights moves to the side on it's own,
it's likely due to a faulty connection down on the bottom electrical area. If you can't fix it there, you can modify the movement.
code slightly to fix the issue. Sometimes motors decide to move faster or slower for no reason, mostly when running the setup
function. I have no idea why or how this happens but 95% of the time the setup still ends up working despite the oddities. 
This can be considered a bug but for now it's not really an issue. If it is in the future, it may possibly be fixed by added 
delay in the right spots as in the past similar but more dire issues of motors just not moving occured due to not enough delay. 

What to do next:

  Software:
  
    GUI: Make things look better. That's about it. The GUI as it is is functional and moderately ok, but it lacks proper style.
    
    Main code: Fix all variables that havent't been fixed yet. Add comments. Lots of comments that explain EXACTLY how things work. Also, the color picker is something that we were unable to finish. The functions work but it needs a lot of adjustments.
  
  Hardware:  Add panels, not now but whenever possible. Most of the panels have already been added to the cut list, but the panel in between the lights and the panel next to the electrical panel needs to be designed. After makeing them on solidworks, you will need to make dxfs of them and put them on the cut list to be routed. 
  In addition to panels, Light Mixing will also need to have its knobs reinstalled, and the anodized tube added to the project. The tube is meant to sheath the wires running up to the top of the machine. Originally, we had planned to add these in before the end of the year, but was unable to due to the coronavirus. 
  Green LED also should be changed so that it is a tri LED. We buy these LEDs from LED supply. You will also need to get a regular clear triple lens for the new LED. Use regular silicon or abrasive to attach the lens to the LED. Be careful to not get glue onto the lens. Ask Mr. Harlow for help on how to replace the LEDs. 
  Note: Wires on the electrical panels have already been somewhat organized and zip-tied, but it would be nice if someone were to go back and make it look even nicer.
  
**This is the most updated and complete version of light mixing, I originally just made a copy of the engineering
repository that eventually became this place. The stuff here will probably eventually be transfered back
to the original repository**


