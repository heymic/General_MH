## Import necessary libraries
import pickle
import pandas as pd
import math as mt

def main():
    df = get_data()
    with_status_df = apply_status(df)
    revert_df = create_final_dataframe(with_status_df)
    edges_df = delete_the_self_reversions(revert_df)

    with open ('edges_df', 'wb') as fw:
        pickle.dump(edges_df, fw)

def get_data():
    '''Loads the wikipedia data as a pandas dataframe'''
    df = pd.read_csv("enwiki_2002.txt", sep = '\t', parse_dates=['time'])
    return df

def apply_status(df):
    '''Adds a new columns to the dataframe with the status'''
    df = df.sort_values('time')
    df['status'] = df.groupby('user').cumcount().add(1)
    df['status'] = df['status'].apply(mt.log10)
    df = df.sort_index()
    return df

def create_final_dataframe(df):
    '''Creates the dataframe with all the edges'''
    index_reverted_flat_list = get_reverted_df(df)
    index_reversions_list = get_indexes_reversion(df)

    revert_df = pd.DataFrame({'Time' : df.loc[index_reversions_list]['time'].tolist(),
     'Reverter' : df.loc[index_reversions_list]['user'].tolist(),
     'Reverted' : df.loc[index_reverted_flat_list]['user'].tolist(),
     'Status_reverter' : df.loc[index_reversions_list]['status'].tolist(),
     'Status_reverted' : df.loc[index_reverted_flat_list]['status'].tolist()})

    return revert_df

def get_reverted_df(df):
    '''MAIN TASK: Searches and outputs the indexes in a list of the reverted (editor)'''
    list_reverts = get_title_version_of_reversion(df)

    index_reverted = []
    for sublist in list_reverts:
        indexex = df[(df['title'] == sublist[0]) & (df['version'] == sublist[1]) & (df['revert'] == 0)].index - 1
        index_reverted.append(indexex.tolist())

    index_reverted_flat_list = flatten_a_list(index_reverted)
    return index_reverted_flat_list

def get_title_version_of_reversion(df):
    '''Returns a list with the title and version of each of the reversions'''
    index_reversions_list = get_indexes_reversion(df)
    return df.loc[index_reversions_list][['title','version']].values.tolist()

def get_indexes_reversion(df):
    '''Returns a list with the indexes of the reversions'''
    return df[df['revert'] == 1].index.tolist()

def flatten_a_list(lst):
    '''Simple operation to flatten a list'''
    return [item for sublist in lst for item in sublist]



def delete_the_self_reversions(revert_df):
    '''Drops the edges that are self-reverted'''
    revert_final_df = revert_df[revert_df['Reverter'] != revert_df['Reverted']].reset_index(drop = True)
    return revert_final_df


if __name__ == '__main__':
    main()
    print('edges.py is runned from the terminal')
else:
    print('edges.py is imported')
