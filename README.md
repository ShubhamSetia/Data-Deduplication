# Data-Deduplication

# Problem Statement 
Variation in names leads to difficulty in identifying a unique person and hence deduplication
of records is an unsolved challenge. The problem becomes more complicated in cases where
data is coming from multiple sources. Following variations are same as Vladimir Frometa:
* Vladimir Antonio Frometa Garo
* Vladimir A Frometa Garo
* Vladimir Frometa
* Vladimir Frometa G
* Vladimir A Frometa
* Vladimir A Frometa G

Train a model to identify unique patients in the dataset

# Dataset Description 
Dataset contains following fields:
* ln: Last name of the patient
* dob: Date of Birth of the patient
* gn: Gender of the patient
* fn: First Name of the patient

# Approach 
* If two entries have either unequal dob or gender then they refer to two different patient
* If two entries have same dob and gender then we check the similarity of the names.Similarity between two names lies between 0.0 and 1.0. Similarity score of 0.0 means two names are completely different and similarity score of 1.0 means they are completely same.
* We fix a threshold value between 0.0 and 1.0. If score is less then that threshold then they refer to different person else they refer to same patient and we remove the duplicate entry.

# Similarity Calculation Algorithm 
Input: two strings name1, name2 <br/>
Output: similarity score between 2 names<br/>
* If two strings are exactly same then we return 1.0
* Else If either of the string is empty we return 0.0
* Else we initialize max (max similarity score) to 0.0 and compute similarity score.
* I have defined 10 different functions to transform each name with a penalty score based on their importance. 
* These functions are applied on both the names in combination and penalty score and resultant name are stored.
* By applying in combinations means that in first iteration each will be applied individually, in second iteration two taken together, in third iterations three taken togther and so on. In final iteration all 10 are applied together.
* After end of each iteration I am storing the resultant string and the total penalty score in a set for each name.
* Then i run two for loop to iterate over the two set if they have same string then i compute score as 1 - penalty1 - penalty2. 
* If score > max then max = score
* Return max


# How to run the program:
`python main.py` <br/>

Tools Used: 
* python 3.6
* pandas module
* re module
* itertools module

# File Descriptions:

* suffixes.txt: contains list of suffixes 
* prefixes.txt: contains list of prefixes
* compound_prefixes: contains list of compound prefixes
* name_parser.py: helps in name parsing like splitting name into 4 parts prefix, first part, last part, suffix and other utility functions
* similarity_evaluation.py: contains implementation of similarity function
* main.py: implements the functionality of reading the file and performing deduplication
* Deduplication Problem - Sample Dataset.csv: input dataset provided by innovaccer. I have added few more entries to test my algorithm
* Output.csv: contains the output of the algorithm.