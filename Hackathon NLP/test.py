import csv
import os
catfile = open("categoryfil.txt", "x")
key_words = ["fashion", "construction", "energy", "fuel", "plastic waste", "e-waste", "paper waste", "waste"]
key_word_list = []

def display_data():
    with open('data.csv', newline='', encoding = "utf8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header if present
        for entry in reader:
            entry[1] = entry[1].split(" ")
            print(entry[1])
            temp = []
            for ite in entry[1]:
                for word in key_words:
                    if (ite == word):
                        temp.append(word)

            if (len(temp)!=0): 
                key_word_list.append(temp[0])
                catfile.write(str(entry))
                catfile.write(str(temp[0]))
                catfile.write('\n')
            else:
                key_word_list.append(temp)
                catfile.write(str(entry))
                catfile.write("check")
                catfile.write('\n')
            #print(key_word_list)

if __name__ == "__main__":
    display_data()



