
from link import *

class user_details:

	def __init__(self, firstname, lastname, username, followers=0, followee=0, public_links=0):
		self.firstname=firstname
		self.lastname=lastname
		self.username=username
		self.followers=followers
		self.followee=followee
		self.public_links=public_links

	def get_firstname(self):
		return self.firstname

	def get_lastname(self):
		return self.lastname

	def get_username(self):
		return self.username
	
	def get_followers(self):
		return self.followers
	
	def get_followee(self):
		return self.followee
	
	def get_public_links(self):
		return self.public_links

	def get_link_details(self):
		return self.link_details

	def set_link_details(self,link):
		self.link_details=link