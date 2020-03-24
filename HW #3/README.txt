This is the README file for A0183821E's submission

== Python Version ==

I'm using Python Version 3.7.3 for this assignment.

== General Notes about this assignment ==

The indexing phase generates postings lists that contain a tuple of two values (docID, normalized_tf) instead of just the docID in HW2. To save runtime during searches, the normalized_tf value stored in the postings is the value generated after the logarithm operation on the raw value, before being normalized.

Additionally, we store a mapping from the list of all docIDs to their idf values with the dictionary. Again, these values are the values generated after the operation log(N/idf) is applied to the raw values. Thus, we move the complexity of both log operations to the indexing phase and speed up searching.

During the searching phase, we first generate the raw tf values for the query by word-tokenizing it via nltk. Following this, we calculate 1 + log(tf) for each term and multiply it with idf values, before normalizing it. Then, retrieve the postings list for each term and accumulate the scores for each term using the cosine-score algorithm described in the lecture.

Finally, we turn the resulting (docID, score) pairs into a heap with ordering based on max score, followed by min docId. After this, we simply perform python heapq n_smallest operation to return the top 10 docIds and print them out to the output file.

== Files included with this submission ==

- index.py - wrapper script that does the command line i/o and passes the args to build_index.py
- dictionaries.py - contains the implementation of a dictionary object
- postings.py - contains the implementation of a postings file object
- search.py - does the command line i/o and passes each query to search_engine.py for evaluation.
              Also writes the results to output file.
- searcher.py - utility class that runs the cosine-score algorithm on the input query.
- utils.py - utility class that has low-level operations for calculation of tf and idf values. 

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0183821E, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0183821E, did not follow the class rules regarding homework
assignment, because of the following reason:

== References ==

None