import pickle

with open('mat_data.pickle', 'rb') as file:
    mat_data = pickle.load(file)
with open('model_knn.pickle', 'rb') as file:
    model_knn = pickle.load(file)
with open('title_to_index.pickle', 'rb') as file:
    title_to_index = pickle.load(file)

print("Please enter your favourite movie:")
input_movie_title = input()
if input_movie_title in title_to_index.keys():
    input_movie_index = title_to_index.get(input_movie_title)

    no_recommendations = 1
    distances, indices = model_knn.kneighbors(mat_data[input_movie_index], n_neighbors=no_recommendations+1)

    top_recommended_movie_index = indices[0][1]
    for movie_title in title_to_index.keys():
        if title_to_index.get(movie_title) == top_recommended_movie_index:
            top_recommended_movie_title = movie_title
    print(f"Your top recommended movie is titled '{top_recommended_movie_title}' as it is the most similar movie to "
          f"your favourite movie '{input_movie_title}'.")
else:
    print(f"'{input_movie_title}' is not in the dataset. Next time please enter the title of a movie that is in the "
          f"dataset.")
