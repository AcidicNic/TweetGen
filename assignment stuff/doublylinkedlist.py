#!python
""" Stretch Challenge!"""

class Node_d(object):
    def __init__(self, data):
        """Initialize this node with the given data."""
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        """Return a string representation of this node."""
        return 'Node_d({!r})'.format(self.data)


class DoublyLinkedList(object):
    def __init__(self, items=None):
        """Initialize this doubly linked list and append the given items, if any."""
        self.head = None  # First node
        self.tail = None  # Last node
        # Append given items
        if items is not None:
            for item in items:
                self.append(item)

    def __str__(self):
        """Return a formatted string representation of this doubly linked list."""
        items = ['({!r})'.format(item) for item in self.items()]
        return '[{}]'.format(' <-> '.join(items))

    def __repr__(self):
        """Return a string representation of this doubly linked list."""
        return 'LinkedList({!r})'.format(self.items())

    def items(self):
        """Return a list (dynamic array) of all items in this doubly linked list.
        Best and worst case running time: O(n) for n items in the list (length)
        because we always need to loop through all n nodes to get each item."""
        items = []  # O(1) time to create empty list
        # Start at head node
        node = self.head  # O(1) time to assign new variable
        # Loop until node is None, which is one node too far past tail
        while node is not None:  # Always n iterations because no early return
            items.append(node.data)  # O(1) time (on average) to append to list
            # Skip to next node to advance forward in linked list
            node = node.next  # O(1) time to reassign variable
        # Now list contains items from all nodes
        return items  # O(1) time to return list

    def is_empty(self):
        """Return a boolean indicating whether this linked list is empty."""
        return self.head is None

    def length(self):
        """Return the length of this linked list by traversing its nodes.
        Running time: O(n) iterating therough every node."""
        if self.is_empty():
            return 0
        node = self.head
        len = 1
        while node.next is not None:
            len += 1
            node = node.next
        return len

    def append(self, item):
        """Insert the given item at the tail of this linked list.
        Running time: O(1) just a conditional!"""
        next_node = Node_d(item)
        # if List is empty:
        if self.is_empty():
            self.head = next_node
            self.tail = next_node
        else:
            next_node.prev = self.tail
            self.tail.next = next_node
            self.tail = next_node

    def prepend(self, item):
        """Insert the given item at the head of this linked list.
        Running time: O(1) just a conditional"""
        new_node = Node_d(item)
        # if List is empty:
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def find(self, quality):
        """Return an item from this linked list satisfying the given quality.
        Return None if nothing is found.
        Best case running time: O(1) head node satisfies the quality.
        Worst case running time: O(n) iterating through every node."""
        node = self.head
        while node is not None:
            if quality(node.data):
                return node.data
            node = node.next
        return None

    def find_by_key(self, key):
        """ Assuming node.data is a (key, value) pair: return node.data if the given key matches.
            Return None if nothing is found.
        Best case running time: O(1) head node
        Worst case running time: O(n) iterates through nodes"""
        node = self.head
        while node is not None:
            if node.data[0] == key:
                return node.data
            node = node.next
        return None

    def delete(self, item):
        """Delete the given item from this linked list, or raise ValueError.
        Best case running time: O(1) head node
        Worst case running time: O(n) iterates through nodes"""
        node = self.head
        prev_node = None
        while node is not None:
            if node.data == item:
                # if the only Node is being deleted:
                if self.head == self.tail == node:
                    self.head = None
                    self.tail = None
                # if the head is being deleted:
                elif node == self.head:
                    self.head = node.next
                    self.head.prev = None
                # if the tail is being deleted:
                elif node == self.tail:
                    self.tail = prev_node
                    self.tail.next = None
                # if a node somewhere in between the head and tail is being deleted:
                else:
                    prev_node.next = node.next
                    node.next.prev = prev_node
                return None

            prev_node = node
            node = node.next
        raise ValueError(f'Item not found: {item}')

    def update(self, item, new_item):
        """Delete the given item from this linked list, or raise ValueError.
        Best case running time: O(1) head node
        Worst case running time: O(n) iterates through nodes"""
        node = self.head
        while node is not None:
            if node.data == item:
                node.data = new_item
                return None
            else:
                node = node.next
        raise ValueError(f'Item not found: {item}')


def test_doubly_linked_list():
    ll = DoublyLinkedList()
    print('list: {}'.format(ll))

    print('\nTesting append:')
    for item in ['A', 'B', 'C', 'D', 'E']:
        print('\nlength: {}'.format(ll.length()))
        print('append({!r})'.format(item))
        ll.append(item)
        print('list: {}'.format(ll))

    print('head: {}'.format(ll.head))
    print('tail: {}'.format(ll.tail))
    print('length: {}'.format(ll.length()))


    # Enable this after implementing delete method
    delete_implemented = True
    if delete_implemented:
        print('\nTesting delete:')
        for item in ['A', 'E', 'C', 'D']:
            print('delete({!r})'.format(item))
            ll.delete(item)
            print('list: {}'.format(ll))

        print('\nhead: {}'.format(ll.head))
        print('tail: {}'.format(ll.tail))
        print('length: {}'.format(ll.length()))

        print("\ndelete('B')")
        ll.delete('B')
        print('list: {}'.format(ll))

        print('head: {}'.format(ll.head))
        print('tail: {}'.format(ll.tail))
        print('length: {}'.format(ll.length()))


if __name__ == '__main__':
    test_doubly_linked_list()
