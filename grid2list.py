#!/usr/bin/python

filename = '/home/longfei/Downloads/test.csv'

import csv


class table():
	"""A class that handle tables in a grid file"""
	plates = list()
	titles = list()
	allcols = list()
	allrows = list()

	def __init__(self,pointer,plate_id,title,columns):
		self.columns = [i.zfill(2) for i in columns]
		self.plate_id = plate_id
		self.title = title

		self.rows=list()
		self.c=list()
		r = pointer.next()
		while r[0]:
			self.rows.append(r[0])
			self.c.append(r[1:])
			r = pointer.next()

		#maintain a list of unique cols rows and titles 
		self.allrows += [i for i in self.rows if i not in self.allrows]
		self.allcols += [i for i in self.columns if i not in self.allcols]
		if title not in self.titles:
			self.titles.append(title)
		if plate_id not in self.plates:
			self.plates.append(plate_id)

	def __getitem__(self,key):
		col = key[-2:]
		row = key[:-2]
		if col in self.columns and row in self.rows:
			try:
				return self.c[self.rows.index(row)][self.columns.index(col)]
			except:
				return ''

	@classmethod
	def wells(self):
		c = list()
		for row in self.allrows:
			for col in self.allcols:
				c.append(row+col)
		return c




plate_id = 0
title = ''
tabledict = dict()


csvfile =  open(filename,'rb')
csv = csv.reader(csvfile)


for rows in csv:#read through the grid csv file and find plates/talbes
	if rows[0] == 'Plate':
		rows = csv.next()

		try:
			plate_id = int(rows[0])
			if plate_id not in tabledict.keys():
				tabledict[plate_id] = dict()
		except:
			pass

	elif ',1,2,3,4,5,6,7,8,9' in ','.join(rows):#the columns header is the idenifier for a table, this might need to be improved
		if title:
			tabledict[plate_id][title] = table(csv,plate_id,title,rows[1:])

	else:
		title = ''.join(rows)


for plate in table.plates:
	for well in table.wells():

		print plate,well,

		for title in table.titles:
			try:
				print tabledict[plate][title][well],
			except:
				print 'N/A',

		print