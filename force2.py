import math, random, bisect, pygame
import numpy as np

 
# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
 
SCALE = SCREEN_HEIGHT * 3 // 5
SHIFT = SCALE // 6

NUM_NODES = 100
NUM_EDGES = 100

NODE_RAD = 15

mouseDragging = False
draggingNode = None
offsetX = 0
offsetY = 0

# --- Classes ---

class Node():
    def __init__(self, xPos, yPos, rad, color, label):
        self.pos = [xPos, yPos]
        self.rad = rad
        self.color = color
        self.font = pygame.font.Font(None, 20)
        self.text = self.font.render(label, True, BLACK)
    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, self.pos, self.rad)
        pygame.draw.circle(screen, self.color, self.pos, self.rad-1)
        screen.blit(self.text, [self.pos[0]-self.rad//2, self.pos[1]-self.rad//2])
    def collided(self, pos):
        dx = self.pos[0] - pos[0]
        dy = self.pos[1] - pos[1]
        return dx*dx + dy*dy <= self.rad*self.rad
 
class Canvas:
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self, coor = list(), edges = list()):

        self.nodes = dict()
        self.edges = []
        self.adjList = {} # adjacency list rep of a graph


        print(coor)
        for i in range(NUM_NODES):
            self.add_node(str(i), min(max(0, coor[i][0]), SCREEN_WIDTH),
                    min(max(0, coor[i][1]), SCREEN_HEIGHT), NODE_RAD, GREEN)
       
        for u, v in edges:
            self.adjList[u].append(v)
            self.adjList[v].append(u)
            self.add_edge(u, v)

    def add_node(self, label, x, y, rad, color):
        self.nodes[label] = Node(x, y, rad, color, label)
        self.adjList[label] = list()

    def add_edge(self, node0, node1):
        '''
        node0, node1 are labels of the two nodes
        '''
        self.edges.append((node0, node1))
        if node0 not in self.adjList:
            self.adjList[node0] = list()
        if node1 not in self.adjList:
            self.adjList[node1] = list()
        self.adjList[node0].append(node1)
        self.adjList[node1].append(node0)
    
    def process_events(self):

        global mouseDragging, offsetX, offsetY, draggingNode

        """ Process all of the events. Return a "True" if we need
            to close the window. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDragging = True
                    mousePos = event.pos

                    for u in self.nodes:
                        if self.nodes[u].collided(mousePos):
                            draggingNode = u
                            offsetX = self.nodes[u].pos[0] - mousePos[0]
                            offsetY = self.nodes[u].pos[1] - mousePos[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouseDragging = False

            elif event.type == pygame.MOUSEMOTION:
                if mouseDragging:
                    mousePos = event.pos
                    self.nodes[draggingNode].pos[0] = mousePos[0] + offsetX
                    self.nodes[draggingNode].pos[1] = mousePos[1] + offsetY
 
        return False
 
    def run_logic(self):
        pass
 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        for e in self.edges:
            pygame.draw.line(screen, BLACK,
                       (self.nodes[e[0]].pos[0],self.nodes[e[0]].pos[1]),
                       (self.nodes[e[1]].pos[0],self.nodes[e[1]].pos[1]),
                    )

        for u in self.nodes:
            self.nodes[u].draw(screen)
        pygame.display.flip()
 

class Layout():
    # spring-force for pushing nearby vertices apart
    def hook(p, q, k=100.0):
        dx = p[0] - q[0]
        dy = p[1] - q[1]
        ds = math.sqrt(dx*dx + dy*dy)

        # if ds >= MAXEDGE: return 0, 0
        return k*dx/ds, k*dy/ds

    # coloumbic force for drawing distant vertices closer
    def coloumb(p, q, k=0.5):
        dx = q[0] - p[0]
        dy = q[1] - p[1]
        ds3 = math.pow(dx*dx + dy*dy, 1.5)
        Fx = k * dx / ds3
        Fy = k * dy / ds3

        # if ds <= MAXEDGE: return 0, 0
        return Fx, Fy

    # relative layout is found using spectral layout;
    # i.e. the elements in the two eigenvectors
    # corresponding to the smallest positive eigenvalues are
    # used to determine the coordinates. Then, the vertices are
    # spaced-out using a force-based correction
    def getCoordinates(L):

        n = len(L)

        print("laplacian: ")
        A = np.array(L)

        print(A)

        # determine relative placement of vertices using spectral layout
        eigval, eigvec = np.linalg.eigh(A)

        EPS = 1e-5
        coor = []
        for i in range(n):
            if eigval[i] > EPS:
                coor.append(eigvec[:,i])

                # scale and shift coordinates so they're inside the first quadrant
                coor[-1] *= SCALE
                coor[-1] += abs(min(coor[-1])) + SHIFT

            if len(coor) >= 2: break

        coor = list(zip(coor[0], coor[1]))
        v = [(0,0)] * n

        print(coor)

        # force-based spacing
        dt, m, steps = 1e-2, 1.0, 6
        for _ in range(steps):
            for i in range(n):
                for j in range(n):
                    if i == j: continue
                    Fx, Fy = Layout.hook(coor[i], coor[j]) if L[i][j] else Layout.coloumb(coor[i], coor[j])
                    vx = v[i][0] + Fx / m * dt
                    vy = v[i][1] + Fy / m * dt
                    x = coor[i][0] + vx * dt
                    y = coor[i][1] + vy * dt
                    coor[i], v[i] = (x, y), (vx, vy)

        print("coordinates:")
        print(coor)
        # (x, y) coordinates for each vertex
        return list(map(lambda x: (int(x[0]), int(x[1])), coor))

    def parser():
        n, m = map(int, input().split())

        global NUM_NODES, NUM_EDGES
        NUM_NODES, NUM_EDGES = n, m
        
        # laplacian matrix
        L = [[0]*n for i in range(n)]
        g = [[] for _ in range(n)]
        edges = [tuple(input().split()) for _ in range(m)]

        for u, v in edges:
            u, v = int(u), int(v)
            L[u][v] = L[v][u] = -1
            L[u][u] += 1
            L[v][v] += 1

        coor = Layout.getCoordinates(L)

        return coor, edges

def main():
    """ Main program function. """
    global mouseDragging, draggingNode, offsetX, offsetY
    mouseDragging = False
    draggingNode = None
    offsetX = 0
    offsetY = 0

    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(True)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    canvas = Canvas(*Layout.parser())

    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = canvas.process_events()
 
        # Update object positions, check for collisions
        canvas.run_logic()
 
        # Draw the current frame
        canvas.display_frame(screen)
 
        # Pause for the next frame
        clock.tick(60)
 
    # Close window and exit
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
