class Player:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.number < other.number

    def __str__(self):
        return f"{self.name} ({self.number})"

p1 = Player("Player 1", 1)
p2 = Player("Player 2", 2)
p3 = Player("Player 3", 3)
players = [p1, p2, p3]
print(p1)
print(p1 == p2)
print(p1 == Player("Player 1", 99))
sorted_players = sorted(players)
for p in sorted_players:
    print(p)

class Pass:
    def __init__(self, sender, receiver, nr_of_times):
        self.sender = sender
        self.receiver = receiver
        self.nr_of_times = nr_of_times

    def get_weight(self):
        return self.nr_of_times

    def get_start(self):
        return self.sender

    def get_end(self):
        return self.receiver

    def __eq__(self, other):
        if not isinstance(other, Pass):
            return NotImplemented
        return self.sender == other.sender and self.receiver == other.receiver

    def __str__(self):
        return f"Pass from {self.sender} to {self.receiver}"

    def __repr__(self):
        return str(self)

p1 = Player("Player 1", 1)
p2 = Player("Player 2", 2)
p3 = Player("Player 3", 3)

pass1 = Pass(p1, p2, 3)
pass2 = Pass(p2, p3, 3)
pass3 = Pass(p3, p1, 3)
print(pass1)
print(pass1 == pass2)
print(pass1 == Pass(p1, p2, 99))
print(pass1.get_weight())

class PassGraph:
    def __init__(self):
        self.player_list = []          # lijst van Player-objecten
        self.adj = {}              # dict: sender_name → lijst van Pass-objecten

    # --------------------------------------------------------
    # 1) BASISOPERATIES
    # --------------------------------------------------------

    def add_player(self, player):
        if player.name not in self.adj:
            self.player_list.append(player)
            self.adj[player.name] = []

    def has_player(self, player):
        if isinstance(player, Player):
            return player.name in self.adj
        if isinstance(player, str):
            return player in self.adj
        return False

    def get_player(self, name):
        for p in self.player_list:
            if p.name == name:
                return p
        return None

    def add_pass(self, sender, receiver, times=1):
        if times <= 0:
            raise ValueError("times must be positive")

        # spelers moeten bestaan
        if sender.name not in self.adj or receiver.name not in self.adj:
            raise ValueError("Both players must be added first")

        # kijk of pass al bestaat
        for p in self.adj[sender.name]:
            if p.receiver == receiver:
                p.nr_of_times += times
                return

        # nieuwe pass
        new_pass = Pass(sender, receiver, times)
        self.adj[sender.name].append(new_pass)

    def get_pass(self, sender_name, receiver_name):
        if sender_name not in self.adj:
            return None
        for p in self.adj[sender_name]:
            if p.receiver.name == receiver_name:
                return p
        return None

    def neighbors(self, sender_name):
        if sender_name not in self.adj:
            return []
        return self.adj[sender_name]

    # --------------------------------------------------------
    # 2) ANALYSEFUNCTIES
    # --------------------------------------------------------

    def total_weight(self, subset=None):
        if subset is None:
            subset = [p.name for p in self.players]

        total = 0

        for sender_name, passes in self.adj.items():
            if sender_name in subset:
                for p in passes:
                    if p.receiver.name in subset:
                        total += p.nr_of_times

        return total

    def pass_intensity(self, subset=None):
        if subset is None:
            subset = [p.name for p in self.players]

        n = len(subset)
        if n < 2:
            return 0.0

        numerator = self.total_weight(subset)
        denominator = n * (n - 1)

        return numerator / denominator

    def top_pairs(self, k=5):
        all_passes = []

        for sender_name in self.adj:
            for p in self.adj[sender_name]:
                all_passes.append(p)

        all_passes.sort(key=lambda p: p.nr_of_times, reverse=True)

        return all_passes[:k]

    def distribution_from(self, sender_name):
        if sender_name not in self.adj:
            return []

        pairs = [(p.receiver.name, p.nr_of_times) for p in self.adj[sender_name]]

        pairs.sort(key=lambda x: x[1], reverse=True)

        return pairs

    def players(self):
        return list(self.player_list)

    def passes(self):
        all_passes = []
        for sender_name in self.adj:
            for p in self.adj[sender_name]:
                all_passes.append(p)
        return list(all_passes)

    def __init__(self, path_name=None):
        self.player_list = []
        self.adj = {}

        if path_name is None:
            return

        try:
            with open(path_name, "r") as f:
                lines = f.readlines()
        except:
            raise ValueError("Cannot read file")

        current_section = None

        for raw in lines:
            line = raw.strip()

            # lege regels en commentaar negeren
            if not line or line.startswith("#"):
                continue

            # sectie wisselen
            if line == "[PLAYERS]":
                current_section = "PLAYERS"
                continue
            elif line == "[PASSES]":
                current_section = "PASSES"
                continue
            elif line.startswith("[") and line.endswith("]"):
                raise ValueError(f"Unknown section: {line}")

            # --------------------------
            # PLAYERS
            # --------------------------
            if current_section == "PLAYERS":
                if ";" not in line:
                    raise ValueError("Invalid player format")

                name, number_str = line.split(";", 1)
                name = name.strip()
                number_str = number_str.strip()

                try:
                    number = int(number_str)
                except:
                    raise ValueError("Invalid player number")

                self.add_player(Player(name, number))
                continue

            # --------------------------
            # PASSES
            # --------------------------
            if current_section == "PASSES":
                if "->" not in line or ":" not in line:
                    raise ValueError("Invalid pass format")

                sender_part, rest = line.split("->", 1)
                receiver_part, nr_str = rest.split(":", 1)

                sender_name = sender_part.strip()
                receiver_name = receiver_part.strip()
                nr_str = nr_str.strip()

                try:
                    nr = int(nr_str)
                    if nr <= 0:
                        raise ValueError
                except:
                    raise ValueError("Invalid pass weight")

                sender_obj = self.get_player(sender_name)
                receiver_obj = self.get_player(receiver_name)

                if sender_obj is None or receiver_obj is None:
                    raise ValueError("Pass refers to unknown player")

                self.add_pass(sender_obj, receiver_obj, nr)
                continue

            raise ValueError("Line outside section")

    def save_to_txt(self, path):
        with open(path, "w") as f:
            f.write("[PLAYERS]\n")
            for p in self.player_list:
                f.write(f"{p.name};{p.number}\n")

            f.write("[PASSES]\n")
            for sender_name in self.adj:
                for p in self.adj[sender_name]:
                    f.write(f"{p.sender.name} -> {p.receiver.name} : {p.nr_of_times}\n")


g = PassGraph()
p1 = Player("Kevin", 7)
p2 = Player("Eden", 10)
p3 = Player("Romelu", 9)
p4 = Player("Dries", 14)
g.add_player(p1)
g.add_player(p2)
g.add_player(p3)
g.add_player(p4)
g.add_pass(p1, p2, 3)   # Kevin → Eden (3)
g.add_pass(p1, p3, 1)   # Kevin → Romelu (1)
g.add_pass(p2, p1, 2)   # Eden → Kevin (2)
g.add_pass(p2, p3, 4)   # Eden → Romelu (4)
g.add_pass(p3, p4, 5)   # Romelu → Dries (5)
g.add_pass(p4, p1, 2)   # Dries → Kevin (2)
print("Neighbors of Kevin:", g.neighbors("Kevin"))
print("Pass Kevin -> Eden:", g.get_pass("Kevin", "Eden"))
print("Top 3 pairs:", g.top_pairs(3))
subset = ["Kevin", "Eden", "Romelu"]
print("Total weight subset:", g.total_weight(subset))
print("Pass intensity subset:", g.pass_intensity(subset))
print("Distribution from Eden:", g.distribution_from("Eden"))

# Testscript Deel 4

g = PassGraph()

# spelers
p1 = Player("Kevin", 7)
p2 = Player("Eden", 10)
p3 = Player("Romelu", 9)
p4 = Player("Dries", 14)

g.add_player(p1)
g.add_player(p2)
g.add_player(p3)
g.add_player(p4)

# passes (let op de dubbele toevoeging!)
g.add_pass(p1, p2, 3)
g.add_pass(p1, p3, 1)
g.add_pass(p2, p3, 2)
g.add_pass(p2, p3, 4)   # zelfde pass opnieuw → nr wordt 6

# opslaan
g.save_to_txt("team.txt")

# opnieuw inlezen
g2 = PassGraph("team.txt")

print("Players loaded:", [str(p) for p in g2.players()])
print("Passes loaded:")
for p in g2.passes():
    print(p)







