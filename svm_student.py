import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, mean_squared_error
from sklearn.feature_selection import RFE
from sklearn import svm
from mlxtend.feature_selection import SequentialFeatureSelector as sfs
from mlxtend.feature_selection import ColumnSelector
from pprint import pprint
from time import time

mydata = pd.read_csv("/Users/Jarvis/Documents/GitHub/student-performance-predictor/clean_full_latest.csv") #sample train, bill_authentication
# mydata.anonStudentId = mydata.anonStudentId.astype(int)
# mydata = mydatafull[:2000]
stuid = dict()
for name in mydata.anonStudentId:
	if name not in stuid.keys():
		idlist = list(stuid.values())
		if idlist:
			a = max(idlist)
		else: 
			a = 0
		stuid[name] = a + 1
	else:
		continue
#print(stuid)
mydata = mydata.replace({'anonStudentId': stuid})
train_cfm = []
test_cfm = []
for k in ('rbf','sigmoid','linear'):
	k1 = time()
	print('\n*****---------' + k + '------------*****')
	train_accuracy_list = []
	test_accuracy_list = []
	train_confmat = []
	test_confmat = []
	# numrows = 0
	# numtestrows = 0
	# numtrainrows = 0
	train_rmse = []
	test_rmse = []
	for cnt,(name,s_id) in enumerate(stuid.items()):
		s1 = time()
		#print('\n')
		#print((name,s_id))
		#print('\n')
		studf = mydata.loc[mydata['anonStudentId'] == s_id]
		# main_rows,main_cols = studf.shape
		# numrows += main_rows
		# Data Preprocessing
		X = studf[['kc','stepDuration']] #'incorrects', 'hints', 'corrects'
		# X = pd.factorize(mydata['kc'].values)[0].reshape(-1, 1)
		y = pd.factorize(studf['correctFirstAttempt'].values)[0].reshape(-1, 1)

		#splitting into train and test
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

		r,c = X_train.shape
		# numtrainrows += r

		r2,c2 = X_test.shape
		# numtestrows += r2

		y_train = y_train.ravel()
		y_test = y_test.ravel()

		#Training the Algorithm
		# for k in ('linear'): #'rbf','sigmoid'
		svclassifier = svm.SVC(kernel=k, gamma='auto', C=1)
		svclassifier.get_params()

		# rfe = RFE(svclassifier, 10)
		# rfe = rfe.fit(X_train, y_train.ravel())
		sfs1 = sfs(svclassifier,
				   k_features=(1,2),
				   forward=True,
				   floating=False,
				   verbose=0,
				   scoring='accuracy',
				   cv=0)

		try:
			sfs1 = sfs1.fit(X_train, y_train)
		except:
			continue

		# col_sel = ColumnSelector(cols=sfs.get_metric_dict()[sorted(sfs.get_metric_dict().keys(), key=lambda x: (sfs.get_metric_dict()[x]['avg_score']), reverse=True)[0]]['feature_idx'])
		# print(col_sel)

		feat_cols = list(sfs1.k_feature_idx_)
		labels = list(sfs1.k_feature_names_)

		svclassifier.fit(X_train.iloc[:,feat_cols], y_train.ravel())

		#Making Predictions
		y_train_pred = svclassifier.predict(X_train.iloc[:,feat_cols])
		y_test_pred = svclassifier.predict(X_test.iloc[:,feat_cols])

		#Evaluating the Algorithm
		
		train_accuracy_list.append(accuracy_score(y_train,y_train_pred))
		test_accuracy_list.append(accuracy_score(y_test,y_test_pred))
		print('\n')
		print(str(cnt)+': '+str({name: {'training acc': accuracy_score(y_train,y_train_pred), 'testing acc': accuracy_score(y_test,y_test_pred)}}))

		print('Best Features: ' + str(labels))

		# print('\nTraining Confusion_matrix: ')
		cm = confusion_matrix(y_train,y_train_pred)
		# print(type(cm))
		train_confmat.append(([cm[0,0],cm[0,1],cm[1,0],cm[1,1]],k))

		cm2 = confusion_matrix(y_test,y_test_pred)
		# print(type(cm))
		try:
			test_confmat.append(([cm2[0,0],cm2[0,1],cm2[1,0],cm2[1,1]],k))
		except:
			print(cm2)
			tn, fp, fn, tp = confusion_matrix(y_test, y_test_pred, labels=[0,1]).ravel()
			test_confmat.append(([tp,fn,fp,tn],k))

		# print('Kernel name: ' + str(k))
		
		# print('\nTraining Accuracy: ')		
		# print(accuracy_score(y_train,y_train_pred))

		# print('\nTraining Classification_report: ')
		# print(classification_report(y_train,y_train_pred))
		# print('\nTraining RMSE: ')
		train_rmse.append(mean_squared_error(y_train,y_train_pred))


		# print('\nTesting Accuracy: ')
		
		# print(accuracy_score(y_test,y_test_pred))
		# print('\nTesting Confusion_matrix: ')
		# print(confusion_matrix(y_test,y_test_pred))
		# print('\nTesting Classification_report: ')
		# print(classification_report(y_test,y_test_pred))
		# print('\nTesting RMSE: ')
		test_rmse.append(mean_squared_error(y_test,y_test_pred))
		# print('+---------------+---------------+-------------+')
		
		s2 = time()
		print(str(s2-s1) + ' sec')
	# print('\n')	
	# print('train_accuracy_list: ')
	# print(train_accuracy_list)
	# print('\n')
	# print('Average train_accuracy: ')
	# print(float(sum(train_accuracy_list)/len(train_accuracy_list)))
	# print('\n')
	# print('train confusion_matrix: ')
	a,b,c,d = 0,0,0,0
	for x,l in train_confmat:
		# print(x)
		a += x[0]
		b += x[1]
		c += x[2]
		d += x[3]
	# train_cfm = np.array([[a,b],[c,d]])
	train_cfm.append(([[a,b],[c,d]],l))
	a,b,c,d = 0,0,0,0
	for x,l in test_confmat:
		# print(x)
		a+= x[0]
		b += x[1]
		c += x[2]
		d += x[3]
	# train_cfm = np.array([[a,b],[c,d]])
	test_cfm.append(([[a,b],[c,d]],l))
	# print('numrows: ' + str(numrows))
	# print('numtrainrows: ' + str(numtrainrows))
	# print('numtestrows: ' + str(numtestrows))
	# print('\n')	
	# print('test_accuracy_list: ')
	# print(test_accuracy_list)
	print('\n')
	print('Average train_accuracy: ' + str(sum(train_accuracy_list)/len(train_accuracy_list)))
	print('\n')
	print('Average test_accuracy: ' + str(sum(test_accuracy_list)/len(test_accuracy_list)))
	print('\n')
	print('Average train_RMSE: ' + str(sum(train_rmse)/len(train_rmse)))
	print('\n')
	print('Average test_RMSE: ' + str(sum(test_rmse)/len(test_rmse)))
	print('\n')
	k2 = time()
	print(str(k2-k1) + ' sec')
for num,(i,ker) in enumerate(train_cfm):
	xlabels = ['Predicted-True','Predicted-False']
	df_cm = pd.DataFrame(i, index = ['Actual-True','Actual-False'], columns = ['PT','PF'])
	plt.subplot(3,2,2*num+1)
	sn.heatmap(df_cm, annot=True, cmap='YlGnBu', fmt='g')
	plt.title(str(ker) + '-train')

for num,(i,ker) in enumerate(test_cfm):
	xlabels = ['Predicted-True','Predicted-False']
	df_cm = pd.DataFrame(i, index = ['Actual-True','Actual-False'], columns = ['PT','PF'])
	plt.subplot(3,2,2*num+2)
	sn.heatmap(df_cm, annot=True, cmap='YlGnBu', fmt='g')
	plt.title(str(ker) + '-test')

plt.show()




