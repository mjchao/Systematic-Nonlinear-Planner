/*
configure.h
------------
This header contains enum definitions for all objects in the project
It also contains hash tables that move between enums and strings.
For example, 
	Name2Predicate.at("adjacent") returns ADJACENT
	Predicate2Name.at(ADJACENT) returns "adjacent"

	The unordered_map structure throws an std::out_of_range exception
	if the referred to object is not found.

The file should be self explanatory from here.
*/
#ifndef CONFIGURE_H
#define CONFIGURE_H

#include <unordered_map>
#include <string>
using namespace std;

enum Categories {
	LOCATIONS,
	ROBOTS,
	CRANES,
	PILES,
	CONTAINERS,
	INITIAL,
	GOAL
};

const unordered_map<string, int> Name2Category = {
	{"locations", LOCATIONS},
	{"robots", ROBOTS},
	{"cranes", CRANES},
	{"piles", PILES},
	{"containers", CONTAINERS},
	{"initial", INITIAL},
	{"goal", GOAL}
};

const unordered_map<int, string> Category2Name {
	{LOCATIONS, "locations"},
	{ROBOTS, "robots"},
	{CRANES, "cranes"},
	{PILES, "piles"},
	{CONTAINERS, "containers"},
	{INITIAL, "initial"},
	{GOAL, "goal"}
};

enum Predicates {
	ADJACENT, 
	ATTACHED, 
	BELONG, 
	OCCUPIED, 
	AT, 
	LOADED, 
	UNLOADED, 
	HOLDING, 
	EMPTY, 
	IN, 
	ON, 
	TOP,
	FREE
};

const unordered_map<string, int> Name2Predicate = {
	{"adjacent", ADJACENT},
	{"attached", ATTACHED},
	{"belong", BELONG},
	{"occupied", OCCUPIED},
	{"at", AT},
	{"loaded", LOADED},
	{"unloaded", UNLOADED},
	{"holding", HOLDING},
	{"empty", EMPTY},
	{"in", IN},
	{"on", ON},
	{"top", TOP},
	{"free", FREE}
};

const unordered_map<int, string> Predicate2Name = {
	{ADJACENT, "adjacent"},
	{ATTACHED, "attached"},
	{BELONG, "belong"},
	{OCCUPIED, "occupied"},
	{AT, "at"},
	{LOADED, "loaded"},
	{UNLOADED, "unloaded"},
	{HOLDING, "holding"},
	{EMPTY, "empty"},
	{IN, "in"},
	{ON, "on"},
	{TOP, "top"},
	{FREE, "free"}
};

enum Actions {
	START, 
	FINISH, 
	MOVE, 
	TAKE, 
	PUT, 
	LOAD, 
	UNLOAD
};

const unordered_map<string, int> Name2Action = {
	{"start", START},
	{"finish", FINISH},
	{"move", MOVE},
	{"take", TAKE},
	{"put", PUT},
	{"load", LOAD},
	{"unload", UNLOAD}
};

const unordered_map<int, string> Action2Name = {
	{START, "start"},
	{FINISH, "finish"},
	{MOVE, "move"},
	{TAKE, "take"},
	{PUT, "put"},
	{LOAD, "load"},
	{UNLOAD, "unload"}
};


#endif