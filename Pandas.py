import pandas as pd
import numpy as np
obj = pd.Series([4,7,-5,3])
print(obj)
print(obj.values)
print(obj.index)

sdata = {'ohio':35000,'Texas':71000,'Oregon':15000,'Utah':5000}
obj2 = pd.Series(sdata)
print(obj2)
print('*'*100)
states= ['California','Ohio','Oregon','Texas']
obj3 = pd.Series(sdata,index=states)
print('*'*100)
print(obj3)
print('*'*100)
obj3.name ='population'
obj3.index.name='state'
print(obj3)

obj.index=['Bob','Steve','Jeff','Ryan']
print(obj)

data = {'State':['ohio','ohio','ohio','nevada','nevada','nevada'],
        'year':[2000,2001,2002,2001,2002,2003],
        'pop':[1.5,1.7,3.6,2.4,2.9,3.2]}
frame = pd.DataFrame(data)
print(frame)
print('*'*100)

print(frame.head())
print('*'*100)

print(pd.DataFrame(data,columns=['year','pop','State']))

frame2 = pd.DataFrame(data,columns=['year','State','pop','dbt'],
                      index=['one','two','three','four','five','six'])
print('*'*100)

print(frame2)

print('*'*100)

print(frame2['year'])

print('*'*100)

print(frame2.loc['three'])
print('*'*100)

frame2['debt']=3.6

print(frame2)
print('*'*100)

frame2['debt']= np.arange(6.)
print(frame2)
print('*'*100)

val = pd.Series([-1.2,-1.5,-1.7], index=['two','four','five'])
frame2['dbt']=val
print(frame2)
print('*'*100)

frame2['easn'] = frame2.State == 'ohio'
print(frame2)

del frame2['easn']
print(frame2)
print('*'*100)

# 중첩 사전 {{}}
pop = {'Nervada':{2001:2.4, 2002:2.9},
       'Ohio':{2000:1.5, 2001:1.7, 2002:3.6}}
frame3 = pd.DataFrame(pop)
print(frame3)