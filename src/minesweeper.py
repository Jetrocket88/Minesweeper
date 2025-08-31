import random
import os
import time
import pygame
import pygame.font

CELL_SQUARE = 70
	
GREEN = (10, 160, 10)
LIGHT_BROWN = (221, 181, 110)
RED = (255, 0, 0)

NUM_CELL_COLS = 8	
NUM_CELL_ROWS = 8

SCREEN_WIDTH = NUM_CELL_ROWS * CELL_SQUARE 
SCREEN_HEIGHT = NUM_CELL_COLS * CELL_SQUARE 

CELLS_TO_REMOVE = NUM_CELL_COLS + NUM_CELL_ROWS 
MINES_TO_ADD = 14 

currentDir = os.path.dirname(os.path.abspath(__file__))
flagPath = currentDir + "\\..\\resources\\flag.png"
print(flagPath)

FLAG_IMG = pygame.image.load(flagPath)
FLAG_IMG = pygame.transform.scale(FLAG_IMG, (CELL_SQUARE, CELL_SQUARE))

FONT_PATH = "c:\WINDOWS\Fonts\CASCADIACODE.TTF"

if MINES_TO_ADD > NUM_CELL_COLS * NUM_CELL_ROWS:
	raise Exception("Too many mines")

class NDCell():
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color 
		self.rect = pygame.Rect(x, y, CELL_SQUARE, CELL_SQUARE)
		self.flagged = False
		if (self.x // CELL_SQUARE) % 2 == (self.y // CELL_SQUARE) % 2:
			self.color = [min(c + 10, 255) for c in self.color]
	def draw(self, canvas):
		pass


class Cell(NDCell): 
	def draw(self, canvas, cells):
		self.rect.update(self.x, self.y, CELL_SQUARE, CELL_SQUARE)
		pygame.draw.rect(canvas, self.color, self.rect)
		if self.flagged:
			canvas.blit(FLAG_IMG, (self.x, self.y))

class mineCell(Cell):
	pass

class numberCell(Cell):
	def __init__(self, x, y, color):
		super().__init__(x, y, color)
		self.number = getAdjacentBombs(self.x, self.y, cells) 
	def draw(self, canvas):
		self.number = getAdjacentBombs(self.x, self.y, cells)
		super().draw(canvas, cells)
		fontSize = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 25 
		font = pygame.font.Font(FONT_PATH, fontSize)
		text = font.render(str(self.number), True, (0, 0, 0))
		if self.number > 0:
			canvas.blit(text, (self.x + (CELL_SQUARE - fontSize // 2) // 2, self.y + (CELL_SQUARE - fontSize // 2) // 2))

def linearSearch(cell, cells):
	for index, x in enumerate(cells):
		if x == cell:
			return index 
	raise Exception("Couldn't find cell, this shouldnt happen")

def findCellInArray(x, y, cells):
	for index, cell in enumerate(cells):
		if cell.x == x and cell.y == y:
			return index 
	raise Exception("Couldn't find cell, this shouldnt happen")


def getAdjacentCells(cellX, cellY, cells):
	adjCells = []
	if (cellX + CELL_SQUARE) < SCREEN_WIDTH:
		adjCells.append(cells[findCellInArray(cellX + CELL_SQUARE, cellY, cells)])
	if (cellX - CELL_SQUARE) >= 0: 
		adjCells.append(cells[findCellInArray(cellX - CELL_SQUARE, cellY, cells)])
	if (cellY + CELL_SQUARE) < SCREEN_HEIGHT:
		adjCells.append(cells[findCellInArray(cellX, cellY + CELL_SQUARE, cells)])
	if (cellY - CELL_SQUARE) >= 0: 
		adjCells.append(cells[findCellInArray(cellX, cellY - CELL_SQUARE, cells)])
	return adjCells

def firstClick(cellX, cellY, cells):
	emptyCellArray = []
	adjCells = []
	emptyCellArray.append(cells[findCellInArray(cellX, cellY, cells)])

	while (len(emptyCellArray) < CELLS_TO_REMOVE):
		for eCell in emptyCellArray:
			temp = getAdjacentCells(eCell.x, eCell.y, cells)
			for t in temp:
				adjCells.append(t)      

		for adjCell in adjCells:
			if random.randint(1, 100) <= 10:
				emptyCellArray.append(adjCell)
		adjCells.clear()

	for eCell in emptyCellArray:
		cells[findCellInArray(eCell.x, eCell.y, cells)] = numberCell(eCell.x, eCell.y, LIGHT_BROWN)

	for eCell in emptyCellArray:
		temp = getAdjacentCells(eCell.x, eCell.y, cells)
		for t in temp:
			if type(t) == Cell:
				cells[findCellInArray(t.x, t.y, cells)] = numberCell(t.x, t.y, LIGHT_BROWN)
	
	cellList = [x for x in cells if type(x) == Cell]
	mineList = []
	random.shuffle(cellList)
	for x in range(MINES_TO_ADD):
		c = cellList[x]
		if type(c) == Cell and c not in mineList:
			mineList.append(c)	
	for m in mineList:
		cells[findCellInArray(m.x, m.y, cells)] = mineCell(m.x, m.y, GREEN)

def getAdjacentBombs(x, y, cells):
	directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
	count = 0
	for dir in directions:
		newX = x + dir[0] * CELL_SQUARE
		newY = y + dir[1] * CELL_SQUARE
		if 0 <= newX < SCREEN_WIDTH and 0 <= newY < SCREEN_HEIGHT:
			adjCell = cells[findCellInArray(newX, newY, cells)]
			if isinstance(adjCell, mineCell):
				count += 1
	return count


def getAdjacentCellsLarger(x, y, cells):
	directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
	adjCells = []
	for dir in directions:
		newX = x + dir[0] * CELL_SQUARE
		newY = y + dir[1] * CELL_SQUARE
		if 0 <= newX < SCREEN_WIDTH and 0 <= newY < SCREEN_HEIGHT:
			adjCells.append(cells[findCellInArray(newX, newY, cells)])
	return adjCells
				
def drawAll(canvas, cells):
	for c in cells:
		if type(c) != numberCell:
			c.draw(canvas, cells)
		else:
			c.draw(canvas)

print("Which size would you like to play?")
print("Small (9x9), Medium (16x16), Large (30x16)")
timeSinceClick = 0
exit2 = False
while exit2 == False:
	cells = []
	canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

	numFlagged = 0
	pygame.font.init()
	clock = pygame.time.Clock()

	exit = False
	first = True
	flaggedArray = []
	won = False
	rightClickCooldown = 1

	for y in range(0, SCREEN_HEIGHT, CELL_SQUARE):
		for x in range(0, SCREEN_WIDTH, CELL_SQUARE):
			cells.append(Cell(x, y, GREEN))

	while exit == False: 
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				exit2 = True
				exit = True
		numMines = len([x for x in cells if type(x) == mineCell])
		numFlags = numMines - numFlagged 
		pygame.display.set_caption(f"Minesweeper - {numFlags} remaining")

		pygame.display.update() 
		canvas.fill((0, 128, 0))

		drawAll(canvas, cells)

		rightClickCooldown -= 1

		for c in cells:
			if pygame.mouse.get_pressed()[0] and c.rect.collidepoint(pygame.mouse.get_pos()): 
				if type(c) == Cell:
					if first == True:
						firstClick(c.x, c.y, cells)
						start = time.time()
						first = False   
					cells[findCellInArray(c.x, c.y, cells)] = numberCell(c.x, c.y, LIGHT_BROWN)
				elif type(c) == mineCell and c.flagged == False:
					exit = True
					won = False 
			elif pygame.mouse.get_pressed()[2] and c.rect.collidepoint(pygame.mouse.get_pos()) and type(c) != numberCell: 
				if rightClickCooldown <= 0:
					if c.flagged == True:
						c.flagged = False
						numFlagged -= 1
						flaggedArray.remove(c)
					else:
						c.flagged = True
						numFlagged += 1
						flaggedArray.append(c)
				rightClickCooldown = 5


		for i in range(len(cells)):
			c = cells[i]
			if isinstance(c, numberCell) and c.number == 0:
				adjCells = getAdjacentCellsLarger(c.x, c.y, cells)
				for aC in adjCells:
					cells[findCellInArray(aC.x, aC.y, cells)] = numberCell(aC.x, aC.y, LIGHT_BROWN)
		

		numMines = len([x for x in cells if type(x) == mineCell])
		mineList = [x for x in cells if type(x) == mineCell and x.flagged is True]	
		if len(mineList) == numMines and numMines != 0 and len([x for x in cells if type(x) == Cell]) == 0:
			end = time.time()
			exit = True
			won = True
		clock.tick(60)

	cells = [numberCell(c.x, c.y, LIGHT_BROWN) if isinstance(c, Cell) else c for c in cells]
	drawAll(canvas, cells)
	pygame.display.update()

	fontSize = 0
	redFactor = 22
	if won:
		fontSize = min(SCREEN_WIDTH, SCREEN_HEIGHT) // redFactor 
		font = pygame.font.Font(FONT_PATH, fontSize)
		youWon = font.render("You Won!", True, (0, 0, 0))
		timeMsg = font.render(f"Time Taken: {round(end - start, 1)}s", True, (0, 0, 0))
		canvas.blit(youWon, (SCREEN_WIDTH // 2 - youWon.get_width() // 2, SCREEN_HEIGHT // 2 - youWon.get_height() // 2))
		canvas.blit(timeMsg, (SCREEN_WIDTH // 2 - timeMsg.get_width() // 2, SCREEN_HEIGHT // 2 - timeMsg.get_height() // 2 + youWon.get_height()))
		pygame.display.update()
	elif not won and not exit2:
		fontSize = min(SCREEN_WIDTH, SCREEN_HEIGHT)	// redFactor 
		font = pygame.font.Font(FONT_PATH, fontSize)
		youLost = font.render("You Lost", True, (0, 0, 0))
		canvas.blit(youLost,  (SCREEN_WIDTH // 2 - youLost.get_width() // 2, SCREEN_HEIGHT // 2 - youLost.get_height() // 2))
		pygame.display.update()

	if not exit2:
		font = pygame.font.Font(FONT_PATH, fontSize)	
		tryAgain = font.render("Press Space to try again", True, (0, 0, 0))
		canvas.blit(tryAgain, (SCREEN_WIDTH // 2 - tryAgain.get_width() // 2, SCREEN_HEIGHT // 2 - tryAgain.get_height() // 2 - 30))
		pygame.display.update()
	
	waitingSpace = True
	while waitingSpace and not exit2:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit2 = True
				waitingSpace = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				waitingSpace = False