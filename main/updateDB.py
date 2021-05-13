from .models import Product
from pathlib import Path
import json

def updateData():
	BASE_DIR = Path(__file__).resolve().parent.parent
	with open(f'{BASE_DIR}/static/data.json') as file:
		datas = json.load(file)
	if len(datas) > 136:
		for data in datas:
			Product.objects.create(
				category=data['Category'],
				sap=data['SAP'],
				description=data['Description'],
				picture=data['Picture'],
				size=data['Sizes in mm'],
				unit_price=data['Unit Price'],
				unit=data['Order Multiples'],
				availability=True,
				)