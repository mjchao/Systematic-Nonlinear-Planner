EECS 492: Artificial Intelligence, Project 2
====================
In this project, we use Planning Domain Definition Language (PDDL) to describe the initial state of a world containing crates, cranes, robots, and locations. Then, we specify a desired state of the world using PDDL. Finally, we apply our search algorithm to produce an ordered plan that when executed on the initial state will produce the desired state.

Project Files Summary
====================
Variables.py : Defines an object that tracks variable names

Configure.py : Defines symbols associated with the project

Structures.py : Classes for predicates, actions, planner, links, threats, ordering constraints, and others. (You must implement the method "adds" for the "Action" class)

Read.py : Functions for reading in files and printing out files

planner.py : The plan search function (you implement)

topSort.py : Provides functions for doing topological sort of plans and checking order consistency

main.py : The main function, takes command line arguments

Running the Program
===================

The following is what I did to produce the output. I wouldn't make any guarantees about the programming running correctly if one does not adhere to the following process.

1. Log on to CAEN with the following command: `ssh -X login-course.engin.umich.edu`

2. `cd` to the directory in which the program files are stored.

3. Run the program with CAEN using the following command: `python planner.py \<input filename\> \<output filename\>` . For example you could run, `python planner.py test1.txt test1.out` to execute test case 1, and the output will be stored in `test1.out`

4. The solution plan will be written to the output file. The information printed to standard output is for the user if s/he is interested in the status of the program.
