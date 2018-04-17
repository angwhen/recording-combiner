import numpy as np
import pandas as pd

def format_data_frame(df):
    # putting data into format we'd like
    df.columns = ["time","x","y","light_change"]
    df = df.drop(labels="light_change",axis=1) 
    #df = df.assign(eq_sep_time=(df['time']).astype('category').cat.codes) 
    return df

def main():
    # reading/setting up data
    chunksize = 10 ** 6
    for chunk in pd.read_csv("yosemite.txt", sep = " ", header=None, chunksize=chunksize):
        break
    df_1 = format_data_frame(chunk)

    for chunk in pd.read_csv("events.txt", sep = " ", header=None, chunksize=chunksize):
        break
    df_2 = format_data_frame(chunk)


    #put the points in each of these things together
    
    
if __name__ == "__main__":
    main()
    
