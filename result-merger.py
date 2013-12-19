#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script merges two result of voms-analyzer.py script
# Script allows to merge result where are only user (method userMerger) or 
# result where are user and workstations (method merger)
#
# Exmaple: python result-merger.py <result-file-1> <result-file-2>
#
# Radek Ludacka (ludacka@fzu.cz) - 2013-12
#

import sys


def parse_lines(ifile):
	lines = open(ifile).readlines()
	numberUserCompTable = []

	for line in lines:
		splitted =  line.split()
		values = [int(splitted[0]), " ".join(splitted[1:-1]).strip(), splitted[-1].strip()]
		numberUserCompTable.append(values)

	return numberUserCompTable


def merger(table1, table2):

	resultTable = []
	for line1 in table1:
		for i, line2 in enumerate(table2):
			if line1[1] == line2[1] and line1[2] == line2[2]:
				line1[0] = int(line1[0]) + int(line2[0])
				del table2[i]

		resultTable.append(line1)

	resultTable += table2
	return resultTable


def userMerger(table1, table2):
	users = set()
	utilization = {}
	resultTable = []
	
	for line in table1:
		users.add(line[1])

	for line in table2:
		users.add(line[1])

	for user in users:
		utilization[user] = 0

	for line in table1:
		utilization[line[1]] = utilization[line[1]] + line[0]

	for line in table2:
		utilization[line[1]] = utilization[line[1]] + line[0]

	return utilization


def main(argv):
	files = argv[1:]
	resultTables = []

	for ifile in files:
		resultTables.append(parse_lines(ifile))

	# result = merger(resultTables[0], resultTables[1])

	# # for row in result:
	# # print str(row[0]) + "\t" + row[1] + "\t" + row[2]

	result = userMerger(resultTables[0], resultTables[1])

	for k, v in result.items():
		print str(v) + "\t" + k


if __name__ == "__main__":
	main(sys.argv)
