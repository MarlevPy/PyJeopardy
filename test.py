# -*- coding: iso-8859-1 -*-
import json

with open('jeopardy.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

POINTS = [int(point) for point in data[next(iter(data.keys()))].keys()]
print(POINTS)