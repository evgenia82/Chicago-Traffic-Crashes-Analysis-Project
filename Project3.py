# 02/01/2019
# Ievgeniia Chubata
# The dataset can be downloaded at the City of Chicago Data Portal
# https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if/data

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
# I don't know what to return common_day or most_com_day and it gives me an error - need some help
def common_day(df):

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    index = int(df_clean['CRASH_DAY_OF_WEEK'].mode())
    most_com_day = days_of_week[index]
    return common_day

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

# The number of fatal injuries in the dataset
def fatal_injury(df):
    fatal_injury=df_clean[df_clean["MOST_SEVERE_INJURY"].apply(lambda injury: injury=='FATAL')]['MOST_SEVERE_INJURY'].count()
    print('\n There were total {} fatal injuries in the dataset.'.format(fatal_injury))

# The number of hit and run accidents
def hit_and_run(df):
    hit_run=df_clean[df_clean["HIT_AND_RUN_I"].apply(lambda hitrun: hitrun=='Y')]['HIT_AND_RUN_I'].count()
    print('\n There were total {} hit and run accidents in the dataset.'.format(hit_run))

# The 5 most common crash types
def common_type(df):
    com_type=df_clean['FIRST_CRASH_TYPE'].value_counts().head()
    print('\n The 5 most common types of traffic crashes were: \n{}.'.format(com_type))

# The 5 most common crash causes
def common_cause(df):
    com_cause=df_clean["PRIM_CONTRIBUTORY_CAUSE"].value_counts().head()
    print('\n The 5 most common causes of traffic crashes were: \n{}.'.format(com_cause))

# The 4 most common injuries
def common_injury(df):
    com_injury=df_clean['MOST_SEVERE_INJURY'].value_counts().head(4)
    print('\n The 4 most common injuries caused by traffic crashes were: \n{}.'.format(com_injury))

# Creating a heatmap of most common crash hour, day of week and cause
def heat_map(df):
    dayHour = df_clean.groupby(by=['CRASH_HOUR','CRASH_DAY_OF_WEEK']).count()['PRIM_CONTRIBUTORY_CAUSE'].unstack()
    plt.figure(figsize=(12,6))
    sns.heatmap(dayHour, cmap='plasma')
    plt.title('HEATMAP BASED ON A CRASH HOUR, CRASH DAY OF WEEK, AND A PRIMARY CONTRIBUTORY CAUSE')
    plt.show()

# The countplot that shows the dollar amount of demage created by traffic crashes
def damage_plot(df):
    plot1=sns.countplot(x="DAMAGE",data=df_clean,palette='viridis')
    plt.show()

# The countplot that shows the crash month and damage related to it
def damage_plot_by_month(df):
    plot2=sns.countplot(x='CRASH_MONTH',data=df_clean,hue='DAMAGE')
    plt.title('CRASH MONTH AND DAMAGE')
    plt.show()

# The plot that shows most common crash hour
def crash_hour_plot(df):
    plot3=sns.countplot(x='CRASH_HOUR', data=df_clean)
    plt.title('MOST COMMON CRASH HOUR')
    plt.show()

# The graph that shows the number of crashes with a primary contributory cause 'WEATHER'
# Let work on this line - don't remeber what it means
df_clean[df_clean['PRIM_CONTRIBUTORY_CAUSE']=='WEATHER'].groupby('CRASH_MONTH').count()['RD_NO'].plot()
plt.title('Number of Crashes Influenced by Weather')
plt.tight_layout()
plt.show()

def main():
    common_day(df_clean)
    common_hour(df_clean)
    fatal_injury(df_clean)
    hit_and_run(df_clean)
    common_type(df_clean)
    common_cause(df_clean)
    common_injury(df_clean)
    heat_map(df_clean)
    damage_plot(df_clean)
    damage_plot_by_month(df_clean)
    crash_hour_plot(df_clean)

    print('\n The most common day of the week when the crash had happened was {}.'.format(most_com_day))

if __name__ == "__main__":
    main()
