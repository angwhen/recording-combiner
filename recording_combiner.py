import numpy as np
import pandas as pd

def format_data_frame(df):
    # putting data into format we'd like
    df.columns = ["time","x","y","light_change"]
    df = df.drop(labels="light_change",axis=1) 
    df = df.assign(eq_sep_time=(df['time']).astype('category').cat.codes) 
    return df

def save_combined_data(df):
    # only keep eq_sep_time
    df.drop(labels = "time",axis=1)
    df = df[['eq_sep_time','x','y']]
    np.savetxt(r'combined.txt', df.values, fmt='%d')
    
def main():
    # reading/setting up data
    chunksize = 10 ** 6
    for chunk in pd.read_csv("yosemite.txt", sep = " ", header=None, chunksize=chunksize):
        break
    df_1 = format_data_frame(chunk)

    for chunk in pd.read_csv("events.txt", sep = " ", header=None, chunksize=chunksize):
        break
    df_2 = format_data_frame(chunk)
    
    """
    # put the points in each of these things together
    # join by their eq_sep_time thing
    combined = df_1.set_index('eq_sep_time').join(df_2.set_index('eq_sep_time'), lsuffix = '_df1',rsuffix = "_df2")
    """

    # put all of the points on top of each other, as if just one dataframe but use eq_sep_time when saving
    combined = pd.concat((df_1,df_2),ignore_index=True)
    print combined

    save_combined_data(combined)
    
    
    
if __name__ == "__main__":
    main()
    
