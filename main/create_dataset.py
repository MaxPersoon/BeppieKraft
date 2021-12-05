import numpy as np
import pandas as pd

files = ['combined_data_1.txt', 'combined_data_2.txt', 'combined_data_3.txt', 'combined_data_4.txt']
contents = []

no_reviews_per_movie = []

for file in files:
    with open(file) as f:
        for line in f.readlines():
            if ":" in line:
                no_reviews_per_movie.append(0)
            else:
                no_reviews_per_movie[len(no_reviews_per_movie) - 1] += 1
        print("Extracted number of reviews per movie from file", file)

average_no_reviews = sum(no_reviews_per_movie) / len(no_reviews_per_movie)
print("Average number of reviews per movie =", average_no_reviews)

offset = 2855
interval = [average_no_reviews - offset, average_no_reviews + offset]
movies = []  # movieIDs
total_no_reviews = 0
for i in range(len(no_reviews_per_movie)):
    no_reviews = no_reviews_per_movie[i]
    if interval[0] <= no_reviews <= interval[1]:
        movies.append(i + 1)
        total_no_reviews += no_reviews
print("Filtered set of movies")

print("Selected interval =", interval)
print("Selected % of original dataset =", total_no_reviews / sum(no_reviews_per_movie) * 100)

users = []  # userIDs
in_dataset = False
for file in files:
    with open(file) as f:
        for line in f.readlines():
            if ":" in line:
                if int(line.split(":")[0]) in movies:
                    in_dataset = True
                else:
                    in_dataset = False
            else:
                if in_dataset:
                    users.append(int(line.split(",")[0]))
        print("Extracted relevant users from file", file)
users = list(set(users))

random_numbers = np.random.rand(len(users))
filtered_users = []
for i in range(len(random_numbers)):
    if random_numbers[i] < 0.1:
        filtered_users.append(users[i])
users = filtered_users
print("Filtered set of users")

no_users = len(users)
no_movies = len(movies)
print("Number of users =", no_users)
print("Number of movies =", no_movies)

data = np.zeros((no_users, no_movies))
column_index = 0
line_counter = 0
for file in files:
    with open(file) as f:
        for line in f.readlines():
            if ":" in line:
                movieID = int(line.split(":")[0])
                try:
                    column_index = movies.index(movieID)
                    in_dataset = True
                except ValueError:
                    in_dataset = False
            else:
                if in_dataset:
                    split = line.split(",")
                    userID = int(split[0])
                    try:
                        row_index = users.index(userID)
                        data[row_index][column_index] = int(split[1])
                    except ValueError:
                        pass
            line_counter += 1
            if line_counter % 1000000 == 0:
                print("Surpassed line", line_counter)
        print("Extracted relevant reviews from file", file)
print("Created dataset")
df = pd.DataFrame(data)
df.columns = movies
df.index = users
df.to_csv("filtered_dataset.csv")
