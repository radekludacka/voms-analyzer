#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script analyzes voms log - how many times each user created 
# proxy certificate from specific machine. Script uses numpy and
# matplotlib to draw usage plot.
#
# Exmaple: python voms-analyzer.py <path to voms log file>
#
# Radek Ludacka (ludacka@fzu.cz) - 2013-12
#

import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import itertools
import time, calendar
from matplotlib.dates import num2date, DateFormatter
import matplotlib.cm as cm
from collections import OrderedDict


def chart(result, name):
    cmap = cm.get_cmap('spectral')
    N = len(result)
    numbers = range(len(result))
    for k, v in result.items(): 
        date_number = {}
        for t in v:
            date = datetime(t.year, t.month, t.day, 0, 0, 0, 0)
            if not date in date_number.keys():
                date_number[date] = 0
            value = date_number[date]
            value += 1
            date_number[date] = value

        date_number = OrderedDict(sorted(date_number.items()))
        name = k.split('=')[-1]

        c = cmap(float(numbers[0])/(N-1))
        numbers = numbers[1:]

	dates = matplotlib.dates.date2num(date_number.keys())
	plt.plot_date(dates, date_number.values(), label=name, color=c, linestyle='-')

    plt.grid()
    ax = plt.gca()
    ax.set_xticks(date_number.keys())
    ax.set_xticklabels([d.strftime('%d') for d in date_number.keys()])

    lgd = plt.legend(bbox_to_anchor=[0.5, 0], loc='upper center', ncol=2, borderaxespad=1.05)                                      
    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('result.pdf')
    plt.savefig(pp, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    pp.close()

    plt.savefig('result.png')

    plt.show()                                       
                                                      
                                                      
def parse_date(value):
    result = None
    try:                               
        result = datetime.strptime(value, '%a %b %d %H:%M:%S %Y')
    except ValueError:
        print value
        result = datetime(1970, 1, 1, 0, 0, 0)

    return result
 
def parse_init_line(line):
    result = []
    date = parse_date(line[:24])
    rest = line[24:].split(':')
    voms_server = rest[1]
    msg = rest[3][6:] + ':' + rest[4]
    command = rest[5].split()[0]
    url = None
    if len(rest) > 8:
        url = rest[8].split()[0]
    return (date, voms_server, msg, command, url)

def main(argv):
    log = open(argv[1]).readlines()
    result = []
    usersAndFrom = set()
    users = set()

    i = 0
    while i < len(log):
        result1 = ('', '', '', '') 
        while i < len(log) and result1[3] != 'logconnection':
            result1 = parse_init_line(log[i])
            i += 1
        while i+1 < len(log) and log[i+1].split(':')[-2].strip() != 'user':
            i += 1
        if i+1 >= len(log):
            break
        user = log[i+1].split(':')[-1].strip()[:-1]
        usersAndFrom.add(user + " " + result1[4])
        users.add(user)
        result.append([user, result1[0], result1[1], result1[2], result1[4]]) 

    utilization = {}
    utilizationWithUrl = {}

    for item in users:
        utilization[item] = []

    for item in usersAndFrom:
        utilizationWithUrl[item] = []

    for res in result:
        item = res[0]
        item1 = res[0] + " " + res[4]
        utilization[item].append(res[1])
        utilizationWithUrl[item1].append(res[1])

    for k, v in utilizationWithUrl.items():
        print str(len(v)) + '\t' + str(k)

    chart(utilization, argv[1])


if __name__ == "__main__":
    main(sys.argv)
