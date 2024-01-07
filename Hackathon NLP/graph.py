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
        
        if category == 3: #unique range since word in more niche, lower correlation score
            create_buckets(points, 0.01, 20, category)
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
                lower, upper = map(float, bucket.split('-'))
                if lower <= value < upper:
                    buckets[bucket] += 1
                    break
                
    buckets = dict(buckets)
    labels = list(buckets.keys())
    values = list(buckets.values())

    plt.figure(figsize=(10, 8))  
    plt.bar(labels, values)
    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.title(f'data distribution of {CATEGORIES[category]}')
    plt.xticks(rotation=90)  
    plt.show()


if __name__ == "__main__":
    main()
