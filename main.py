import tkinter as tk
from tkinter import messagebox
import requests
import html
from PIL import ImageTk, Image

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizzifyHub")
        self.root.geometry("800x700")
        self.root.resizable(0, 0)
        self.root.config(bg="#27005D")
        self.root.iconbitmap('QuizzifyHub-logos_transparent.ico')
        
        background_picture = tk.PhotoImage(file="Background Picture.png")
        # Main Frame
        self.main_frame = tk.Frame(root, bg="#27005D")
        self.main_frame.pack(expand=True)

        
        title_label = tk.Label(self.main_frame, text="QuizzifyHub", font=("Times", 40, "bold"), fg="white", bg="#27005D", image=background_picture, compound="center")
        title_label.image = background_picture
        title_label.pack(pady=50)

        start_button = tk.Button(self.main_frame, text="Start", command=self.show_instruction_manual, bg="#AED2FF", font=("Times", 30), fg="#9400FF")
        start_button.place(x=180, y=370)

        # Instruction Manual Frame
        self.instruction_frame = tk.Frame(root, bg="#F11A7B", width=600, height=600)

        instruction_label = tk.Label(self.instruction_frame, text="Instruction Manual", font=("Times", 20), fg="black", bg="#F11A7B")
        instruction_label.pack(pady=20)

        instructions_text = (
            "1. There are 10 questions in the quiz.\n"
            "2. The question difficulty is medium.\n"
            "3. It is a multiple-choice quiz.\n"
            "4. When you choose the answer, it also shows the correct answer and records the scores.\n"
            "5. When the quiz ends, you will get a message box saying, 'Quiz Completed' and your scores."
        )

        instructions_label = tk.Label(self.instruction_frame, text=instructions_text, font=("Times", 15), fg="black", bg="#F11A7B", justify="left")
        instructions_label.pack(pady=20)

        start_quiz_button = tk.Button(self.instruction_frame, text="Start the Quiz", command=self.show_quiz_section, bg="#AED2FF", font=("Times", 15), fg="#F11A7B")
        start_quiz_button.pack(pady=10)

        # Second Frame (Quiz Section)
        self.quiz_frame = tk.Frame(root, bg="#F11A7B", width=600, height=600)

        self.question_label = tk.Label(self.quiz_frame, text="", wraplength=300, justify="center", font=("Times", 15), fg="black", bg="#F11A7B")
        self.question_label.pack(pady=20)

        self.choices_frame = tk.Frame(self.quiz_frame, bg="#F11A7B")
        self.choices_frame.pack(pady=10)

        self.score_label = tk.Label(self.quiz_frame, text="Score: 0", font=("Times", 12), fg="black", bg="#F11A7B")
        self.score_label.pack(pady=10)

        self.correct_answer_label = tk.Label(self.quiz_frame, text="Correct Answer: ", fg="green", font=("Times", 12), bg="#F11A7B")
        self.correct_answer_label.pack(pady=10)

        self.next_question_button = tk.Button(self.quiz_frame, text="Next Question", command=self.get_next_question, bg="#AED2FF", font=("Times", 15), fg="#F11A7B")
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
            else:
                messagebox.showerror("Error", "Failed to fetch questions from the API.")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    def show_instruction_manual(self):
        self.main_frame.pack_forget()
        self.instruction_frame.pack()

    def show_quiz_section(self):
        self.instruction_frame.pack_forget()
        self.quiz_frame.pack()
        self.show_question()

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
                               variable=self.var, value=choice, command=self.check_answer, bg="#F11A7B", activebackground="#F11A7B", selectcolor="#F11A7B", fg="white", font=("Times", 13)).pack(anchor="w")

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
