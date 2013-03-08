#!/usr/bin/python

import copy
import code
fp = open('input.txt')

data = fp.readlines()

grid = []

for item in data[0:7]:
   grid.append([x for x in item[:-1]])

bunnyX = -1
bunnyY = -1

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '@' or grid[i][j] == '+':
            bunnyX = i
            bunnyY = j
        print grid[i][j],
    print ""

print bunnyX, bunnyY


def canMoveTo(grid, x, y, velX, velY):
    if (x+velX >= 0 and x+velX < len(grid) and y+velY >= 0 and y+velY < len(grid[0])):
        if grid[x+velX][y+velY] == ' ' or grid[x+velX][y+velY] == '.':
            return True
    
    if (x+2*velX >= 0 and x+2*velX < len(grid) and y+2*velY >= 0 and y+2*velY < len(grid[0])):
        if (grid[x+velX][y+velY] == '$' or grid[x+velX][y+velY] == '*') and (grid[x+2*velX][y+2*velY] == ' ' or grid[x+2*velX][y+2*velY] == '.'):
            return True
    
    return False

def moveTo(_grid, x, y, velX, velY):
    grid = copy.deepcopy(_grid)    
    push = False

    if grid[x][y] == '@':
        grid[x][y] = ' '
    elif grid[x][y] == '+':
        grid[x][y] = '.'
    else:
        print "invalid grid"

    if grid[x+velX][y+velY] == ' ':
        grid[x+velX][y+velY] = '@'
    elif grid[x+velX][y+velY] == '.':
        grid[x+velX][y+velY] = '+'
    elif grid[x+velX][y+velY] == '$':
        grid[x+velX][y+velY] = '@'
        push = True
        if grid[x+velX*2][y+velY*2] == ' ':            
            grid[x+velX*2][y+velY*2] = '$'
        elif grid[x+velX*2][y+velY*2] == '.':
            grid[x+velX*2][y+velY*2] = '*'  
        else:
            print "invalid grid"          
    elif grid[x+velX][y+velY] == '*':
        grid[x+velX][y+velY] = '+'
        push = True
        if grid[x+velX*2][y+velY*2] == ' ':            
            grid[x+velX*2][y+velY*2] = '$'
        elif grid[x+velX*2][y+velY*2] == '.':
            grid[x+velX*2][y+velY*2] = '*'  
        else:
            print "invalid grid"          
    else:
        print "invalid grid"
    
    return [grid, push]      
    
def isSolved(grid):
    boxes = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '$':
                boxes = boxes + 1
    return boxes == 0
    
def neighbors(grid, bunnyX, bunnyY, depth, path):
    n = []
    
    if canMoveTo(grid, bunnyX, bunnyY, 1, 0):
        [g, push] = moveTo(grid, bunnyX, bunnyY, 1, 0)                
        if push:
            n.append([g, bunnyX+1, bunnyY, depth+1, path + "D"])
        else:
            n.append([g, bunnyX+1, bunnyY, depth+1, path + "d"])
    
    if canMoveTo(grid, bunnyX, bunnyY, 0, 1):
        [g, push] = moveTo(grid, bunnyX, bunnyY, 0, 1)                
        if push:
            n.append([g, bunnyX, bunnyY+1, depth+1, path + "R"])
        else:
            n.append([g, bunnyX, bunnyY+1, depth+1, path + "r"])
    
    if canMoveTo(grid, bunnyX, bunnyY, -1, 0):
        [g, push] = moveTo(grid, bunnyX, bunnyY, -1, 0)       
        if push:
            n.append([g, bunnyX-1, bunnyY, depth+1, path + "U"])
        else:
            n.append([g, bunnyX-1, bunnyY, depth+1, path + "u"])
    
    if canMoveTo(grid, bunnyX, bunnyY, 0, -1):
        [g, push] = moveTo(grid, bunnyX, bunnyY, 0, -1)                

        if push:
            n.append([g, bunnyX, bunnyY-1, depth+1, path + "L"])
        else:
            n.append([g, bunnyX, bunnyY-1, depth+1, path + "l"])
    
    return n
    

def hashesh(grid):
    s = ""
    for row in grid:
        for char in row:
            s = s + char
    return s
    
def BFS(grid, bunnyX, bunnyY):
    queue = [[grid, bunnyX, bunnyY, 0, ""]]
    lastDepth = -1
    
    hsh = {}
    soln = 0
    parent = {}
    
    solutions = []
    
    while len(queue) > 0:
        top = queue.pop(0)

        if hashesh(top[0]) in hsh:
            continue
        
        hsh[hashesh(top[0])] = True
        
        if lastDepth != top[3]:
            print "Trying depth %d with %d" % (top[3], len(queue))
            lastDepth = top[3]
            
        
        if isSolved(top[0]):
            print "Solved in %d moves with %s" % (top[3], top[4])
            solutions.append(hashesh(top[0]))
            soln = soln + 1
#            break                     
        
        for item in neighbors(top[0], top[1], top[2], top[3], top[4]):                        

            if hashesh(item[0]) in parent:
                parent[hashesh(item[0])].append(hashesh(top[0]))
            else:
                parent[hashesh(item[0])] = [hashesh(top[0])]
                
            if hashesh(item[0]) in hsh:
                continue
            queue.append(item)
    print soln
    
    seen = {}
    sumA = copy.deepcopy(solutions)
    q2 = copy.deepcopy(solutions)
    
    
    while len(q2) > 0:
        top = q2.pop(0)
        
        if top in seen:
            continue
        
        seen[top] = True

        if top in parent:
            
            for item in parent[top]:
                if item in seen:
                    continue            
                sumA.append(item)
                q2.append(item)
    
    print len(sumA), len(set(sumA))
    
    
BFS(grid, bunnyX, bunnyY)
    
    