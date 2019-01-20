import math, random, bisect, pygame
import re, sys
import numpy as np

 
# --- Global constants ---
# ------------------------------------------------------------------------
# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (182, 204, 239)
PINK = (255, 175, 175)

# Screen dimensions
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

BACKCOLOR = LIGHTBLUE

# Spectral layout variables
SCALE = SCREEN_HEIGHT * 3 // 5
SHIFT = SCALE // 6

# Graph drawing variables
NUM_NODES = 100
NUM_EDGES = 100
NODE_RAD = 15

# Event handling variables
mouseDragging = False
draggingNode = None
offsetX = 0
offsetY = 0

mouseSelecting = False

UNSELECTED = 0
SELECTING = 1
SELECTED = 2
DRAGGING = 3
DRAG_SELECT = 4
selectStatus = UNSELECTED
point0 = None
point1 = None
# ------------------------------------------------------------------------
# --- Classes ---

class Node():
    def __init__(self, xPos, yPos, rad, color, label):
        self.pos = [xPos, yPos]
        self.rad = rad
        self.color = color
        self.font = pygame.font.Font(None, 20)
        self.text = self.font.render(label, True, BLACK)
        self.highlight = False
    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, self.pos, self.rad)
        if self.highlight:
            pygame.draw.circle(screen, BLUE, self.pos, self.rad-2)
        else:
            pygame.draw.circle(screen, self.color, self.pos, self.rad-2)
        screen.blit(self.text, [self.pos[0]-self.rad//2, self.pos[1]-self.rad//2])
    def collided(self, pos):
        dx = self.pos[0] - pos[0]
        dy = self.pos[1] - pos[1]
        return dx*dx + dy*dy <= self.rad*self.rad
    def selected(self):
        maxX = max(point0[0], point1[0])
        minX = min(point0[0], point1[0])
        maxY = max(point0[1], point1[1])
        minY = min(point0[1], point1[1])
        return minX <= self.pos[0] <= maxX and minY <= self.pos[1] <= maxY
 
class Canvas:
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self, nodes, coor = list(), edges = list()):

        print(coor)
        print(edges)
        self.nodes = dict()
        self.edges = []
        self.adjList = dict() # adjacency list rep of a graph


        print("before adding nodes")
        # print(coor)
        for i in range(NUM_NODES):
            self.add_node(nodes[i], min(max(0, coor[i][0]), SCREEN_WIDTH),
                    min(max(0, coor[i][1]), SCREEN_HEIGHT), NODE_RAD, PINK)
       
        print("added nodes")
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
        global mouseSelecting, selectStatus, point0, point1

        """ Process all of the events. Return a "True" if we need
            to close the window. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if selectStatus == UNSELECTED:
                        mousePos = event.pos
                        for u in self.nodes:
                            if self.nodes[u].collided(mousePos):
                                selectStatus = DRAGGING
                                draggingNode = u
                                offsetX = self.nodes[u].pos[0] - mousePos[0]
                                offsetY = self.nodes[u].pos[1] - mousePos[1]
                                break
                            else:
                                selectStatus = SELECTING
                                point0 = mousePos

                    elif selectStatus == SELECTING:
                        selectStatus = UNSELECTED

                    elif selectStatus == SELECTED:
                        mousePos = event.pos
                        for u in self.nodes:
                            if self.nodes[u].collided(mousePos) and self.nodes[u].highlight:
                                offsetX = self.nodes[u].pos[0] - mousePos[0]
                                offsetY = self.nodes[u].pos[1] - mousePos[1]
                                break
                            else:
                                selectStatus = SELECTING
                                point0 = mousePos

                        selectStatus = DRAG_SELECT

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if selectStatus == DRAGGING:
                        selectStatus = UNSELECTED
                        offsetX = offsetY = 0
                        draggingNode = None
                    elif selectStatus == UNSELECTED:
                        pass
                    elif selectStatus == SELECTING:
                        selectStatus = SELECTED
                        point1 = event.pos

                        # find all nodes lying in the selection box
                        selectedNodes = []
                        for u in self.nodes:
                            if self.nodes[u].selected():
                                selectedNodes.append(u)
                                self.nodes[u].highlight = True

                        print(selectedNodes)
                    elif selectStatus == SELECTED:
                        selectStatus = DRAGGING

                    elif selectStatus == DRAG_SELECT:
                        selectStatus = UNSELECTED
                        offsetX = offsetY = 0

                        for u in self.nodes:
                            self.nodes[u].highlight = False

            elif event.type == pygame.MOUSEMOTION:
                mousePos = event.pos
                if selectStatus == DRAGGING:
                    self.nodes[draggingNode].pos[0] = mousePos[0] + offsetX
                    self.nodes[draggingNode].pos[1] = mousePos[1] + offsetY
                elif selectStatus == DRAG_SELECT:
                    for u in self.nodes:
                        if self.nodes[u].highlight:
                            self.nodes[u].pos[0] = mousePos[0] + offsetX
                            self.nodes[u].pos[1] = mousePos[1] + offsetY
 
        return False
 
    def run_logic(self):
        pass
 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BACKCOLOR)

        # draw graph
        for e in self.edges:
            pygame.draw.line(screen, BLACK,
                       (self.nodes[e[0]].pos[0],self.nodes[e[0]].pos[1]),
                       (self.nodes[e[1]].pos[0],self.nodes[e[1]].pos[1]),
                    )
        for u in self.nodes:
            self.nodes[u].draw(screen)
        
        # draw selection if applicable
        if selectStatus == SELECTING:
            self.draw_selection(screen)
        pygame.display.flip()

    def draw_selection(self, screen):
        global point0
        mousePos = pygame.mouse.get_pos()
        width = min(abs(mousePos[0] - point0[0]), abs(SCREEN_WIDTH - point0[0]))
        height = min(abs(mousePos[1] - point0[1]), abs(SCREEN_HEIGHT - point0[1]))
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((0,0,255, 64))

        startPos = list(point0)
        if mousePos[0] < point0[0]:
            startPos[0] = mousePos[0]

        if mousePos[1] < point0[1]:
            startPos[1] = mousePos[1]

        screen.blit(surf, startPos)

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

        # print("laplacian: ")
        A = np.array(L)

        # print(A)

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

        # print(coor)

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

        # print("coordinates:")
        # print(coor)
        # (x, y) coordinates for each vertex
        return list(map(lambda x: (int(x[0]), int(x[1])), coor))

    def parser():

        global NUM_NODES, NUM_EDGES
        
        
        s = ""
        for line in sys.stdin: s += line;

        matches = re.compile(r'(\\(?:begin|end)\{tikzpicture\})').finditer(s)
        matches = [(m.start(0), m.end(0)) for m in matches]
        graphData = s[matches[0][1]:matches[1][0]]

        nodeData = re.findall(r'\\node(.+);', graphData)

        nodeData = [re.sub(r'(\$)', "", re.findall(r'\{(.*)\}', n)[0]) for n in nodeData]
        print(nodeData)


        edgeData = re.findall(r'\((.*)\)(?:.*)(?:edge|--)(?:.*)\((.*)\)', graphData)

        print(edgeData)

        n, m = len(nodeData), len(edgeData)
        coor = re.findall(r'(?:at.*)\((\d+,\d+)\)', graphData)

        # laplacian matrix
        L = [[0]*n for i in range(n)]
        g = [[] for _ in range(n)]
        edges = edgeData

        for u, v in edges:
            u, v = nodeData.index(u), nodeData.index(v)
            L[u][v] = L[v][u] = -1
            L[u][u] += 1
            L[v][v] += 1

        NUM_NODES, NUM_EDGES = n, m
        coor = Layout.getCoordinates(L)

        return nodeData, coor, edges

def main():
    mouseDragging = False
    draggingNode = None
    offsetX = 0
    offsetY = 0

    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Graph drawing using spectral layout")
    pygame.mouse.set_visible(True)

    done = False
    clock = pygame.time.Clock()
 
    canvas = Canvas(*Layout.parser())

    while not done:
        done = canvas.process_events()
        canvas.run_logic()
        canvas.display_frame(screen)
        clock.tick(60)
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
