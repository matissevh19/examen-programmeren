class TaskNode:
    def __init__(self, task_name, duration, priority):
        # Eén knoop (taak) in de LinkedList
        self.task_name = task_name
        self.duration = duration
        self.priority = priority
        self.next = None   # verwijzing naar de volgende node


class LinkedList:
    def __init__(self):
        # begin van de lijst (None bij start)
        self.head = None

    # ------------------------------------------------------------
    # 1. Taak toevoegen aan het EINDE van de linked list
    # ------------------------------------------------------------
    def add_task(self, task_name, duration, priority):
        new_task = TaskNode(task_name, duration, priority)

        # Als lijst leeg is → nieuwe taak wordt head
        if self.head is None:
            self.head = new_task
            return

        # Anders naar het einde van de lijst lopen
        current = self.head
        while current.next is not None:
            current = current.next

        # Nieuwe taak achteraan koppelen
        current.next = new_task

    # ------------------------------------------------------------
    # 2. Taak verwijderen op basis van naam
    # ------------------------------------------------------------
    def remove_task(self, task_name):

        # Lijst is leeg → niets te verwijderen
        if self.head is None:
            return

        # Speciale case: head moet verwijderd worden
        if self.head.task_name == task_name:
            self.head = self.head.next
            return

        # Anders door de lijst lopen om taak te zoeken
        previous = self.head
        current = self.head.next

        while current is not None and current.task_name != task_name:
            previous = current
            current = current.next

        # Taak niet gevonden → stoppen
        if current is None:
            return

        # Taak gevonden → overslaan in de chain
        previous.next = current.next

    # ------------------------------------------------------------
    # 3. Alle taken afprinten (voor debug/test)
    # ------------------------------------------------------------
    def display_tasks(self):
        current = self.head
        while current is not None:
            print(f"{current.task_name}, {current.duration}, {current.priority}")
            current = current.next

    # ------------------------------------------------------------
    # 4. Taak zoeken op naam
    # ------------------------------------------------------------
    def find_task(self, task_name):
        current = self.head
        while current is not None:
            if current.task_name == task_name:
                return current   # gevonden
            current = current.next
        return None  # niet gevonden

    # ------------------------------------------------------------
    # 5. Totale duur van alle taken in de lijst
    # ------------------------------------------------------------
    def calculate_total_duration(self):
        total = 0
        current = self.head

        # Alle durations optellen
        while current is not None:
            total += current.duration
            current = current.next

        return total

    # ------------------------------------------------------------
    # 6. Taken inladen uit CSV-bestand
    # ------------------------------------------------------------
    def read_tasks_from_csv(self, file_path):
        import csv
        with open(file_path) as file:
            reader = csv.reader(file)
            next(reader)  # header overslaan

            # Elke rij is 1 taak
            for row in reader:
                task_name = row[0]
                duration = int(row[1])
                priority = int(row[2])
                self.add_task(task_name, duration, priority)

    # ------------------------------------------------------------
    # 7. Reorder enkel op PRIORITY (1 → 2 → 3)
    # ------------------------------------------------------------
    def reorder_tasks_by_priority(self):

        new_head = None
        current = self.head

        # We halen elke node uit de originele lijst
        # en steken die één voor één in een NIEUWE gesorteerde lijst
        while current is not None:
            next_node = current.next     # safe bijhouden
            current.next = None          # node losmaken
            new_head = self.sorted_insert_by_priority(new_head, current)
            current = next_node

        self.head = new_head   # lijst vervangen

    # ------------------------------------------------------------
    # 8. Reorder op PRIORITY + daarna DURATION
    # ------------------------------------------------------------
    def reorder_tasks_by_priority_duration(self):

        new_head = None
        current = self.head

        # Zelfde idee als hierboven: alle nodes één per één
        # opnieuw invoegen in een NIEUWE lijst
        while current is not None:
            next_node = current.next
            current.next = None
            new_head = self.sorted_insert_by_priority_duration(new_head, current)
            current = next_node

        self.head = new_head

    # ------------------------------------------------------------
    # 9. Hulpfunctie: één node in gesorteerde lijst steken op BASIS VAN PRIORITY
    # ------------------------------------------------------------
    def sorted_insert_by_priority(self, head, node):

        # Lijst leeg of node moet helemaal vooraan komen
        if head is None or node.priority < head.priority:
            node.next = head
            return node

        current = head

        # Zolang priority kleiner of gelijk is → verder lopen
        while current.next is not None and current.next.priority <= node.priority:
            current = current.next

        # Node invoegen
        node.next = current.next
        current.next = node

        return head

    # ------------------------------------------------------------
    # 10. Hulpfunctie: sorteren op PRIORITY én dan DURATION
    # ------------------------------------------------------------
    def sorted_insert_by_priority_duration(self, head, node):

        # Node moet vooraan komen → betere priority of zelfde priority maar kortere duration
        if (head is None or
            node.priority < head.priority or
            (node.priority == head.priority and node.duration < head.duration)):
            node.next = head
            return node

        current = head

        # Zoek correcte positie
        while current.next is not None:
            next_node = current.next

            # Stop als node vóór next_node moet komen
            if (node.priority < next_node.priority or
                (node.priority == next_node.priority and node.duration < next_node.duration)):
                break

            current = current.next

        # Node invoegen
        node.next = current.next
        current.next = node

        return head






