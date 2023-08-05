"""
This is Command line tool for recognizing most Common colors in any given image
"""
#import argparse
from colours_library import colours
from webcolors import name_to_rgb

BREAKLINE = '----------------------------------'
def recognizer(if_rgb):
    """
    Main function in this module
    """
    to_rgb = if_rgb
    while True:
        try:
            #retrieving path and count input
            path = input('Add path to the image. \nIf u want to quit type q\n')
            if path == 'q':
                break
            numb = input('How many most frequent colors? ')
            print(BREAKLINE)
            #producing output
            mcc = colours.MostCommonColor(path, int(numb))
            output = mcc.produce()
            output_colors(output, to_rgb)
            #prompt if user wants to repeat
            repeat = input('Do you want to repeat?\ny for yes \\ anything else for no ')
            if repeat == 'y':
                print('Let\'s go')
                print(BREAKLINE)
            else:
                break
        except FileNotFoundError:
            print('Seems like no such file exists ;/')
            print('try again')
            print(BREAKLINE)
        except TypeError:
            print('I work with jpg files only.')
            print('try again')
            print(BREAKLINE)
        except ValueError:
            print('No support for this color count.')
            print('try again')
            print(BREAKLINE)

def output_colors(col_arr, to_rg):
    """
    Function improves output of color array
    """
    for col in col_arr:
        if to_rg:
            print(name_to_rgb(col))
        else:
            print(col)
