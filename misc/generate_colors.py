# -*- coding: utf-8 -*-

"""

Generate colors from the named color table from CSS4 in 
https://github.com/w3c/csswg-drafts/blob/main/css-color-4/Overview.bs

and

Wikipedia page
https://en.wikipedia.org/wiki/Web_colors
https://en.wikipedia.org/wiki/Template:Color_chart_X11
(copy the csv content to a file named colors.csv)
"""


from os import name
import re
import csv


WRITE_LOWERCASE = True
WRITE_CAMELCASE = True
OUTPUT_FILE_CAMELCASE = '../vmathlib/vcolors.py'

# download or copy-n-paste these two input file
X11_COLORS_CSV_FILE = 'temp/colors.csv'
CSS_OVERVIEW_BS_FILE = 'temp/Overview.bs'

PREFACE = """
Web named colors generated from generate_colors.py

You can install the Color Highlight vscode extension to see colors in editor.
"""
PREFACE_TEXT = '"""{}"""\n\n'.format(PREFACE)


def parse_csv_color(row):
	category, name, r, g, b = row
	code = '#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))
	return (category, name, code)


def get_categorized_colors():
	categorized_colors = {}
	with open(X11_COLORS_CSV_FILE, newline='') as csvfile:
		reader = csv.reader(csvfile)
		header = next(reader)
		for row in reader:
			if row:
				res = parse_csv_color(row)
				category, name, code = res
				categorized_colors.setdefault(category, {})[name] = code
	return categorized_colors


def get_named_color_table():
	input_file = CSS_OVERVIEW_BS_FILE
	with open(input_file, 'r', encoding='utf-8') as f:
		started = False
		table_lines = []
		for line in f:
			if not started:
				if '<table class="named-color-table"' in line:
					started = True
			if started:
				table_lines.append(line)
				if '</table>' in line:
					break

	return table_lines


def parse_named_color(line):
	m_name = re.search('<dfn>(.*?)</dfn>', line)
	if not m_name:
		return
	name = m_name.group(1)
	m_code = re.search('<td>(.*?)<td>', line[m_name.end():])
	assert m_code
	code = m_code.group(1)
	return (name, code)


def get_named_colors():
	named_colors = {}
	table_lines = get_named_color_table()
	for line in table_lines:
		if '<dfn>' in line:
			res = parse_named_color(line)
			if res:
				named_colors[res[0]] = res[1]
	return named_colors


def code_to_ints(code):
	r = code[1:3]
	g = code[3:5]
	b = code[5:7]
	return (int(r, 16), int(g, 16), int(b, 16))


def ints_to_floats(ints):
	return (ints[0] / 255.0, ints[1] / 255.0, ints[2] / 255.0)


def format_named_color(named_color):
	name, code = named_color
	float_format = '{:.4f}'
	vec_format = 'Vector3({}, {}, {})'.format(float_format, float_format, float_format)
	color_ints = code_to_ints(code)
	color_floats = ints_to_floats(color_ints)
	vec_str = vec_format.format(*color_floats)
	assign_str = '{} = {}'.format(name, vec_str)
	res = '{:55} {}'.format(assign_str, code)
	return res


def write_named_colors(f, named_colors, is_lowercase=False):
	for named_color in named_colors.items():
		if is_lowercase:
			named_color = (named_color[0].lower(), named_color[1])
		line = format_named_color(named_color)
		f.write(line + '\n')


def write_categorized_color_file(categorized_colors):
	with open(OUTPUT_FILE_CAMELCASE, 'w', newline='\n') as f:
		f.write(PREFACE_TEXT)
		f.write('from vmath import Vector3\n\n\n')
		if WRITE_CAMELCASE:
			f.write('# ---------- CamelCase ----------\n\n')
			for category, named_colors in categorized_colors.items():
				f.write('# {} colors\n'.format(category))
				write_named_colors(f, named_colors)
				f.write('\n')
		if WRITE_LOWERCASE:
			f.write('\n')
			f.write('# ---------- lowercase ----------\n\n')
			for category, named_colors in categorized_colors.items():
				f.write('# {} colors\n'.format(category))
				write_named_colors(f, named_colors, is_lowercase=True)
				f.write('\n')

def fix_categorized_colors(categorized_colors, named_colors):
	# add grey colors, from gray to grey
	gray_colors = categorized_colors['Gray']
	new_gray_colors = {}
	for name, code in gray_colors.items():
		new_gray_colors[name] = code
		if name.endswith('Gray'):
			gray_to_grey = name[:-4] + 'Grey'
			new_gray_colors[gray_to_grey] = code
	categorized_colors['Gray'] = new_gray_colors

	# add rebeccapurple
	violet_colors = categorized_colors['Violet']
	if 'RebeccaPurple' not in violet_colors:
		rebeccapurple_code = named_colors['rebeccapurple']
		violet_colors['RebeccaPurple'] = rebeccapurple_code


def check_colors(named_colors, categorized_colors):
	print('checking ...')
	names = list(named_colors)

	x11_names = []
	for colors in categorized_colors.values():
		x11_names.extend([name.lower() for name in colors])

	print('css4', len(names), 'x11', len(x11_names))
	diff_names_1 = set(names) - set(x11_names)
	print('css4 - x11', len(diff_names_1))
	print(diff_names_1)
	diff_names_2 = set(x11_names) - set(names)
	print('x11 - css4', len(diff_names_2))
	print(diff_names_2)
	if not (diff_names_1 or diff_names_2):
		print('checking result: ok')
	else:
		print('checking result: error')

if __name__ == '__main__':
	# css4 named colors, all lowercase, no category
	named_colors = get_named_colors()

	# x11 named colors from wikipedia page Web_colors, CamelCase with category
	categorized_colors = get_categorized_colors()
	# the x11 names don't have gr*e*y names and rebeccapurple, fix it
	fix_categorized_colors(categorized_colors, named_colors)

	# write the colors
	write_categorized_color_file(categorized_colors)
	
	# can use the categorized_colors to do other work


	# checking, ensure the two sources' names match
	check_colors(named_colors, categorized_colors)
