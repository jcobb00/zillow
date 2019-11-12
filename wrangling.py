import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
# from matplotlib.pyplot import figure
 import seaborn as sns
# import datetime as dt

#%%
# read data
prop_16 = pd.read_csv('/Users/johncobb/python/zillow/zillow-prize-1/properties_2016.csv', index_col='parcelid')
prop_16['data'] = 'prop_16'
prop_17 = pd.read_csv('/Users/johncobb/python/zillow/zillow-prize-1/properties_2017.csv', index_col='parcelid')
prop_17['data'] = 'prop_17'
train_16 = pd.read_csv('/Users/johncobb/python/zillow/zillow-prize-1/train_2016_v2.csv', index_col='parcelid')
train_16['data'] = 'train_16'
train_17 = pd.read_csv('/Users/johncobb/python/zillow/zillow-prize-1/train_2017.csv', index_col='parcelid')
train_17['data'] = 'train_17'
#%%

# merge by join then concat
df_16 = pd.merge(prop_16, train_16, how='right' ,left_index=True, right_index=True, suffixes=('_x', '_y'))
df_17 = pd.merge(prop_17, train_17, how='right' ,left_index=True, right_index=True, suffixes=('_x', '_y'))
df = pd.concat([df_16, df_17]).sort_index()
# clear data
del prop_16, prop_17, train_16, train_17, df_16, df_17
#%%
# change data types
cat_columns = [0, 1, 5, 8, 16, 21, 22, 28, 29, 30, 31, 32, 35, 36, 37, 38, 40, 42, 48, 54]
df.iloc[:,cat_columns] = df.iloc[:,cat_columns].astype('category')
df['transactiondate'] = pd.to_datetime(df['transactiondate'])
# create additional views
df_percent_null = 1-(df.describe(include='all').iloc[0,:]/len(df.index))#.sort_values()
df_columns = pd.DataFrame(zip(list(df.columns),range(0,len(df.columns)),list(df_percent_null)),list(df.columns),columns=['col_name','col_num','pcnt_null']).transpose()
df_dtypes = pd.DataFrame(df.dtypes, columns=['dtypes']).transpose()
df_describe1 = df.describe(include='all')
df_col_distinct = pd.DataFrame(df.nunique(),columns=['uniques']).transpose()
df_describe = pd.concat([df_columns, df_dtypes, df_col_distinct, df_describe1]).transpose()
df_col_interest = df_columns.iloc[:,[0, 3, 4, 6, 10, 11, 19, 20, 22, 23, 24, 25, 26, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 43, 46, 47, 49, 50, 51, 52, 53, 57, 57, 58, 59, 60]]
df_describe_interest = df_describe.iloc[[0, 3, 4, 6, 10, 11, 19, 20, 22, 23, 24, 25, 26, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 43, 46, 47, 49, 50, 51, 52, 53, 57, 57, 58, 59, 60],:]
# clear temp variables
del cat_columns, df_columns, df_percent_null, df_describe1, df_dtypes, df_col_distinct, df_col_interest

#   del df_col_interest, df_col_interest_describe

#%%
# check censustractandblock columns (34 and 56)
subset1 = df.loc[df['rawcensustractandblock'] != df['censustractandblock']]
subset2 = df.bathroomcnt.dropna()
subset3 = df.calculatedbathnbr.dropna()
del subset1, subset2, subset3
#%%

# quick reference for column names
a_col_1 = df.columns[10]
a_col_2 = df.columns[50]
a_col_3 = df.columns[58]


plt.xscale('log')
x_tick_val = [100, 1000, 10000, 100000]
x_tick_lab = ['100','1k', '10k', '100k']
plt.xlim(x_tick_val[0], x_tick_val[-1])
plt.xticks(x_tick_val, x_tick_lab)
plt.xlabel(a_col_1)

plt.yscale('log') 
y_tick_val = [1000, 10000, 100000, 1000000, 100000000]
y_tick_lab = ['1k', '10k', '100k', '1M', '10M']
plt.ylim(y_tick_val[0], y_tick_val[-1])
plt.yticks(y_tick_val, y_tick_lab)
plt.ylabel(a_col_2)

plt.title('scatterplot')

plt.scatter(x=df[a_col_1], y=df[a_col_2], c=df[a_col_3], s=df[a_col_3], alpha=.25,  marker='o', cmap='YlGnBu')
#plt.gray()

del a_col_1, a_col_2, x_tick_lab, x_tick_val, y_tick_lab, y_tick_val

