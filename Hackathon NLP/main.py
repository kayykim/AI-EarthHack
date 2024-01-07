import nltk
import os
import string
import csv
import sys
from colorama import Fore
from gensim.models import Word2Vec
import gensim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import KeyedVectors

CATEGORIES = ['sustainability','feasible','innovative','novelty']
TESTBATCH = 10

def main():
    os.system('clear')
    print("Preparing Data\n")
    data = preprocessing() #1-indexed

    #load data in raw form
    spam = []

    #remove all spam, vague, repetative, genaric, poorly written solutions
    for idx, d in enumerate(data):
        if filter_idea(d[0], d[1]):
            #print("Index: ", idx, "\n") #TEST SPAM DETECTION
            spam.append(idx)
    
    for index in sorted(spam, reverse=True):
        del data[index]

    #data = tokenize(data)



    #2Vec to find strong correlations between certain topics and solutions
    print("Calculating Scores")
    with open('scores.txt','w') as file1, open('topsentences.txt','w') as file2:
        for category in CATEGORIES:
            file1.write(f"{category} ")
            file2.write(f"{category} ")      
        file1.write("\n")
        file2.write("\n")
        for idx, info in enumerate(data):
            score, best = relationship_scoring(info[1])
            file1.write(f"{score}\n")
            file2.write(f"{best}\n")
            if idx == TESTBATCH:
                break
            show_progress(idx + 1, len(data))

    print("\nData in scores.txt and topsentences.txt")

def preprocessing():
    data = [["problem", "solution"]] #1-indexed
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for entry in reader:
            data.append([entry[1],entry[2]])
    return data

def tokenize(sentence):
    words = sentence.lower().split()
    words = [word.strip(string.punctuation) for word in words if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")]
    return words

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
    if solution_length < 20:
        #print("TOO SHORT", solution_length)
        return True

    #2) weak tone
    if weak_count / solution_length > 0.05:
        #print("WEAK:", weak_count)
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

def relationship_scoring(solution): #raw data
    scores = [0 for _ in CATEGORIES] # consider how to deal with outliers also similars like economics & economy

    # Load pre-trained word vectors
    word_vectors = KeyedVectors.load_word2vec_format('Word2VecTest/GoogleNewsSmall.bin', binary=True)

    scoring = 0
    
    best = [0 for i in range(len(CATEGORIES))]
    current_sentence_scores = [0 for i in range(len(CATEGORIES))]
    solution = solution.split('.')
    for idx, sentence in enumerate(solution):
        solution[idx] = tokenize(sentence)

    # Check similarity between words
    count = 0
    for cur, sentence in enumerate(solution): #sentence is a list of words
        for word in sentence: 
            for idx, category in enumerate(CATEGORIES): #rank eachword against its cateogry
                try:
                    similarity = word_vectors.similarity(category, word)
                    scores[idx] += similarity
                    current_sentence_scores[idx] += similarity
                except:
                    continue
            count += 1

        for idx, sentences in enumerate(best):
            if current_sentence_scores[idx] > best[idx]:
                best[idx] = cur #find top rated sentences

        current_sentence_scores = [0 for i in range(len(CATEGORIES))]
    scores[idx] /= count #average the scores

    return scores, best


def show_progress(current_solution, total_solution):
    progress = current_solution / total_solution
    bar_length = 40
    block = int(round(bar_length * progress))
    
    progress_bar = "[" + Fore.GREEN + "░" * block + Fore.WHITE + "-" * (bar_length - block) + "]"
    sys.stdout.write(f"\rLoading: {progress_bar} {progress*100:.2f}% {current_solution}/{total_solution}")
    sys.stdout.flush()

if __name__ == "__main__":
    main()


