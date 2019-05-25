# Automate timetable creation using python and FET

## DONE
- Classes in different days have same timings.
- Classes in different days have same room
- Division of major into subgroups based on choices of minors
- Minor subgroup added in the 'compulsory' minor courses.
- Thursday 12-2 break time
- Lunch hour for everyone
- Minor subgroups for electives. 
    - Each subgroup added to two randomly selected minor-electives
    - If UWE requirement still not met, more courses added from minor dept UWEs which are not part of minor.

- Remove Zia's name from the course offering list. Replace with dummy TAs.
- Remove instructors from TAs name in large classes. Replace them with dummy TAs. 

- Adjust for CCC courses
    - Make groups of year wise students
    - Make four random groups of CCC courses
    - Added year group of students to yearwise CCC group.


## In progress


## TODO
- Add compactness constraint (minimal gaps) for students
- Add compactness constraint (minimal gaps) for faculty
- Simulation is taking long time to converge in 8am to 5 pm slot. For testing purpose, current simulation slots are from 8am to 9pm. 
    - Eventually try to shrink it to 5 pm.


- Make ajustments in the room allottment so that large class gets big rooms.


## Notes:
- Seems like major electives are treated as Compulsory for time-tabling purpose. Can this be relaxed? Lets leave it for now.
- Treat minor-electives as same as UWE for time-tabling purpose.
- UWE which are not part of minors, needs to provide a target audience for their course. Else, how about randomly mapping from students doing minors as target audience. 