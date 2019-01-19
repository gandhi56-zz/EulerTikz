import random
from tkinter import *

n, m = map(int, input().split())
dim = 500

g = [[] for _ in range(n)]
coor = [(random.randint(0, dim), random.randint(0, dim)) for _ in range(n)]
edges = []

def clicked():
    print("clicked registered")

for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u,v))
    g[u].append(v)
    g[v].append(u)

master = Tk()
master.title("Force-based Graph Layout")

canvas = Canvas(master, width=500, height=500)
canvas.pack()

nodes = [Button(canvas, text=str(i), command = clicked) for i in range(n)]
for i in range(n):
    canvas.create_window(*coor[i], window=nodes[i]) 

print(coor)
for e in edges:
    print(e)
    canvas.create_line(*coor[e[0]], *coor[e[1]])

def close_window():
    master.destroy()

exit_btn = Button(master, text = "Close", command = close_window)
exit_btn.pack()

canvas.mainloop()
