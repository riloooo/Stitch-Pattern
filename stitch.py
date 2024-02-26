from random import random
from PIL import Image
class Grid_Node:
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.color = 0
    
    def __str__(self):
        '''
        ┌─┐
        │█│
        └─┘
        '''
        s = [' ',' ',' ','\n',' ',' ',' ','\n',' ',' ',' ']
        
        #Sides
        if self.up:
            s[1] = '─'
        if self.left:
            s[4] = '│'
        if self.right:
            s[6] = '│'
        if self.down:
            s[9] = '─'
        #Corners
        '''
        if self.up and self.left:
            s[0] = '┌'
        if self.up and self.right:
            s[2] = '┐'
        if self.down and self.left:
            s[8] = '└'
        if self.down and self.right:
            s[10] = '┘'
        '''

        #Center
        if self.color == 1:
            s[5] = '█'
        if self.color == 2:
            s[5] = '░'
        if self.color == 0:
            s[5] = ' '
        
        return ''.join(s)
        

class Grid:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    def __init__(self, size):
        self.size = size
        self.node_list = [[Grid_Node() for i in range(self.size)] for j in range(self.size)]
    
    def get_node(self, x, y):
        return self.node_list[y][x]
    
    
    def add_line(self, x, y, side):
        '''
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3 
        '''
        node = self.get_node(x, y)
        node_neighbor = None
        if side == 0:
            node.up = True
            if y > 0:
                node_neighbor = self.get_node(x, y-1)
                node_neighbor.down = True
        if side == 1:
            node.down = True
            if y < self.size - 1:
                node_neighbor = self.get_node(x, y+1)
                node_neighbor.up = True
        if side == 2:
            node.left = True
            if x > 0:
                node_neighbor = self.get_node(x - 1, y)
                node_neighbor.right = True
        if side == 3:
            if x < self.size - 1:
                node_neighbor = self.get_node(x + 1, y)
                node_neighbor.left = True

    def fill_colors(self, startx = 0, starty = 0, color = 1):
        node_stack = [(startx,starty,color)]
        self.get_node(startx, starty).color = color

        #Pop node from stack. For adjacent nodes, if not painted: paint then add to stack
        while node_stack:
            x, y, color = node_stack.pop()
            curr_node = self.get_node(x, y)

            #Left
            if x > 0:
                adj_node = self.get_node(x - 1, y)
                if not adj_node.color:
                    if curr_node.left:
                        adj_node.color = 3 - curr_node.color #Flips color between 1 and 2. 3-1=2 3-2=1
                    else:
                        adj_node.color = curr_node.color
                    node_stack.append((x - 1, y, adj_node.color))

            #Right
            if x < self.size - 1:
                adj_node = self.get_node(x + 1, y)
                if not adj_node.color:
                    if curr_node.right:
                        adj_node.color = 3 - curr_node.color
                    else:
                        adj_node.color = curr_node.color
                    node_stack.append((x + 1, y, adj_node.color))

            #Up
            if y > 0:
                adj_node = self.get_node(x, y - 1)
                if not adj_node.color:
                    if curr_node.up:
                        adj_node.color = 3 - curr_node.color
                    else:
                        adj_node.color = curr_node.color
                    node_stack.append((x, y - 1, adj_node.color))

            #Down
            if y < self.size - 1:
                adj_node = self.get_node(x, y + 1)
                if not adj_node.color:
                    if curr_node.down:
                        adj_node.color = 3 - curr_node.color
                    else:
                        adj_node.color = curr_node.color
                    node_stack.append((x, y + 1, adj_node.color))

    
    def __str__(self):
        ret = ''
        for y in range(self.size):
            row = ['','']
            for x in range(self.size):
                
                node = self.get_node(x, y)
                node_rows = str(node).split('\n')
                if x == self.size - 1:
                    row[0] += node_rows[0]
                    row[1] += node_rows[1]
                else:    
                    row[0] += node_rows[0][:2]
                    row[1] += node_rows[1][:2]
                if y == self.size - 1:
                    if x == self.size - 1:
                        row.append(node_rows[2][:2])
                    else:
                        row.append(node_rows[2])
            ret += '\n'.join(row) + '\n'
        return ret


def generate_stitch_pattern(size) -> Grid:
    grid = Grid(size)

    for x in range(size):
        coin = random() > 0.5
        for y in range(size):
            if coin and y % 2 == 0:
                grid.add_line(x,y,2)
            if not coin and y % 2 == 1:
                grid.add_line(x,y,2)
    for y in range(size):
        coin = random() > 0.5
        for x in range(size):
            if coin and x % 2 == 0:
                grid.add_line(x, y, 0)
            if not coin and x % 2 == 1:
                grid.add_line(x, y, 0)
    return grid



size = 1000
grid = generate_stitch_pattern(size)
grid.fill_colors()
image = Image.new('RGB', (size, size))

for x in range(size):
    for y in range(size):
        node = grid.get_node(x, y)
        color = node.color

        if color == 1:
            image.putpixel((x, y), (255, 255, 255))
        else:
            image.putpixel((x, y), (0, 0, 0))

##image = image.resize((size * 5, size * 5))
image.save('C:\\Users\\riley\\Pictures\\stitch.png')
image.show()