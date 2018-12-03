create database edm;
use edm;
create table algebraTrain 
(
	rowNumber int,	
	anonStudentId varchar(50),
    problemHierarchy varchar(50),
    problemName varchar(100),
    problemView int,
    stepName varchar(50),
    stepStartTime varchar(50),
    firstTransactionTime varchar(50),	
    correctTransactionTime varchar(50),
    stepEndTime varchar(50),	
    stepDuration double,
    correctStepDuration double,
    errorStepDuration double,
    correctFirstAttempt int,
    incorrects int,
	hints int,
    corrects int,
	kc varchar(2000),
    opportunity varchar(100)
);
LOAD DATA LOCAL INFILE '/home/anjali/Downloads/algebra_2005_2006_train.csv'
INTO TABLE edm.algebraTrain FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\n';

DELETE FROM edm.algebraTrain where rowNumber = 0;
drop table edm.algebraTrain_clean;
create table edm.algebraTrain_clean
(
	anonStudentId varchar(50),
    unit varchar(50),
    problem varchar(50),
    correctFirstAttempt int,
	kc varchar(2000)
);

use edm;

create view algebraTrainSample2 as
select * from algebraTrain limit 0,30;
