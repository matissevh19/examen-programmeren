#✅ 1. Node.py
class Node:
    def __init__(self, element):
        self.element = element
        self.next = None

    def __str__(self):
        return str(self.element)

#✅ 2. LinkedList.py
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # add at beginning
    def addFirst(self, e):
        node = Node(e)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head = node
        self.size += 1

    # add at end
    def addLast(self, e):
        node = Node(e)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    # alias for addLast
    def add(self, e):
        self.addLast(e)

    # remove first element
    def removeFirst(self):
        if self.head is None:
            return None
        value = self.head.element
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return value

    # remove last element
    def removeLast(self):
        if self.head is None:
            return None
        if self.head == self.tail:
            value = self.head.element
            self.head = self.tail = None
            self.size -= 1
            return value
        current = self.head
        while current.next != self.tail:
            current = current.next
        value = self.tail.element
        self.tail = current
        current.next = None
        self.size -= 1
        return value

    # insert at index
    def insert(self, index, e):
        if index < 0 or index > self.size:
            return
        if index == 0:
            self.addFirst(e)
            return
        if index == self.size:
            self.addLast(e)
            return

        node = Node(e)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        node.next = current.next
        current.next = node
        self.size += 1

    # remove element at index
    def removeAt(self, index):
        if index < 0 or index >= self.size:
            return None
        if index == 0:
            return self.removeFirst()

        current = self.head
        for _ in range(index - 1):
            current = current.next

        removed = current.next
        current.next = removed.next
        if removed == self.tail:
            self.tail = current
        self.size -= 1
        return removed.element

    # remove first occurrence of element
    def remove(self, e):
        if self.head is None:
            return False
        if self.head.element == e:
            self.removeFirst()
            return True

        current = self.head
        while current.next is not None:
            if current.next.element == e:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def getFirst(self):
        return None if self.head is None else self.head.element

    def getLast(self):
        return None if self.tail is None else self.tail.element

    def contains(self, e):
        return self.indexOf(e) != -1

    def get(self, index):
        if index < 0 or index >= self.size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.element

    def indexOf(self, e):
        current = self.head
        index = 0
        while current:
            if current.element == e:
                return index
            current = current.next
            index += 1
        return -1

    def lastIndexOf(self, e):
        current = self.head
        index = 0
        last = -1
        while current:
            if current.element == e:
                last = index
            current = current.next
            index += 1
        return last

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def getSize(self):
        return self.size

    def __str__(self):
        s = "["
        current = self.head
        while current:
            s += str(current.element)
            if current.next:
                s += ", "
            current = current.next
        s += "]"
        return s

#✅ 3. Stack.py
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            return None
        return self.items.pop()

    def peek(self):
        if not self.items:
            return None
        return self.items[-1]

    def isEmpty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return "Stack: " + str(self.items)

#✅ 4. Queue.py (gebaseerd op LinkedList zoals in slides)
class Queue:
    def __init__(self):
        self.elements = LinkedList()

    def enqueue(self, e):
        self.elements.addLast(e)

    def dequeue(self):
        return self.elements.removeFirst()

    def getSize(self):
        return self.elements.size

    def isEmpty(self):
        return self.elements.size == 0

    def __str__(self):
        return "Queue: " + str(self.elements)

#✅ 5. DictionaryMethodsDemo.py
def dictionary_demo():
    d = {"a": 1, "b": 2, "c": 3}

    print(d.keys())          # dict_keys(['a', 'b', 'c'])
    print(d.values())        # dict_values([1, 2, 3])
    print(d.items())         # dict_items([('a', 1), ('b', 2), ('c', 3)])

    print(d.get("a"))        # 1
    print(d.get("x", 100))   # 100

    print(d.pop("b"))        # 2
    print(d)

    print(d.popitem())       # removes last added

    d.clear()
    print(d)

def main():

    print("=== STACK TEST ===")
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    print(s)
    print(s.pop())
    print(s)

    print("\n=== QUEUE TEST ===")
    q = Queue()
    q.enqueue(5)
    q.enqueue(6)
    q.enqueue(7)
    print(q)
    print(q.dequeue())
    print(q)

    print("\n=== LINKED LIST TEST ===")
    ll = LinkedList()
    ll.addFirst(3)
    ll.addLast(5)
    ll.addLast(7)
    print(ll)
    print("remove first:", ll.removeFirst())
    print(ll)

if __name__ == "__main__":
    main()
