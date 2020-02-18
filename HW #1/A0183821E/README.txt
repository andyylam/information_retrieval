This is the README file for A0183821E's submission

== Python Version ==

I'm using Python Version 3.7.3 for this assignment.

== General Notes about this assignment ==

I completed the implementation of the two skeleton methods without additional files. I have added helper methods that abstract out certain operations for better code readability. The language models are represented by nested python dictionaries. I lowercased all characters so that characters of starting words and names do not affect the vocabulary, which led to better results. I also padded the included the <START> and <END> tags, which helped reduce the THRESHOLD_VALUE. 

build_LM():
Builds the language model for each label. Takes in file name that is then opened and parsed line by line. 
- It uses the nltk API for tokenisation of the lines. These tokens are then counted and stored in the model dictionaries.
- The model is then smoothed (Add One/ Laplace Smoothing) and converted to a probabilistic model. The smoothing and conversion is abstracted out to helper methods. 

test_LM(): 
Test the language model on new strings. 
- The unigram model of calculating the probablities is used (completely independent tokens). When calculating probabilities, some values were so small they became zero. My solution to this was to use the logarithm of these probabilities and take their sum instead. 
- The proportion of quadgrams missing is calculated from the number of invalid quadgrams (quadgrams that are not in the vocabulary) divided by the total number of quadgrams. A hard coded THRESHOLD_VALUE is used to determine the allowed proportion of invalid grams. This value is derived from trial-and-error experiments to find its lowest possible value. If the proportion of quadgrams missing is less than the THRESHOLD_VALUE, then LM contains insufficient information and therefore the predicted language is OTHER. I implemented the threshold system myself, but the idea itself is not mine (from StackOverflow).


== Files included with this submission ==

build_test_LM.py - builds and tests the LM
ESSAY.txt - contains answers to the essay questions
README.txt - this file

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0183821E, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0183821E, did not follow the class rules regarding homework
assignment, because of the following reason:

== References ==

- Generic resources from StackOverflow for python. 