#!/usr/bin/python
#
#
#A program to process the report file(grid view) from Envision reader/ICCB
#
#Longfei Wang
#

import csv
import sys

if len(sys.argv) < 2:
	print "Usage: python grid2list.py INPUT_FILE [OUTPUT_FILE]"
	sys.exit()

else:
	inputfile = sys.argv[1]
	outputfile = sys.argv[2] if len(sys.argv)>2 else inputfile.split('.')[0]+'_listout.csv'


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

		#maintain a list of unique plates cols rows and titles 
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

print "Processing grid csv file....."

with open(inputfile,'rb') as csvfile:
	reader = csv.reader(csvfile)

	for rows in reader:#read through the grid csv file and find plates/talbes
		if rows[0] == 'Plate':
			rows = reader.next()

			try:
				plate_id = rows[0]
				if plate_id not in tabledict.keys():
					tabledict[plate_id] = dict()
			except:
				pass

		elif ',1,2,3,4,5,6,7,8,9' in ','.join(rows):#the columns header is the idenifier for a table, this might need to be improved
			if title:
				print plate_id,title,reader.line_num
				tabledict[plate_id][title] = table(reader,plate_id,title,rows[1:])

		else:
			title = ''.join(rows)

print
print
print "Writing list csv file....."

with open(outputfile,'wb') as csvfile:
	writer=csv.writer(csvfile,delimiter=',')

	writer.writerow(['plate','well']+table.titles)#header
	
	for plate in table.plates:
		for well in table.wells():

			print plate,well,

			line = list()

			line+=[plate,well]

			for title in table.titles:
				try:
					line.append(tabledict[plate][title][well])
				except:
					line.append('None')

			writer.writerow(line)


print
print
print "============================================Summary==========================================="
print "Plates:",",".join(table.plates)
print "cols:",",".join(table.allcols)
print "rows:",",".join(table.allrows)
print "Num of Wells:",len(table.allcols)*len(table.allrows)
print "Columns:",",".join(table.titles)
