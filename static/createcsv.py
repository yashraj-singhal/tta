import os 
import pandas as pd
dic = { 'filename':[] , 'type':[] , 'emotion':[] }

a = ['static/tt_dataset/' + i for i in os.listdir("static/tt_dataset/")]
for i in a:
    for j in os.listdir(i):
        
        ii = i[18:]
        print(ii)
        typ = ii[:ii.index('_')]
        emo = int(i[-1])
        filepath = i +'/' +j 
        dic['filename' ].append(filepath[filepath.index('/') +1:])
        dic['type' ].append(typ)
        dic['emotion' ].append(emo)
df = pd.DataFrame.from_dict(dic)
df = df.sample(frac=1)
df = df.sample(frac=1)
df = df.sample(frac=1)
df = df.sample(frac=1)
df = df.sample(frac=1)
df = df.sample(frac=1)
df = df.sample(frac=1)
df.to_csv('data.csv', index=False)
    
        