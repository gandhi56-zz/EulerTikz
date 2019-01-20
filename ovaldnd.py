import tkinter as tk

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Drag and drop")
		self.dnd = None
		self.canvas = tk.Canvas(self, bg="white")
		self.canvas.pack()

		x, y = 30,30
		self.canvas.create_oval(x, y, 60, 60, fill="green", tags="draggable")
		# self.canvas.create_text(x+15, y+15, text="0")
		self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.button_press)
		self.canvas.tag_bind("draggable", "<Button1-Motion>", self.button_motion)
		self.canvas.update()

	def button_press(self, event):
		item = self.canvas.find_withtag(tk.CURRENT)
		self.dnd = (item, event.x, event.y)

	def button_motion(self, event):
		x, y = event.x, event.y
		item, x0, y0 = self.dnd
		self.canvas.move(item, x - x0, y - y0)
		self.dnd = (item, x, y)

if __name__ == '__main__':
	app = App()
	app.mainloop()