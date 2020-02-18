from math import sqrt, floor


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


class SkipList:
    def __init__(self, head):
        super().__init__()
        self.head = head

    @classmethod
    def create_skip_list_from_list(cls, posting):
        head = SkipList.create_skip_list(posting)
        return cls(head)

    @classmethod
    def create_skip_list_from_node(cls, node):
        return cls(node)

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

    def to_string(self):
        result_string, current = '', self.head
        while current:
            result_string += str(current.val) + ' '
            current = current.next
        return result_string

    @staticmethod
    def intersection(s1, s2):
        current1, current2 = s1.head, s2.head
        if not current1 or not current2:
            return SkipList(None)
        newhead = current = None
        while current1 and current2:
            if current1.val == current2.val:
                if not newhead:
                    newhead = current1
                    current = newhead
                else:
                    current.next = current1
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
        current.next = None
        return SkipList.create_skip_list_from_node(newhead)

    @staticmethod
    def union(s1, s2):
        current1, current2 = s1.head, s2.head
        if not current1:
            return s2
        if not current2:
            return s1

        newhead = None
        if current1.val < current2.val:
            newhead = current1
            current1 = current1.next
        else:
            newhead = current2
            current2 = current2.next

        current = newhead
        while current1 and current2:
            if current1.val < current2.val:
                current.next = current1
                current = current.next
                current1 = current1.next
            elif current1.val == current2.val:
                current.next = current1
                current = current.next
                current1 = current1.next
                current2 = current2.next
            else:
                current.next = current2
                current = current.next
                current2 = current2.next

        if not current1:
            current.next = current2
        else:
            current.next = current1
        return SkipList.create_skip_list_from_node(newhead)

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
                    newhead = current1
                    current = newhead
                else:
                    current.next = current1
                    current = current.next
                current1 = current1.next
            elif current1.val == current2.val:
                current1 = current1.next
                current2 = current2.next
            else:
                while current2 and current2.val < current1.val:
                    current2 = current2.next

        if not current2:
            if not current:
                newhead = current1
            else:
                current.next = current1
        return SkipList.create_skip_list_from_node(newhead)
