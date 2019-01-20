import pygame
import random
 
# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
 
NUM_NODES = 100
NUM_EDGES = 100

NODE_RAD = 15

mouseDragging = False
draggingNode = None
offsetX = 0
offsetY = 0

def input_graph(canvas):
    '''
    g : adjacency list of a graph
    edges: list of undirected edges (u,v)
    '''
    NUM_NODES, NUM_EDGES = map(int, input().split())
    g = {str(i) : [] for i in range(NUM_NODES)} # adjacency list rep of a graph

    for i in range(NUM_NODES):
        # win.add_node(str(i))
        canvas.add_node(str(i), random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
            NODE_RAD, GREEN)

    edges = []  # edge list
    for i in range(NUM_EDGES):
        u, v = map(str, input().split())
        edges.append((u,v))
        g[u].append(v)
        g[v].append(u)
        canvas.add_edge(u, v)

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
 
    def __init__(self):
        self.nodes = dict()
        self.edges = list()
        self.adjList = dict()

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
        self.adjList[node0].append(node1)
 
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
    canvas = Canvas()

    input_graph(canvas)
 
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