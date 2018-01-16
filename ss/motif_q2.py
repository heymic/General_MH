## Import necessary libraries
import pickle
import pandas as pd


def main():
    edges_df = unpickle_reverts_data()
    motif_merged_df = merge_motif_asof(edges_df)

    with open ('motif_df', 'wb') as fw:
        pickle.dump(motif_merged_df, fw)

def unpickle_reverts_data():
    with open ('edges_df', 'rb') as fr:
        edges_df = pickle.load(fr)
    return edges_df

def merge_motif_asof(df):
    df1 = sort_df_by_time(df)

    motif_merged_df = pd.merge_asof(df1, df1, on='Time',
    left_by=['Reverted', 'Reverter'],
    right_by=['Reverter', 'Reverted'],
    tolerance=pd.Timedelta('24hours'),
    direction='forward',
    suffixes=('', '_hitback')).dropna(how = 'any', axis = 0).reset_index(drop = True)

    return motif_merged_df

def sort_df_by_time(df):
    return df.sort_values('Time').reset_index(drop = True)

if __name__ == '__main__':
    main()
    print('motif_q2.py is runned from the terminal')
else:
    print('motif_q2.py is imported')
