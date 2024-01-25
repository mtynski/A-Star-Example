import pygame
import math
import random
from queue import PriorityQueue

#Screen Setings
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Simple Simulation")

#Color Definitions
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#Function class for visualization and grid drawing
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):        
        self.neighbors = []
        #DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): 
            self.neighbors.append(grid[self.row + 1][self.col])
        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): 
            self.neighbors.append(grid[self.row - 1][self.col])
        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col + 1])
        #LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col - 1])
        #TOP LEFT
        if ((self.row > 0) and (self.col > 0)) and not grid[self.row - 1][self.col - 1].is_barrier(): 
            self.neighbors.append(grid[self.row - 1][self.col - 1])
        #BOTTOM LEFT
        if ((self.row > 0) and (self.col < self.total_rows - 1)) and not grid[self.row - 1][self.col + 1].is_barrier(): 
            self.neighbors.append(grid[self.row - 1][self.col + 1])
        #BOTTOM RIGHT
        if ((self.row < self.total_rows - 1) and (self.col < self.total_rows - 1)) and not grid[self.row + 1][self.col +1].is_barrier():
            self.neighbors.append(grid[self.row +1 ][self.col + 1])  
        #TOP RIGHT   
        if ((self.row < self.total_rows - 1) and (self.col > 0)) and not grid[self.row + 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col -1 ])
    
    def __lt__(self, other):
        return False


#Heuristic function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#Path reconstruction after found
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

#A* Implimentation
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False






#Creates grid but not visible
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

#Just draws grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


#Draws Everything and Updates Game Window
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

#Finds Where user clicks
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


#Puts it all together
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    count = 0
    end_count = random.randint(1,12)
    start = None
    end = None
    
    

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not start:
                start_x = random.randint(0,49)
                start_y = random.randint(0,49)
                start = grid[start_x][start_y] 
                start.make_start()
            if not end and end != start:
                end_place_x = random.randint(0,45)
                end_place_y = random.randint(0,45)
                end_place = grid[end_place_x][end_place_y]
                if end_place != start:
                    end = end_place
                    end.make_end()
                else:
                  end_place_x = random.randint(0,45)
                  end_place_y = random.randint(0,45)
                  end_place = grid[end_place_x][end_place_y]


            


                            
#Drawing Circles
            while count < end_count:
                
                dump = 0
                while dump != 1:
                        radius = random.randint(0,6)+0.5
                        r = 0
                        center_x = random.randint(0,40)
                        center_y = random.randint(0,40)
                        
                        
                        
                        while (math.sqrt(((start_x-center_x)**2)+((start_y-center_y)** 2)) <= (radius+1)) or (math.sqrt(((end_place_x-center_x)**2)+((end_place_y-center_y)** 2)) <= (radius+1)):
                            center_x = random.randint(0,40)
                            center_y = random.randint(0,40)
                            radius = random.randint(1,6)+0.5
                     
                            
                        
                        while r <= math.floor(radius*(math.sqrt(0.5))):
                            d = int(math.floor(math.sqrt((radius*radius) - (r*r))))
                            circle1_x = center_x - d
                            circle1_y = center_y + r
                            circle2_x = center_x + d
                            circle2_y = center_y + r
                            
                            circle3_x = center_x - d
                            circle3_y = center_y - r
                            
                            circle4_x = center_x + d 
                            circle4_y = center_y - r 
                            
                            circle5_x = center_x + r 
                            circle5_y = center_y - d
                            
                            circle6_x = center_x + r
                            circle6_y = center_y + d
                            
                            circle7_x = center_x - r
                            circle7_y = center_y - d
                            
                            circle8_x = center_x - r
                            circle8_y = center_y + d
                            
                            circle1 = grid[circle1_x][circle1_y]
                            circle1.make_barrier()
                            
                            circle2 = grid[circle2_x][circle2_y]
                            circle2.make_barrier()
                            
                            circle3 = grid[circle3_x][circle3_y]
                            circle3.make_barrier()
                            
                            circle4 = grid[circle4_x][circle4_y]
                            circle4.make_barrier()
                            
                            circle5 = grid[circle5_x][circle5_y]
                            circle5.make_barrier()
                            
                            circle6 = grid[circle6_x][circle6_y]
                            circle6.make_barrier()
                            
                            circle7 = grid[circle7_x][circle7_y]
                            circle7.make_barrier()
                            
                            circle8 = grid[circle8_x][circle8_y]
                            circle8.make_barrier()
                            
                            r = r+1
                            
                        for i in range(int(center_y-radius-0.5), int(center_y +radius-0.5+2)):
                            for j in range(int(center_x-radius-0.5), int(center_x +radius-0.5+2)):
                                if math.sqrt(((j-center_x)**2)+((i-center_y)** 2)) <= (radius - 0.5):
                                               inside_circle = grid[j][i]
                                               inside_circle.make_barrier()
                        
                        dump = 1
                
                count += 1



          
            
#Left Mouse Button To press
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                

                if spot != end and spot != start:
                    spot.make_barrier()


#Right Mouse Button
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    count = 0
                    end_count = random.randint(1,12)
                    grid = make_grid(ROWS, width)
                    

    pygame.quit()

main(WIN, WIDTH)