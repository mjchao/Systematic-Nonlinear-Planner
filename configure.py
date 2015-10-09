'''
configure.py
------------
This header contains enum definitions for all objects in the project
It also contains dictionaries that move between enums and strings.
For example, 
    Name2Predicate.at("adjacent") returns ADJACENT
    Predicate2Name.at(ADJACENT) returns "adjacent"

The file should be self explanatory from here.
'''

class Categories:
    LOCATIONS = 0
    ROBOTS = 1
    CRANES = 2
    PILES = 3
    CONTAINERS = 4
    INITIAL = 5
    GOAL = 6


Name2Category = {"locations" : Categories.LOCATIONS, "robots" : Categories.ROBOTS, "cranes" : Categories.CRANES, "piles" : Categories.PILES, "containers" : Categories.CONTAINERS, "initial" : Categories.INITIAL, "goal" : Categories.GOAL}


Category2Name = {Categories.LOCATIONS : "locations", Categories.ROBOTS : "robots", Categories.CRANES : "cranes", Categories.PILES : "piles", Categories.CONTAINERS : "containers", Categories.INITIAL : "initial", Categories.GOAL : "goal"}


class Predicates:
    ADJACENT = 0
    ATTACHED = 1
    BELONG = 2
    OCCUPIED = 3
    AT = 4
    LOADED = 5
    UNLOADED = 6
    HOLDING = 7
    EMPTY = 8
    IN = 9
    ON = 10
    TOP = 11
    FREE = 12


Name2Predicate = {"adjacent" : Predicates.ADJACENT, "attached" : Predicates.ATTACHED, "belong" : Predicates.BELONG, "occupied" : Predicates.OCCUPIED, "at" : Predicates.AT, "loaded" : Predicates.LOADED, "unloaded" : Predicates.UNLOADED, "holding" : Predicates.HOLDING, "empty" : Predicates.EMPTY, "in" : Predicates.IN, "on" : Predicates.ON, "top" : Predicates.TOP, "free" : Predicates.FREE}


Predicate2Name = {Predicates.ADJACENT : "adjacent", Predicates.ATTACHED : "attached", Predicates.BELONG : "belong", Predicates.OCCUPIED : "occupied", Predicates.AT : "at", Predicates.LOADED : "loaded", Predicates.UNLOADED : "unloaded", Predicates.HOLDING : "holding", Predicates.EMPTY : "empty", Predicates.IN : "in", Predicates.ON : "on", Predicates.TOP : "top", Predicates.FREE : "free"}


class Actions:
    START = 0
    FINISH = 1
    MOVE = 2
    TAKE = 3
    PUT = 4
    LOAD = 5
    UNLOAD = 6


Name2Action = {"start" : Actions.START, "finish" : Actions.FINISH, "move" : Actions.MOVE, "take" : Actions.TAKE, "put" : Actions.PUT, "load" : Actions.LOAD, "unload" : Actions.UNLOAD}


Action2Name = {Actions.START : "start", Actions.FINISH : "finish", Actions.MOVE : "move", Actions.TAKE : "take", Actions.PUT : "put", Actions.LOAD : "load", Actions.UNLOAD : "unload"}



