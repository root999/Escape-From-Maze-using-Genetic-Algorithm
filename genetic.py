import numpy as np
import random
import math
from sklearn import preprocessing

POPULATION_SIZE = 100

class Solution():
    def __init__(self,sol):
        self.M = len(sol)
        self.sol = sol
        self.fitness = -1
    
    @classmethod
    def create_sol(self,M):
        DIRECTIONS = "1234"         #left, up, right, down respectively
        sol = []
        for i in range(M):
            sol.append(random.choice(DIRECTIONS))
        return sol
    def mutation(self):
        DIRECTIONS = "1234"
        gene = random.choice(DIRECTIONS)
        return gene

    def crossover(self,parent2):
        child = []
        for genome1, genome2 in zip(self.sol, parent2.sol):     
  
            prob = random.random() 
            if prob < 0.45: 
                child.append(genome1) 

            elif prob < 0.90: 
                child.append(genome2) 
            else: 
                child.append(self.mutation()) 
        child.append(self.mutation())
        return Solution(child) 
    
    def calculate_fitness(self,x,y,N,command_count,length):
        #fitness = (lenght+command_count)*calculate_distance(x, y, N)
        fitness =calculate_distance(x, y, N) 
        self.fitness = fitness
        
def calculate_distance(x,y,N):
    dist = math.sqrt(((N-x)**2)+((N-y)**2))
    return dist

def print_maze(maze):
    for i  in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            print(f"{maze[i][j]}",end=" ")
        print("\n")
        
def print_solution(maze,final_solution):
    (x,y)=(1,1)
    for command in final_solution.sol:
        if(x != N and y != N):
            if (command == "1"):
                y-=1
                maze[x][y]=4
            elif (command == "2"):
                x-=1
                maze[x][y]=4
            elif (command == "3"):
                y +=1
                maze[x][y]=4
            elif (command == "4"):
                x +=1
                maze[x][y]=4
            
    for i  in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if(maze[i][j]==0):
                print(" ",end=" ")
            if(maze[i][j]==1):
                print("--",end=" ")
            if(maze[i][j]==2):
                print("S",end=" ")
            if(maze[i][j]==3):
                print("|",end=" ")
            if(maze[i][j]==4):
                print("X",end=" ")
            if(maze[i][j]==9):
                print("F",end=" ")
        print("\n")
            
    
    
    
    
def create_maze(N,K):
    
    """
    N is the size of maze, K is the number of 4x1 obstacles (horizontal or vertical) inside of maze 
    Maze will be represented as matrix.  1's will be obstacles, 0's will be empty spaces.
    For outer walls, N+2 x N+2 shape matrix will be created
    """

    maze = np.zeros(shape=(N+2,N+2),dtype=int)
    for i in range(N+2):
        for j in range(N+2):
            # if i==0 or j==0 or i==N+1 or j==N+1:
            #     maze[i][j]=1
            if j==0 or j==N+1:
                maze[i][j]=3
            elif i==0 or i==N+1:
                maze[i][j]=1
    
    for i in range(K):
        rotation = random.choice(["vertical","horizontal"])
        if rotation == "vertical":
            start_ind_x = random.randint(1,N)
            start_ind_y = random.randint(1,N-3)
            for i in range(4):
                maze[start_ind_x][start_ind_y]=1 #vertical walls will be represented as 3
                start_ind_y += 1
        else:
            start_ind_x = random.randint(1,N-3)
            start_ind_y = random.randint(1,N)
            for i in range(4):
                maze[start_ind_x][start_ind_y]=3 #horizontal walls will be represented as 1
                start_ind_x += 1
    maze[1][1]=2            #starting position
    if maze[N-1][N] == 1 and maze[N][N-1] == 1:
        choice = random.choice(["left","up"])
        if choice == "left":
            maze[N-1][N]=0
        else:
            maze[N][N-1]=0
    maze[N][N]=9        #finish position
    
    
    return maze 


if __name__ == "__main__":
    
    # N = int(input("Enter matrix size "))
    # K = int(input("How many obstacles should we add? "))
    
    N=30
    K=20
    maze = create_maze(N,K)
    generation = 1
    population = []
    for i in range(POPULATION_SIZE):
        gnome = Solution.create_sol(6)
        gnome = Solution(gnome)
        population.append(gnome)
    found = False
    
    while not found:
        count = 0
        for solution in population:
            count +=1
            x,y=(1,1)
            command_count = 0
            for com in solution.sol:
                if (com == "1"):
                    if (maze[x][y-1] != 1 and maze[x][y-1] != 3):
                        y-=1
                    else:
                        break
                elif (com == "2"):
                    if (maze[x-1][y] != 1 and maze[x-1][y] != 3):
                        x-=1
                    else:
                        break
                elif (com == "3"):
                    if (maze[x][y+1] != 1 and maze[x][y+1] != 3):
                        y +=1
                    else:
                        break
                elif (com == "4"):
                    if (maze[x+1][y] != 1 and maze[x+1][y] != 3):
                        x +=1
                    else:
                        break
                if(maze[x][y]==9):
                    final_solution=solution
                    found = True
                command_count +=1
            solution.calculate_fitness(x,y,N,command_count,len(solution.sol))
            if found:
                break
        new_population = []
        population = sorted(population, key = lambda x:x.fitness) 
        
        new_size = int((10*POPULATION_SIZE)/100) 
        new_population = population[:new_size]
  
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            parent1 = random.choice(population[:50]) 
            parent2 = random.choice(population[:50]) 
            child = parent1.crossover(parent2) 
            new_population.append(child) 
        population = new_population
        print(f"Generation: {generation}\tFitness: {population[0].fitness}") 
  
        generation += 1
    print_solution(maze, final_solution)
                        
                               
