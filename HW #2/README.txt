This is the README file for A0183821E's submission

== Python Version ==

I'm using Python Version 3.7.3 for this assignment.

== General Notes about this assignment ==

For indexing, I iterate through all documents, tokenise the document, and each token is processed into a term with stemming and lowercasing. This term is then added to the dictionary, while every doc_id is added to the postings list. I also maintain a counter starting from 1, named as `offset`. This provides a unique identifier for each term in both the dictionary and posting. 

During indexing, both dictionary and postings are in memory. During the indexing, each term in the dictionary is associated with the unique identifier. This identifier is later replaced by the byte offset in the postings file, once the file has been saved to disk. For postings, each identifier is associated with a SkipList object, which contains all the docID of documents that the term is found in. The dictionary and postings are serialised and deserialised using pickle. 

For searching, I implemented the shunting yard algorithm to parse queries. Queries are then evaluated by processing the postfix expression. The posting lists (SkipList) are loaded for every term in the expression, and then the boolean operator ("AND", "OR", "NOT") is executed as intended. A special condition is implemented so as to facilitate faster "AND NOT" queries as taught in the lecture. The python garbage collector is explicitly called after every line of query so that postings do not get too large in memory. 

== Files included with this submission ==

index.py: Contains code for going through all documents and indexing them
search.py: Contains code for performing search
dictionary.py: Code for the Dictionary class
postings.py: Code for the Postings class
skiplist.py: Code for the SkipList class, represents a SkipList
searcher.py: Code for Searcher class, a utility class that has methods to perform query parsing, query proessing and search operations


== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0183821E, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0183821E, did not follow the class rules regarding homework
assignment, because of the following reason: