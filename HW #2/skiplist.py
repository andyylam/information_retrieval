from math import sqrt, floor

# Represents a node in a traditional singly linked list


class Node:
    def __init__(self, val):
        super().__init__()
        self.val = val
        self.next = None

    def set_value(self, val):
        self.val = val

    def set_next(self, next):
        self.next = next

    def get_next(self):
        return self.next

    def get_value(self):
        return self.val

    def to_string(self):
        result_string, current = f'{self.val} ', self.next
        while current:
            result_string += str(current.val) + ' '
            current = current.next
        return result_string.strip()

# Represents a node in the SkipList. Extends Node.


class SkipNode(Node):
    def __init__(self, val):
        super().__init__(val)
        self.skip = None

    def set_skip(self, skip):
        self.skip = skip

    def get_skip(self):
        return self.skip

    def has_skip(self):
        return self.skip is not None

# SkipList class that represents a SkipList, used in posting lists.


class SkipList:
    def __init__(self, head):
        super().__init__()
        self.head = head

    # Constructor for initialising a SkipList from a python list.
    @classmethod
    def create_skip_list_from_list(cls, posting):
        head = SkipList.create_skip_list(posting)
        return cls(head)

    # Constructor for initialising a SkipList from file, with the head node.
    @classmethod
    def create_skip_list_from_node(cls, node):
        return cls(node)

    # Create a skip list from a python list.
    @staticmethod
    def create_skip_list(posting):
        current = newhead = None
        count = 0
        for num in posting:
            new_node = SkipNode(num)
            if not newhead:
                newhead = new_node
                current = newhead
            else:
                current.set_next(new_node)
                current = new_node
            count += 1
        SkipList.set_skip_pointers(newhead, count)
        return newhead

    # Set sqroot(n) evenly spaced skip pointers across the skip list.
    @staticmethod
    def set_skip_pointers(head, count):
        num_skip_pointers = floor(sqrt(count))
        num_next_pointers = count - 1
        skip = num_next_pointers // num_skip_pointers
        remaining = num_next_pointers % num_skip_pointers

        current = head
        while current and remaining:
            skip_node = current
            for i in range(skip):
                skip_node = skip_node.next
            current.set_skip(skip_node)
            current = skip_node
            if remaining > 0:
                current = current.next
                remaining -= 1

    # Returns a string representation of the SkipList
    def to_string(self):
        result_string, current = '', self.head
        while current:
            result_string += str(current.val) + ' '
            current = current.next
        return result_string

    # Operation for intersection between two SkipLists. Used for "AND" queries.
    @staticmethod
    def intersection(s1, s2):
        current1, current2 = s1.head, s2.head
        if not current1 or not current2:
            return SkipList(None)
        newhead = current = None
        while current1 and current2:
            if current1.val == current2.val:
                if not newhead:
                    newhead = SkipNode(current1.val)
                    current = newhead
                else:
                    current.next = SkipNode(current1.val)
                    current = current.next
                current1 = current1.next
                current2 = current2.next
            elif current1.val < current2.val:
                if current1.skip and current1.skip.val < current2.val:
                    current1 = current1.skip
                else:
                    current1 = current1.next
            else:
                if current2.skip and current2.skip.val < current1.val:
                    current2 = current2.skip
                else:
                    current2 = current2.next
        if not current:
            return SkipList(None)
        current.next = None
        return SkipList.create_skip_list_from_node(newhead)

    # Operation for union between two SkipLists. Used for "OR" queries.
    @staticmethod
    def union(s1, s2):
        current1, current2 = s1.head, s2.head
        if not current1:
            return s2
        if not current2:
            return s1

        newhead = None
        if current1.val < current2.val:
            newhead = SkipNode(current1.val)
            current1 = current1.next
        else:
            newhead = SkipNode(current2.val)
            current2 = current2.next

        current = newhead
        while current1 and current2:
            if current1.val < current2.val:
                current.next = SkipNode(current1.val)
                current = current.next
                current1 = current1.next
            elif current1.val == current2.val:
                current.next = SkipNode(current1.val)
                current = current.next
                current1 = current1.next
                current2 = current2.next
            else:
                current.next = SkipNode(current2.val)
                current = current.next
                current2 = current2.next

        if not current1:
            while current2:
                current.next = SkipNode(current2.val)
                current = current.next
                current2 = current2.next
        else:
            while current1:
                current.next = SkipNode(current1.val)
                current = current.next
                current1 = current1.next
        return SkipList.create_skip_list_from_node(newhead)

    # Operation for intersection between a SkipList `other` and the complement of SkipList `complement`.
    # Used for "NOT" and "AND NOT" queries.
    @staticmethod
    def intersection_complement(complement, other):
        current1, current2 = other.head, complement.head
        if not current1:
            return SkipList(None)
        if not current2:
            return other

        newhead = current = None
        while current1 and current2:
            if current1.val < current2.val:
                if not newhead:
                    newhead = SkipNode(current1.val)
                    current = newhead
                else:
                    current.next = SkipNode(current1.val)
                    current = current.next
                current1 = current1.next
            elif current1.val == current2.val:
                current1 = current1.next
                current2 = current2.next
            else:
                current2 = current2.next
        if not current2:
            while current1:
                if not current:
                    newhead = SkipNode(current1.val)
                    current = newhead
                else:
                    current.next = SkipNode(current1.val)
                    current = current.next
                current1 = current1.next
        return SkipList.create_skip_list_from_node(newhead)
