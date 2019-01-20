from tkinter import *
import math, random, bisect
import numpy as np

SIZE = 300
SHIFT = 50
MAXEDGE = 25.0

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
            coor[-1] *= SIZE
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
                Fx, Fy = hook(coor[i], coor[j]) if L[i][j] else coloumb(coor[i], coor[j])
                vx = v[i][0] + Fx / m * dt
                vy = v[i][1] + Fy / m * dt
                x = coor[i][0] + vx * dt
                y = coor[i][1] + vy * dt
                coor[i], v[i] = (x, y), (vx, vy)

    print(coor)
    # (x, y) coordinates for each vertex
    return list(map(lambda x: (int(x[0]), int(x[1])), coor))

def plot(coor, L):
    n = len(L)
    for i in range(n):
        for j in range(i):
            if i == j: continue
            if L[i][j]:
                plt.plot((coor[i][0], coor[j][0]), (coor[i][1], coor[j][1]), linestyle=':', marker = 'o', ms=5)
    
        plt.text(*coor[i], s=str(i), fontweight='bold')
    plt.title('Eulertikz')
    plt.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

n, m = map(int, input().split())

# laplacian matrix
L = [[0]*n for i in range(n)]
g = [[] for _ in range(n)]
edges = []

for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u, v))
    g[u].append(v)
    g[v].append(u)
    L[u][v] = L[v][u] = -1
    L[u][u] += 1
    L[v][v] += 1

coor = getCoordinates(L)

print("positions: ")
print(coor)

# plot graph
# plot(coor, L)

dim = 500

# coor = [(random.randint(0, dim), random.randint(0, dim)) for _ in range(n)]


"""
while True:
        for i in range(n):
            Fx = Fy = 0
            for j in range(n):
                if i == j: continue
                fx, fy = hook(coor[i], coor[j], 15) if L[i][j] else coloumb(coor[i], coor[j], 0.5)
                print("{} - {}".format())

                Fx += fx
                Fy += fy
            
            vx = v[i][0] + Fx / m * dt
            vy = v[i][1] + Fy / m * dt
            x = coor[i][0] + vx * dt
            y = coor[i][1] + vy * dt
            canvas.move(nodes[i], vx*dt, vy*dt)
            coor[i], v[i] = (x, y), (vx, vy)
        
        canvas.update()
"""

canvas.mainloop()
