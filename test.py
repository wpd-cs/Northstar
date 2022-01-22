# -*- coding: utf-8 -*-
import csv

if __name__ == "__main__":

	with open("cairs.txt", "r") as f:
		csv_reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
		next(csv_reader)

		for row in csv_reader:
			print(row)