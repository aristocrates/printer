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
    return tree.xpath('//*[@id="SupplyGauge'+colormap[color]+'"]')[0].text_content()

html_tree = tree(text())
print('Black: ' + get('black', html_tree))
print('Cyan: ' + get('cyan', html_tree))
print('Magenta: ' + get('magenta', html_tree))
print('Yellow: ' + get('yellow', html_tree))
print('Fuser: ' + get('fuser', html_tree))
