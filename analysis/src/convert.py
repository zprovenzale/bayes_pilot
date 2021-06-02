#!usr/bin/python
#encoding: utf-8

import json
import csv
import sys
import math

######### Functions
def filterDebug( arr ):
	return [elem for elem in arr if elem.has_key('workerId') and elem['workerId'] != 'debug']

def filterIncomplete( arr ):
	return [elem for elem in arr if elem.has_key("time_end_experiment")]

def filterNames ( arr, name_list ):
	return [elem for elem in arr if elem.has_key('workerId') and elem['workerId'] in name_list]
	
def filterTasks ( arr, tasks ):
	return [elem for elem in arr if elem.has_key('taskType') and elem['taskType'] in tasks]

def mean(numbers):
	return float(sum(numbers)) / max(len(numbers), 1)

def median(thelist):
    sorted_list = sorted(thelist)
    length = len(sorted_list)
    center = length // 2

    if length == 1:
        return sorted_list[0]

    elif length % 2 == 0:
        return sum(sorted_list[center - 1: center + 1]) / 2.0

    else:
        return sorted_list[center]


def calculateBonus( user ):
	user['_bonus'] = 0

	if user.has_key("time_end_experiment"):

		# +1 bonus points are possible for completing section I task (you start off with $1 as base)
		# +3 bonus points are possible for attempting/completing the section II surveys
		# if user attempts spatial test and gets over 1 correct, receives +1 bonus
		# if user.has_key('task0'): 
		# 	user['_bonus'] += 1;
		# else:
		# 	pass
		
		if user.has_key('task1'): 
			user['_bonus'] += 1;
		else:
			pass

		if (user['spatial_numCorrect'] > 1): 
			user['_bonus'] += 1;
		
		# if user completes personality test, receives +1 bonus
		if user.has_key("pers-attPassed"):	
			if (user['pers-attPassed'] == 'true'):
 				user['_bonus'] += 1;
		else:
			pass

		# if user attempts numeracy test and gets over 1 correct, receives +1 bonus
		if (user['numeracy_numCorrect'] > 1): 
			user['_bonus'] += 1;

def calculateSpatial( user ):
	blank_count = 0
	correct_count = 0
	incorrect_count = 0
	file_path = "../../public/modules/data/spatial-answers.json"
	
	json_data = open(file_path)
	answers = json.load(json_data)['answers']

	for i in range(1, 21):
		if( user.has_key("spatial_" + str(i)) ):
			if(user["spatial_" + str(i)] == answers[str(i)]):
				correct_count += 1
			else:
				incorrect_count += 1
		else:
			blank_count += 1
	
	
	user["spatial_numCorrect"] = correct_count
	user["spatial_score"] = correct_count - (incorrect_count / 4.0);


def calculateNumeracy( user ):
	blank_count = 0
	correct_count = 0
	incorrect_count = 0
	file_path = "../../public/modules/data/numeracy-answers.json"
	
	json_data = open(file_path)
	answers = json.load(json_data)['answers']

	for i in range(1, 21):
		if( user.has_key("numeracy_" + str(i)) ):
			if(user["numeracy_" + str(i)] == answers[str(i)]):
				correct_count += 1
			else:
				incorrect_count += 1
		else:
			blank_count += 1
	
	user["numeracy_numCorrect"] = correct_count
	user["numeracy_score"] = correct_count - (incorrect_count / 4.0);

def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def calculateTaskInputs( user ):

	for i in range(0, 25):
		task_data = json.loads( user['sheet'+ str(i)])

		p = float(task_data['p'])
		x1 = float(task_data['x1'])
		x2 = float(task_data['x2'])
		payments = task_data['payments']
		choice = task_data['lotterychoice']
	

		user['condition'] = task_data['condition']
		user['vis'] = vis_id(task_data['condition'])
		user['sheet' + str(i) + '_p'] = p
		
		
		if not(user['condition'] == 'none'):
			user['sheet' + str(i) + '_prob1'] = float(task_data['prob1'])/100
			user['sheet' + str(i) + '_prob2'] = float(task_data['prob2'])/100
		else: 
			user['sheet' + str(i) + '_prob1'] = p
			user['sheet' + str(i) + '_prob2'] = 1 - p

		user['sheet' + str(i) + '_lotterychoice'] = task_data['lotterychoice']
		user['sheet' + str(i) + '_x1'] = x1
		user['sheet' + str(i) + '_x2'] = x2
		user['sheet' + str(i) + '_payments'] = task_data['payments']
		

		
		#error
		lnerror = math.log(user['sheet' + str(i) + '_prob1'] / p) 
		error = user['sheet' + str(i) + '_prob1'] / p
		

		#expected value
		ev = (p * x1) + ( (1-p) * x2 )
		_ev = (user['sheet' + str(i) + '_prob1'] * x1) + ( (1-user['sheet' + str(i) + '_prob1']) * x2 )

		
		#certainty equivalent
		row = int(choice[0:len(choice)-1])
		col = choice[len(choice)-1]
		ce = 0

		if col == 'a' and row > 0:
			ce = (payments[row] + payments[row -1]) / 2
		elif col == 'b' and row < len(payments) -1:
			ce = (payments[row] + payments[row + 1]) / 2
		else:
			ce = payments[row]

		#relative risk premia
		rrp = (ev-ce)/abs(ev)
		_rrp = (_ev - ce) / abs(_ev)
		

		user['sheet' + str(i) + '_ev'] = ev
		user['sheet' + str(i) + '_ce'] = ce
		user['sheet' + str(i) + '_rrp'] = rrp
		user['sheet' + str(i) + '_error'] = error
		user['sheet' + str(i) + '_lnerror'] = lnerror
		user['sheet' + str(i) + '_ev_perceived'] = _ev
		user['sheet' + str(i) + '_rrp_perceived'] = _rrp

		if(p == user['sheet' + str(i) + '_prob1']):
			user['sheet' + str(i) + '_exact'] = 1
		else: 
			user['sheet' + str(i) + '_exact'] = 0



def vis_id(vis):
	if (vis == 'none'):
		return 0
	elif (vis == 'icon'):
		return 1
	elif (vis == 'pie'):
		return 2
	elif (vis == 'circle'):
		return 3
	elif (vis == 'triangle'):
		return 4
	elif (vis == 'bar'):
		return 5 


		
def addDefault(user, fields):
	for f in fields:
		if (not user.has_key(f)):
			user[f] = '-'
		
########## Main
in_file = '../results/data.json'

fields = [ # EDIT THESE
      'postId', 
	  'time_diff_experiment', 
	  'condition',
	  'vis',
	  'bonus',
	  'age',
	  'gender',
	  'education'
	]


json_data = open(in_file)
data = json.load(json_data)

# filter
data = filterIncomplete( data )
visualizations = ['icon', 'pie', 'circle', 'triangle', 'bar', 'none']

perceptions = {}
for vis in visualizations:
	perceptions[vis] = {}
	for d in [.05, .1, .25, .5, .75, .9, .95]:
		perceptions[vis][d] = []



for user in data:
	addDefault(user, fields) # add default for missing values
	calculateTaskInputs(user)

for user in data:
	for i in range(0, 25):
		perceptions[user['condition']][user['sheet' + str(i) + '_p']].append(user['sheet' + str(i) + '_rrp_perceived'])

# print perceptions


for vis in ['icon', 'pie', 'circle', 'triangle', 'bar', 'none']:
	print
	print vis
	for d in [.05, .1, .25, .5, .75, .9, .95]:
		print(str(median(perceptions[vis][d])) + ', ' ), 
# 		print(vis)
#  		print("Average Errors")
# 		print (perceptions[vis][d])

# for vis, i in enumerate(perceptions):
# 	val = perceptions[i]
# 	print(vis)
# 	print(val)
# 	for perc, j in enumerate(val):
# 		errors = perc[j]
# 		print(vis)
# 		print(val)
# 		print("Average Errors")
# 		print(str(perc) +  " : " + str(mean(errors) ))




out_file = in_file.replace('.json', '.csv')
print('Coverting from json to csv. File written to ' + out_file)




sheetkeys = ['p', 'prob1', 'prob2', 'x1', 'x2', 'lotterychoice', 'ev', 'ce', 'rrp', 'error', 'lnerror', 'exact', 'ev_perceived', 'rrp_perceived']
output = csv.writer(open(out_file, "w")) # delimiter='\t'
output.writerow(fields + sheetkeys)


# for user in data:
# 	output.writerow([user[key] for key in fields if key in user])


#between
for user in data:
	for i in range(0, 25):
		output.writerow([user[key] for key in fields if key in user] +
			 [user['sheet'+ str(i) + '_' + key] for key in sheetkeys])



		
	
