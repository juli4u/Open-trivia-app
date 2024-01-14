import tkinter as tk
from tkinter import messagebox
import requests
import html

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("400x400")
        self.root.resizable(0,0)
        self.root.config(bg="#F11A7B")

        self.question_label = tk.Label(root, text="", wraplength=300, justify="center", font=("Helvetica", 15), fg="white", bg="#F11A7B")
        self.question_label.pack(pady=20)

        self.choices_frame = tk.Frame(root, bg="#F11A7B")
        self.choices_frame.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 10), fg="white", bg="#F11A7B")
        self.score_label.pack(pady=10)

        self.correct_answer_label = tk.Label(root, text="Correct Answer: ", fg="green", font=("Helvetica", 10), bg="#F11A7B")
        self.correct_answer_label.pack(pady=10)

        self.next_question_button = tk.Button(root, text="Next Question", command=self.get_next_question, bg="#AED2FF", font=("Helvetica",15), fg="#F11A7B")
        self.next_question_button.pack(pady=10)

        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.user_answers = []

        self.var = tk.StringVar()
        self.get_questions_from_api()

    def get_questions_from_api(self):
        api_url = "https://opentdb.com/api.php?amount=10&category=12&difficulty=medium&type=multiple"

        try:
            response = requests.get(api_url)
            data = response.json()

            if data["response_code"] == 0:
                self.questions = data["results"]
                self.show_question()
            else:
                messagebox.showerror("Error", "Failed to fetch questions from the API.")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    def show_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            question = html.unescape(question_data["question"])
            choices = question_data["incorrect_answers"]
            correct_choice = question_data["correct_answer"]

            # Shuffle choices and insert the correct choice at a random position
            choices.append(correct_choice)
            choices = sorted(choices, key=lambda x: hash(x))

            self.question_label.config(text=question)

            for widget in self.choices_frame.winfo_children():
                widget.destroy()

            for choice in choices:
                tk.Radiobutton(self.choices_frame, text=html.unescape(choice),
                               variable=self.var, value=choice, command=self.check_answer, bg="#F11A7B", activebackground="#F11A7B", selectcolor="#F11A7B", fg="white").pack(anchor="w")

            self.var.set("")
            self.correct_choice = correct_choice
            self.correct_answer_label.config(text="Correct Answer: ")

        else:
            self.show_final_results()

    def check_answer(self):
        user_choice = self.var.get()
        self.user_answers.append((self.questions[self.current_question_index], user_choice))

        if user_choice == self.correct_choice:
            self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.correct_answer_label.config(text=f"Correct Answer: {html.unescape(self.correct_choice)}")

    def get_next_question(self):
        self.current_question_index += 1
        self.show_question()

    def show_final_results(self):
        result_message = f"Quiz Completed\n\nYour final score: {self.score}"
        messagebox.showinfo("Quiz Completed", result_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()