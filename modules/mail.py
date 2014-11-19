from gluon.tools import Mail

class Send_Mail:

	def __init__(self):
		self.server = Mail('smtp.gmail.com:587', 'this.save.bookmark@gmail.com', 'this.save.bookmark@gmail.com:Admin!@#')


	def send(self, subject, content, to):
		self.server.send(to, subject, content)

