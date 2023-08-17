import PySimpleGUI as sg 
from random import randint

sg.theme('DarkAmber')
roll_result = None
rolled_sides = None
rolled_num = None
max_size = 1000
FONT_MAIN = ('any', 12)
FONT_WINDOW = ('any', 15)
MIN_VALUE = 1

def calculate_roll(modifiers):
	'''Using the values set in the "Number of Dice" and
	"Number of Sides" windows, rolls (dice) quantity of
	(sides)-sided dice. Any modifiers that were entered
	in the "Flat Bonuses" windows will be totaled as well.

	The modifiers argument should be a list containing the
	keys for all InputText elements in the "Flat Bonuses"
	frame.

	If invalid integers are passed into any of these fields,
	or if values above max_size or lower than 1 are entered for
	the number of dice or sides, they will default to None
	values.

	If invalid values are present for the number of dice or
	sides, no processing of random values will occur.'''
	if not values['NUM_DICE']:
		return None
	dice_arr = []
	num_dice = None
	dice_sides = None
	total_mod = 0

	if values['NUM_DICE']:
		if values['NUM_DICE'].isdigit():
			try:
				num_dice = int(values['NUM_DICE']) #check if the number of dice is a valid int
			except ValueError:
				num_dice = None
			if num_dice > max_size or num_dice<1:
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
			elif values['CUSTOM']:
				if values['CUSTOM_VAL']:
					if values['CUSTOM_VAL'].isdigit(): #check if the number of sides is a valid int
						dice_sides = int(values['CUSTOM_VAL'])
						if dice_sides > max_size or dice_sides<1:
							dice_sides = None
	if num_dice and dice_sides:
		while num_dice > 0:
			dice_arr.append(randint(1, dice_sides)) #iterate through dice and roll values for each
			num_dice -= 1
		window['INDIV_RESULTS'].update(' '.join([str(x) for x in dice_arr])) #generate a string containing all individual dice
		window['SUM'].update(sum(dice_arr)) #take the sum of all individual dice rolls

		#apply modifiers
		if modifiers:
			for val in modifiers:
				try:
					total_mod += int(values[val])
				except ValueError:
					pass
			window['MODS'].update(total_mod)
			window['TOTAL'].update(sum(dice_arr)+total_mod)


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
	window limits user values to a maximum of max_size dice with max_size
	sides each.'''
	frequency_graph = ''
	dupes_graph = ''
	min_counter = 0
	max_counter = 0

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
	frequency_chart = [	[sg.Multiline(default_text=frequency_graph, size=(20,5), disabled=True, key='FREQUENCY', tooltip='The number of dice that rolled each\nof the possible results.\nShown as RESULT | FREQUENCY')]	]

	#window for displaying any duplicate values and how many of each duplicate were rolled
	duplicates = [	[sg.Multiline(default_text=dupes_graph, size=(20,5), disabled=True, key='DUPLICATES', tooltip='The number of dice with identical results.\nShown as RESULT | FREQUENCY')]	]

	#window for displaying how many dice rolled a 1 or maximum value
	mins_maxes = [	[sg.Text('Min Rolls: ', tooltip='The number of dice that rolled a 1')],
					[sg.Text(min_counter, key='MINS')],
					[sg.Text('Max Rolls:', tooltip='The number of dice that rolled the maximum value')],
					[sg.Text(max_counter, key='MAXES')]	]

	#overall layout for the analysis window
	layout = [	[sg.Frame(title='Frequency', layout=frequency_chart), sg.Frame(title='Duplicates', layout=duplicates), sg.Frame(title='Extremes', layout=mins_maxes)],
				[sg.Button('Back')]	]

	window = sg.Window('Detailed Analysis', layout, font=FONT_WINDOW, modal=True)



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

	window = sg.Window('About', layout, font=FONT_WINDOW, modal=True, element_justification='center')

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'OK'):
			break

	window.close()

# def settings_window(max_size_amt = max_size):
# 	global max_size
# 	max_val_tt = 'Set the maximum value of dice/sides.\nWARNING: Extremely large values may adversely affect performance!'
# 	layout = [[sg.Text('Maximum Value', font = FONT_MAIN, tooltip=max_val_tt), sg.Multiline(default_text=max_size_amt, size=(10,0), no_scrollbar=True, key='NEW_MAX')],
# 	   		 [sg.OK(), sg.Cancel()]]
	
# 	window = sg.Window('Settings', layout, font=FONT_WINDOW, modal=True, element_justification='center')

# 	while True:
# 		event,_ = window.read()
# 		if event in (sg.WIN_CLOSED, 'Cancel'):
# 			break
# 		if event == 'OK':
# 			max_size = int(max_size_amt)
# 			break
# 	window.close()
	

def input_error():
	'''Simple window that is displayed when the user inputs
	an invalid entry for the number of dice or sides.'''
	layout =[	[sg.Text(f'The number of dice/sides must be a positive\nnumber between 1 and {max_size}!')],
				[sg.OK()]	]

	window = sg.Window('Error', layout, modal=True, element_justification='center', font=FONT_WINDOW)

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'OK'):
			break

	window.close()

def roll_dice():
	roll_result, rolled_sides, rolled_num = calculate_roll(add_mods)
	if roll_result:
		window['DETAILS'].update(disabled=False)
	return roll_result, rolled_sides, rolled_num


def validate_numeric_input(input_value, allow_negative = False, min_output = MIN_VALUE):
	if input_value == '':
		return min_output
	first_char = ''
	if allow_negative:
		if input_value[0] == '-':
			first_char = '-'
	if not input_value.isnumeric():
		input_value = (''.join(list(x for x in input_value if x.isnumeric())))
	return first_char + input_value

def validate_numeric_range(input_value):
	if input_value == '':
		return MIN_VALUE
	input_value = int(input_value)
	if input_value < 1:
		input_value = 1
	elif input_value > max_size:
		input_value = max_size
	return input_value

def full_validation(val_to_validate):
	val_to_validate = validate_numeric_input(val_to_validate)
	val_to_validate = validate_numeric_range(val_to_validate)
	return val_to_validate

#selection window for the number of sides per dice
dice_select = [[sg.Radio('4', 'DICE', default=True, key='-4-'), sg.Radio('6','DICE', pad=(15,0), key='-6-')],
			[sg.Radio('8','DICE', key='-8-'), sg.Radio('10','DICE',pad=(15,0), key='-10-')],
			[sg.Radio('20','DICE', key='-20-'), sg.Radio('100','DICE',pad=(4,0), key='-100-')],
			[sg.Radio('Custom','DICE', key='CUSTOM'), sg.InputText('1', size=6, tooltip=f'Maximum of {max_size}', key='CUSTOM_VAL', enable_events=True)]	]

#selection window for the number of dice to roll
num_dice = [	[sg.InputText(size=8, tooltip=f'Maximum of {max_size}', key='NUM_DICE', enable_events=True)]	]

#organizational frame for the dice sides and quantity windows
dice_window = [	[sg.Frame(title='Number of dice', layout = num_dice, size=(190, 60), element_justification='center')],
			[sg.Frame(title='Number of sides', layout=dice_select, size=(190,180))], 
			[sg.Button(button_text='Roll',font=FONT_MAIN, tooltip='Roll the currently set dice', key='ROLL'),
			sg.Button(button_text='Details',font=FONT_MAIN, disabled=True, tooltip='View details about the roll such as frequency and duplicates', key='DETAILS'),
			sg.Button(button_text='About',font=FONT_MAIN, key='ABOUT')]]
			# sg.Button(button_text='Setttings', font=FONT_MAIN, key='SETTINGS')]	]

#window for displaying list of all individual dice
indv_results = [	[sg.Multiline(default_text='', tooltip='A list of all individual dice rolls',size=(28,5), disabled=True, key='INDIV_RESULTS')]	]

#window for displaying the total of the dice roll, including modifiers
sum_results = [	[sg.Multiline(default_text='',tooltip='The sum of all dice rolled before modifiers', size=(7,1), disabled=True, no_scrollbar=True, key='SUM'),
				sg.Text('+/-'),
				sg.Multiline(default_text='',tooltip='The total of all modifiers entered under\'Flat Bonuses\'', size=(7,1), disabled=True, no_scrollbar=True, key='MODS'),
				sg.Text('='),
				sg.Multiline(default_text='',tooltip='The total of the dice roll + all modifiers', size=(7,1), disabled=True, no_scrollbar=True, key='TOTAL')]	]

#window for entering flat increases or decreases to be added to the dice roll
flat_mods = [	[sg.InputText(size=8, pad=(0,5), key='ADD1', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='ADD2', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='ADD3', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='ADD4', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='ADD5', enable_events=True)],
				[sg.InputText(size=8, pad=(0,5), key='ADD6', enable_events=True)]	]

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

window = sg.Window('MultiRoll', layout, font=FONT_WINDOW)

add_mods = ['ADD1','ADD2','ADD3','ADD4','ADD5','ADD6']



while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	if event in ('CUSTOM_VAL', 'NUM_DICE'):
		window[event].update(full_validation(values[event]))
	if event in add_mods:
		window[event].update(validate_numeric_input(values[event], True, 0))
	if event == 'ROLL':
		roll_result, rolled_sides, rolled_num = roll_dice()
	if event == 'DETAILS':
		analyze_window(roll_result, rolled_sides, rolled_num)
	# if event == 'SETTINGS':
	# 	settings_window()
	if event == 'ABOUT':
		about_window()



window.close()