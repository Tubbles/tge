#!/usr/bin/env python3

from editor import elementary_cellular_automata

assert(elementary_cellular_automata([True, True, True], 110) == False)
assert(elementary_cellular_automata([True, True, False], 110) == True)
assert(elementary_cellular_automata([True, False, True], 110) == True)
assert(elementary_cellular_automata([True, False, False], 110) == False)
assert(elementary_cellular_automata([False, True, True], 110) == True)
assert(elementary_cellular_automata([False, True, False], 110) == True)
assert(elementary_cellular_automata([False, False, True], 110) == True)
assert(elementary_cellular_automata([False, False, False], 110) == False)
