import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse
import sys

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'.")
        sys.exit(1)

def combine_features(row):
    # Combine relevant features into a single string
    features = str(row['genres']) + " " + str(row['director']) + " " + str(row['lead_actor']) + " " + str(row['description'])
    return features

def get_recommendations(title, df, cosine_sim):
    # Get the index of the movie that matches the title
    try:
        idx = df[df['title'].str.lower() == title.lower()].index[0]
    except IndexError:
        return f"Error: Movie '{title}' not found in the dataset."

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 5 most similar movies (ignoring the first one as it's the movie itself)
    sim_scores = sim_scores[1:6]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 5 most similar movies
    return df['title'].iloc[movie_indices].tolist()

def main():
    parser = argparse.ArgumentParser(description="Tamil Movie Recommendation System (Content-Based)")
    parser.add_argument("movie_title", type=str, nargs='?', help="The title of the movie you liked (e.g., 'Vikram')")
    parser.add_argument("--list", action="store_true", help="List all available movies in the dataset")
    args = parser.parse_args()

    data_path = 'tamil_movies.csv'
    df = load_data(data_path)

    if args.list:
        print("Available Movies:")
        for title in df['title']:
            print(f"- {title}")
        return

    if not args.movie_title:
        print("Please provide a movie title. Use --list to see all available movies.")
        print("Example usage: python recommend.py \"Vikram\"")
        return

    # Create combined features
    df['combined_features'] = df.apply(combine_features, axis=1)

    # Initialize TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    # Fit and transform the data
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])

    # Calculate Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get Recommendations
    print(f"\nFinding recommendations for '{args.movie_title}'...\n")
    recommendations = get_recommendations(args.movie_title, df, cosine_sim)

    if isinstance(recommendations, str) and recommendations.startswith("Error"):
        print(recommendations)
    else:
        print("We recommend you watch:")
        for i, movie in enumerate(recommendations, 1):
            print(f"{i}. {movie}")
        print()

if __name__ == "__main__":
    main()
