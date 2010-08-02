import curses, sys, random
from time import sleep

# snake's directions (this snake lives in 2D world, so...)
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

# redraw and refresh entire screen
def redraw():
	win.erase()

	if paused == True:
		drawCaption(" press space to continue ")
	else:
		drawCaption(" snake "+str(len(snake))+" ")

	drawFood()
	drawSnake()
	win.refresh()

# draw top border with specified text
def drawCaption(text):
	global cols
	win.addstr(0, 0, "." * cols)
	win.addstr(0, (cols - len(text)) / 2, text)

# draw snake
def drawSnake():
	try:
		n = 0
		for pos in snake:
			if n == 0:
				win.addstr(pos[1], pos[0], "@")
			else:
				win.addstr(pos[1], pos[0], "#")
			n += 1
	except:
		pass

# draw all the food
def drawFood():
	try:
		for pos in food:
			win.addstr(pos[1], pos[0], "+")
	except:
		pass

# check if snake has just eaten the food
def isFoodCollision():
	for pos in food:
		if pos == snake[0]:
			food.remove(pos)
			return True
	return False

# check if snake has just commited suicide
def isSuicide():
	for i in xrange(0, len(snake)):
		if i > 0 and snake[i] == snake[0]:
			return True
	return False

# end game gracefully
def endGame():
	curses.nocbreak();
	win.keypad(0);
	curses.echo()
	curses.endwin()

# move snake one step forward
def moveSnake():
	global snake
	global grow_snake
	global cols, rows

	# get head
	head = snake[0]

	# remove tail
	if (grow_snake == False):
		snake.pop()
	else:
		grow_snake = False

	# calculate where head will be
	if (dir == DIR_UP):
		head = [head[0], head[1]-1]
		if head[1] == -1:
			head[1] = rows
	elif (dir == DIR_RIGHT):
		head = [head[0]+1, head[1]]
		if head[0] == cols:
			head[0] = 0
	elif (dir == DIR_DOWN):
		head = [head[0], head[1]+1]
		if head[1] == rows+1:
			head[1] = 0
	elif (dir == DIR_LEFT):
		head = [head[0]-1, head[1]]
		if head[0] == -1:
			head[0] = cols-1

	# insert new head
	snake.insert(0, head)

# drop new food, but not on snake or on another food
def dropFood():
	x = random.randint(0, cols)
	y = random.randint(1, rows)

	for pos in food:
		if pos == [x,y]:
			dropFood()
			return

	for pos in snake:
		if pos == [x,y]:
			dropFood()
			return

	food.append([x,y])

# stop all the action and print the sad news
def gameOver():
	global is_game_over
	is_game_over = True
	drawCaption("game over. total points: "+str(len(snake))+". press q to exit")

# init -------------------------------------------------------------------------

field = []
snake = [[10,5], [9,5], [8,5], [7,5]]
dir = DIR_RIGHT;
food = []
grow_snake = False
is_game_over = False

# start in non paused mode
paused = False

# init curses library
win = curses.initscr();

# enable arrow keys
win.keypad(1)

# do not wait for keypress
win.nodelay(1)

# hide cursor
curses.curs_set(0)

# read keys instantaneously
curses.cbreak()

# do not print stuff when key is presses
curses.noecho()

# get terminal size
rows, cols = win.getmaxyx()
rows -= 1

# start -------------------------------------------------------------------------

dropFood()
redraw()

while (True):
	if (is_game_over == False and paused == False):
		redraw()
	key = win.getch()
	sleep(0.1)

	if (key != -1):

		if (key == curses.KEY_UP):
			if dir != DIR_DOWN:
				dir = DIR_UP
		elif (key == curses.KEY_RIGHT):
			if dir != DIR_LEFT:
				dir = DIR_RIGHT
		elif (key == curses.KEY_DOWN):
			if dir != DIR_UP:
				dir = DIR_DOWN
		elif (key == curses.KEY_LEFT):
			if dir != DIR_RIGHT:
				dir = DIR_LEFT
		elif (key == 32):
			paused = not paused
			redraw()
		elif (chr(key) == "q"):
			break

	if (is_game_over == False and paused == False):
		moveSnake()

		if (isSuicide()):
			gameOver()

		if (isFoodCollision()):
			dropFood()
			grow_snake = True

endGame()
