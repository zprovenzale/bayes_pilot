#!/usr/bin/python
##Reads in a csv file and outputs a list of commands to pay bonuses



import csv
import subprocess
import os


file_bonus = '../results/data.csv' #### CHANGE
file_mturk = '../results/Batch_3578918_batch_results.csv'
setup_cmd = '/Users/alvitta/aws-mturk-clt-1.3.4/bin/setUp.sh'


bonuses = {}
ids = []
bns = []
for row in csv.DictReader(open(file_bonus, 'rU'), delimiter=','):
	ids.append( row['postId'].strip().lower() )
	bns.append( row['bonus'] )

bonuses = dict(zip(ids, bns))
# print bonuses


data_mturk = []
for row in csv.DictReader(open(file_mturk, 'rU'), delimiter=','):
	data_mturk.append(row)
	
#step env variables for mturk
os.system('. ' + setup_cmd)

total_bonus = 0	
outfile = open('payBonuses.sh', 'w')
outfile.write('#!/bin/bash\n\n')
count = 0

for worker in data_mturk:
	workerid = worker['WorkerId']
	postid = worker['Answer.surveycode']

	if postid == 'A3D70ANCSMGX5F':
		postid = 'jtkg1rhx'

	if postid not in bonuses:
		print workerid + " not found. ID: " + worker["Answer.surveycode"]
 	elif bonuses[postid] > 0 and worker["AssignmentStatus"] == 'Approved':
 		total_bonus += float(bonuses[postid])
 		# cmd = '$MTURK_CMD_HOME/bin/grantBonus.sh -workerid ' + workerid + ' -amount ' + \
 		cmd = './grantBonus.sh -workerid ' + workerid + ' -amount ' + \
 			"{0:.2f}".format(float(bonuses[postid])) + ' -assignment ' + \
 			worker['AssignmentId'] + ' -reason "Lottery Winnings. Thanks"'
 		outfile.write( cmd + '\n')
 		count += 1
 		#print cmd
 	else:
 		print workerid + " Something went wrong. Parhaps Bonus = 0? " + worker["Answer.Q2"]


print "Total bonus paid: " + str( total_bonus )
total = total_bonus + (total_bonus * .2)
print "Total deducted from account: " + str(total)
print "Number of people paid: " + str(count)