from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader
from pathlib import Path
import os
import json

# Get main folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Create product image directory if does not exist
Path(f"{BASE_DIR}/static/product image").mkdir(parents=True, exist_ok=True)
# Make product image path
img_dir = os.path.join(BASE_DIR, "static", "product image")

def openBook():
	wb = load_workbook('data.xlsx')
	ws = wb['Product Details']
	return ws

def savePicture(sheet):
	image_loader = SheetImageLoader(sheet)
	image = image_loader.get('E3')
	image.save(f"{img_dir}/test.jpg")

def makeJson(ws):
	title = []
	for row in ws.iter_rows(min_row=2, max_col=8, max_row=2):
		print(row)
		for cell in row:
			title.append(cell.value)
	print(title)



def main():
	sheet = openBook()
	makeJson(sheet)

main()

