# Demo
# This is a demo repository. I am currently working on a Pyhton project with a goal of analyzing Chicago traffic crashes data
# 02/01/2019
# Ievgeniia Chubata

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

df = pd.read_csv('Traffic_Crashes.csv', low_memory=False)
df1=df[df.isnull().any(axis=1)]
print(df1.head())

# Our data needs to be cleaned up because 6 of the columns have blank fields : LANE COUNT, REPORT TYPE, INTERSECTION RELATED, NOT RIGHT OF WAY, HIT AND RUN,
# AND MOST SEVERE INJURY.

df1=df1.fillna({"LANE_CNT": 2})

# Applying lambda function - if data type is in 'biufc' (boolean, integer, unicode, float, and complex), N/A values will be replaced with "NO".

df_clean = df1.apply(lambda x: x.fillna("NO") if x.dtype.kind in 'biufc' else x.fillna('.'))


# The most common day of the week when the crash had happened
def common_day(df):

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    index = int(df_clean['CRASH_DAY_OF_WEEK'].mode())
    most_com_day = days_of_week[index]
    print('\n The most common day of the week when the crash had happened was {}.'.format(most_com_day))
common_day(df_clean)

# The most common hour the crash had happened
def common_hour(df):
    most_com_hour = int(df_clean["CRASH_HOUR"].mode())
    if most_com_hour == 0:
        am_pm = 'am'
        pop_hour_readable = 12
    elif 1 <= most_com_hour < 13:
        am_pm = 'am'
        pop_hour_readable = most_com_hour
    elif 13 <= most_com_hour < 24:
        am_pm = 'pm'
        pop_hour_readable = most_com_hour - 12
    print('\n The most common hour of day when the crash had happened was {} {}.'.format(pop_hour_readable, am_pm))
common_hour(df_clean)

# The number of fatal injuries in the dataset
def fatal_injury(df):
    fatal_injury=df_clean[df_clean["MOST_SEVERE_INJURY"].apply(lambda injury: injury=='FATAL')]['MOST_SEVERE_INJURY'].count()
    print('\n There were total {} fatal injuries in the dataset.'.format(fatal_injury))
fatal_injury(df_clean)

# The number of hit and run accidents
def hit_and_run(df):
    hit_run=df_clean[df_clean["HIT_AND_RUN_I"].apply(lambda hitrun: hitrun=='Y')]['HIT_AND_RUN_I'].count()
    print('\n There were total {} hit and run accidents in the dataset.'.format(hit_run))
hit_and_run(df_clean)

# The 5 most common crash types
def common_type(df):
    com_type=df_clean['FIRST_CRASH_TYPE'].value_counts().head()
    print('\n The 5 most common types of traffic crashes were: \n{}.'.format(com_type))
common_type(df_clean)
    
# The 5 most common crash causes
def common_cause(df):
    com_cause=df_clean["PRIM_CONTRIBUTORY_CAUSE"].value_counts().head()
    print('\n The 5 most common causes of traffic crashes were: \n{}.'.format(com_cause))
common_cause(df_clean)

# The 4 most common injuries
def common_injury(df):
    com_injury=df_clean['MOST_SEVERE_INJURY'].value_counts().head(4)
    print('\n The 4 most common injuries caused by traffic crashes were: \n{}.'.format(com_injury))
common_injury(df_clean)

# Creating a heatmap of most common crash hour, day of week and cause
def heat_map(df):
    dayHour = df_clean.groupby(by=['CRASH_HOUR','CRASH_DAY_OF_WEEK']).count()['PRIM_CONTRIBUTORY_CAUSE'].unstack()
    plt.figure(figsize=(12,6))
    sns.heatmap(dayHour, cmap='plasma')
    plt.show()
heat_map(df_clean)

# The countplot that shows the dollar amount of demage created by traffic crashes
def damage_plot(df):
    plot1=sns.countplot(x="DAMAGE",data=df_clean,palette='viridis')
    plt.show()
damage_plot(df_clean)

# The countplot that shows the crash month and damage related to it
def damage_plot_by_month(df):
    plot2=sns.countplot(x='CRASH_MONTH',data=df_clean,hue='DAMAGE')
    plt.show()
damage_plot_by_month(df_clean)

# The plot that shows most common crash hour
def crash_hour_plot(df):
    plot3=sns.countplot(x='CRASH_HOUR', data=df_clean)
    plt.show()
crash_hour_plot(df_clean)

# The graph that shows the number of crashes with a primary contributory cause 'WEATHER'
df_clean[df_clean['PRIM_CONTRIBUTORY_CAUSE']=='WEATHER'].groupby('CRASH_MONTH').count()['RD_NO'].plot()
plt.title('Number of Crashes Influenced by Weather')
plt.tight_layout()
plt.show()
