import csv
import os

def display_data():
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header if present
        for entry in reader:
            input("Press Enter to view the next entry...")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
            print(f"Index: {entry[0]}\n")
            print(f"Problem: {entry[1]}\n")
            print(f"Solution: {entry[2]}")

if __name__ == "__main__":
    display_data()
