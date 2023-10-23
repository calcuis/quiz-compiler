import json, time, random, concurrent.futures
import tkinter as tk
from tkinter import messagebox

countdownstatue = True

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
            
            data_length = len(questions)
            random_indices = list(range(data_length))
            random.shuffle(random_indices)
            randomized_data = [questions[i] for i in random_indices]

            with open('randomized_questions.json', 'w') as output_file:
                json.dump(randomized_data, output_file, indent=4)

            with open('randomized_questions.json', 'r') as file2:
                questions = json.load(file2)

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
        global countdownstatue
        countdownstatue = False

        user_answer = self.var.get()
        question = self.questions[self.current_question_index]

        with open ('results.txt','a') as file:
            file.write(f"[{question['id']}]{user_answer}\n")

        if user_answer != question['answer']:
            messagebox.showinfo("Sorry", f"The correct answer is: {question[question['answer']]}")
        else:
            time.sleep(0.5)
        self.user_answers.append(user_answer)
        self.next_question()

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            print(f'Progress: {self.current_question_index}/{len(self.questions)}')
            self.display_question()

            global countdownstatue
            self.var.set(0)
            countdownstatue = True

            pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
            pool.submit(self.display_option)
            pool.submit(self.countdowntimer)

        else:
            self.evaluate_quiz()

    def display_option(self):
        ypos = 80
        question = self.questions[self.current_question_index]

        if question[chr(100)]=="all of the above." or question[chr(100)]=="All of the above." or question[chr(100)]=="All of the above":
            with open ('results.txt','a') as file:
                file.write('[0]')

            for i in range(4):
                option_button = tk.Radiobutton(self.master,text=question[chr(97+i)],font=("Calibri",12),width=50,anchor='w',variable=self.var,value=chr(97+i))
                option_button.place(x=50,y=ypos)
                ypos+=25
        else:
            order = random.randint(0, 1)

            with open ('results.txt','a') as file:
                file.write(f'[{order}]')

            if order==0:
                for i in range(4):
                    option_button = tk.Radiobutton(self.master,text=question[chr(97+i)],font=("Calibri",12),width=50,anchor='w',variable=self.var,value=chr(97+i))
                    option_button.place(x=50,y=ypos)
                    ypos+=25
            else:
                for i in range(4):
                    option_button = tk.Radiobutton(self.master,text=question[chr(100-i)],font=("Calibri",12),width=50,anchor='w',variable=self.var,value=chr(100-i))
                    option_button.place(x=50,y=ypos)
                    ypos+=25

    def evaluate_quiz(self):
        global countdownstatue
        countdownstatue = False
        score = 0
        for question, user_answer in zip(self.questions, self.user_answers):
            if user_answer == question['answer']:
                score += 1
        messagebox.showinfo('Result', f'Score: {int(score/len(self.questions)*100)}%\nRatio: {score}/{len(self.questions)}')
        print("Finishing up...")

        with open ('results.txt','a') as file:
            file.write(f'Correct Rate: {score}/{len(self.questions)}\nTimestamp: {time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}\n')

        self.master.destroy()

    def start_quiz(self):
        self.var = tk.StringVar()
        self.var.set(0)
        self.display_question()

        tk.Button(self.master,text='Next',font=("Calibri",12),command=self.get_user_answer).place(x=280,y=220)
        tk.Button(self.master,text='Quit',font=("Calibri",12),command=self.quitbutton).place(x=550,y=0)
        self.mins = tk.StringVar()
        tk.Label(textvariable=self.mins,width=2,font='Calibri').place(x=0, y=0)
        tk.Label(text=":",font='Calibri').place(x=20, y=0)
        self.sec = tk.StringVar()
        tk.Label(textvariable=self.sec,width=2,font='Calibri').place(x=30, y=0)

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        pool.submit(self.display_option)
        pool.submit(self.countdowntimer)

    def countdowntimer(self):
        self.mins.set('02')
        self.sec.set('00')
        times = int(self.mins.get()) * 60 + int(self.sec.get())
        while times > -1:
            if (not countdownstatue):
                break

            minute, second = (times // 60, times % 60)
            self.sec.set(second)
            self.mins.set(minute)

            root.update()
            time.sleep(0.5)
            
            if (times == 0):
                messagebox.showinfo("Timer", "Time's up!")
                self.get_user_answer()
            times -= 1

    def quitbutton(self):
        global countdownstatue
        countdownstatue = False
        print("Terminating...")

        with open ('results.txt','a') as file:
            file.write(f'\nTerminated by User\nTimestamp: {time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}\n')
            
        quit()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Quiz')
    root.geometry("600x300")
    root.resizable(False, False)
    quiz = Quiz(root)
    quiz.start_quiz()
    root.mainloop()
