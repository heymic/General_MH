### MY470 Computer Programming

---
### Are status-equals more likely to get into fights?

In the assignment, we will study reverts on Wikipedia. A revert occurs when an editor undoes the changes made by another editor. We will first identify who reverted whom and when, then identify situations in which if $A$ reverted $B$, $B$ reverted $A$ within 24 hours, and finally compare the status difference between $A$ and $B$ to the expected status difference.

### Data

We will use data from the file `enwiki_2002.txt`. 
To data were originally obtained from the Wikipedia XML Dumps (https://dumps.wikimedia.org/mirrors.html) and include every article edit made on English Wikipedia since the online encyclopaedia was founded on January 15th, 2001 until the end of 2002. Each line in the file is an edit and includes the title of the edited article, the time when the edit was submitted, whether the edit was a revert, the version of the article, and the user who submitted the edit. To detect the article versions, a hash was calculated for the complete article text following each revision and the hashes were compared between edits. 

The table below describes the variables in the data:

| Variable   | Explanation   
|:-----------|:-------
| title      | title of the edited article               
| time       | time in the format YYYY-MM-DD HH:MM:SS when the edit was completed  
| revert     | 1 if the edit was detected to revert to a previous article version, 0 otherwise 
| version    | an integer indicating a unique state of the article, generally increasing over time; -1 indicates the article was empty (usually due to vandalism); if the same number appears more than once, then the article was exactly in the same state at these different time points  
| user       | the editor's username or if not logged in, the editor's IP address  


### 1. Who reverted whom?

Your goal is to create an edge list, where an edge goes from the editor who restored an earlier version of the article (the "reverter") to the editor who made the revision immediately after that version (the "reverted"). For every edge, you should know when it occured and what the "status" of the the reverter and the reverted were at this point in time.

We will ignore the article titles for the analyses so you don't need to save these.

In addition, you will need to clean up the self-reverts – we will not use them in the analyses here.

The measure of "status" we will use is related to seniority and activity. We will estimate status $s_i$ of editor $i$ as the base-ten logarithm of the number of edits $i$ has completed by the time of the revert under question. Transforming the number of edits with the logarithm makes sense because they follow a power-law distribution (the majority of individuals have very few edits, while a handful of individuals are responsible for most of the work). This operationalization allows to express the difference in status between two editors as the base-ten logarithm of the ratio of number of edits since $s_i - s_j = \log_{10} e_i - \log_{10} e_j = \log_{10} \frac{e_i}{e_j}$, where $e_i$ is the number of edits of editor $i$ and $e_j$ is the number of edits of editor $j$. In essence, we assume that an editor who has 10 edits compares to one with 100 edits the same way that an editor with 1,000 edits compares to one with 10,000. 

Save the edge data in a `pickle` file, which you will need for the next task.

### 2. If $A$ reverted $B$, did $B$ revert $A$?

Temporal motifs are classes of event sequences that are similar not only in the topology but also in the temporal order of the events. Our aim is to identify the two-event temporal motifs in which after $A$ reverts $B$, $B$ reverts $A$ back ($AB–BA$). To identify the motifs, use the data you pickled in the previous task. Then look at every revert and identify if and when a response occurs, restricted to a time window of 24?hours. Ignore the article titles — we are agnostic as to whether the response happens in the same or in different articles. Further, it does not matter whether the response occurs immediately after the original revert or alternatively, the reverter and the reverted are involved in other reverts in-between the original revert and the response. If more than one response occurs within 24 hours, consider only the first one as part of the motif.

When you identify a motif, save information about the edges that allows you to identify them later. Save this information in a `pickle` file, which you will need for the next task.

### 3. Are $A$ and $B$ more similar in status than expected?

Social comparison theory states that people strive to gain accurate self-evaluations and as a result, they tend to compare themselves to those who are similar. But since focus on relative performance heightens feelings of competitiveness, rivalry is stronger among similar individuals. This leads us to expect that the editors involved in the $AB–BA$ motif tend to be closer in status than expected.

To find evidence that retaliation is more likely among status-equals, we need to compare the status difference between ediotrs involved in $AB–BA$ motifs with the status difference between editors involved in any other type of revert.

To do this, use the data you pickled in the previous two tasks and the `matplotlib` library to plot a histogram of $s_A - s_B$ for reverts that are part of $AB–BA$ motifs on top of a histogram of $s_i - s_j$ for all other reverts. Then estimate the mean $s_A - s_B$ and the mean $s_i - s_j$ and print them. In a comment, use a couple of sentences to summarize what you observe.
