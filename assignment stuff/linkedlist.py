#!python


class Node(object):

    def __init__(self, data):
        """Initialize this node with the given data."""
        self.data = data
        self.next = None

    def __repr__(self):
        """Return a string representation of this node."""
        return 'Node({!r})'.format(self.data)


class LinkedList(object):

    def __init__(self, items=None):
        """Initialize this linked list and append the given items, if any."""
        self.head = None  # First node
        self.tail = None  # Last node
        # Append given items
        if items is not None:
            for item in items:
                self.append(item)

    def __str__(self):
        """Return a formatted string representation of this linked list."""
        items = ['({!r})'.format(item) for item in self.items()]
        return '[{}]'.format(' -> '.join(items))

    def __repr__(self):
        """Return a string representation of this linked list."""
        return 'LinkedList({!r})'.format(self.items())

    def items(self):
        """Return a list (dynamic array) of all items in this linked list.
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
        TODO: Running time: O(???) Why and under what conditions?"""
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
        TODO: Running time: O(???) Why and under what conditions?"""
        next_node = Node(item)
        # if List is empty:
        if self.is_empty():
            self.head = next_node
            self.tail = next_node
        else:
            self.tail.next = next_node
            self.tail = next_node

    def prepend(self, item):
        """Insert the given item at the head of this linked list.
        TODO: Running time: O(???) Why and under what conditions?"""
        new_node = Node(item)
        # if List is empty:
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def find(self, quality):
        """Return an item from this linked list satisfying the given quality.
        Return None if nothing is found.
        TODO: Best case running time: O(???) Why and under what conditions?
        TODO: Worst case running time: O(???) Why and under what conditions?"""
        node = self.head
        while node is not None:
            if quality(node.data):
                return node.data
            node = node.next
        return None

    def find_by_key(self, key):
        """ Assuming node.data is a (key, value) pair: return node.data if the given key matches.
            Return None if nothing is found.
        TODO: Best case running time: O(1) Why and under what conditions?
        TODO: Worst case running time: O(n) Why and under what conditions?"""
        node = self.head
        while node is not None:
            if node.data[0] == key:
                return node.data
            node = node.next
        return None

    def delete(self, item):
        """Delete the given item from this linked list, or raise ValueError.
        TODO: Best case running time: O(???) Why and under what conditions?
        TODO: Worst case running time: O(???) Why and under what conditions?"""
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
                # if the tail is being deleted:
                elif node == self.tail:
                    self.tail = prev_node
                    self.tail.next = None
                # if a node somewhere in between the head and tail is being deleted:
                else:
                    prev_node.next = node.next
                return None

            prev_node = node
            node = node.next
        raise ValueError(f'Item not found: {item}')

    def update(self, item, new_item):
        """Delete the given item from this linked list, or raise ValueError.
        TODO: Best case running time: O(???) Why and under what conditions?
        TODO: Worst case running time: O(???) Why and under what conditions?"""
        node = self.head
        while node is not None:
            if node.data == item:
                node.data = new_item
                return None
            else:
                node = node.next
        raise ValueError(f'Item not found: {item}')


def test_linked_list():
    ll = LinkedList()
    print('list: {}'.format(ll))

    print('\nTesting append:')
    for item in ['A', 'B', 'C']:
        print('\nlength: {}'.format(ll.length()))
        print('append({!r})'.format(item))
        ll.append(item)
        print('list: {}'.format(ll))

    # print('\nlength: {}'.format(ll.length()))
    # ll.prepend('0')
    # print("prepend('0')")
    # print('list: {}'.format(ll))

    print('head: {}'.format(ll.head))
    print('tail: {}'.format(ll.tail))
    print('length: {}'.format(ll.length()))


    # Enable this after implementing delete method
    delete_implemented = True
    if delete_implemented:
        print('\nTesting delete:')
        for item in ['A', 'B', 'C']:
            print('delete({!r})'.format(item))
            ll.delete(item)
            print('list: {}'.format(ll))

        print('head: {}'.format(ll.head))
        print('tail: {}'.format(ll.tail))
        print('length: {}'.format(ll.length()))


if __name__ == '__main__':
    test_linked_list()
