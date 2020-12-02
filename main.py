import random
import time


class Manager:
	def __init__(self):
		menu = input('Привет!\nЭто игра крестики нолики\n1)Начать игру\n2)Посмотреть рейтинг ')
		if menu == '2':
			self.show_rating()
		else:

			size_map = int(input('Введите размер карты : '))
			game = Game(size_map)

			game.start_game_loop()


	@staticmethod
	def show_rating():
		with open('score.txt') as file:
			lines = [line.strip() for line in file]
			counts_wins_cross = int(lines[0][20])
			counts_wins_zero = int(lines[1][19])
			print(f'Количество побед крестиков - {counts_wins_cross}')
			print(f'Количество побед ноликов - {counts_wins_zero}')

	
class Game:
	def __init__(self,size_map):
		self.size_map = size_map
		self.map = [[-1 for x in range(size_map)] for row in range(size_map)]
		self.cross = '✖ '
		self.zero = '● '
		self.score_for_win = len(self.map[0])

		self.turn_right = random.randint(0,1)
		self.situation = 0

	def draw_map(self):
		for line in self.map:
			for row in line:
				if row == -1:
					print('- ',end='')
				else:
					print(self.cross if row == self.cross else self.zero, end='')
			print('')


	def turn(self,position,turn_right):
		if self.map[int(position[0]) - 1][int(position[1]) - 1] != -1:
			return False 
		self.map[int(position[0]) - 1][int(position[1]) - 1] = turn_right

	def game_over(self,last_turn):
		# проверка на лайн горизантально
		if last_turn == -1:
			return False
		if self.map[int(last_turn[0]) - 1][:] == [self.cross for line in range(self.score_for_win)] or self.map[int(last_turn[0]) - 1][:] == [self.zero for line in range(self.score_for_win)]:
			return True
		correct_map_order = []
		# проверка на лайн вертикально
		for row in range(self.score_for_win):
			correct_map_order.append(self.map[row][int(last_turn[1]) - 1])
		if correct_map_order == [self.cross for line in range(self.score_for_win)] or correct_map_order == [self.zero for line in range(self.score_for_win)]:
			return True 
		# проверка на лайн косыми
		correct_map_order = []
		for row in range(self.score_for_win - 1,-1,-1):
			correct_map_order.append(self.map[row][row])
		if correct_map_order == [self.cross for line in range(self.score_for_win)] or correct_map_order == [self.zero for line in range(self.score_for_win)]:
			return True

		correct_map_order = []
		line = self.score_for_win - 1
		for row in range(self.score_for_win):
			correct_map_order.append(self.map[line][row])
			line -= 1
		if correct_map_order == [self.cross for line in range(self.score_for_win)] or correct_map_order == [self.zero for line in range(self.score_for_win)]:
			return True

		score = 0
		for el in self.map:
			for zel in el:
				if zel == -1:
					score += 1

		if score == 0:
			self.situation = 'Ничья'
			return 'Ничья'

		return False
		

	def start_game_loop(self):
		turn_pos = -1
		while not self.game_over(turn_pos):
			try:
				self.draw_map()
				turn_right_notification = 'крестиков' if self.turn_right == 0 else 'ноликов'
				print(f'Ход {turn_right_notification}')
				
				turn_pos = input('Введите позицию(пример 3 3, 3 ряд 3 ячейка) : ').split(' ')

				if self.turn(turn_pos, self.cross if self.turn_right == 0 else self.zero) == False:
					print('Ячейка уже занята!')
					self.start_game_loop()

				self.turn_right = 0 if self.turn_right == 1 else 1
			except IndexError:
					print('Такой ячейки нет!')
					self.start_game_loop()
		self.draw_map()
		if self.situation == 'Ничья':
			print('Ничья')
			exit()
		else:
			print(f'Выиграла команда {turn_right_notification}')
			for_upgrade = 'cross' if turn_right_notification == 'крестиков' else 'null'
			self.add_counts_wins(for_upgrade)
			time.sleep(2)
			exit()

	def add_counts_wins(self,aim_for_upgrade):
		with open('score.txt') as file:
			lines = [line.strip() for line in file]
			counts_wins_cross = int(lines[0][20])
			counts_wins_null = int(lines[1][19])


		with open('score.txt','w') as file:
			file.write(f'counts wins cross = {counts_wins_cross + 1}\ncounts wins null = {counts_wins_null}') if aim_for_upgrade == 'cross' else file.write(f'counts wins cross = {counts_wins_cross}\ncounts wins null = {counts_wins_null + 1}')





if __name__ == '__main__':
	manager = Manager()
