from Tkinter import *
import datetime
import time as t
import subprocess
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np


#starttime = '14:00'
#person = 'Lis'

if not ('guesses.txt' in os.listdir('.')):
	open('guesses.txt','w').close()

if ('details.txt' in os.listdir('.')):
	with open('details.txt','r') as f:
		temp = f.readline().rstrip()
		starttime = temp
		person = f.readline()
else:
	with open('details.txt','w') as f:
		starttime = raw_input('Type viva start time (HH:MM): ')
		person = raw_input('Type who is taking the viva: ')
		f.write(str(starttime)+'\n'+str(person))
				
				
##### Window Setup
root = Tk()
root.title('Viva Extravaganza')
root.attributes('-fullscreen', True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

############## Main Title
if list(person)[-1] == 's' or list(person)[-1] == 'S':
	titext = "' Viva Party"
else:
	titext = "'s Viva Party"
vname = Label(root, text=person + titext, font=(None, 40), width=screen_width, bg='#daa520') 
vname.place(x=screen_width*0.5, y=screen_height*0.03, anchor='center')


############## Rules
rulestext = 'Rules: One guess per person, closest non-exceeded time wins.'
rules = Label(root, text=rulestext, font=(None, 18), width=screen_width, fg='black') 
rules.place(x=screen_width*0.5, y=screen_height*0.89, anchor='center')

############## Table of Guesses
starthour, startminute = starttime.split(':')

hours = range(int(starthour), int(starthour)+6)
mins_list = range(0, 60, 5)
diffs = [abs(int(startminute)-mins) for mins in mins_list]

shift = diffs.index(min(diffs))
mins_list = mins_list[shift:]+mins_list[:shift]
mins = mins_list

times = []
for h in hours:
	for m in mins:
		if m == 0:
			m = '00'
		if m == 5:
			m = '05'
		times.append(str(h)+':'+str(m))

usedtimes = []
label_array = []   
height = 12
width = 5*2
count = 0
for i in range(width): #columns
	for j in range(height): #rows
		if i % 2 == 0:
			curr_time = str(times[count])
			b = Label(root, text=curr_time, font=(None, 20), height=2, bg='lightsteelblue')
			xpos = i * screen_width * 0.08
			ypos = j * screen_height * 0.05
			b.place(x=xpos+screen_width*0.115, y=ypos+screen_height*0.3, anchor='center')
			usedtimes.append(curr_time)
			count += 1
		else:
			c = Label(root, text='', font=(None, 20), width=20, height=2, bg='lightgrey')
			xpos = i * screen_width * 0.08
			ypos = j * screen_height * 0.05
			c.place(x=xpos+screen_width*0.115, y=ypos+screen_height*0.3, anchor='center')
			label_array.append(c)

############# Load Saved Guesses
guessers, guessers_raw, guessed_times = [], [], []

with open('guesses.txt', 'r') as f:
	data = f.read()
	guesses = data.split('\n')
	for guess in guesses:
		try:
			name, time = guess.split(',')
		except ValueError:
			continue
		try:
			time_ind = usedtimes.index(time)
		except ValueError:
			continue
		label_array[time_ind].config(text=name)
		
		guessers_raw.append(name)
		guessers.append(name.replace(" ", ""))
		guessed_times.append(time)

label_array[0].config(text='Start Time', bg='#daa520')

def endprogram():
	with open('details.txt','r') as f:
		f.readline()
		person = f.readline()
	os.rename('guesses.txt', person+'_guesses.txt')
	os.remove('details.txt')
	exit()

def printprogram(lth, ltm, usedtimes, guessers_raw, guessed_times):
	with open('details.txt','r') as f:
		f.readline()
		person = f.readline()
	printed = False
	if printed != True:
		with open('vivaparty_printout.tex', 'w') as g:
			g.write('\documentclass{article}' + '\n')
			g.write('\usepackage[utf8]{inputenc}' + '\n')
			g.write('\pagestyle{empty}' + '\n')
			g.write('\\addtolength{\oddsidemargin}{-1.7in}' + '\n')
			g.write('\\addtolength{\evensidemargin}{-1.7in}' + '\n')
			g.write('\\addtolength{\\textwidth}{3.4in}' + '\n')
			g.write('\\begin{document}' + '\n')
			g.write('\\begin{center}' + '\n')
			g.write('\Huge{CONGRATULATIONS}' + '\n')
			g.write('\\vspace{10mm}' + '\n')
			g.write('\n')
			g.write('\huge{{{}}}'.format(person) + '\n')
			g.write('\n')
			g.write('\\vspace{15mm}' + '\n')
			g.write('\LARGE{{Viva completed at: {}:{}}}'.format(lth, ltm) + '\n')
			g.write('\n')			
			g.write('\\vspace{15mm}' + '\n')
			g.write('\Large{}' + '\n')
			g.write('\\begin{tabular}{l c@{\hskip 10mm} l c@{\hskip 10mm} c l}' + '\n')
			for i in range(len(usedtimes)/3):
				name1 = ""
				name2 = ""
				name3 = ""
				time1 = usedtimes[i]
				time2 = usedtimes[i+len(usedtimes)/3]
				time3 = usedtimes[i+(len(usedtimes)*2)/3]

				if i == 0:
					name1 = 'Start'

				if time1 in guessed_times:
					index = guessed_times.index(time1)
					print guessers_raw
					name1 = guessers_raw[index]
				if time2 in guessed_times:
					index = guessed_times.index(time2)
					name2 = guessers_raw[index]
				if time3 in guessed_times:
					index = guessed_times.index(time3)
					name3 = guessers_raw[index]

				g.write('{} & {} & {} & {} & {} & {}  \\\\ \n'.format(name1, time1, name2, time2, name3, time3))

			g.write('\end{tabular}' + '\n')
			g.write('\end{center}' + '\n')
			g.write('\end{document}')

		os.system("pdflatex vivaparty_printout.tex")
		os.system("lpr -P HP_LaserJet_P4015__4th_Floor_ vivaparty_printout.pdf")
	return

############# Guess Entry and Update
def save_guess_and_update(usedtimes, guessed_times, warning):
	name = nameentry.get()
	time = timeentry.get()

	##### Input Checks ######
	if name == '':
		warning.config(text='A girl has no name.', fg='red')
		return
	if time == '':
		warning.config(text='You have a lovely name, but when will they finish?', fg='red')
		return 
	if not all(s.isalnum() or s.isspace() for s in name):
		warning.config(text='You have a strange name...', fg='red')
		return
	if len(name) > 12:
		warning.config(text='Your name is too long, shrink it!')
		return
	if time in guessed_times:
		warning.config(text='That time has already been guessed!', fg='red')
		return
	if name.replace(" ", "") in guessers:
		warning.config(text="You've already had one guess!", fg='red')
		return
	if time == usedtimes[0]:
		warning.config(text="That's the start of the viva!", fg='red')
		return
	try:
		time_ind = usedtimes.index(time)
	except ValueError:
		warning.config(text="That isn't a valid time!", fg='red')
		return 
	livetime = datetime.datetime.now().strftime("%H:%M")
	h, m = time.split(":")
	lh, lm = livetime.split(":")
	if h <= lh and m <= lm:
		warning.config(text='Your stupidity is impressive.', fg='red')
		return
	
	##### Save Guess #####
	warning.config(text='What time will '+person+' finish?', fg='black')
	with open('guesses.txt', 'a') as f:
		f.write(name + ',' + time + '\n')

	label_array[time_ind].config(text=name)
	guessers_raw.append(name)
	guessers.append(name.replace(" ", ""))
	guessed_times.append(time)

nname = Label(root, text="Name:", font=(None, 18))
nname.place(x=screen_width*0.625, y=screen_height*0.135, anchor='center')
nameentry = Entry(root)
nameentry.place(x=screen_width*0.70, y=screen_height*0.135, anchor='center')
tname = Label(root, text="Guess:", font=(None, 18))
tname.place(x=screen_width*0.625, y=screen_height*0.165, anchor='center')
timeentry = Entry(root)
timeentry.place(x=screen_width*0.70, y=screen_height*0.165, anchor='center')

entrybutton = Button(root, text='Add Guess', command=lambda: save_guess_and_update(usedtimes, guessed_times, warning), font=(None, 18), height=2, width=15, fg='black')
entrybutton.place(x=screen_width*0.82, y=screen_height*0.15, anchor='center')

warning = Label(root, font=(None, 24), fg='black', text='What time will '+person+' finish?')
warning.place(x=screen_width*0.73, y=screen_height*0.22, anchor='center')
		
######### Live Winner and Clock
winner = Label(root, font=(None, 40))
winner.place(x=screen_width*0.40, y=screen_height*0.15, anchor='center')
clock = Label(root, font=(None, 40))
clock.place(x=screen_width*0.20, y=screen_height*0.15, anchor='center')
sstopbutton = Button(root, font=(None, 18), bg='red', fg='white')
sstopbutton.place(x=screen_width*0.20, y=screen_height*0.22, anchor='center')

printed = False
playing = False
number = 0
def whoswinning(usedtimes, endbutton=0, printbutton=0):
	global playing,number
	number += 1
	if (number >= 1000):
		number = 0
	colourline = np.linspace(0,1,1000)

	if printbutton != 0:
		printbutton.destroy()
	if endbutton != 0:
		endbutton.destroy()

	cmap = plt.cm.get_cmap('gnuplot')
	rgba = 255.*np.asarray(cmap(colourline[number]))
	colour = '#%02x%02x%02x' % (rgba[1],rgba[2],rgba[3])
	#root.configure(background=colour)
	t1 = t.time()
	livetime = datetime.datetime.now().strftime("%H:%M")
	clocktime = datetime.datetime.now().strftime("%H:%M:%S")
	clock.config(text=clocktime)
	names = []
	gtimes = []
	with open('guesses.txt', 'r') as f:
		data = f.read()
		guesses = data.split('\n')
		for guess in guesses:
			try:
				name, gtime = guess.split(',')
				names.append(name)
				gtimes.append(gtime)
			except ValueError:
				continue
		
	poss_winners, proxs = [], []
	lth, ltm = livetime.split(':')
	for gtime in gtimes:
		tth, ttm = gtime.split(':')

		prox = (int(tth)-int(lth))*60
		prox += int(ttm)-int(ltm)-1 
		
		try:
			time_ind = usedtimes.index(gtime)
		except ValueError:
			continue
		if prox >=0:
			poss_winners.append(gtime)
			proxs.append(abs(prox))
			label_array[time_ind].config(bg='powderblue')
		else:
			label_array[time_ind].config(bg='tomato')

	if poss_winners == []:
		curr_winner = 'Make a guess!'
	else:
		twinner = poss_winners[proxs.index(min(proxs))]
		time_ind = usedtimes.index(twinner)
		label_array[time_ind].config(bg='chartreuse3')

		curr_winner = names[gtimes.index(twinner)]

		if min(proxs) == 0:
			if int(clocktime.split(':')[2]) > 29:
				clock.config(fg='red')

			if int(clocktime.split(':')[2]) > 25:
				if playing == False:
					subprocess.Popen(['afplay', 'countdown.mp3'])
					playing = True

			if int(clocktime.split(':')[2]) > 0 and int(clocktime.split(':')[2]) < 1:
				playing = False

		else:
			clock.config(fg='black')

	winner.config(text=curr_winner, fg='Black')#, bg='white')
	t2 = t.time()

	def stopprogram(usedtimes, job):
		root.after_cancel(job)
		sstopbutton.configure(text='RESTART', command=lambda: whoswinning(usedtimes,endbutton,printbutton))
		winner.config(fg='chartreuse3')
		endbutton = Button(root, font=(None, 18), bg='red', fg='white')
		endbutton.place(x=screen_width*0.35, y=screen_height*0.22, anchor='center')
		endbutton.configure(text='END VIVA PARTY', command=lambda: endprogram())

		printbutton = Button(root, font=(None, 18), bg='red', fg='white')
		printbutton.place(x=screen_width*0.45, y=screen_height*0.22, anchor='center')
		printbutton.configure(text='PRINT', command=lambda: printprogram(lth, ltm, usedtimes, guessers_raw, guessed_times))
				
	job = root.after(50, lambda: whoswinning(usedtimes))
	sstopbutton.configure(text='STOP', command=lambda: stopprogram(usedtimes, job))
		
whoswinning(usedtimes)
root.mainloop()



