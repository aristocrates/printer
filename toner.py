'''A module to check the toner levels at war.caltech.edu
Provided by the gdbimssreps
@author Nicholas Meyer
@date August 9, 2015
'''

from lxml import html
import requests

def text():
    '''@return    the text of war.caltech.edu, None if timed out
    '''
    # for now verify is set to false because we are using a self signed
    # ssl certificate, remove when that is no longer the case
    page = requests.get('https://war.caltech.edu', verify=False)
    return page.text

def tree(text):
    '''@return    html tree
    '''
    return html.fromstring(text)

colormap = {'black':'0', 'cyan':'1', 'magenta':'2', 'yellow':'3', 'fuser':'4'}

def get(color, tree):
    '''@return the ink level left in the color
    '''
    return tree.xpath('//*[@id="SupplyGauge'+colormap[color]+'"]')[0].text_content()

def check(color, tree):
    '''@return True if needs changing
    '''
    level = get(color, tree)
    return int(level[:-1]) < 25

html_tree = tree(text())
print('Black: ' + get('black', html_tree))
print('Black needs changing: ' + str(check('black', html_tree)))
print('Cyan: ' + get('cyan', html_tree))
print('Cyan needs changing: ' + str(check('cyan', html_tree)))
print('Magenta: ' + get('magenta', html_tree))
print('Magenta needs changing: ' + str(check('magenta', html_tree)))
print('Yellow: ' + get('yellow', html_tree))
print('Yellow needs changing: ' + str(check('yellow', html_tree)))
print('Fuser: ' + get('fuser', html_tree))
print('Fuser needs changing: ' + str(check('fuser', html_tree)))
