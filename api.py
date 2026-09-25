import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys

app = Flask(__name__)
CORS(app)

# Load data and prepare the model
data_path = 'tamil_movies.csv'
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    print(f"Error: Could not find '{data_path}'.")
    sys.exit(1)

def combine_features(row):
    return str(row['genres']) + " " + str(row['director']) + " " + str(row['lead_actor']) + " " + str(row['description'])

df['combined_features'] = df.apply(combine_features, axis=1)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, df, cosine_sim):
    try:
        idx = df[df['title'].str.lower() == title.lower()].index[0]
    except IndexError:
        return {"error": f"Movie '{title}' not found in the dataset."}

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    
    # Return list of movie objects with their details
    recommendations = []
    for i in movie_indices:
        movie = df.iloc[i]
        recommendations.append({
            "title": movie['title'],
            "genres": movie['genres'],
            "director": movie['director'],
            "lead_actor": movie['lead_actor'],
            "description": movie['description']
        })
    return {"recommendations": recommendations}

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = df[['title', 'genres']].to_dict(orient='records')
    return jsonify({"movies": movies})

@app.route('/api/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "No title provided."}), 400
    
    result = get_recommendations(title, df, cosine_sim)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
