import matplotlib.pyplot as plt
import matplotlib.lines as lines
from random import randrange as rand
from random import choice as rand_choice
from random import sample as rand_sample
import numpy as np

# global variables
eps = 1e-5
minx = 0
miny = 0
maxx = 100
maxy = 100
node_rad = 1
nodes = {}  # stores the node shape objects

# for force based layout algorithm
scale = (maxy - miny) * 3 // 5
shift = scale // 6

class Node:
  def __init__(self, xx=None, yy=None):
    self.x = xx
    self.y = yy
    if self.x is None:
      self.x = rand(minx+5, maxx-5)
    if self.y is None:
      self.y = rand(miny+5, maxy-5)
    self.shape = plt.Circle((self.x, self.y), node_rad)
    self.adj = set()

  def get_shape(self):
    return self.shape

  def adj_node(self, u):
    self.adj.add(u)

  def set_coor(self, tup):
    self.x = tup[0]
    self.y = tup[1]

def show(patch):
  ax.add_patch(patch)
  plt.show()

def input_graph():
  n, m = map(int, input().split())
  for i in range(n):
    nodes[i] = Node(rand(1, maxx), rand(1, maxy))
  for i in range(m):
    x, y = map(int, input().split())
    if x not in nodes:
      nodes[x] = []
    nodes[y].adj_node(x)
    nodes[x].adj_node(y)

def random_edges(m):
  # add m random edges to the graph
  while m > 0:
    u, v = rand_sample(set(nodes.keys()), 2)
    if v in nodes[u].adj:
      continue
    nodes[u].adj_node(v)
    nodes[v].adj_node(u)
    m -= 1

# force-based layout algorithm -------------------------------------
def hook(p, q, k=100.0):
  dx = p[0] - q[0]
  dy = p[1] - q[1]
  ds = (dx*dx + dy*dy)**0.5
  return k*dx/ds, k*dy/ds

def coloumb(p, q, k=0.5):
  dx = q[0] - p[0]
  dy = q[1] - p[1]
  ds3 = (dx*dx + dy*dy)**1.5
  fx = k*dy / ds3
  fy = k*dy / ds3
  return fx, fy

def force_layout():
  n = len(nodes)  # number of nodes
  L = [[0]*n for i in range(n)] # Laplacian matrix
  for u in nodes:
    for v in nodes[u].adj:
      L[u][v] = L[v][u] = -1
      L[u][u] += 1
      L[v][v] += 1

  A = np.array(L)
  eigval, eigvec = np.linalg.eigh(A)
  coor = []
  for i in range(n):
    if eigval[i] > eps:
      coor.append(eigvec[:,i])
      coor[-1] *= scale
      coor[-1] += abs(min(coor[-1])) + shift

    if len(coor) >= 2:
      break

  coor = list(zip(coor[0], coor[1]))
  v = [(0,0)] * n
  dt, m, steps = 1e-2, 1.0, 6
  for _ in range(steps):
    for i in range(n):
      for j in range(n):
        if i == j:
          continue
        fx, fy = hook(coor[i], coor[j]) if L[i][j] else coloumb(coor[i], coor[j])
        vx = v[i][0] + fx/m * dt
        vy = v[i][1] + fy/m * dt
        x = coor[i][0] + vx * dt
        y = coor[i][1] + vy * dt
        coor[i], v[i] = (x, y), (vx, vy)

  return list(map(lambda x : (int(x[0]), int(x[1])), coor))
# ------------------------------------------------------------------


def draw_graph():
  ax = plt.gca()
  
  # render -------------------------------
  # nodes
  for u in nodes:
    ax.add_patch(nodes[u].get_shape())

  # edges
  for u in nodes:
    for v in nodes[u].adj:
      ax.add_line(lines.Line2D([nodes[u].x, nodes[v].x], [nodes[u].y, nodes[v].y]))

if __name__ == '__main__':
  plt.axis([minx, maxx, miny, maxy])
  input_graph()
  random_edges(1)

  coor = force_layout()
  ax = plt.gca()
  for u in nodes:
    nodes[u].set_coor(coor[u])
    ax.add_patch(nodes[u].get_shape())
    for v in nodes[u].adj:
      ax.add_line(lines.Line2D([nodes[u].x, nodes[v].x], [nodes[u].y, nodes[v].y]))

  plt.show()












