class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next = next

    def __init__(self):
        self.head = LinkedList.Node(None)  # sentinel node (never to be removed)
        self.head.prior = self.head.next = self.head  # set up "circular" topology
        self.length = 0


    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1

    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1

    ### subscript-based access ###

    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx

    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        assert (isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx >= self.length:
            raise IndexError()
        n = self.head.next
        for x in range(0, nidx):
            n = n.next
        return n.val

    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert (isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx > self.length:
            raise IndexError()
        n = self.head.next
        for x in range(0, nidx):
            n = n.next
        n.val = value
    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert (isinstance(idx, int))
        nidx = self._normalize_idx(idx)
        if nidx > self.length:
            raise IndexError()
        n = self.head.next
        for x in range(0, nidx):
            n = n.next
        n.prior.next = n.next
        n.next.prior = n.prior
        self.length -= 1

        # Requires changing location of head and tail of node to be delted
        # Route Around!

        #      --> <--|__| -> <-|__| -> <-|__|--> <--

    ### stringification ###

    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        return '[' + ', '.join(str(x) for x in self) + ']'
    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        return str(self)
    ### single-element manipulation ###

    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        nidx = self._normalize_idx(idx)
        if nidx > self.length:
            raise IndexError()
        if nidx == len(self):
            self.append(value)
        n = self.head.next
        for x in range(0, nidx):
            n = n.next
        nn = LinkedList.Node(value)

        nn.next = n
        nn.prior = n.prior
        n.prior.next = nn
        n.prior = nn

        self.length += 1

        # Requires changing location of head and tail of node at idx

        #      --> <--|__| -> <-|__|-> <-|__| -> <-|__|--> <--

    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        tval = self[idx]
        del self[idx]

        return tval

    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        for x in range(len(self)):
            if self[x] == value:
                del self[x]
                break
        else:
            raise ValueError

    ### predicates (T/F queries) ###

    def __eq__(self, other):
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""
        if not isinstance(other, LinkedList) or len(self) != len(other):
            return False
        for x in range(0, len(self)):
            if self[x] != other[x]:
                return False
        else:
            return True

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        for val in self:
            if val == value:
                return True
        else:
            return False
    ### queries ###

    def __len__(self):
        """Implements `len(self)`"""
        return self.length

    def min(self):
        """Returns the minimum value in this list."""
        minVal = self[0]

        for val in self:
            if val < minVal:
                minVal = val
        return minVal
    def max(self):
        """Returns the maximum value in this list."""
        maxVal = self[0]
        for val in self:
            if val > maxVal:
                maxVal = val
        return maxVal
    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        if j == None:
            j = len(self)

        i = self._normalize_idx(i)
        j = self._normalize_idx(j)

        for x in range(i, j):
            if self[x] == value:
                return x
        else:
            raise ValueError

    def count(self, value):
        """Returns the number of times value appears in this list."""
        appears = 0
        for x in self:
            if x == value:
                appears += 1
        return appears
    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those
        of other."""
        assert (isinstance(other, LinkedList))
        new = LinkedList()
        if len(self) > 0:
            for x in self:
                new.append(x)
        if len(other) > 0:
            for x in other:
                new.append(x)
        return new

    def clear(self):
        """Removes all elements from this list."""
        self.head.prior = self.head.next = self.head  # set up "circular" topology
        self.length = 0
        return self

    def copy(self):
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""
        new = LinkedList()
        for x in self:
            new.append(x)
        return new

    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        for x in other:
            self.append(x)
        return self

    ### iteration ###

    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        n = self.head
        for i in range(0, len(self)):
            n = n.next
            yield n.val