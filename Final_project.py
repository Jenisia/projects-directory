import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import openai

#openai.api_key = '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'

class ExerciseRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Fitness Routine Generator")
        self.root.resizable(False, False)

        image = Image.open("small_picture.png")  
        new_size = (300, 200)  
        image = image.resize(new_size)

        
        background_photo = ImageTk.PhotoImage(image)

        
        background_label = tk.Label(root, image=background_photo)
        background_label.image = background_photo
        background_label.place(relwidth=1, relheight=1)

        categories = ["Cardio", "Core", "Warm up", "Strength Training", "Flexibility"]

        tk.Label(root, text="Select Category:",bg="#FFB",font=('bold', 10)).pack(pady=10)
        self.category_combobox = ttk.Combobox(root, values=categories)
        self.category_combobox.pack(pady=5)
        self.category_combobox.set("Select")

        tk.Label(root, text="Duration (minutes):",bg="#FFB",font=('bold', 10)).pack(pady=5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack(pady=5)

        intensity_level = ["Beginner","Intermediate","Advanced"]

        tk.Label(root, text="Select Intensity Level:",bg="#FFB",font=('bold', 10)).pack(pady=5)
        self.intensity_combobox = ttk.Combobox(root, values=intensity_level)
        self.intensity_combobox.pack(pady=5)
        self.intensity_combobox.set("Select")

        fitness_goals = ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "General Fitness"]

        tk.Label(root, text="Select Fitness Goals:",bg="#FFB",font=('bold', 10)).pack(pady=5)
        self.goals_combobox = ttk.Combobox(root, values=fitness_goals)
        self.goals_combobox.pack(pady=5)
        self.goals_combobox.set("Select")

        self.get_recommendations_button=tk.Button(root, text="Get Suggestions", command=self.get_recommendations, bg="#4CAF50",fg="white",bd=2,font=('bold', 10))
        self.get_recommendations_button.pack(pady=10)

        tk.Label(root, text="Generated Exercises:",bg="#FFB",font=('bold', 10)).pack(pady=5)
        self.generated_content_text = tk.Text(root, height=10, width=50)
        self.generated_content_text.pack(pady=10)

    def get_recommendations(self):
        
        category = self.category_combobox.get().strip()
        duration = self.duration_entry.get().strip()
        intensity = self.intensity_combobox.get().strip()
        goals = self.goals_combobox.get().strip()

        
        prompt = f"Generate a {intensity} workout routine for {duration} minutes, focusing on {category} exercises to achieve {goals}."

       
        generated_content = self.generate_content(prompt)

        
        self.generated_content_text.delete(1.0, tk.END)
        self.generated_content_text.insert(tk.END, generated_content)

    def generate_content(self, prompt):
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()

if __name__ == "__main__":
    
    root = tk.Tk()
    app = ExerciseRecommendationApp(root)
    root.mainloop()
