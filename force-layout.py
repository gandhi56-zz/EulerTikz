import random
from tkinter import *
from tkinter.dnd import Tester as DragWindow, Icon as Dragable

# GLOBAL variables --------------------------------------------------
WIN_WIDTH = 500
WIN_HEIGHT = 500

# -------------------------------------------------------------------

class DragManager():
    def add_dragable(self, widget):
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        # you could use this method to create a floating window
        # that represents what is being dragged.
        pass

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        pass

    def on_drop(self, event):
        # find the widget under the cursor
        x,y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x,y)
        try:
            target.configure(image=event.widget.cget("image"))
        except:
            pass


# Window class ------------------------------------------------------
class Window:
	def __init__(self, winTitle, winWidth, winHeight):
		self.master = Tk()
		self.master.title(winTitle)

		self.canvas = Canvas(
						self.master, 
						width=winWidth, 
						height=winHeight
					)
		self.canvas.pack()
		self.nodes = list()
		self.edges = list()
		self.coor = list()

		self.master.withdraw()

		self.dragWindow = DragWindow(self.master)

	def add_node(self, lbl):
		self.nodes.append(Button(self.dragWindow.top, text=lbl, command=self.make_btn, args=lbl).pack())

	def make_btn(self,lbl):
		Dragable(lbl).attach(self.dragWindow.canvas)

	def add_edge(self, edge):
		self.edges.append(edge)

	def init_coords(self):	
		self.coor = [(	random.randint(0, WIN_WIDTH), 
			random.randint(0, WIN_HEIGHT)) 
			for _ in range(len(self.nodes))]

	def render(self):
		for i in range(len(self.nodes)):
			self.canvas.create_window(*self.coor[i], window=self.nodes[i])
		print(self.coor)

		for edge in self.edges:
			print(edge)
			self.canvas.create_line(*self.coor[edge[0]], 
				*self.coor[edge[1]])

	def close(self, ):
		self.master.destroy()

# -------------------------------------------------------------------

# Procedures --------------------------------------------------------
def input_graph():
	n, m = map(int, input().split())
	g = [[] for i in range(n)]	# adjacency list rep of a graph

	for i in range(n):
		win.add_node(str(i))

	edges = []	# edge list
	for i in range(m):
		u, v = map(int, input().split())
		edges.append((u,v))
		g[u].append(v)
		g[v].append(u)
		win.add_edge((u,v))
# -------------------------------------------------------------------

if __name__ == '__main__':
	win = Window("Force-based layout", 500, 500)
	input_graph()
	win.init_coords()
	print("rendering graph")
	win.render()
	win.canvas.mainloop()


