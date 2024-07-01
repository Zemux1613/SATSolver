from collections import defaultdict

class TwoSAT:
    def __init__(self, num_vars):
        """
        Initialisiert die TwoSAT-Klasse mit der Anzahl der Variablen und den benötigten Datenstrukturen.

        Args:
            num_vars (int): Anzahl der Variablen.
        """
        self.n = num_vars * 2  # Jede Variable und ihre Negation
        self.adj = defaultdict(list)  # Adjazenzliste für den implizierten Graphen
        self.adj_t = defaultdict(list)  # Transponierte Adjazenzliste
        self.used = [False] * self.n  # Zur Verfolgung besuchter Knoten
        self.order = []  # Reihenfolge der Knoten nach Abschlusszeiten
        self.comp = [-1] * self.n  # Komponenten-Zuordnungen nach DFS
        self.assignment = [False] * num_vars  # Wahrheitszuweisungen für Variablen
        self.formula = ""  # Zur Speicherung der Formel für Erklärungszwecke

    def dfs1(self, v):
        """
        Führt eine Tiefensuche durch, um die Reihenfolge der Knoten nach Abschlusszeiten zu erhalten.

        Args:
            v (int): Aktueller Knoten.
        """
        self.used[v] = True
        for u in self.adj[v]:
            if not self.used[u]:
                self.dfs1(u)
        self.order.append(v)

    def dfs2(self, v, cl):
        """
        Führt eine Tiefensuche durch, um die stark zusammenhängenden Komponenten zu bestimmen.

        Args:
            v (int): Aktueller Knoten.
            cl (int): Aktuelle Komponente.
        """
        self.comp[v] = cl
        for u in self.adj_t[v]:
            if self.comp[u] == -1:
                self.dfs2(u, cl)

    def solve_2SAT(self):
        """
        Löst das 2-SAT-Problem.

        Returns:
            bool: True, wenn das Problem erfüllbar ist, sonst False.
        """
        self.order.clear()
        self.used = [False] * self.n
        for i in range(self.n):
            if not self.used[i]:
                self.dfs1(i)

        self.comp = [-1] * self.n
        for i in range(self.n):
            v = self.order[self.n - i - 1]
            if self.comp[v] == -1:
                self.dfs2(v, i)

        for i in range(0, self.n, 2):
            if self.comp[i] == self.comp[i + 1]:
                return False
            self.assignment[i // 2] = self.comp[i] > self.comp[i + 1]
        return True

    def add_disjunction(self, a, na, b, nb):
        """
        Fügt eine Disjunktion zur Formel hinzu und aktualisiert den implizierten Graphen entsprechend.

        Args:
            a (int): Variable a.
            na (bool): True, wenn a negiert ist, sonst False.
            b (int): Variable b.
            nb (bool): True, wenn b negiert ist, sonst False.
        """
        a = 2 * a + int(na)
        b = 2 * b + int(nb)
        neg_a = a ^ 1
        neg_b = b ^ 1
        self.adj[neg_a].append(b)
        self.adj[neg_b].append(a)
        self.adj_t[b].append(neg_a)
        self.adj_t[a].append(neg_b)
        self.formula += '(' + ('-' if na else '') + 'x' + str(a) + ' | ' + ('-' if nb else '') + 'x' + str(b) + ') & '
