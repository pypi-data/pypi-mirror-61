import numpy as np
import pandas as pd
import sys
import math

def outlier_remover(data,new_data):
    data = pd.DataFrame(data)
    a = data.shape
    no_cols = a[1]
    no_rows = a[0]
    data_top = list(data.columns.values)
    for i in range(0,no_cols):
        data = data.sort_values(by = data_top[i])
        data = data.reset_index(drop = True)
        data.index = np.arange(1,len(data)+1)
        a = data.shape
        no_rows = a[0]
        y = data.iloc[:,i]
        f1 = math.floor((no_rows+1)/4)
        c1 = math.ceil((no_rows+1)/4)
        Q1 = (y[f1] + y[c1])/2 
        f2 = math.floor(3*(no_rows+1)/4)
        c2 = math.ceil(3*(no_rows+1)/4)
        Q3 = (y[f2] + y[c2]) / 2 
        IQR = Q3 - Q1
        min_range = Q1 - 1.5 * IQR
        max_range = Q3 + 1.5 * IQR
        data = data[data[data_top[i]] > min_range]
        data = data[data[data_top[i]] < max_range]
        data.index = np.arange(1,len(data)+1)
    
    data.to_csv(new_data, header = False, index=False)
    

def main():
    dataset = pd.read_csv(sys.argv[1]).values
    new_dataset = sys.argv[2]
    outlier_remover(dataset,new_dataset)



if __name__=="__main__":
    main()