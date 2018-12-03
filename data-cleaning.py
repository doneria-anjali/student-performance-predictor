#import numpy as np
import pandas as pd
import database as conn

def read_table(table_name):
    engine = conn.connect()
    datafull = pd.read_sql_table(table_name, engine)
    return datafull, engine

def add_to_table(df, engine, final_name):
    df.to_sql(name=final_name, con=engine, if_exists='append', index=False)
    
def clean_student_data():
    student_df, engine = read_table('algebraTrainSample2')
    print("Records fetched = " + str(len(student_df)))
    
    for count in range(len(student_df)):
        record = student_df.loc[[count]]
        #print(type(record))
        df = create_final_df(record)
        add_to_table(df, engine, 'algebraTrain_clean')
        
    print("Finished inserting data to clean table")


def create_final_df(record):
    print(record)
    #clean data
    try:
        anon_student_id = record['anonStudentId'].to_string().split()[1].strip()
        #print(anon_student_id[0])
        #print(anon_student_id[1])
        ProblemHierarchy = record['problemHierarchy'].to_string()
        #print('problem hierarchy' + record['problemHierarchy'])
        
        """
        Problem_Name = record['problemName'].to_string().strip()[1]
        Problem_View = record['problemView'].to_string().strip()[1]
        Step_Name = record['stepName'].to_string().strip()[1]
        
        Step_Start_Time = record['stepStartTime'].to_string().strip()[1]
        First_Transaction_Time = record['firstTransactionTime'].to_string().strip()[1]
        Step_Duration = record['stepDuration'].to_string().strip()[1]
        Step_End_Time = record['stepEndTime'].to_string().strip()[1]
        if not Step_Start_Time:
            if First_Transaction_Time:
                Step_Start_Time = First_Transaction_Time
                Step_Duration = str(int(Step_End_Time) - int(Step_Start_Time))
        
        print('Step start time' + str(Step_Start_Time))
        print('step duration' + str(Step_Duration))
        
        Correct_Transaction_Time = record['correctTransactionTime'].to_string().strip()[1]
        Correct_Step_Duration = record['correctStepDuration'].to_string().strip()[1]
        Error_Step_Duration= record['errorStepDuration'].to_string().strip()[1]
        
        Incorrects = record['incorrects'].to_string().strip()[1]
        Hints = record['hints'].to_string().strip()[1]
        Corrects = record['corrects'].to_string().strip()[1]
        Opportunity_default = record['opportunity'].to_string().strip()[1]
        """
        
        KC_default = record['kc'].to_string()
        Correct_First_Attempt = record['correctFirstAttempt'].to_string().split()[1].strip()
        
        unit = ProblemHierarchy.split(',')[0].split()[2]
        #print('Unit' + str(unit))
        prob = ProblemHierarchy.split(',')[1].split('-')[1]
        #print('Problem' + str(prob))
        #prob = ProblemHierarchy.split(',')[1].split('-')[1]
        
        #pd.options.display.max_colwidth=500
        kc_final = ''
        if KC_default:
            wordlist = []
            kc = set()
            wordlist = KC_default.split('~~')
            str1 = ''
            for word in wordlist:
                if 'SkillRule' in word:
                  str1 = word.strip().split('[SkillRule:')[1]
                  str1 = str1.split(';')[0].strip()
                  if str1 not in kc:
                      kc_final += str1 + ','
                      kc.add(str1)
                else:
                  print('in else')
                  str1 = word.split(' ',1)[1].split('~~')
                  for string in str1:
                      if string not in kc:
                          kc_final += str1 + ','
                          kc.add(str1)
                
            kc_final = kc_final[:-1]
        else:
            kc_final = 'empty'      
            
        #print(kc_final)
         
        
        #insert data to dataframe
        list_data = pd.DataFrame(data = [[anon_student_id, 
                                   unit,prob, Correct_First_Attempt, kc_final]],
                                   columns=['anonStudentId','unit','problem',
                                   'correctFirstAttempt','kc'])
        #print(list_data)
        record.append(list_data, ignore_index=True)
        return list_data
    except:
        print('exception occured')
        list_data = pd.DataFrame(data = [['x', 
                                   'x','x', 0, 'x']],
                                   columns=['anonStudentId','unit','problem',
                                   'correctFirstAttempt','kc'])
        return list_data

clean_student_data()