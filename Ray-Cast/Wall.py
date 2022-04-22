import random

class Wall:
	def __init__(self, *args):
		
		if len(args) == 2:
			# window width, window height (random)
			self.p1 = (random.randint(0,args[0]),random.randint(0,args[1]))
			self.p2 = (random.randint(0,args[0]),random.randint(0,args[1]))

		if len(args) == 4:
			# x1, y1, x2, y2
			self.p1 = (args[0],args[1])
			self.p2 = (args[2],args[3])
		
	def hit(self, p1, p2):
		x1 = self.p1[0]
		y1 = self.p1[1]
		x2 = self.p2[0]
		y2 = self.p2[1]
		x3 = p1[0]
		y3 = p1[1]
		x4 = p2[0]
		y4 = p2[1]

		den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
		if den == 0:
			return
		else:
			t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
			u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

			if t > 0 and t < 1 and u > 0:
				pt = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
				return pt
			else:
				return