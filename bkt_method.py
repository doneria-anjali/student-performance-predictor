import csv
import sys
import pprint
# #print('Python %s on %s' % (sys.version, sys.platform))
# sys.path.extend(['/Users/Jarvis/Documents/NC State Sem III/Educational Data Mining/assignment3_BKT'])

class BKT:
	
	accurateCount = 0
	totalLines = 0
	visitedStudents = dict()
	kc_dict = dict()
	initial= 0.0
	threshold = 0.0
	transit = 0.0
	guess = 0.0
	slip = 0.0

	def __init__(self, param):
		self.initial = param[0]
		self.transit = param[1]
		self.slip = param[2]
		self.guess = param[3]
		self.threshold = param[4]

	def accuracy(self):
		# with open('AssignmentData.csv') as bktfile:
		with open('/Users/Jarvis/Documents/GitHub/student-performance-predictor/clean_full_latest.csv') as bktfile:
			reader = csv.DictReader(bktfile)
			csvlist = list(reader)
			print('Initial: ' + str(self.initial) + '\nTransit: ' + str(self.transit) + '\nGuess: ' 
				+ str(self.guess) + '\nSlip: ' + str(self.slip))
			for rec in csvlist:
				#print('**********')
				#print(rec)
				self.totalLines += 1
				keyl = list(rec.keys())
				valuel = list(rec.values())
				#print('valuel: ' + str(valuel))
		
				stu = valuel[0]
				if stu not in self.visitedStudents:
					self.kc_dict = dict()
					self.visitedStudents[stu] = self.kc_dict
				else:
					self.kc_dict = self.visitedStudents[stu]

				kcID = valuel[4]
				#print(valuel)
				#print('kcid: ')
				#print(kcID)
				prediction = self.getpred(kcID, valuel[3],stu)

				if (self.validate(valuel[3], prediction)):
					self.accurateCount += 1
		# #print("self.kc_dict: ")
		# #print(self.kc_dict)
		#print('Visited students: ')
		# pprint.pprint(self.visitedStudents)
		print('\nAccuracy: ')
		return float(self.accurateCount/self.totalLines)

	def getpred(self, kcid, curr_groundtruth, student):
		pred = 0.0
		if kcid in self.kc_dict:
			prev = float(self.kc_dict.get(kcid)[0])
			prev_groundtruth = self.kc_dict.get(kcid)[1] 
			#print('prev: ')
			#print(prev)
			transitProb = 0.0
			if prev_groundtruth=='1':
				transitProb = (prev*(1 - self.slip))/(prev*(1-self.slip) + (1-prev)*self.guess)
			else:
				transitProb = (prev * self.slip) / (prev * self.slip + (1 - prev) * (1 - self.guess))
			#print('prev_groundtruth: ')
			#print(prev_groundtruth)
			#print('transitProb: ')
			#print(transitProb)
			prob = float(transitProb + (1 - transitProb) * self.transit)
			#print('prob: ')
			#print(prob)
			pred = float(prob * (1 - self.slip) + (1 - prob) * self.guess)
			#print('pred: ')
			#print(pred)
		else:
			pred = self.initial
			#print('pred: initial ')
			#print(pred)
		self.kc_dict[kcid]=[pred,curr_groundtruth]
		self.visitedStudents[student]=self.kc_dict
		return pred

	def validate(self,correct,pred):
		if ((pred >= self.threshold and int(correct) == 1) or (pred < self.threshold and int(correct) == 0)):
			return True
		return False


if __name__ == '__main__':
	#print((sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]))
	param = sys.argv[1:]
	param = list(map(float, param))
	acc1 = BKT(param)
	#print('&&&&&&&&&&&&&&')
	print(acc1.accuracy())
