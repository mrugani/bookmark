#!/usr/bin/env python

class link:
	
	def __init__(self, url, lid, tags, description, date, visibility):
		self.url = url
		self.lid = lid
		self.tags = tags
		self.description = description
		self.date = date
		self.visibility = visibility

	def get_url(self):
		return self.url

	def get_lid(self):
		return self.lid

	def get_tags(self):
		return self.tags

	def get_desc(self):
		return self.description

	def get_date(self):
		return self.date

	def is_private(self):
		
		return self.visibility == "private"
