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
    student_df, engine = read_table('algebraTrain')
    print("Records fetched = " + str(len(student_df)))
    
    #for count in range(len(student_df)):
    for count in range(5):
        record = student_df.iloc[count]
        df = create_final_df(record)
        add_to_table(df, engine, 'algebraTrain_clean')
        
    print("Finished inserting data to purchase_data")


def create_final_df(record):
    record = pd.DataFrame(columns=['rowNumber','anonStudentId','problemHierarchy',
                               'problemName','problemView',
                               'stepName','stepStartTime','firstTransactionTime',
                               'correctTransactionTime','stepEndTime',
                               'stepDuration','correctStepDuration', 
                               'errorStepDuration','correctFirstAttempt',
                               'incorrects','hints','corrects','kc',
                               'opportunity'])
    
    #clean data
    row = record['rowNumber']
    
    anon_student_id = record['anonStudentId']    
    record['problemHierarchy'] = record['problemHierarchy'].astype('str')
    print('problem hierarchy' + record['problemHierarchy'])
    
    Problem_Name = record['problemName']
    Problem_View = record['problemView']
    Step_Name = record['stepName']
    
    Step_Start_Time = record['stepStartTime'].to_string()
    First_Transaction_Time = record['firstTransactionTime'].to_string()
    Step_Duration = record['stepDuration'].to_string()
    Step_End_Time = record['stepEndTime'].to_string()
    if not Step_Start_Time:
        if First_Transaction_Time:
            Step_Start_Time = First_Transaction_Time
            Step_Duration = str(int(Step_End_Time) - int(Step_Start_Time))
    
    print(Step_Start_Time)
    print(Step_Duration)
    
    Correct_Transaction_Time = record['correctTransactionTime']
    Correct_Step_Duration = record['correctStepDuration']
    Error_Step_Duration= record['errorStepDuration']
    Correct_First_Attempt = record['correctFirstAttempt']
    Incorrects = record['incorrects']
    Hints = record['hints']
    Corrects = record['corrects']
    KC_default = record['kc'].to_string()
    Opportunity_default = record['opportunity']
    
    ph1 = (record['problemHierarchy'] + '.')[:-1]
    
    unit = record['problemHierarchy'].split(',')[0].split('Unit')[1].strip()
    prob = ph1.split(',')[1].split('-')[1]
    
    #pd.options.display.max_colwidth=500
    kc_final = "empty"
    if KC_default:
        wordlist = []
        kc = set()
        wordlist = KC_default.split('~~')
        str1 = ''
        for word in wordlist:
          str1 = word.strip().split('[SkillRule:')[1]
          str1 = str1.split(';')[0].strip()
          kc.add(str1)
          
        kc_final = str(kc)
        print(kc_final)
     
    opp = Opportunity_default.split('~~')
    opp_set = set()
    for opportunity in opp:
        str2 = opportunity.strip()
        opp_set.add(str2)
      
    print(opp_set)
    
    #insert data to dataframe
    list_data = pd.DataFrame(data = [[row, anon_student_id, 
                               unit,prob,Problem_Name,Problem_View,
                               Step_Name, Step_Start_Time, First_Transaction_Time,
                               Correct_Transaction_Time, Step_End_Time,
                               Step_Duration, Correct_Step_Duration, 
                               Error_Step_Duration, Correct_First_Attempt,
                               Incorrects, Hints, Corrects, str(opp_set), kc_final]],
                               columns=['rowNumber','anonStudentId','unit','problem',
                               'problemName','problemView',
                               'stepName','stepStartTime','firstTransactionTime',
                               'correctTransactionTime','stepEndTime',
                               'stepDuration','correctStepDuration', 
                               'errorStepDuration','correctFirstAttempt',
                               'incorrects','hints','corrects',
                               'opportunity','kc'])
    record = record.append(list_data, ignore_index=True)
    return list_data

clean_student_data()