
import random,math
from PIL import Image, ImageDraw


# ----------------------- Classes definion -----------------------

#class "Ant"
class Ant:
    def __init__(self, x, y, C=0):
        self.x = x #x coordinate
        self.y = y #y coordinate
        self.C = C #food carried by the ant (0 = no food, 1 = food is carried)

        # it is just used for the implementation of the exercise 3.e
        self.backToNestPath = [] #list of the cells that the ant has visited to go back to the nest

#class "Grid_cell"
class Grid_cell:
    def __init__(self, tag, pheromone=0.0):
        self.tag = tag #tag of the cell (E = empty, N = nest, F = food, P = pheromone)
        self.pheromone = pheromone #pheromone level of the cell

# ----------------------- Classes definion -----------------------


# ---------- Declaration and initialization of global variables ----------

ant_list=[];    #list of ants
grid=[[]];      #grid
delta=1         #incrementing factor of the pheromone level when an ant with food passes on a cell 
epsilon = 0.25  #evaporation factor of the pheromone level

# ---------- Declaration and initialization of global variables ----------


# ----------------------- Functions definition -----------------------


#scene_grid function
#Initialize the grid with grass, nests, ants, and food. Start the pheromone level of each cell of the grid at zero. 
#This will represent the initialstate of the environment before the simulation begins.

#@param m: number of rows of the grid
#@param n: number of columns of the grid
#@param k: number of ants

def scene_grid(m, n, k):


    #grid parameters for randomically generated the elements inside it

    max_Nest=5  # max number of nests
    max_Food=math.ceil(k*2.5) # max number of food sources

    nests_coordinates = [] #list of nests coordinates , it is needed to position the ants into the nests


    # Generate a grid G with m rows and n columns
    global grid 
    grid=[[Grid_cell(tag='E',pheromone=0) for _ in range(n)] for _ in range(m)]

    #Initilize the ants_list
    global ant_list 
    ant_list=[Ant(x=0,y=0,C=0) for _ in range(k)]

    # Generate nests in random positions on the grid
    for w in range(0,max_Nest):
        # Generate a random position for the "max_Nest" nests
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)

        # Add the nest to the grid
        grid[i][j].tag = 'N'

        # Add the coordinates of the new nest to the list
        nests_coordinates.append([i, j])

    # Generate food sources in random positions on the grid
    for w  in range(0,max_Food):
        # Generate a random position for the "max_Food" food sources
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)

        # Check not to overwrite a nest cell
        while grid[i][j].tag == 'N':    
            i = random.randint(0, m - 1)
            j = random.randint(0, n - 1)

        #Add the food source to the grid
        grid[i][j].tag = 'F'


    # Initialize the ants' positions
    for ant in ant_list:
        #randomly choose the nest and set the ant position to it
        nest=random.choice(nests_coordinates)
        ant.x,ant.y=nest[0],nest[1]



#plot_ants function
#Visualize the current state of the grid using different colors for each type of area.
#The ants are represented by black dots in the center of each cell.
def plot_ants():
    global grid, ant_list,gif

    # Define the colors of the cells
    colors = {'E': 'green', 'F': 'red', 'N': 'brown', 'P': 'darkgreen'}

    cell_size = 20  # Size of the cell (in pixels)
    line_color = 'black'
    ant_color = 'black'  # Colore delle formiche

    #Inizialize the image for the grid
    height = len(grid) * cell_size
    width = len(grid[0]) * cell_size

    grid_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(grid_image)

    #Draw the cells with the corresponding colors and the black lines to delimite the cells
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cell_type = grid[i][j].tag
            cell_color = colors.get(cell_type)

            # Create the image of the cell
            x1, y1 = j * cell_size, i * cell_size #starting point coordinates
            x2, y2 = x1 + cell_size, y1 + cell_size # ending point coordinates

            #Draw the cell
            draw.rectangle([x1, y1, x2, y2], fill=cell_color, outline=line_color)

    #Draw the ants in the center of each cell
    for ant in ant_list:
        ant_x = ant.x * cell_size + cell_size // 2
        ant_y = ant.y * cell_size + cell_size // 2
        ant_size = 5  # Size of the ant (in pixels)
        draw.rectangle([ ant_y - ant_size,ant_x - ant_size, ant_y + ant_size,ant_x + ant_size], fill=ant_color)

    #Show the grid with the ants
    grid_image.show()


#neighbours function
#Identify neighboring cells of a given point
#@param ant: ant object of which we want to know the neighbors    
#@return neighbors_list: list of the neighbors of the ant
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

    # fill the list with the neighbors of the ant (only if they are valid positions on the grid)
    for neighbor in neighbors_cells:
        if 0 <= neighbor[0]<len(grid) and 0<= neighbor[1]<len(grid[0]):
            neighbors_list.append(neighbor)             


    return neighbors_list


#transit function
#Manage ant movements based on probabilities.
#@param ant: ant object of which we want to update the position on grid
#@return ant: ant object updated with the new position on grid

def transit(ant):

    # Get information from neighboring cells
    neighbors_cells = neighbors(ant)
    
    # Calculate probabilities based on pheromone levels
    probabilities = probability(ant)
    
    # Choose a cell randomly based on probabilities
    selected_cell = random.choices(neighbors_cells, weights=probabilities)[0]

    #It is the implementation of the exercise 3.e

    #if the ant is not carrying food, it saves the cell in the list of the cells that the ant has visited for later when it has to go back to the nest
    #if the ant is carrying food, it gets the coordinates updated with the last cell visited and it removes the cell from the list of the cells in order to come back to the nest
    if ant.C == 0:
        ant.backToNestPath.append((ant.x,ant.y)) #save the cell in the list of the cells that the ant has visited

        # Update ant's position on the grid
        ant.x,ant.y=selected_cell[0],selected_cell[1]
    else:
        ant.x,ant.y=ant.backToNestPath.pop()    #the ant retraces its steps to come back to the nest
        
    return ant



#probability function
#Calculate probabilities based on pheromone levels (it is used by "transit" function)
#@param ant: ant object of which we want to know calculate the probabilities of the neighbors based on their own pheromone level
#@return cells_probability: list of the probabilities of the neighbors of the ant based on their own pheromone level

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



#update_ants function
#Manage ant movements, food interactions, and pheromone modifications.
#@param ants_list: list of the ants of which we want to update the position on grid
#@return ants_list: list of the ants updated with the new position on grid

def update_ants(ants_list):

    global grid, delta,epsilon

    # Update ants position on the grid
    for ant in ants_list:
        ant = transit(ant)

    #food interaction and pheromone update
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
                grid[i][j].tag = 'P'    #set up for the next "transit" function call
        
    


    return ants_list



#foraging function
#Manage the entire simulation over multiple iterations
#@param k: number of iterations
#@return grid: final grid after the simulation
def foraging(k):
    global grid, ant_list    
    #prints the grid at the beginning of the simulation
    plot_ants()
    for t in range(1,k):
        #update the ants position on the grid
        ant_list=update_ants(ant_list)
        #prints the grid at each iteration
        plot_ants()
    
    return grid



# ----------------------- Functions definition -----------------------



#Example of simulation

m=47
n=63
k=21
iteration = 5


scene_grid(m,n,k)
foraging(iteration)

#--------------------------------------------------------------