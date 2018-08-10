import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
window = tk.Tk()
window.title("Arlen's Hashcat Tool")
window.geometry("500x190")
#change these paths to match where you keep caps, hccaps and dicts
pcapPath = str('~/hs')
hccapPath = str('~/hccaps')
dictPath = str('~')
homePath = str('~')
def chunk():
	os.system('clear')
pcap = str('x')
hccap = str('x')
dictionary = str('x')

#adjust this to your version of hashcat and path
 
com1 = str(homePath + '/Hashcat/hashcat-4.1.0/hashcat64.bin -m 2500 ')
def option1():
	global pcap
	global hccap
	chunk()
	print('Please run as sudo before beginning')
	print("1. Convert a pcap to hccap")
	print("2. Crack hccap")
	print("3. Exit")
	choice1 = input("What would you like to do: ")
	if choice1 == '1':
		chunk()
		pcap = input("path of your pcap: ")
		hccap = input("path to save hccap (add filename.hccap please): ")
		
		#this assumes you have hashcat util 1.8 installed off your homepath
		
		mycommand=str(homePath + '/hashcat-utils-1.8/bin/cap2hccapx.bin ' + str(pcap) + ' ' + str(hccap))
		os.system(str(mycommand))
		print()
		print("1. yes")
		print("2. no")
		choice2 = input("Crack your new hccap now?: ")
		if choice2 == "1":
			chunk()
			crack(hccap)
		else:
			chunk()
			pass
		option1()
	elif choice1 == '2':
		chunk()
		crack2()
	elif choice1 == '3':
		chunk()
		print('done')
		exit()
def crack2():
	global hccap
	hccap = input("Path to hccap: ")
	chunk()
	dictionary = input("Path to dictionary file: ")
	os.system(str(com1) + str(hccap) + ' ' + str(dictionary) + ' -w 3')
def crack(hccap):
	if hccap != 'x':
		chunk()
		dictionary = input("Path to dictionary file: ")
		mycommand = str(com1) + str(hccap) + ' ' + str(dictionary) + ' -w 3'
		chunk()
		print(mycommand)
		print()
		x = input('start crack')
		os.system(str(mycommand))
	else:
		chunk()
		crack2()
		
		
# BEGIN GUI HERE ----------

# Label Section 1
labelConvert = tk.Label(text="Convert a cap to hccap")
labelConvert.grid(column=0, row=0, sticky="W", columnspan=4)

# Label Cap File
labelCap = tk.Label(text="Cap File")
labelCap.grid(column=0, row=1, sticky="W")

# Entry Cap File
def browse1():
	global hccap
	global pcap
	
	# this path is defaulted if you're using wifite
	
	window.filename =  filedialog.askopenfilename(initialdir = str(pcapPath),title = "Select file",filetypes = (("cap files","*.cap"),("all files","*.*")))
	pcap = str(window.filename)
	print('file: ',pcap, ' loaded')
	
# Browse Cap File BUTTON
buttonCap = tk.Button(text="Source", command=browse1, width=10, bg='black', fg='white')
buttonCap.grid(column=1, row=1, sticky="W")

# Label Hccap File
labelHccap = tk.Label(text="Hccap File")
labelHccap.grid(column=2, row=1, sticky="W")

# Entry Cap File
def browse2():
	global hccap
	global pcap
	
	#This path assumes calls your hccap variable
	
	window.filename =  filedialog.asksaveasfilename(initialdir = str(hccapPath),title = "Select file",filetypes = (("hccap files","*.hccap"),("all files","*.*")))
	hccap = str(window.filename)
	print('file: ',hccap, ' loaded')
	
# Browse Hccap File BUTTON
buttonHccap = tk.Button(text="Destination", command=browse2, width=10, bg='black', fg='white')
buttonHccap.grid(column=3, row=1, sticky="W")

def convert2hccap():
	
	#update this to where you have hashcat-utils
	
	mycommand=str(homePath) + '/hashcat-utils-1.8/bin/cap2hccapx.bin ' + str(pcap) + ' ' + str(hccap)
	os.system('sudo ' + str(mycommand))
	
# Convert to hccap BUTTON
buttonConvert = tk.Button(text="Convert to hccap", command=convert2hccap, width=60, bg='red', fg='white')
buttonConvert.grid(column=0, row=2, sticky="W", columnspan = 4)

# THIS IS THE SECTION FOR HASHCAT
# YOU NEED TO HAVE A VALID HCCAP BEFORE USING THIS SECTION

# ----------------------------------------------------------------------
# Label Section 2
labelHack = tk.Label(text="Convert a cap to hccap")
labelHack.grid(column=0, row=3, sticky="W", columnspan = 4)

# Label Hccap File
labelHccap2 = tk.Label(text="Hccap File")
labelHccap2.grid(column=0, row=4, sticky="W")

# Entry Cap File
def browse3():
	global hccap
	global pcap
	
	#this calls on your hccap location variable
	
	window.filename =  filedialog.askopenfilename(initialdir = str(hccapPath), title = "Select file",filetypes = (("hccap files","*.hccap"),("all files","*.*")))
	hccap = str(window.filename)
	print('file: ',hccap, ' loaded')
	
# Browse Hccap File BUTTON
buttonHccap2 = tk.Button(text="Source", command=browse3, width=10, bg='black', fg='white')
buttonHccap2.grid(column=1, row=4, sticky="W")

# Label Dictionary File
labelDictionary = tk.Label(text="Dictionary File")
labelDictionary.grid(column=2, row=4, sticky="W")

# Entry Dictionary File
def browse4():
	global dictionary
	
	#this calls your dictionary location variable
	
	window.filename =  filedialog.askopenfilename(initialdir = str(dictPath),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
	dictionary = str(window.filename)
	print('file: ',dictionary, ' loaded')
	
# Browse Dictionary File BUTTON
buttonDictionary = tk.Button(text="Locate", command=browse4, width=10, bg='black', fg='white')
buttonDictionary.grid(column=3, row=4, sticky="W")

def hashcat():
	mycommand = str(com1) + str(hccap) + ' ' + str(dictionary) + ' -w 3'
	os.system('sudo ' + str(mycommand))
	
# Hashcat Go BUTTON
buttonHashcat = tk.Button(text="Crack Hash", command=hashcat, width=60, bg='red', fg='white')
buttonHashcat.grid(column=0, row=5, sticky="W", columnspan=4)

def hashcatShow():
	if hccap == 'x':
		print("You need to load a cracked hccap first")
	else:
		pass
	mycommand = str(com1) + str(hccap) + ' --show'
	os.system('sudo ' + str(mycommand))

# Hashcat Show BUTTON
buttonShow = tk.Button(text="Show Known", command=hashcatShow, width=60, bg='black', fg='white')
buttonShow.grid(column=0, row=6, sticky="W", columnspan=4)

# Terminal Window Embed --------------coming soon
#termf = Frame(window, height=480, width=100)

#termf.grid(column=0,row=7, sticky="W", columnspan=4)
#wid = termf.winfo_id()
#os.system('xterm -into %d -geometry 100x450 -sb  &' % wid)

#-- begin program   
window.mainloop()
