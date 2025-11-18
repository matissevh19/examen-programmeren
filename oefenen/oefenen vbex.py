class TaskNode:
    def __init__(self, task_name, duration, priority):
        self.task_name = task_name
        self.duration = duration
        self.priority = priority
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task_name, duration, priority):
        new_task = TaskNode(task_name, duration, priority)

        if self.head is None:
            self.head = new_task
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_task

    def remove_task(self, task_name):
        # 1. lege lijst
        if self.head is None:
            return
        # 2. head verwijderen
        if self.head.task_name == task_name:
            self.head = self.head.next
            return
        # 3. zoeklus starten
        previous = self.head
        current = self.head.next
        # 4. zoeken naar de taak
        while current is not None and current.task_name != task_name:
            previous = current
            current = current.next
        # 5. taak niet gevonden
        if current is None:
            return
        # 6. taak gevonden → verwijderen
        previous.next = current.next

    def display_tasks(self):
        current = self.head
        while current is not None:
            print(f"{current.task_name}, {current.duration}, {current.priority}")
            current = current.next

    def find_task(self, task_name):
        current = self.head
        while current is not None:
            if current.task_name == task_name:
                return current
            current = current.next
        return None

    def calculate_total_duration(self):
        total = 0
        current = self.head
        while current is not None:
            total += current.duration
            current = current.next
        return total

    def read_tasks_from_csv(self, file_path):
        import csv
        with open(file_path) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                task_name = row[0]
                duration = int(row[1])
                priority = int(row[2])
                self.add_task(task_name, duration, priority)

    def reorder_tasks_by_priority(self):
            new_head = None
            current = self.head

            while current is not None:
                next_node = current.next
                current.next = None
                new_head = self.sorted_insert_by_priority(new_head, current)
                current = next_node

            self.head = new_head

    def reorder_tasks_by_priority_duration(self):
        new_head = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = None
            new_head = self.sorted_insert_by_priority_duration(new_head, current)
            current = next_node

        self.head = new_head

    def sorted_insert_by_priority(self, head, node):
        # als lijst leeg is of node moet helemaal vooraan komen
        if head is None or node.priority < head.priority:
            node.next = head
            return node

        current = head

        # loop totdat we op de juiste plaats zijn
        while current.next is not None and current.next.priority <= node.priority:
            current = current.next

        # invoegen
        node.next = current.next
        current.next = node
        return head

    def sorted_insert_by_priority_duration(self, head, node):
        # als lijst leeg is of node moet vooraan komen
        if (head is None or
                node.priority < head.priority or
                (node.priority == head.priority and node.duration < head.duration)):
            node.next = head
            return node

        current = head

        # zoek juiste plek
        while current.next is not None:
            next_node = current.next

            if (node.priority < next_node.priority or
                    (node.priority == next_node.priority and node.duration < next_node.duration)):
                break

            current = current.next

        node.next = current.next
        current.next = node
        return head

def test_read_from_csv():
    print("\n=== TEST 1: read_tasks_from_csv ===")
    ll = LinkedList()
    ll.read_tasks_from_csv("tasks.csv")
    ll.display_tasks()

def test_add_task():
    print("\n=== TEST 2: add_task ===")
    ll = LinkedList()
    ll.add_task("A", 10, 2)
    ll.add_task("B", 5, 1)
    ll.add_task("C", 30, 3)
    ll.display_tasks()

def test_remove_task():
    print("\n=== TEST 3: remove_task ===")
    ll = LinkedList()
    ll.add_task("A", 10, 2)
    ll.add_task("B", 20, 1)
    ll.add_task("C", 30, 3)

    print("Before removal:")
    ll.display_tasks()

    ll.remove_task("B")

    print("After removing B:")
    ll.display_tasks()

def test_find_task():
    print("\n=== TEST 4: find_task ===")
    ll = LinkedList()
    ll.add_task("A", 10, 2)
    ll.add_task("B", 20, 3)

    found = ll.find_task("B")
    print("Found:", found.task_name, found.duration, found.priority)

    not_found = ll.find_task("X")
    print("Not found:", not_found)

def test_total_duration():
    print("\n=== TEST 5: calculate_total_duration ===")
    ll = LinkedList()
    ll.add_task("A", 10, 2)
    ll.add_task("B", 20, 3)
    ll.add_task("C", 5, 1)
    print("Total duration =", ll.calculate_total_duration())

def test_reorder_priority():
    print("\n=== TEST 6: reorder_tasks_by_priority ===")
    ll = LinkedList()
    ll.read_tasks_from_csv("tasks.csv")

    print("Before reorder:")
    ll.display_tasks()

    ll.reorder_tasks_by_priority()

    print("After reorder by PRIORITY:")
    ll.display_tasks()

def test_reorder_priority_duration():
    print("\n=== TEST 7: reorder_tasks_by_priority_duration ===")
    ll = LinkedList()
    ll.read_tasks_from_csv("tasks.csv")

    print("Before reorder:")
    ll.display_tasks()

    ll.reorder_tasks_by_priority_duration()

    print("After reorder by PRIORITY + DURATION:")
    ll.display_tasks()

if __name__ == "__main__":
    test_read_from_csv()
    test_add_task()
    test_remove_task()
    test_find_task()
    test_total_duration()
    test_reorder_priority()
    test_reorder_priority_duration()
