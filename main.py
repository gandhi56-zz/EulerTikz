import matplotlib.pyplot as plt
import matplotlib.lines as lines
from random import randrange as rand
from random import choice as rand_choice
from random import sample as rand_sample

# global variables
minx = 0
miny = 0
maxx = 50
maxy = 50
node_rad = 1
nodes = {}  # stores the node shape objects

class Node:
  def __init__(self, xx=None, yy=None):
    self.x = xx
    self.y = yy
    if self.x is None:
      self.x = rand(1, maxx)
    if self.y is None:
      self.y = rand(1, maxy)
    self.shape = plt.Circle((self.x, self.y), node_rad)
    self.adj = set()

  def get_shape(self):
    return self.shape

  def adj_node(self, u):
    self.adj.add(u)

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
  input_graph()
  random_edges(15)
  plt.axis([minx, maxx, miny, maxy])
  draw_graph()
  plt.show()












