import nltk
import os
import string
import csv
from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CATEGORIES = ['sustainability','feasability','technological innovation','circular economics','innovation','breakthrough'] 

def main():
    #load data in raw form
    spam = []
    data = [["Problem", "solution"]] #1-indexed

    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for entry in reader:
            data.append([entry[1],entry[2]])

    #remove all spam, vague, repetative, genaric, poorly written solutions
    for idx, d in enumerate(data):
        if filter_idea(d[0], d[1]):
            print("Index: ", idx, "\n")
            spam.append(idx)
    

    for index in sorted(spam, reverse = True):
        del data[index]

    data = tokenize(data)
    #2Vec to find strong correlations between certain topics and solutions



def tokenize(data):
    for idx, pair in enumerate(data):
        p_words = data[idx][0].lower().split()
        s_words = data[idx][1].lower().split()

        p_words = [word.strip(string.punctuation) for word in p_words if word not in string.punctuation]# and word not in nltk.corpus.stopwords.words("english")]
        s_words = [word.strip(string.punctuation) for word in s_words if word not in string.punctuation]# and word not in nltk.corpus.stopwords.words("english")]
        
        data[idx] = [p_words, s_words]
    return data

def relationship_scoring(data, categories):
    scores = [0 for _ in categories] # consider how to deal with outliers also similars like economics & economy

    for idx, category in enumerate(categories):

        sample = open(f"articles/{category}.txt")
        s = sample.read()
        f = s.replace("\n", )
        info = []
        for i in sent_tokenize(f):
            temp = []
            for j in word_tokenize(i):
                temp.append(j.lower())
            data.append(temp)
        model1 = gensim.models.Word2Vec(info, min_count = 1, vector_size = 100, window = 5)


        for word in data:
            scores[idx] += model1.wv.similarity(word,category)#modify addition of score based on algo

        scores[idx] /= len(data) #average data (will need to change model later)

def filter_idea(problem, solution): #input is raw data
    #ADD TOPIC WORDS TO PROBLEM************
    topics = []
    #weak words
    weak_words = ['can', 'could', 'might', 'may', 'maybe', 'perhaps', 'possibly', 'likely', 'seems', 'appears', 'potentially', 'probably', 'generally', 'typically', 'suggests']
    weak_words = ' '.join(word.lower() for word in weak_words)

    #spam algo
    solution_length = len(solution.split())
    problem_length = len(problem.split())

    vectorizer = CountVectorizer().fit_transform([problem,solution])
    vectors = vectorizer.toarray()
    similarity_score = cosine_similarity(vectors)[0][1]#0-1 scoring, 0 no similarities, 1 identical

    weak_count = 0
    for word in solution.split():
        if word in weak_words.split():
            weak_count += 1

    #1) not enough info
    if solution_length < 25:
        print("TOO SHORT", solution_length)
        return True

    #2) weak tone
    if weak_count / solution_length > 0.05:
        print("WEAK:", weak_count)
        return True

    topic_score = 0 # EDIT
    #3) off-topic
    # if (similarity_score + topic_score < 0.3 or similarity_score > 0.8) and solution_length < 40:
    #     print("Indentical or Completely Irrelevent")
    #     return True
    #off-topic (index is TOO LOW or unrelated to topic)
    #use relationship matrix to figure out this
        
    
    # if(similarity_score < 0.05 and solution_length < 40):
    #     print("Low relationship")
    #     return True 
    

    #4) spelling errors amount is too high/poor grammar



    return False

# scores the relationship index between a problem and solution
def similarity(problem, solution, sensitivity):
    score = 0
    return score


def scoring(problem, solution):
    score = 0
    socre += similarity(problem, solution)

    return score

def result(spam_labels, data):
    score = 0
    return score 


if __name__ == "__main__":
    main()
