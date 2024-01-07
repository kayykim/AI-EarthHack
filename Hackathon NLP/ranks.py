import heapq

# Read data from the file
CATEGORIES = ['sustainability','feasible','innovative','novelty']
def main():
    data = []

    with open('scores.txt', 'r') as file:
        file.readline() #ignore header line
        for line in file:
            line = line.strip(']\n')
            line = line.split(', [')
            line[1] = line[1].split(',')
            data.append(line) #line is now a list of [index, [values]]
        
    file.close()


    for i in range(len(CATEGORIES)):
        print(f"\nCategory: {CATEGORIES[i]}")
        sol = (get_indices_with_largest_element(data, i, 10))
        for rank, info in enumerate(sol):
            print(f"Rank {rank}: Index {info[0]}")


def get_indices_with_largest_element(data, position, n):
    return heapq.nlargest(n, data, key=lambda x: float(x[1][position]))

if __name__ == "__main__":
    main()


