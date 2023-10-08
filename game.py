import json
import tkinter as tk
from tkinter import messagebox

class Quiz:
    def __init__(self, master):
        self.master = master
        self.questions = self.load_questions('questions.json')
        self.current_question_index = 0
        self.user_answers = []
        self.create_widgets()

    def load_questions(self, filename):
        try:
            with open(filename, 'r') as file:
                questions = json.load(file)
            return questions
        except FileNotFoundError:
            print("Please create your item bank with the item editor.")
            quit()

    def create_widgets(self):
        self.question_label = tk.Label(self.master, text='', wraplength=400)
        self.question_label.pack(pady=10)

    def display_question(self):
        question = self.questions[self.current_question_index]
        self.question_label.config(text=question['question'],font = ("Calibri",12,"bold"))

    def get_user_answer(self):
        user_answer = self.var.get()
        question = self.questions[self.current_question_index]
        if user_answer != question['answer']:
            messagebox.showinfo("Sorry", f"The correct answer is option {question['answer']}")
        self.user_answers.append(user_answer)
        self.next_question()

        self.var.set(0)

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            print(f'Progress: {self.current_question_index}/{len(self.questions)}')
            self.display_question()
            self.display_option()
        else:
            self.evaluate_quiz()

    def display_option(self):
        ypos = 80
        for i in range(4):
            question = self.questions[self.current_question_index]
            option_button = tk.Radiobutton(self.master,text=question[chr(97+i)],font=("Calibri",12),width=50,anchor='w',variable=self.var,value=chr(97+i))
            option_button.place(x=50,y=ypos)
            ypos+=25

    def evaluate_quiz(self):
        score = 0
        for question, user_answer in zip(self.questions, self.user_answers):
            if user_answer == question['answer']:
                score += 1
        messagebox.showinfo('Quiz Result', f'Score: {int(score/len(self.questions)*100)}%\nRatio: {score}/{len(self.questions)}')
        self.master.destroy()

    def start_quiz(self):
        self.var = tk.StringVar()
        self.var.set(0)
        self.display_question()
        self.display_option()

        submit_button = tk.Button(self.master,text='Next',font=("Calibri",12),command=self.get_user_answer)
        submit_button.place(x=250,y=200)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Quiz')
    root.geometry("600x300")
    quiz = Quiz(root)
    quiz.start_quiz()
    root.mainloop()
