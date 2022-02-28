import pandas as pd
import os
import numpy as np

paths = {
    'Data' : os.path.join(os.getcwd(), 'Data')
}


def json_reader(file):
    df = pd.read_json(os.path.join(paths['Data'], file),encoding='utf-8', dtype=int)
    df.set_index('Lesson-Code')
    return df

def DataFrame_appender(df : pd.DataFrame , ld : pd.DataFrame):
    lessons_DataFrame : pd.DataFrame = ld.append(df, ignore_index=True,verify_integrity=False)
    return lessons_DataFrame


def DataFrame_Build():
    lessons_DataFrame : pd.DataFrame = json_reader(os.path.join(paths['Data'], os.listdir(paths['Data'])[0])) 

    for file in os.listdir(paths['Data'])[1:]:
        df = json_reader(os.path.join(paths['Data'], file))
        lessons_DataFrame = DataFrame_appender(df, lessons_DataFrame)

    lessons_DataFrame = lessons_DataFrame.convert_dtypes()

    lessons_DataFrame.dropna(inplace=True,)
    lessons_DataFrame.drop_duplicates(inplace=True,ignore_index=True,subset=['Lesson-Code'])
    return lessons_DataFrame

def comparing_DataFrames(df1:pd.DataFrame, df2 :pd.DataFrame):
    try:
        df2['Registered_diff'] = np.where(df1['Registered'] == df2['Registered'], 0, df2['Registered'] - df1['Registered'])
        df2['Capacity_diff'] = np.where(df1['Capacity'] == df2['Capacity'], 0, df2['Capacity'] - df1['Capacity'])
    except:
        new_removed_lessons = pd.concat([df1, df2]).drop_duplicates(keep=False,subset=['Lesson-Code'])
        changed_lessons_list = list(new_removed_lessons['Lesson-Code'])
        changed_lessons_dict = dict.fromkeys(changed_lessons_list) 
        while len(changed_lessons_list) > 0:
            try:
                for x in changed_lessons_list:
                    if x in list(df2['Lesson-Code']):
                        df2 = df2[df2['Lesson-Code'] != x]
                        changed_lessons_list.remove(x)
                #df2.drop(df2.index[df2['Lesson-Code'] == x], axis=0, inplace=True)
                        changed_lessons_dict[x] = 'Added'
                for x in changed_lessons_list:
                    if x in list(df1['Lesson-Code']):
                        df1 = df1[df1['Lesson-Code'] != x]
                        changed_lessons_list.remove(x)
                #df1.drop(df1.index[df1['Lesson-Code'] == x], axis=0, inplace=True)
                        changed_lessons_dict[x] = 'Removed'
            except Exception as e:
                print(e)
        df2['Registered_diff'] = np.where(df1['Registered'] == df2['Registered'], 0, df2['Registered'] - df1['Registered'])
        df2['Capacity_diff'] = np.where(df1['Capacity'] == df2['Capacity'], 0, df2['Capacity'] - df1['Capacity'])
    if 'new_removed_lessons' in locals():
        return [changed_lessons_dict, new_removed_lessons,df2]
    else:
        return []

def reporter(df2 :pd.DataFrame,df1 :pd.DataFrame):
    report = comparing_DataFrames(df1=df1,df2=df2)
    if len(report) == 3:
        df2 = report[2]
    report_list = list()
    
    for code,lesson,registered,capacity,updates,teacher,C_updates in zip(df2['Lesson-Code'], df2['Lesson-Name'], df2['Registered'],df2['Capacity'], df2['Registered_diff'],df2['Teacher'],df2['Capacity_diff']):
        if updates != 0:
            if updates > 0:
                report_list.append(f"{lesson} {teacher}،{abs(updates)} {'نفر ثبت نام شد|شدن'}.\nظرفیت:{registered}/{capacity}\nکد: #{code}")
            else:
                report_list.append(f"{lesson} {teacher}،{abs(updates)} {'نفر حذف کرد|کردن'}.\nظرفیت:{registered}/{capacity}\nکد: #{code}")
        if C_updates != 0:
            if C_updates > 0:
                report_list.append(f"{lesson} {teacher}،{abs(C_updates)} {'نفر به ظرفیت اضافه شد'}.\nظرفیت:{registered}/{capacity}\nکد: #{code}")
            else:
                report_list.append(f"{lesson} {teacher}،{abs(C_updates)} {'نفر از ظرفیت کم شد'}.\nظرفیت:{registered}/{capacity}\nکد: #{code}")
    if len(report) == 3:
        ind = 0
        report[1] = report[1].reset_index()
        for les in report[0]:
            for ind in report[1].reset_index().index[ind:]:
                if report[0][les] == 'Added':
                    report_list.append(f"{report[1]['Lesson-Name'][ind]} {report[1]['Teacher'][ind]},{'اضافه شد'}.\nکد: #{report[1]['Lesson-Code'][ind]}")
                elif report[0][les] == 'Removed':
                    report_list.append(f"{report[1]['Lesson-Name'][ind]} {report[1]['Teacher'][ind]},{'حذف شد'}.\nکد: #{report[1]['Lesson-Code'][ind]}")
                ind += 1
                break
    return report_list

def Capacity_Report(df :pd.DataFrame , Lesson_Code : int):
    return f"{df[df['Lesson-Code'] == Lesson_Code]['Lesson-Name'].values[0]},{df[df['Lesson-Code'] == Lesson_Code]['Teacher'].values[0]}:\nظرفیت:{df[df['Lesson-Code'] == Lesson_Code]['Registered'].values[0]}/{df[df['Lesson-Code'] == Lesson_Code]['Capacity'].values[0]}\nصف:{df[df['Lesson-Code'] == Lesson_Code]['Queue'].values[0]}\nکد: #{df[df['Lesson-Code'] == Lesson_Code]['Lesson-Code'].values[0]}"

"""df1 = DataFrame_Build()
df2 = DataFrame_Build()
df2['Registered'][8] = 27
df2['Registered'][30] = 42
df2['Capacity'][60] = 0
df2['Capacity'][56] = 42

dic ={
            'Lesson-Code' : [333010333,333010334],
            'Lesson-Name' : ['رياضيات مهندسي','رياضيات مهندسي'],
            'Lesson-Weight' : [3,3],
            'Lesson-A-Weight' : [0,0],
            'Capacity' : [40,30],
            'Registered' : [10,15],
            'Queue' : [0,0],
            'Sex' : ['مختلط','مختلط'],
            'Teacher' : ['رشولي آيسا','رسولي آيسا'],
            'schedule' : ['درس(ت): يك شنبه ۱۰:۳۰-۱۲:۳۰ مکان: ۲۰۲، درس(ت):...','درس(ت): يك شنبه ۱۰:۳۰-۱۲:۳۰ مکان: ۲۰۲، درس(ت):...'],
            'Exam-schedule' : ['تاريخ: ۱۴۰۱/۰۳/۱۶ ساعت: ۱۳:۳۰-۱۶:۳۰','تاريخ: ۱۴۰۱/۰۳/۱۶ ساعت: ۱۳:۳۰-۱۶:۳۰'],
            'Abandon' : ['مجاز براي مقطع كارشناسي، دانشکده مهندسي مكانيك،','تاريخ: ۱۴۰۱/۰۳/۱۶ ساعت: ۱۳:۳۰-۱۶:۳۰'],
            'Specification' : ['ترم ۳۹۹۱','ترم ۳۹۹۱'],
            'Anti-Lesson' : ['ندارد','ندارد'],
            'Presentation-Mode' : ['عادي','عادي'],
            'Offline-Online' : ['حضوري','حضوري'],
            'Description' : ['كلاس اين درس بصورت حضوري برگزار مي شود و به دا...','كلاس اين درس بصورت حضوري برگزار مي شود و به دا...'],
        }

df3 = pd.DataFrame(dic)

#df2 = df2.append(df3)
#df2.drop([89,34], inplace=True)
#df2.reset_index()
report = reporter(df2,df1)

for r in report:
    print(r)

for i in list(df2['Lesson-Code']):
    print(Capacity_Report(df2,i))"""