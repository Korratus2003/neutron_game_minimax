# Dokumentacja projektu: Neutron z AI

## Opis projektu

Projekt przedstawia komputerową wersję planszowej gry **Neutron**, w której gracz mierzy się z przeciwnikiem sterowanym przez algorytm sztucznej inteligencji. Interfejs graficzny został zaimplementowany z wykorzystaniem biblioteki `tkinter`, natomiast logika gry oraz AI opierają się na module `minimax` z przycinaniem alfa-beta.

Projekt umożliwia:

* Grę człowieka przeciwko AI (gracz "W", AI "B").
* Pełną wizualizację planszy i pionków.
* Automatyczne ruchy przeciwnika AI.

---

## Zasady gry Neutron

Gra odbywa się na planszy 5x5. Każdy gracz posiada 5 pionków:
(początkowo był gracz biały i czarny teraz gracz zielony i czerwony - nie zmienialiśmy tych zmiennych)

* **W**: gracz (biały/zielony)
* **B**: komputer (czarny/czerwony)
* **N**: neutron (neutralny)

### Cel gry

Doprowadzić neutron na własną linię bazową (W: góra, B: dół) lub zablokować przeciwnika.

### Tura

Każda tura składa się z 2 ruchów:

1. **Ruch neutronem** (obowiązkowy).
2. **Ruch jednym własnym pionkiem**.

Neutron i pionki poruszają się w dowolnym z 8 kierunków (jak hetman w szachach), do najdalszego wolnego pola.

Gra kończy się, gdy:

* Neutron dotrze do bazy któregoś gracza.
* Neutron nie ma żadnego legalnego ruchu.
* Gracz nie ma żadnego legalnego ruchu po ruchu neutronem.

---

## Szczegóły implementacji

### Struktura plików

* **`game_logic.py`**: reprezentacja stanu gry, reguły, możliwe ruchy.
* **`ai_minimax.py`**: algorytm AI (minimax + przycinanie alfa-beta).
* **`neutron_gui.py`**: graficzny interfejs gry oparty na `tkinter`.

---

### Klasa GameState (logika gry)

```python
class GameState:
    def __init__(self, board, neutron_pos, current_player):
        self.board = [list(row) for row in board]
        self.neutron_pos = neutron_pos
        self.current_player = current_player
```

* `board`: 5x5 plansza z kropkami (`.`), pionkami (`W`, `B`) i neutronem (`N`).
* `neutron_pos`: pozycja neutronu (wiersz, kolumna).
* `current_player`: `"W"` lub `"B"`.

#### Ruchy pionków i neutrona

Ruch odbywa się po prostych liniach do pierwszej napotkanej przeszkody.

```python
def get_piece_moves(self, pos, board=None):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), ...]
    # Każdy kierunek, dopóki nie napotkamy innego pionka
```

#### Sprawdzenie legalnych ruchów:

```python
def get_legal_moves(self):
    neutron_moves = self.get_piece_moves(self.neutron_pos)
    for nm in neutron_moves:
        if self.is_winning_neutron_move(nm):
            moves.append((nm, None))
        else:
            temp_board = self.apply_neutron_move(nm)
            for piece in self.get_own_pieces(temp_board):
                for pm in self.get_piece_moves(piece, temp_board):
                    moves.append((nm, (piece, pm)))
```

### Funkcja oceny heurystycznej

```python
def evaluate(state, maximizing_player):
    if state.is_terminal():
        return math.inf if winner == maximizing_player else -math.inf

    if maximizing_player == 'W':
        return 4 - state.neutron_pos[0]  # Im bliżej góry, tym lepiej dla W
    else:
        return state.neutron_pos[0]      # Im bliżej dołu, tym lepiej dla B
```

Ta prosta funkcja heurystyczna ocenia tylko **poziom neutronu**, co jest skuteczne przy ograniczonej głębokości, ale nie uwzględnia pozycji pionków.

---

### Jak działa minimax z przycinaniem

Algorytm minimax przeszukuje drzewo wszystkich możliwych ruchów, zakładając, że:

* gracz maksymalizujący (AI) wybiera najlepszy dostępny ruch,
* gracz minimalizujący (człowiek) wybiera ruch najgorszy dla AI.

Przycinanie alfa-beta pozwala **pominąć całe poddrzewa**, które nie mogą wpłynąć na ostateczny wynik.

Schematycznie:

```text
AI (max)
|
|- ruch 1 (wartość = 3)
|
|- ruch 2
     |- gracz (min): ruch a (eval = 2)  ✓
     |- gracz (min): ruch b (eval = 6)  X (przycięte)
```

### Przykład

Załóżmy, że neutron jest na pozycji (2,2). AI (czarny) ma pionki na dolnym rzędzie.
Jeśli AI może przesunąć neutron do (3,2), a potem pionek do (2,2), to zatrzymuje neutron w centrum planszy.

Drzewo głębokości 3 może przewidzieć tylko najbliższe zagrożenia, natomiast głębokość 5 pozwoli przewidzieć, że przeciwnik może wykona kontratak i przejąć kontrolę nad neutronem.

---

### Funkcja oceny heurystycznej

```python
def evaluate(state, maximizing_player):
    if state.is_terminal():
        return math.inf if winner == maximizing_player else -math.inf

    if maximizing_player == 'W':
        return 4 - state.neutron_pos[0]  # Im bliżej góry, tym lepiej dla W
    else:
        return state.neutron_pos[0]      # Im bliżej dołu, tym lepiej dla B
```

### Przykład działania heurystyki:

- **Neutron na (2,2)**: wynik = 2 dla B  
  → Pozycja centralna – daje elastyczność, ale jeszcze daleko od dolnej krawędzi, więc nie daje przewagi punktowej.

- **Neutron na (inf,2)**: wynik = 4 (idealny wynik dla B)  
  → Neutron znajduje się bezpośrednio na dolnej linii, czyli linii zwycięstwa B. AI wygrywa lub ma natychmiastową przewagę.

- **Neutron na (-inf,1)**: wynik = 0 (bardzo zły dla B)  
  → Neutron znajduje się tuż przy linii zwycięstwa przeciwnika (W). W następnej turze może go po prostu przesunąć na swoją linię i wygrać – krytyczne zagrożenie.


## Heurystyki: jakie można by użyć?

### Aktualna:

* Pozycja neutronu na osi pionowej (wiersz).
* Bardzo szybka, skuteczna w połączeniu z przycinaniem.

### Alternatywne heurystyki:

1. **Liczba możliwych ruchów przeciwnika** (im mniej, tym lepiej).
2. **Odległość neutrona od baz gracza** (np. Manhattan distance).
3. **Zablokowanie neutrona przez pionki przeciwnika.**

### Dlaczego nasza jest optymalna?

* Jest **deterministyczna**, szybka do policzenia.
* Działa wystarczająco dobrze przy głębokości 3–5.

---

## Rozszerzenia projektu

1. **Nowe heurystyki** (hybrydowe funkcje oceny, z wagami).
2. **Inne tryby gry**:

   * Gracz vs Gracz (lokalnie lub online).
   * AI vs AI (tryb testowy).
3. **Wizualizacja drzew decyzyjnych AI**.
4. **Tryb "undo" / zapis stanu gry**.
5. **Zmienna wielkość planszy (np. 7x7)**.

---

## Instalacja i uruchomienie

### Wymagania

* Python 3.x
* `tkinter` (wbudowany w standardowe instalacje Pythona)

### Uruchomienie

```bash
python neutron_gui.py
```

---

## Autorzy

- Konrad Szyszlak, 131524
- Nobert Fuk, 131431
- Krzysztof Majka, 131467

---
