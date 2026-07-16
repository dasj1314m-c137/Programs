from collections import deque

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = deque()
        self.frontier_set = set()
        self.explored = set()

    def add(self, node):
        self.frontier.append(node)
        self.frontier_set.add(node.state)

    def add_explored(self, state):
        self.explored.add(state)
        self.frontier_set.discard(state)

    def contains_state(self, state):
        return state in self.frontier_set

    def explored_state(self, state):
        return state in self.explored

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop()
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.popleft()
            return node
