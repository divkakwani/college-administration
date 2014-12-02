# Implementation of Trie as a finite automaton

# Operations on Trie
#	Searching - O(L)
#	Addition  - O(L)


# The structure will be stored in cache.

class Trie:
    def __init__(self):
        # 0 is the root - denoting empty string
        self._parent = {0: -1}          # collection of node, parent pair
        # Mapping of the satellite data to their states
        self._acceptance = {0: None}    # None implies non-accepting; 
        self._total_states = 1
        self._transitions = {0: {}}     # stores the adjacency-list of each of the state
        
    def get_sat_data(self, state):
        return self._acceptance[state]
    
    # @params word: input to the automaton
    # @params sat_data: satellite data associated with a state
    def addWord(self, word, sat_data):  
        current_state = 0
        for letter in word[:-1]:
            if letter not in self._transitions[current_state]:
                self._transitions[self._total_states] = {}      # create a new state
                self._acceptance[self._total_states] = None    # Non-accepting
                self._parent[self._total_states] = current_state
                self._transitions[current_state][letter] = self._total_states
                self._total_states += 1
            current_state = self._transitions[current_state][letter]
        if word[-1] not in self._transitions[current_state]:
            self._transitions[self._total_states] = {}      # create a new state
            self._acceptance[self._total_states] = sat_data     # Accepting
            self._parent[self._total_states] = current_state
            self._transitions[current_state][word[-1]] = self._total_states
            self._total_states += 1

    def findState(self, word):
        current_state = 0
        for letter in word:
            current_state = self._transitions.get(current_state, None).get(letter, None)
            if current_state is None:
                return None
        return current_state

    def remove_word(self, word):
        state = self.findState(word)
        if not state:
            raise Exception('The word does not exist')
        if len(self._transitions[state]) != 0:    # There exists word(s) whose prefixes are the given word. So we can't remove it
            self._acceptance[state] = None   # Make it non-accepting
        else:
            parent_state = self._parent[state]
            del self._acceptance[state]
            del self._parent[state]
            del self._transitions[state]
            while len(self._transitions[parent_state]) == 1 and parent_state != 0:
                del_state = parent_state
                parent_state = self._parent[parent_state]
                del self._acceptance[del_state]
                del self._parent[del_state]
                del self._transitions[del_state]
            for letter in self._transitions[parent_state]:
                if self._transitions[parent_state][letter] == del_state:
                    del_letter =  letter
            del self._transitions[parent_state][del_letter]

      
    def isWord(self, word):
        state = self.findState(word)
        if state:
            return self._acceptance[state] != None
        return False

    def wordsStartingFrom(self, word):
        current_state = self.findState(word)  # locate the state which denotes the prefix word
        if current_state is not None:
            return self.TrieDFS(current_state, word)
        return []

    # @params state: state is the node from where the DFS starts
    # @params word: word is the word associated withe the starting state
    def TrieDFS(self, state, word):
        words = []
        if self._acceptance[state] is not None:
           words.append((word, self._acceptance[state]))
        for letter in self._transitions[state]:
            words += self.TrieDFS(self._transitions[state][letter], word + letter)
        return words

"""
# Test code
t = Trie()

import csv
csvfile = open('census.csv', 'r')
for row in csv.reader(csvfile):
    t.addWord(row[0], 'name')
print t.wordsStartingFrom('DAVI')
t.remove_word('DAVIS')
print t.wordsStartingFrom('DAVI')
"""