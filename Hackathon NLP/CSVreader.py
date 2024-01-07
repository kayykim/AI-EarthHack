#Goes through all the problem and solutions one by one
import csv
import os

def display_data():
    with open('data.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for entry in reader:
            input()
            os.system('clear')  
            print(f"Index: {entry[0]}\n")
            print(f"Problem: {entry[1]}\n")
            print(f"Solution: {entry[2]}")

if __name__ == "__main__":
    display_data()
