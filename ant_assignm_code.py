
import random
import matplotlib.pyplot as plt



#classes definion

#class "ant"
class Ant:
    def __init__(self, x, y, C=0):
        self.x = x
        self.y = y
        self.C = C

#class "Grid_cell"
class Grid_cell:
    def __init__(self, tag, pheromone=0):
        self.tag = tag
        self.pheromone = pheromone



#declaration and initialization of global variables
ant_list=[];
grid=[[]];
delta=1
epsilon = 0.2

# scene_grid
#m rows, n columns, k ants

#ok, funziona ed è stata testata
def scene_grid(m, n, k):
    # Generate a grid G with m rows and n columns
    global grid 
    grid=[[Grid_cell(tag='E',pheromone=0) for _ in range(m)] for _ in range(n)]

    # Define a predefined grid
    # 1. Nest
    grid[0][0].tag = 'N'
    
    # 2. Set food
    grid[m-2][n-2].tag = 'F'
    grid[m-2][0].tag = 'F'
    grid[0][n-2].tag = 'F'

    #initilize the ants_list
    global ant_list 
    ant_list=[Ant(x=0,y=0,C=0) for _ in range(k)]




# neighbours function
#ok, funziona ed è stata testata
def neighbors(ant):
    global grid

    x, y = ant.x, ant.y

    # Get information from neighboring cells (8-connected grid) of the ant
    neighbors_cells = [
        [x-1,y-1],
        [x-1,y],
        [x-1,y+1],
        [x,y-1],
        [x,y+1],
        [x+1,y-1],
        [x+1,y],
        [x+1,y+1]
                      ]
    
    #inizialize the list of neighbors
    neighbors_list=[]

    # fill the list with the neighbors of the ant (only if are in the grid)
    for neighbor in neighbors_cells:
        if 0 <= neighbor[0]<len(grid) and 0<= neighbor[1]<len(grid[0]):
            neighbors_list.append(neighbor)             #neighbors_list.append(grid[neighbor[0]][neighbor[1]]) l'operazione restituisce la cella della grigli a quelal posizione


    return neighbors_list


# Calculate probabilities based on pheromone levels
#ok, funziona ed è stata testata

def probability(ant):
    global grid

    neighbors_list = neighbors(ant)

    tot_pheromone = 0
    cells_probability = []

    #calculate the total pheromone level of the neighbors
    for neighbor in neighbors_list:
        tot_pheromone += (grid[neighbor[0]][neighbor[1]].pheromone + 1)

    # Create a list of probabilities for each neighbor based on pheromone levels
    for neighbor in neighbors_list:
        cells_probability.append((grid[neighbor[0]][neighbor[1]].pheromone + 1) / tot_pheromone)
    return cells_probability


# transit function
#ok, funziona ed è stata testata
def transit(ant):

    # Get information from neighboring cells
    neighbors_cells = neighbors(ant)
    
    # Calculate probabilities based on pheromone levels
    probabilities = probability(ant)
    
    # Choose a cell randomly based on probabilities
    selected_cell = random.choices(neighbors_cells, weights=probabilities)[0]


    # Update ant's position on the grid
    ant.x,ant.y=selected_cell[0],selected_cell[1]

    return ant


#da testare
def update_ants(ants_list):

    global grid, delta,epsilon

    # Update ants position on the grid
    for ant in ants_list:
        ant = transit(ant)
    
    #food interaction
    #pheromone modifications
    for ant in ants_list:
        #the ant finds food and starts carrying it . Moreover, the pheromone level of the cell is increased of delta
        if grid[ant.x][ant.y].tag == 'F' and ant.C == 0:
            ant.C = 1
            grid[ant.x][ant.y].pheromone +=delta
            grid[ant.x][ant.y].tag = 'P'
        elif grid[ant.x][ant.y].tag == 'N' and ant.C == 1:
            ant.C = 0
        elif ant.C == 1 and grid[ant.x][ant.y].tag != 'F':    #the ant brings food so the pheromone level of the cell is increased of delta
            grid[ant.x][ant.y].pheromone +=delta
            grid[ant.x][ant.y].tag = 'P'
    

    #pheromone evaporation
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j].tag == 'P':
                if grid[i][j].pheromone-epsilon >= 0:
                    grid[i][j].pheromone =(1-epsilon)*grid[i][j].pheromone
                else :
                    grid[i][j].pheromone = 0
                    grid[i][j].tag = 'E'
        

    return ants_list




# foraging function
#da finire


    # Stampa la matrice riga per riga



# plot_ants
#da verificare che la funzione works correctly


# da verificare che funzioni l'import della funzione e dopodiché modificare il seguente codice in maniera più elegante
#test

colors = {'E': 'green', 'F': 'red', 'N': 'blue', 'P': 'yellow'}

# Function to visualize the grid
def visualize_grid(grid):
    nrow = len(grid)
    ncol = len(grid[0])
    
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    for i in range(nrow):
        for j in range(ncol):
            area_type = grid[i][j]
            color = colors.get(area_type, 'gray')  # Default to gray if the type is not recognized
            ax.add_patch(plt.Rectangle((j, nrow - 1 - i), 1, 1, color=color))

    ax.set_aspect('equal')
    ax.set_xticks(range(ncol))
    ax.set_yticks(range(nrow))
    ax.grid(linewidth=1, color='black')
    plt.gca().invert_yaxis()
    plt.show()


#--------------------------------------------------------------

#test the functions

scene_grid(4,4,5)

def print_grid():
        #stampa la matrice
    print("Grid:\n")
    for i in range(0,4):
        for j in range(0,4):
            print(grid[i][j].tag, grid[i][j].pheromone, end='\t')  # Usa 'end' per separare gli elementi con uno spazio invece di una nuova riga
        print()  # Vai a capo alla fine di ogni riga
        print("-----------------------------------\n")


def print_ants():
    print("-----------------------------------\n")
    print("Ants:\n")
    #stampa la lista delle formiche
    for i in range(0,len(ant_list)):
        print(ant_list[i].x, ant_list[i].y, ant_list[i].C, end='\t')  # Usa 'end' per separare gli elementi con uno spazio invece di una nuova riga
        print()  # Vai a capo alla fine di ogni riga



#print("Neighbors:\n")
#stampa la lista dei vicini della prima formica
#neighbors_list=neighbors(ant_list[0])

#for i in neighbors_list:
#    print(i[0], i[1], end='\t')  # Usa 'end' per separare gli elementi con uno spazio invece di una nuova riga

#print_grid()

ant_list_test=[ant_list[0]]
for i in range(0, 10):


    print("%d° transit of the first ant:",i,"\n")

    ant_list_test=update_ants(ant_list_test)
    print("Dati della formica :",ant_list_test[0].x, ant_list_test[0].y, ant_list_test[0].C, "\n")  # Usa 'end' per separare gli elementi con uno spazio invece di una nuova riga

    print("Probabilities after the %d° transiction ant:",i,"\n")
    #stampa la lista delle probabilità della prima formica
    probabilities=probability(ant_list_test[0])
    print(probabilities)


    print("Grid after the %d° transiction ant:",i)
    print_grid()
    print("\n-----------------------------------\n")


#test the functions
#--------------------------------------------------------------

    

