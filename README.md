# MultiRoll

A versatile dice-rolling utility

Version: 1.0
Date: 12/3/2022

--- Usage Instructions ---

Requirements:
    Python 3.10.4 or greater

Using the program:

Number of Dice:
    Enter the number of dice to roll in this field. The number of dice must be an integer from 1 to 1000.

Number of Sides:
    Select the number of sides per die here. Presets for most common dice types are provided, or use a custom number by selecting "Custom" and typing the number of sides in the input box. The number of sides must be an integer from 1 to 1000.

Flat Bonuses:
    Enter any values to be added or subtracted to the final result in these fields. Which field is used does not matter - 6 fields are provided for convienience. Values in these fields must be a positive or negative integer. All filled fields will be used to adjust the final roll result.

'Roll' Button:
    Provided valid choices for number of dice and sides are entered, rolls XdY, where X is the number of dice, and Y is the number of sides.

'Details' Button:
    After rolling a set of dice, click this button to open the Analysis window for a detailed breakdown of the dice roll.

Individual Results:
    Shows all individual values rolled, unsorted.

Sum of Rolls:
    The first window shows the total value of all dice rolled. The second window shows the total of all entries in the Flat Modifiers window. The third window shows the sum of the dice roll and flat modifiers.

# Analysis Window

Frequency:
    Shows all possible values that could be rolled, and how many times each value appeared. For example,
    #4 | 2 indicates that a value of four occurred two times.

Duplicates:
    If any value occurred two or more times in a roll, those values will be shown here, as well as how many times that value occurred.

Extremes:
    The 'Min Rolls' and 'Max Rolls' fields show the number of dice that rolled a 1 or the highest value on the die, respectively.
