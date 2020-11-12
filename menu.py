from PyInquirer import prompt
from pprint import pprint

def mainMenu():

    menuOpts = [
        {
            'type': 'list',
            'name': 'Action menu',
            'message': 'Select wanted action',
            'choices': [
                'Cut video',
                'Extract YUV + create Video',
                'Resize video',
                'Change audio codec + mono'

            ]
        },
        {
            'type': 'input',
            'name': 'video file',
            'message': 'Introduce video file path'
        }
    ]

    return prompt(menuOpts)

def sizeMenu():

    menuOpts = [
        {
            'type': 'list',
            'name': 'Resizing size',
            'message': 'Select wanted resizing size',
            'choices': [
                '720p',
                '480p',
                '360x240',
                '160x120'
            ]
        }
    ]

    return prompt(menuOpts)

def codecMenu():

    menuOpts = [
        {
            'type': 'input',
            'name': 'codec',
            'message': 'Introduce the wanted codec'
        }
    ]

    return prompt(menuOpts)