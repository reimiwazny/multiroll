import PySimpleGUI as sg 
from random import randint

sg.theme('DarkAmber')
roll_result = None
rolled_sides = None
rolled_num = None

def roll_dice(modifiers):
	'''Using the values set in the "Number of Dice" and
	"Number of Sides" windows, rolls (dice) quantity of
	(sides)-sided dice. Any modifiers that were entered
	in the "Flat Bonuses" windows will be totaled as well.

	The modifiers argument should be a list containing the
	keys for all InputText elements in the "Flat Bonuses"
	frame.

	If invalid integers are passed into any of these fields,
	or if values above 1000 or lower than 1 are entered for
	the number of dice or sides, they will default to None
	values.

	If invalid values are present for the number of dice or
	sides, no processing of random values will occur.'''
	if not values['-DICE_NUM-']:
		return None
	dice_arr = []
	num_dice = None
	dice_sides = None
	total_mod = 0

	if values['-DICE_NUM-']:
		if values['-DICE_NUM-'].isdigit():
			try:
				num_dice = int(values['-DICE_NUM-']) #check if the number of dice is a valid int
			except ValueError:
				num_dice = None
			if num_dice > 1000 or num_dice<1:
				num_dice = None
			if values['-4-']:
				dice_sides = 4
			elif values['-6-']:
				dice_sides = 6
			elif values['-8-']:
				dice_sides = 8
			elif values['-10-']:
				dice_sides = 10
			elif values['-20-']:
				dice_sides = 20
			elif values['-100-']:
				dice_sides = 100
			elif values['-CUSTOM-']:
				if values['-C_VAL-']:
					if values['-C_VAL-'].isdigit(): #check if the number of sides is a valid int
						dice_sides = int(values['-C_VAL-'])
						if dice_sides > 1000 or dice_sides<1:
							dice_sides = None
	if num_dice and dice_sides:
		while num_dice > 0:
			dice_arr.append(randint(1, dice_sides)) #iterate through dice and roll values for each
			num_dice -= 1
		window['-INDV_RES-'].update(' '.join([str(x) for x in dice_arr])) #generate a string containing all individual dice
		window['-SUM-'].update(sum(dice_arr)) #take the sum of all individual dice rolls

		#apply modifiers
		if modifiers:
			for val in modifiers:
				try:
					total_mod += int(values[val])
				except ValueError:
					pass
			window['-MODS-'].update(total_mod)
			window['-TOTAL-'].update(sum(dice_arr)+total_mod)


		return dice_arr, dice_sides, num_dice

def analyze_window(all_dice, sides, num_dice):
	'''Window that takes the results of a given dice roll and
	displays the frequency of values, frequency of duplicates,
	and frequency of minimum/maximum rolls.

	The all_dice parameter should be a list containing all
	individual dice from a roll. The sides parameter should
	be an integer representing the maximum value of a roll.
	The num_dice parameter should be an integer representing
	the number of rolled dice.

	Note that these calculations can cause noticable performance
	impact when large sample sizes are used. This is why the main
	window limits user values to a maximum of 1000 dice with 1000
	sides each.'''
	frequency_graph = ''
	dupes_graph = ''
	min_counter = 0
	max_counter = 0
	init = True

	for x in range(1, sides+1):
		count = 0
		for roll in all_dice:
			if roll == x:
				count += 1 
		frequency_graph += f'#{x}  |  {count}\n'
		if count >1:
				dupes_graph += f'#{x}  |  {count}\n'
	min_counter = len([roll for roll in all_dice if roll == 1])
	max_counter = len([roll for roll in all_dice if roll == sides])

	#window for displaying the frequency of each possible result
	frequency_chart = [	[sg.Multiline(default_text=frequency_graph, size=(20,5), disabled=True, key='-FREQUENCY-', tooltip='The number of dice that rolled each\nof the possible results.\nShown as RESULT | FREQUENCY')]	]

	#window for displaying any duplicate values and how many of each duplicate were rolled
	duplicates = [	[sg.Multiline(default_text=dupes_graph, size=(20,5), disabled=True, key='-DUPES-', tooltip='The number of dice with identical results.\nShown as RESULT | FREQUENCY')]	]

	#window for displaying how many dice rolled a 1 or maximum value
	mins_maxes = [	[sg.Text('Min Rolls: ', tooltip='The number of dice that rolled a 1')],
					[sg.Text(min_counter, key='-MINS-')],
					[sg.Text('Max Rolls:', tooltip='The number of dice that rolled the maximum value')],
					[sg.Text(max_counter, key='-MAXES-')]	]

	#overall layout for the analysis window
	layout = [	[sg.Frame(title='Frequency', layout=frequency_chart), sg.Frame(title='Duplicates', layout=duplicates), sg.Frame(title='Extremes', layout=mins_maxes)],
				[sg.Button('Back')]	]

	window = sg.Window('Detailed Analysis', layout, font=('any',15), modal=True)



	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'Back'):
			break
	window.close()


def about_window():
	'''Simple window that displays the author name
	and program credits.'''

	layout = [	[sg.Text('MultiRoll+, written by Reimi Wazny')],
				[sg.Text('Powered by Python and PySimpleGUI')],
				[sg.OK()]	]

	window = sg.Window('About', layout, modal=True, element_justification='center')

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'OK'):
			break

	window.close()

def input_error():
	'''Simple window that is displayed when the user inputs
	an invalid entry for the number of dice or sides.'''
	layout =[	[sg.Text('The number of dice/sides must be a positive\nnumber between 1 and 1000!')],
				[sg.OK()]	]

	window = sg.Window('Error', layout, modal=True, element_justification='center', font=('any', 15))

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'OK'):
			break

	window.close()



#selection window for the number of sides per dice
dice_select = [[sg.Radio('4', 'DICE', default=True, key='-4-'), sg.Radio('6','DICE', pad=(15,0), key='-6-')],
			[sg.Radio('8','DICE', key='-8-'), sg.Radio('10','DICE',pad=(15,0), key='-10-')],
			[sg.Radio('20','DICE', key='-20-'), sg.Radio('100','DICE',pad=(4,0), key='-100-')],
			[sg.Radio('Custom','DICE', key='-CUSTOM-'), sg.InputText(size=6, tooltip='Maximum of 1000', key='-C_VAL-', enable_events=True)]	]

#selection window for the number of dice to roll
num_dice = [	[sg.InputText(size=8, tooltip='Maximum of 1000', key='-DICE_NUM-', enable_events=True)]	]

#organizational frame for the dice sides and quantity windows
dice_window = [	[sg.Frame(title='Number of dice', layout = num_dice, size=(190, 60), element_justification='center')],
			[sg.Frame(title='Number of sides', layout=dice_select, size=(190,180))], 
			[sg.Button(button_text='Roll',font=('any',12), tooltip='Roll the currently set dice'),
			sg.Button(button_text='Details',font=('any',12),pad=((14,14),(0,0)), disabled=True, tooltip='View details about the roll such as frequency and duplicates', key='-DETAILS-'),
			sg.Button(button_text='About',font=('any',12))]	]

#window for displaying list of all individual dice
indv_results = [	[sg.Multiline(default_text='', tooltip='A list of all individual dice rolls',size=(28,5), disabled=True, key='-INDV_RES-')]	]

#window for displaying the total of the dice roll, including modifiers
sum_results = [	[sg.Multiline(default_text='',tooltip='The sum of all dice rolled before modifiers', size=(7,1), disabled=True, no_scrollbar=True, key='-SUM-'),
				sg.Text('+/-'),
				sg.Multiline(default_text='',tooltip='The total of all modifiers entered under\'Flat Bonuses\'', size=(7,1), disabled=True, no_scrollbar=True, key='-MODS-'),
				sg.Text('='),
				sg.Multiline(default_text='',tooltip='The total of the dice roll + all modifiers', size=(7,1), disabled=True, no_scrollbar=True, key='-TOTAL-')]	]

#window for entering flat increases or decreases to be added to the dice roll
flat_mods = [	[sg.InputText(size=8, pad=(0,5), key='-ADD1-', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='-ADD2-', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='-ADD3-', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='-ADD4-', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='-ADD5-', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='-ADD6-', enable_events=True)]	]

#organizational frame for the results display
results_window = [	[sg.Frame(title='Individual Results', layout=indv_results, border_width=0)],
					[sg.Text()],
					[sg.Frame(title='Sum of Rolls', layout=sum_results, border_width=0)],
					[sg.Push()]	]

#overarching screen layout
layout = [	[sg.Frame(title=None, layout=dice_window, border_width=0),
			sg.Frame(title='Flat Bonuses', layout=flat_mods,
					element_justification='center',vertical_alignment='top',
					tooltip='Numbers entered here will be added or subtracted\nfrom the final result.'),
			sg.Frame(title=None, layout=results_window, border_width=0, vertical_alignment='top')] 	]

window = sg.Window('MultiRoll', layout, font=('any', 15))

add_mods = ['-ADD1-','-ADD2-','-ADD3-','-ADD4-','-ADD5-','-ADD6-']

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	if event in ('-C_VAL-', '-DICE_NUM-'):
		if not values[event].isnumeric():
			window[event].update(''.join(list(x for x in values[event] if x.isnumeric())))
		if window[event].get() != '':
			if int(window[event].get()) < 1:
				window[event].update(1)
			elif int(window[event].get()) > 1000:
				window[event].update(1000)
	if event in add_mods:
		if values[event] != '':
			val = values[event]
			if values[event][0] == '-':
				first_char = '-'
			else:
				first_char = ''
			if not values[event].isnumeric():
				window[event].update(first_char + (''.join(list(x for x in values[event] if x.isnumeric()))))

	if event == 'Roll':
		if values['-DICE_NUM-'].isdigit():
			if int(values['-DICE_NUM-']) > 1000 or int(values['-DICE_NUM-']) < 1:
				input_error()
			else:
				if not values['-CUSTOM-'] or (values['-CUSTOM-'] and values['-C_VAL-'].isdigit()):
					if values['-CUSTOM-'] and (int(values['-C_VAL-']) > 1000 or int(values['-C_VAL-']) < 1):
						input_error()
					else:
						roll_result, rolled_sides, rolled_num = roll_dice(add_mods)
						if roll_result:
							window['-DETAILS-'].update(disabled=False)
				else:
					input_error()
		else:
			input_error()
	if event == '-DETAILS-':
		analyze_window(roll_result, rolled_sides, rolled_num)
	if event == 'About':
		about_window()



window.close()