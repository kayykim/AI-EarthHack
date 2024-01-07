import matplotlib.pyplot as plt

# Read data from the file
CATEGORIES = ['sustainability','feasible','innovative','novelty']
data = []

def main():
    with open('scores.txt', 'r') as file:
        file.readline() #ignore header line
        for line in file:
            line = line.strip(']\n')
            line = line.split(', [')
            line[1] = line[1].split(',')
            data.append(line) #line is now a list of [index, [values]]
        
    file.close()
            
    #graph output
    for category in range(len(CATEGORIES)):
        points = []
        for i in range(len(data)):
            points.append(float(data[i][1][category]))
        
        if category == 3:
            create_decimal_buckets(points, 0.01, 20, category)
        else:
            create_buckets(points, 2, 20, category)
        

def create_buckets(points, bucket_size, num_buckets, category):
    buckets = {str(i * bucket_size) + '-' + str((i + 1) * bucket_size): 0 for i in range(num_buckets)}
    buckets[str(bucket_size * num_buckets) + '+'] = 0  
    
    for value in points:
        if value > bucket_size * num_buckets:
            buckets[str(bucket_size * num_buckets) + '+'] += 1
        else:
            for bucket in buckets:
                if bucket != str(bucket_size * num_buckets) + '+':  
                    lower, upper = map(int, bucket.split('-'))
                    if lower <= value < upper:
                        buckets[bucket] += 1
                        break

    # Sorting the buckets by their keys
    sorted_buckets = sorted(buckets.items(), key=lambda item: float(item[0].split('-')[0]) if item[0] != str(bucket_size * num_buckets) + '+' else float('inf'))
    buckets = dict(sorted_buckets)

    # Extracting bucket labels and values
    labels = list(buckets.keys())
    values = list(buckets.values())

    # Creating the bar graph
    plt.figure(figsize=(10, 5))  # Adjust figure size
    plt.bar(labels, values)
    plt.xlabel('Ranges')
    plt.ylabel('Frequency')
    plt.title(f'data distribution of {CATEGORIES[category]}')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.show()

def create_decimal_buckets(points, bucket_size, num_buckets, category):
    buckets = {str(i * bucket_size) + '-' + str((i + 1) * bucket_size): 0 for i in range(num_buckets)}
    buckets[str(bucket_size * num_buckets) + '+'] = 0  
    
    for value in points:
        if value > bucket_size * num_buckets:
            buckets[str(bucket_size * num_buckets) + '+'] += 1
        else:
            for bucket in buckets:
                if bucket != str(bucket_size * num_buckets) + '+': 
                    lower, upper = map(float, bucket.split('-'))
                    if lower <= value < upper:
                        buckets[bucket] += 1
                        break

    sorted_buckets = sorted(buckets.items(), key=lambda item: float(item[0].split('-')[0]) if item[0] != str(bucket_size * num_buckets) + '+' else float('inf'))
    buckets = dict(sorted_buckets)

    labels = list(buckets.keys())
    values = list(buckets.values())

    plt.figure(figsize=(10, 5))  
    plt.bar(labels, values)
    plt.xlabel('Ranges')
    plt.ylabel('Frequency')
    plt.title(f'data distribution of {CATEGORIES[category]}')
    plt.xticks(rotation=90)  
    plt.show()


if __name__ == "__main__":
    main()
