# Kollywood Movie Recommender 🎬

A modern, visually stunning movie recommendation system built for Tamil movies. It suggests movies you might like based on the genres, director, lead actor, and plot description of a movie you already enjoy.

## 🌟 Features

- **Content-Based Filtering**: Recommends movies by analyzing textual features (Director, Lead Actor, Genres, Description) using **TF-IDF Vectorization** and **Cosine Similarity**.
- **Modern UI/UX**: A beautiful frontend featuring glassmorphism, smooth animations, and glowing aesthetics.
- **Real-time Search**: Search for your favorite movies with a responsive autocomplete dropdown.

## 🛠️ Technology Stack

**Frontend:**
- [React.js](https://reactjs.org/) (via [Vite](https://vitejs.dev/))
- Vanilla CSS (Glassmorphism design)
- [Lucide-React](https://lucide.dev/) (Icons)

**Backend:**
- [Flask](https://flask.palletsprojects.com/) (Python API)
- [Pandas](https://pandas.pydata.org/) (Data manipulation)
- [Scikit-learn](https://scikit-learn.org/) (Machine Learning logic)

## 🚀 Getting Started

To run this project locally, you will need to start both the Python backend API and the React frontend development server.

### 1. Start the Backend API

1. Ensure you have Python installed.
2. Open a terminal in the root directory of this project.
3. Install the required Python dependencies:
   ```bash
   pip install pandas scikit-learn flask flask-cors
   ```
4. Run the Flask API server:
   ```bash
   python api.py
   ```
   *The server will start on `http://localhost:5000`.*

### 2. Start the Frontend Application

1. Open a **new terminal** and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install the required Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open your browser and go to `http://localhost:5173` to see the application!

## 📂 Project Structure

- `api.py`: The Flask API backend serving movie data and generating recommendations.
- `tamil_movies.csv`: The dataset containing movie information. Feel free to add more movies here!
- `recommend.py`: A command-line version of the recommendation script.
- `frontend/`: Contains the React/Vite web application source code.
