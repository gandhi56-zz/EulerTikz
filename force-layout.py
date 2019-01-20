import random
from tkinter import *
from tkinter.dnd import Tester as DragWindow, Icon as Dragable

# GLOBAL variables --------------------------------------------------
WIN_WIDTH = 500
WIN_HEIGHT = 500
SIZE = 20
NUM_NODES = 100
NUM_EDGES = 100
# -------------------------------------------------------------------

# Window class ------------------------------------------------------
class Window(Tk):
	def __init__(self, winTitle, winWidth, winHeight):
		super().__init__()
		self.title(winTitle)
		self.canvas = Canvas(self.master, width=winWidth, height=winHeight,bg="white")
		self.canvas.pack()
		self.nodes = list()
		self.edges = list()
		self.coor = {}
		for i in range(NUM_NODES):
			self.coor[str(i)] = (random.randint(0, WIN_WIDTH), 
								random.randint(0, WIN_HEIGHT))
		self.dnd = None
		self.lines = list()
		self.adjList = {}

	def add_node(self, lbl):
		# self.nodes.append(Button(self.dragWindow.top, text=lbl, command=self.make_btn, args=lbl).pack())
		
		if lbl not in self.adjList:
			self.adjList[lbl] = list()

		x = self.coor[lbl][0]
		y = self.coor[lbl][1]
		self.canvas.create_oval(x, y, x+SIZE, y+SIZE, fill = "pink", tags="draggable")
		self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.button_press)
		self.canvas.tag_bind("draggable", "<Button1-Motion>", self.button_motion)
		self.canvas.update()

	def button_press(self, event):
		item = self.canvas.find_withtag(CURRENT)
		self.dnd = (item, event.x, event.y)
		print("click:", self.dnd)

	def button_motion(self, event):
		x, y = event.x, event.y
		item, x0, y0 = self.dnd
		self.canvas.move(item, x - x0, y - y0)
		self.dnd = (item, x, y)

	def add_edge(self, edge):
		self.edges.append(edge)
		self.adjList[edge[0]].append(edge[1])
		self.adjList[edge[1]].append(edge[0])

	def render(self):
		for i in range(len(self.nodes)):
			self.canvas.create_window(*self.coor[i], window=self.nodes[i])

		for edge in self.edges:
			self.canvas.create_line(*self.coor[edge[0]], *self.coor[edge[1]])

	def close(self):
		self.master.destroy()

# -------------------------------------------------------------------

# Procedures --------------------------------------------------------
def input_graph():
	NUM_NODES, NUM_EDGES = map(int, input().split())
	g = {str(i) : [] for i in range(NUM_NODES)}	# adjacency list rep of a graph

	for i in range(NUM_NODES):
		win.add_node(str(i))

	edges = []	# edge list
	for i in range(NUM_EDGES):
		u, v = map(str, input().split())
		edges.append((u,v))
		g[u].append(v)
		g[v].append(u)
		win.add_edge((u,v))
# -------------------------------------------------------------------

if __name__ == '__main__':
	win = Window("Force-based layout", 500, 500)
	input_graph()
	win.render()
	win.canvas.mainloop()


