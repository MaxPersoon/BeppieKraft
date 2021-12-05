import numpy as np
import pandas as pd

files = ['combined_data_1.txt', 'combined_data_2.txt', 'combined_data_3.txt', 'combined_data_4.txt']
contents = []

for file in files:
    with open(file) as f:
        contents.append(f.readlines())
        print('Finished loading file', file)

no_reviews_per_movie = []

file_counter = 0
movie_counter = 0
for file in contents:
    for line in file:
        if ":" in line:
            movie_counter += 1
            no_reviews_per_movie.append(0)
        else:
            no_reviews_per_movie[movie_counter-1] += 1
    print("Extracted number of ratings per movie from file", files[file_counter])
    file_counter += 1

average_no_ratings = sum(no_reviews_per_movie) / len(no_reviews_per_movie)
print("Average number of ratings per movie =", average_no_ratings)

offset = 2855
interval = [average_no_ratings - offset, average_no_ratings + offset]
movies = []  # movieIDs
total_no_reviews = 0
for i in range(len(no_reviews_per_movie)):
    no_reviews = no_reviews_per_movie[i]
    if interval[0] <= no_reviews <= interval[1]:
        movies.append(i + 1)
        total_no_reviews += no_reviews

print("Selected interval =", interval)
print("Selected % of original dataset =", total_no_reviews / sum(no_reviews_per_movie) * 100)

file_counter = 0
users = []  # userIDs
in_dataset = False
for file in contents:
    for line in file:
        if ":" in line:
            if int(line.split(":")[0]) in movies:
                in_dataset = True
            else:
                in_dataset = False
        else:
            if in_dataset:
                users.append(int(line.split(",")[0]))
    print("Extracted users from file", files[file_counter])
    file_counter += 1
users = list(set(users))

no_reviews_per_user = [0] * len(users)

file_counter = 0
in_dataset = False
for file in contents:
    for line in file:
        if ":" in line:
            if int(line.split(":")[0]) in movies:
                in_dataset = True
            else:
                in_dataset = False
        else:
            if in_dataset:
                user = int(line.split(",")[0])
                try:
                    index = users.index(user)
                    no_reviews_per_user[index] += 1
                except ValueError:
                    pass
    print("Extracted users from file", files[file_counter])
    file_counter += 1

no_users = len(users)
no_movies = len(movies)
print("Number of users =", no_users)
print("Number of movies =", no_movies)

data = np.zeros((no_users, no_movies))
file_counter = 0
column_index = 0
line_counter = 0
for file in contents:
    for line in file:
        if ":" in line:
            movie = int(line.split(":")[0])
            try:
                column_index = movies.index(movie)
                in_dataset = True
            except ValueError:
                in_dataset = False
        else:
            if in_dataset:
                split = line.split(",")
                user = int(split[0])
                try:
                    row_index = users.index(user)
                    data[row_index][column_index] = int(split[1])
                except ValueError:
                    pass
        line_counter += 1
        if line_counter % 1000000 == 0:
            print("Surpassed line", line_counter)
    print("Extracted ratings from file", files[file_counter])
    file_counter += 1
