import tkinter as tk
from tkinter import ttk
import time
import threading
import openai
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

openai.api_key = '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'

class ExerciseRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Recommendation App")

        # Label and Entry for entering the category
        tk.Label(root, text="Enter Category:").pack(pady=10)
        self.category_entry = tk.Entry(root)
        self.category_entry.pack(pady=10)

        # Button to get recommendations
        tk.Button(root, text="Get Recommendations", command=self.get_recommendations).pack(pady=10)

        tk.Label(root, text="Choose Exercise:").pack(pady=5)
        self.exercise_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5, width=50)
        self.exercise_listbox.pack(pady=5)

        # Text widget to display recommendations
        self.recommendations_text = tk.Text(root, height=10, width=50)
        self.recommendations_text.pack(pady=10)

        tk.Button(root, text="Start Timer", command=self.show_timer_page).pack(pady=10)

    def get_recommendations(self):
        selected_exercises = [self.exercise_listbox.get(idx) for idx in self.exercise_listbox.curselection()]

        # OpenAI GPT-3 prompt
        prompt = f"Generate a workout routine including exercises: {', '.join(selected_exercises)}."

        # Generate content using GPT-3
        generated_content = self.generate_content(prompt)

        # Display the generated content
        self.show_generated_content(generated_content)
    
    def generate_content(self, prompt):
        # Use the openai.ChatCompletion.create method for GPT-3.5
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    
    def show_generated_content(self, content):
        # Open a new window to display the generated content
        content_window = tk.Toplevel(self.root)
        content_window.title("Generated Content")

        # Display the generated content
        tk.Label(content_window, text="Generated Workout Routine:").pack(pady=5)
        tk.Label(content_window, text=content).pack(pady=5)

    def show_timer_page(self):
        # Get the selected exercises from the listbox
        selected_exercises = [self.exercise_listbox.get(idx) for idx in self.exercise_listbox.curselection()]

        # Open a new window for the timer page
        self.timer_window = tk.Toplevel(self.root)
        self.timer_window.title("Workout Timer")
        tk.Label(self.timer_window, text="Selected Exercises:").pack(pady=5)
        tk.Label(self.timer_window, text=", ".join(selected_exercises)).pack(pady=5)
        self.start_timer(selected_exercises, 0)  # Start with the first exercise

    def start_timer(self, exercises, index):
        if index < len(exercises):
            current_exercise = exercises[index]
            tk.Label(self.timer_window, text=f"Current Exercise: {current_exercise}").pack(pady=5)
            self.timer_label = tk.Label(self.timer_window, text="")
            self.timer_label.pack(pady=5)
            self.update_timer(1000, exercises, index)  # 900 seconds = 15 minutes
        else:
            self.timer_window.destroy()  # Close the timer window when all exercises are done

    def update_timer(self, duration, exercises, index):
        if duration > 0:
            self.timer_label.config(text=f"Time remaining: {duration // 60} min {duration % 60} sec")
            duration -= 1
            self.timer_label.after(1000, lambda: self.update_timer(duration, exercises, index))
        else:
            self.timer_label.config(text="Workout Complete!")
            self.timer_window.after(2000, lambda: self.start_timer(exercises, index + 1))

    
if __name__ == "__main__":
    # Load the dataset
    dataset_path = 'workout_dataset.csv'
    df = pd.read_csv(dataset_path)

    # Preprocess and Vectorize Text Data
    df['exercise_description'] = (
        df['Exercise'] + ' ' +
        df['Types'].str.strip() + ' ' +
        df['Intensity'] + ' ' +
        df['Equipment'] + ' ' +
        df['Difficulty level']
    )

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['exercise_description'])

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Function to get recommendations
    def get_category_recommendations(category, cosine_sim=cosine_sim):
        # Check if the category exists in the DataFrame
        if category not in df['Types'].values:
            return "Category not found in the dataset"

        # Get the indices of exercises that match the category
        indices = df[df['Types'] == category].index.tolist()

        # Check if the indices are not empty
        if not indices:
            return "No exercises found in the dataset for the given category"

        # Aggregate cosine similarity scores for exercises in the specified category
        aggregate_scores = cosine_sim[indices].sum(axis=0)

        # Get the indices of the top 10 most similar exercises
        top_indices = aggregate_scores.argsort()[::-1][:5]

        # Return the top 10 most similar exercises
        return df.iloc[top_indices]['Exercise']
        

    # Create the Tkinter window
    root = tk.Tk()
    app = ExerciseRecommendationApp(root)
    root.mainloop()
    
