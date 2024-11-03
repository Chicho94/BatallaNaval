import random

class BatallaNaval:

  def __init__(self):
    self.__ships = {}
    self.__players = {
          0: {'name': 'jugador1', 'opponent': 1, 'board': [], 'ships': {}},
          1: {'name': 'cpu', 'opponent': 0, 'board': [], 'ships': {}}
      }
    self.__board_len = 10
    self.__current_turn = 0

  # Definiendo piezas del juego
  def __assign_piece(self):
    self.__ships = {
        'crucero': {'posiciones': 2, 'icono': 'C', 'hits': 0},
        'submarino':{'posiciones': 3, 'icono': 'S', 'hits': 0},
        'buque':{'posiciones': 4, 'icono': 'B', 'hits': 0}
      }

  # Creando tablero de juego
  def __make_board(self):
    return [[0 for _ in range(0,self.__board_len)] for _ in range(0,self.__board_len)]

  def __place_ship(self, board, ship, positions):
    for pos in positions:
      board[pos[0]][pos[1]] = ship

  def __can_place_ship(self, board, positions):
    return all(0 <= row < self.__board_len and 0 <= column < self.__board_len and board[row][column] == 0 for row, column in positions)

  def __generate_opponent_board(self):
      opponent_board = self.__make_board()
      for ship, info in self.__ships.items():
        placed = False
        while not placed:
          orientation = random.choice(['H', 'V'])
          row = random.randint(0, self.__board_len - 1)
          column = random.randint(0, self.__board_len - 1)

          positions = [(row + (i if orientation == 'V' else 0), column + (i if orientation == 'H' else 0))
                        for i in range(info['posiciones'])]
          if self.__can_place_ship(opponent_board, positions):
            self.__place_ship(opponent_board, ship, positions)
            placed = True

      return opponent_board

  # Asignacion de posiciones (para atacar o colocar una nave)
  def __choose_position(self,ship_size = 0):
    while True:
      try:
        row = int(input(f'Ingrese una fila del 0 al {self.__board_len - 1}: '))
        column = int(input(f'Ingrese una columna del 0 al {self.__board_len - 1}: '))
        if (0 <= row < self.__board_len - ship_size) and (0 <= column < self.__board_len - ship_size):
          return row, column
        print(f"El valor esta fuera del rango o ya está ocupado.")
      except ValueError:
        print(f'ERROR: al cargar filas o columnas')

  # Colocando piezas en el tablero
  def __get_position(self, position_quantity):
    row, column = self.__choose_position(position_quantity)

    while True:
      orientation = input('Ingrese alineación (H: Horizontal, V: Vertical): ').strip().upper()
      if orientation in ['H', 'V']:
        break
      print(f'ERROR: El valor debe ser H o V')

    positions = [[row + (i if orientation == 'V' else 0), column + (i if orientation == 'H' else 0)]
      for i in range(position_quantity)]

    return positions

  # Convirtiendo en X la celda seleccionada por el jugador para atacar a su oponente
  def __attack(self, player):
    print(f'Seleccione posiciones entre 0 y {self.__board_len} para atacar')
    row, column = self.__choose_position()
    cell = self.__players[player]['board'][row][column]
    self.__players[player]['board'][row][column] = 'X'

    if cell not in ['X', 0]:
      self.__players[player]['ships'][cell]['hits'] += 1

  def __cpu_attack(self):
    while True:
      row = random.randint(0, self.__board_len - 1)
      column = random.randint(0, self.__board_len - 1)
      if self.__players[0]['board'][row][column] not in ['X', 'O']:  # O could be a hit or miss marker
        cell = self.__players[0]['board'][row][column]
        self.__players[0]['board'][row][column] = 'X'
        if cell != 0:
          self.__players[0]['ships'][cell]['hits'] += 1
        print(f'El CPU ataca en la posición {row}, {column}.')
        break

  # Evaluando si todos los barcos del jugador fueron eliminados para finalizar el juego
  def __ongoing_game(self, player):
    print(self.__players[player]['name'], self.__players[player]['board'])
    return any(ship['hits'] != ship['posiciones'] for ship in self.__players[player]['ships'].values())

  # Cambiando de turno
  def __switch_turn(self):
    self.__current_turn = (self.__current_turn + 1) % 2

  # funcion principal para iniciar el juego
  def init_game(self):
    print(f'Creando un tablero de {self.__board_len} por {self.__board_len}\n')
    self.__assign_piece()
    self.__players[1]['board'] = self.__generate_opponent_board()  # Generar el tablero del cpu
    self.__players[0]['board'] = self.__make_board()

    # Preparando pieces del tablero del juegador
    for ship, info in self.__ships.items():
      
      while True:
        print(f'Coloca el barco "{ship.upper()}" en tu tablero (ocupara {info["posiciones"]} posiciones)')
        positions = self.__get_position(info["posiciones"])

        if self.__can_place_ship(self.__players[0]['board'], positions):
          for pos in positions:
            self.__players[0]['board'][pos[0]][pos[1]] = ship
          break
        else:
          print(f'El  "{ship.upper()}" no puede colocarse en ese lugar')

    print("Tablero Final:")
    for fila in self.__players[0]['board']:
      print(fila)

    self.__players[0]['ships'] = {k: v.copy() for k, v in self.__ships.items()}  # deep copy for ships dictionary
    self.__players[1]['ships'] = {k: v.copy() for k, v in self.__ships.items()}  # deep copy for ships dictionary

    print('Empezamos el juego \n')

    while self.__ongoing_game(self.__players[self.__current_turn]['opponent']):
      print(f'Es el turno del jugador {self.__players[self.__current_turn]["name"]}')
      if self.__current_turn == 0:
        self.__attack(self.__players[self.__current_turn]['opponent'])
      else:
        self.__cpu_attack()  # Ataque automático del CPU
      self.__switch_turn()
    
    print(f'El {self.__players[self.__current_turn]["name"]} es el ganador')

game = BatallaNaval()
game.init_game()