import numpy as np
import pandas as pd

def remove_outliers(incsv_filename, outcsv_filename,threshold=1.5):

    dataset = pd.read_csv(incsv_filename)	
    data = dataset.iloc[:,1:]  

    for i, row in data.iterrows():
        mean = np.mean(row)
        std = np.std(row)
        for value in row:
            z_score = (value-mean)/std
            if np.abs(z_score)>threshold:
                dataset = dataset.drop(data.index[i])
                break
            
    dataset.to_csv(outcsv_filename, index=False)
    print ('The no of rows removed:',len(data) - len(dataset))