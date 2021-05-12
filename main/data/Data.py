from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader
from openpyxl.utils import get_column_letter
from pathlib import Path
import os
import json

# Get main folder# Create product image directory if does not exist
current_dir = os.getcwd()
Path(f"{current_dir}/product image").mkdir(parents=True, exist_ok=True)
# Make product image path
img_dir = f"{current_dir}/product image"

def openBook():
	wb = load_workbook('data1.xlsx')
	ws = wb['Product Details']
	return ws

def makeJson(ws):
	pic_name = 3
	image_loader = SheetImageLoader(ws)
	title = []
	datalist = []
	data = {}
	for row in ws.iter_rows(min_row=2, max_col=8, max_row=2):
		for cell in row:
			title.append(cell.value)

	for row in range(3,139):
		for col in range(1,9):	
			letter = f'{get_column_letter(col)}{row}'
			if image_loader.image_in(letter):
				image = image_loader.get(letter)
				img_path = f"{img_dir}/{pic_name}.png"
				image.save(img_path)
				data[f'{title[col-1]}'] = img_path
			else:
				cell = ws[letter]
				data[f'{title[col-1]}'] = cell.value
		pic_name+=1
		datalist.append(data)
		data = {}

	with open('data.json', 'w+') as output:
		json.dump(datalist, output, indent=4, separators=(',', ': '))
			
	



def main():
	sheet = openBook()
	makeJson(sheet)

main()

