import numpy as np
import random
import math
from matplotlib import pyplot as plt
POPULATION_SIZE = 10
SHOW_EVERY =400
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

    def crossover(self,parent2,threshold):
        child = []
        for genome1, genome2 in zip(self.sol, parent2.sol):     
  
            prob = random.random() 
            if prob < threshold: 
                child.append(genome1) 

            elif prob < threshold: 
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
                maze[x][y]=4            #4 will be used as guide to solution road.
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
        for j in range(maze.shape[1]):          #printing solution road
            if(maze[i][j]==0):
                print(" ",end=" ")
            if(maze[i][j]==1):
                print("—",end=" ")
            if(maze[i][j]==2):
                print("S",end=" ")
            if(maze[i][j]==3):
                print("|",end=" ")
            if(maze[i][j]==4):
                print("X",end=" ")
            if(maze[i][j]==9):
                print("F",end=" ")
        print("\n")
    for i  in range(maze.shape[0]):
        for j in range(maze.shape[1]):              #clear maze
            if maze[i][j] == 4:
                maze[i][j]=0   
    
    
    
    
def create_maze(N,K):
    
    """
    N is the size of maze, K is the number of 4x1 obstacles (horizontal or vertical) inside of maze 
    Maze will be represented as matrix.  1s and 3s will be obstacles, 0's will be empty spaces.
    For outer walls, N+2 x N+2 shape matrix will be created. I used 2 for marking starting position and 9 for finish position.
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
    if maze[N-1][N] == 1 and maze[N][N-1] == 1: # if finish position surrounded by walls, creating a random empty space for access 
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
    N=25
    K=25
    
    maze = create_maze(N,K)
    pop_gen_list = []
    threshold_list = []
    threshold = 0
    for _ in range(9):
        avg_list = []
        threshold +=0.25 
        threshold_list.append(threshold)
        generation = 1
        population = []
        for i in range(POPULATION_SIZE):
            solution = Solution.create_sol(6)  # each solution in population firstly created in default length, it will increase by each generation
            solution = Solution(solution)
            population.append(solution)
        found = False
        
        while not found:
            for solution in population:
                                                 #each solution has 2 field: fitness and solution string
                x,y=(1,1)                   #initial starting position
                command_count = 0       # it stores commands that executed before hitting to a wall and exiting the sequence.
                for com in solution.sol:    #it can be used in fitness function.
                    if (com == "1"):        #if command in solution string is 1, go left unless it doesnt hit a wall
                        if (maze[x][y-1] != 1 and maze[x][y-1] != 3):
                            y-=1
                        else:
                            break
                    elif (com == "2"):          #GO UP
                        if (maze[x-1][y] != 1 and maze[x-1][y] != 3):
                            x-=1
                        else:
                            break
                    elif (com == "3"):          #go right
                        if (maze[x][y+1] != 1 and maze[x][y+1] != 3):
                            y +=1
                        else:
                            break
                    elif (com == "4"):          #go down
                        if (maze[x+1][y] != 1 and maze[x+1][y] != 3):
                            x +=1
                        else:
                            break
                    if(maze[x][y]==9):              # if maze[x][y]=9 it means we successfully reached the finish. Save solution for printing.
                        solution.fitness=0
                        final_solution=solution
                        found = True
                    command_count +=1
                solution.calculate_fitness(x,y,N,command_count,len(solution.sol))
                if found:
                    break
            new_population = []
            population = sorted(population, key = lambda x:x.fitness) 
            if generation % SHOW_EVERY == 0:
                print_solution(maze,population[0])     #print possible solutions in every few hundred episode
            avg = 0
            pop_count = len(population)
            for solution in population:
                avg += solution.fitness
            avg /= pop_count            #calculate average fitness for graph
            avg_list.append(avg)
            new_size = int((10*POPULATION_SIZE)/100)        #get fittest %10 of population to new population. 
            new_population = population[:new_size]
            for i in range(new_size):                           #fittest %10 gets mutated directly without crossover
                child = population[i].sol                         
                child.append(population[i].mutation())
                child = Solution(child)
                new_population.append(child)
            new_size = int((80*POPULATION_SIZE)/100) 
            for i in range(new_size): 
                parent1 = random.choice(population[:50])    #create new solutions using fittest %50 of the old population. Use Crossover 
                parent2 = random.choice(population[:50]) 
                child = parent1.crossover(parent2,threshold) 
                new_population.append(child) 
            population = new_population
            print(f"Generation: {generation}\tFitness: {population[0].fitness}") 
    
            generation += 1
        print_solution(maze,final_solution)
        print(f"Population size: {POPULATION_SIZE}\tFinal Generation: {generation}\tFitness: {final_solution.fitness}") 
        plt.plot(avg_list)
        plt.show()

                        
                               
