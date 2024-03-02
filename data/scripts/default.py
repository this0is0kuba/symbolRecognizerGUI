import webbrowser
from sys import platform

url = 'https://github.com/this0is0kuba/symbolRecognizerGUI'

if platform == "win32":
    directory = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

elif platform == "darwin":
    directory = 'open -a /Applications/Google\ Chrome.app %s'

elif platform == "linux":
    directory = '/usr/bin/google-chrome %s'

webbrowser.get(directory).open(url)


