# Importando las librerías necesarias para el juego
import random

# Definición de las constantes para los niveles de dificultad
LEVELS = {
    "beginner": (8, 8, 10),  # 8x8 tablero con 10 minas
    "intermediate": (16, 16, 40),  # 16x16 tablero con 40 minas
    "expert": (16, 30, 99)  # 16x30 tablero con 99 minas
}


# Función para imprimir el tablero
def print_board(board):
    print("  " + " ".join([chr(i) for i in range(ord('a'), ord('a') + len(board[0]))]))
    for idx, row in enumerate(board):
        print(str(idx + 1).rjust(2) + " " + " ".join(row))


# Función para inicializar el tablero de juego
def initialize_board(rows, cols, mines):
    board = [['-' for _ in range(cols)] for _ in range(rows)]
    mine_locations = set()
    while len(mine_locations) < mines:
        location = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        mine_locations.add(location)
    return board, mine_locations


# Función para comenzar el juego, permitiendo al usuario elegir la dificultad
def start_game():
    print("Selecciona la dificultad:")
    print("1. Principiante (8x8, 10 minas)")
    print("2. Intermedio (16x16, 40 minas)")
    print("3. Experto (16x30, 99 minas)")

    choice = input("Elige una opción (1, 2, 3): ")
    if choice in ['1', '2', '3']:
        choice = int(choice)
        if choice == 1:
            level = "beginner"
        elif choice == 2:
            level = "intermediate"
        else:
            level = "expert"

        rows, cols, mines = LEVELS[level]
        board, mine_locations = initialize_board(rows, cols, mines)
        print_board(board)
        return board, mine_locations
    else:
        print("Opción no válida.")
        return start_game()


# Función para revelar una casilla en el tablero
def reveal_cell(board, mine_locations, x, y):
    # Chequear si la casilla contiene una mina
    if (x, y) in mine_locations:
        return True  # El jugador ha revelado una mina

    # Contar minas adyacentes
    adjacent_mines = 0
    for i in range(max(0, x - 1), min(len(board), x + 2)):
        for j in range(max(0, y - 1), min(len(board[0]), y + 2)):
            if (i, j) in mine_locations:
                adjacent_mines += 1

    # Actualizar la casilla con el número de minas adyacentes
    board[x][y] = str(adjacent_mines) if adjacent_mines > 0 else ' '

    return False  # No se ha revelado una mina


# Función para colocar una bandera
def place_flag(board, x, y):
    if board[x][y] == '-':
        board[x][y] = 'F'
    elif board[x][y] == 'F':
        board[x][y] = '-'


# Función para convertir la entrada del usuario a coordenadas
def parse_input(input_str, rows, cols):
    if len(input_str) < 2 or not input_str[0].isalpha() or not input_str[1:].isdigit():
        return None

    col = ord(input_str[0].lower()) - ord('a')
    row = int(input_str[1:]) - 1

    # Asegurar que la fila y la columna estén dentro de los límites del tablero
    if col < 0 or col >= cols or row < 0 or row >= rows:
        return None

    return row, col


# Actualización de la función del bucle principal del juego para usar la función parse_input mejorada
def main_game_loop(board, mine_locations):
    rows, cols = len(board), len(board[0])
    while True:
        print_board(board)
        user_input = input("Introduce la coordenada (e.g., 'a1') y acción ('d' para cavar, 'f' para bandera): ")
        if len(user_input.split()) != 2:
            print("Entrada no válida. Por favor, sigue el formato 'a1 f'.")
            continue

        coord, action = user_input.split()
        coord = parse_input(coord, rows, cols)  # Usar la función mejorada con límites
        if not coord:
            print("Coordenadas no válidas.")
            continue

        x, y = coord
        if action == 'd':  # Cavar
            if reveal_cell(board, mine_locations, x, y):
                print("¡Boom! Has encontrado una mina.")
                break
        elif action == 'f':  # Colocar bandera
            place_flag(board, x, y)
        else:
            print("Acción no reconocida.")
            continue

        # Comprobar si el juego ha sido ganado
        if check_win(board, mine_locations):
            print("¡Felicidades! Has despejado todas las minas.")
            break

# Función para verificar si el jugador ha ganado
def check_win(board, mine_locations):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '-' and (x, y) not in mine_locations:
                return False  # Aún hay casillas seguras sin revelar
    return True  # Todas las casillas seguras han sido reveladas

# Corremos el juego
def play_buscaminas():
    board, mine_locations = start_game()
    main_game_loop(board, mine_locations)

play_buscaminas()
