'''A module to check the toner levels at war.caltech.edu
Provided by the gdbimssreps
@author Nicholas Meyer
@date August 9, 2015
'''
import sys
from lxml import html
import requests

def text():
    '''@return    the text of war.caltech.edu, None if timed out
    '''
    # for now verify is set to false because we are using a self signed
    # ssl certificate, remove when that is no longer the case
    # also for now warnings are suppressed
    import warnings
    warnings.filterwarnings("ignore")
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

def check(color, threshold, tree):
    '''@return True if needs changing
    '''
    level = get(color, tree)
    return int(level[:-1]) < threshold

def check_all(tree, threshold=10):
    '''@return tuple (action_needed, message)
                     action_needed: boolean
                     message: string
    '''
    ans = False
    message = ""
    check_list = ['black', 'cyan', 'magenta', 'yellow', 'fuser']
    for i in check_list:
        if (check(i, threshold, tree)):
            ans = True
            message += "%s needs changing (%s), " % (i, get(i, tree))
    return (ans, message)

def status(tree):
    '''@return a string of the status of all toner levels
    '''
    ans = "Ink levels:\n"
    check_list = ['black', 'cyan', 'magenta', 'yellow', 'fuser']
    for i in check_list:
        ans += i + ": " + get(i, tree) + "\n"
    return ans

def usage():
    '''@return a usage statement in string representation
    '''
    return "Usage: python toner.py [status|check] [threshold]"
    
if __name__ == "__main__":
    # Usage: python toner.py [status|check] [threshold]
    if (len(sys.argv) >= 2 and sys.argv[1] == "status") \
       or (len(sys.argv) >= 3 and sys.argv[1] == "check"):
        try:
            html_tree = tree(text())
            if sys.argv[1] == "status":
                print(status(html_tree))
            elif sys.argv[1] == "check":
                result = check_all(html_tree, threshold=int(sys.argv[2]))
                if result[0]:
                    print("Hi IMSS reps,\n\n%s\n\nLove,\nNickbot" % result[1])
        except ConnectionError:
            print("Hi IMSS reps,\n\nWar isn't responding, someone should turn it on or restart it.\n\nLove,\nNickbot")
    else:
        print(usage())
