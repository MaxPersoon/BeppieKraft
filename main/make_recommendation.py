import pickle

with open('mat_data.pickle', 'rb') as file:
    mat_data = pickle.load(file)
with open('model_knn.pickle', 'rb') as file:
    model_knn = pickle.load(file)
with open('title_to_index.pickle', 'rb') as file:
    title_to_index = pickle.load(file)

print("Please enter your favourite movie:")
input_movie = input()
input_index = title_to_index.get(input_movie)

no_recommendations = 10
distances, indices = model_knn.kneighbors(mat_data[input_index], n_neighbors=no_recommendations+1)

print(f"Top {no_recommendations} recommendations:")
for i in range(1, len(indices[0])):
    movie_index = indices[0][i]
    for movie_title in title_to_index.keys():
        if title_to_index.get(movie_title) == movie_index:
            break
    print(f"#{i}: '{movie_title}' with distance {distances[0][i]}")
