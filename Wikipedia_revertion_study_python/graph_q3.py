## Import necessary libraries
import pickle
import pandas as pd
import matplotlib.pyplot as plt

def main():
    motif_df = unpickle_motif_data()
    edges_df = unpickle_reverts_data()

    motif_df = calculate_status_difference(motif_df)
    edges_df = calculate_status_difference(edges_df)

    draw_graph(edges_df, motif_df)
    print_means(edges_df, motif_df)

def unpickle_motif_data():
    '''Unpickles and loads the motif dataframe'''
    with open ('motif_df', 'rb') as fr:
        motif_df = pickle.load(fr)
    return motif_df

def unpickle_reverts_data():
    '''Unpickles and loads the reverts dataframe'''
    with open ('edges_df', 'rb') as fr:
        edges_df = pickle.load(fr)
    return edges_df

def calculate_status_difference(df):
    '''Calculates the status difference between the editors'''
    df['Status_diff'] = df['Status_reverter'] - df['Status_reverted']
    return df

def draw_graph(edges_df, motif_df):
    '''Draws the histograms'''
    fig, ax = plt.subplots(figsize = (15, 10))

    #Histograms
    edges_df['Status_diff'].hist(bins = 10, normed = True, ax = ax, alpha = 0.75, label = "All-Reverts Hist." )
    motif_df['Status_diff'].hist(bins = 10,normed = True, ax = ax, alpha = 0.75, label = "Motif-Reverts Hist.")

    #Vertical Lines
    ax.axvline(x = edges_df['Status_diff'].mean(), color="Blue", label = "All-Reverts Mean")
    ax.axvline(x = motif_df['Status_diff'].mean(), color="Red", label = "Motif-Reverts Mean")

    ax.set_xlabel("Status Difference")
    ax.set_ylabel("Normalized number of reverts")
    ax.legend(loc='upper left')

    plt.show()

def print_means(edges_df, motif_df):
    '''Print the means of Status_diff of the all the reverts and the motif'''
    print("The status mean difference of all reverts is :", edges_df['Status_diff'].mean())
    print("The status mean difference of temporal reverts:", motif_df['Status_diff'].mean())


if __name__ == '__main__':
    main()
    print('\ngraph_q3.py is runned from the terminal')
else:
    print('graph_q3.py is imported')
