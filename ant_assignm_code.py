
import random,math
from PIL import Image, ImageDraw
from matplotlib.pyplot import plot
import os

current_directory = os.getcwd()


#classes definion

#class "ant"
class Ant:
    def __init__(self, x, y, C=0):
        self.x = x
        self.y = y
        self.C = C

#class "Grid_cell"
class Grid_cell:
    def __init__(self, tag, pheromone=0.0):
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

    #grid parameters for randomically generated grid
    max_Nest=5 # max number of nests
    max_Food=math.ceil(k*2) # max number of food sources

    nests_coordinates = [] #list of nests coordinates


    # Generate a grid G with m rows and n columns
    global grid 
    grid=[[Grid_cell(tag='E',pheromone=0) for _ in range(n)] for _ in range(m)]

    #Initilize the ants_list
    global ant_list 
    ant_list=[Ant(x=0,y=0,C=0) for _ in range(k)]


    for i in range(0,max_Nest):

        # Generate a random position for the "max_Nest" nests
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)

        # Add the nest to the grid
        grid[i][j].tag = 'N'

        # Add the coordinates of the new nest to the list
        nests_coordinates.append([i, j])

    for i in range(0,max_Food):
        # Generate a random position for the "max_Food" food sources
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)

        #Add the food source to the grid
        grid[i][j].tag = 'F'


    # Initialize the ants' positions
    for ant in ant_list:
        #randomly choose the nest
        nest=random.choice(nests_coordinates)
        ant.x,ant.y=nest[0],nest[1]




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


#per il resto funziona
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
            grid[ant.x][ant.y].tag = 'NP' #NP = new pheromone not to evaporate, it is a temporary tag used to check the cell has a new pheromone level but for this cycle it has not to evaporate

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
            elif grid[i][j].tag == 'NP':
                grid[i][j].tag = 'P' #set up for the next cycle
        
    


    return ants_list

#ok, funziona ed è stata testata
def plot_ants(z):
    global grid, ant_list,current_directory

    # Define the colors of the cells
    colors = {'E': 'green', 'F': 'red', 'N': 'brown', 'P': 'darkgreen'}

    cell_size = 20  # Size of the cell (in pixels)
    line_color = 'black'
    ant_color = 'black'  # Colore delle formiche

    # Inizializza l'immagine per la griglia
    height = len(grid) * cell_size
    width = len(grid[0]) * cell_size

    grid_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(grid_image)

    # Disegna le celle con i colori corrispondenti e le linee nere
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cell_type = grid[i][j].tag
            cell_color = colors.get(cell_type)

            # Creazione dell'immagine della cella
            x1, y1 = j * cell_size, i * cell_size  # Punto di inizio
            x2, y2 = x1 + cell_size, y1 + cell_size  # Punto di fine

            # Disegna la cella
            draw.rectangle([x1, y1, x2, y2], fill=cell_color, outline=line_color)

    # Disegna le formiche al centro di ciascuna cella
    for ant in ant_list:
        ant_x = ant.x * cell_size + cell_size // 2
        ant_y = ant.y * cell_size + cell_size // 2
        ant_size = 5  # Dimensione della formica
        draw.rectangle([ ant_y - ant_size,ant_x - ant_size, ant_y + ant_size,ant_x + ant_size], fill=ant_color)

    #grid_image.save(current_directory + "\\bonusAssignmQuestion\\%d.png" %i)
    grid_image.save(os.path.join(current_directory, 'bonusAssignmQuestion', f"{z}.png"))

    # Mostra la griglia con le formiche
    grid_image.show()



# foraging function
# k = numero di iterazioni
#ok, funziona ed è stata testata
def foraging(k):
    global grid, ant_list    
    plot_ants(0)
    for t in range(1,k):
        ant_list=update_ants(ant_list)
        plot_ants(t)
    
    return grid



#--------------------------------------------------------------

#test the debugging functions

def print_grid():
        #stampa la matrice
    print("Grid:\n")
    for i in range(0,4):
        for j in range(0,4):
            print(grid[i][j].tag, grid[i][j].pheromone, end='\t')  # Usa 'end' per separare gli elementi con uno spazio invece di una nuova riga
        print()  # Vai a capo alla fine di ogni riga
        print("-----------------------------------\n")

#print the ants info on terminal
def print_ants():
    print("-----------------------------------\n")
    print("Ants:\n")
    #stampa la lista delle formiche
    for i in range(0,len(ant_list)):
        print(ant_list[i].x, ant_list[i].y, ant_list[i].C, end='\t')  # Usa 'end' per separare gli elementi con uno spazio invece di una nuova riga
        print()  # Vai a capo alla fine di ogni riga



#test the assignment functions
m=84
n=92

scene_grid(m,n,30)




foraging(220)

#test the functions
#--------------------------------------------------------------