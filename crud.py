from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Answers
from database import insert_data
import tkinter as tk
from tkinter import *
from main import Base
from quiz_module import QuizGame

engine = create_engine('sqlite:///quiz_game.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
insert_data()

# Tkinter functions.


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.buttons = []


    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_answers(self):
        questions_answers = session.query(Answers).filter_by(question_id=quiz_obj.current_question.id).all()
        for i, answer in enumerate(questions_answers):
            split_answers = answer.answers.split(',')
            for j, answer_text in enumerate(split_answers):
                answer_button = tk.Button(root, text=answer_text, command=lambda idx=i, j=j: quiz_obj.correct_answer(str(j + 1)))
                answer_button.configure(bg="black", fg="white")
                answer_button.pack(pady=10)
                quiz_obj.answer_buttons.append(answer_button)
        return questions_answers

    def hide_elements(self):
        name_entry.forget()
        confirm_button.pack_forget()
        name_exists.pack_forget()
        button1.pack_forget()
        button2.pack_forget()
        button3.pack_forget()

    def logocreation(self):
        logo_image = PhotoImage(file="assets/logo.png")
        logo_label = tk.Label(self, image=logo_image)
        logo_label.image = logo_image
        logo_label.pack(pady=20)

    def input_window(self):
        self.hide_elements()
        label.config(text="Įveskite savo slapyvardį. Įsitikinkite, kad jis yra unikalus.")
        label.pack(pady=20)
        name_entry.pack()
        confirm_button.pack(pady=10)





root = Main()
root.title("Quiz žaidimas")
root.iconbitmap(r'assets/icon.ico')

root.center_window(root, 1440, 800)
root.configure(bg="#34495e")
root.logocreation()

quiz_obj = QuizGame()

button1 = tk.Button(root, text="Pradėti žaidimą", command=root.input_window)
button1.configure(bg="black", fg="white")
button2 = tk.Button(root, text="TOP 5 Žaidėjai", command=quiz_obj.show_top_players)
button2.configure(bg="black", fg="white")
button3 = tk.Button(root, text="Išeiti iš žaidimo", command=root.destroy)
button3.configure(bg="black", fg="white")

label = tk.Label(root, text="", font=("Helvetica", 16))
level_label = tk.Label(root, text="", font=("Helvetica", 20))
name_exists = tk.Label(root, text="", font=("Helvetica", 16))
name_entry = tk.Entry(root, bd=3)
is_correct_answer = tk.Label(root, text="", font=("Helvetica", 16))
remaining_time_label = tk.Label(root, text="", font=("Helvetica", 20))

confirm_button = tk.Button(root, text="Registruotis", command=lambda: quiz_obj.register(name_entry.get()))
confirm_button.configure(bg="black", fg="red")
name_entry.bind("<Return>", lambda event: quiz_obj.register(name_entry.get()))\

button1.pack(pady=10)
button2.pack(pady=10)
button3.pack(pady=10)

root.mainloop()
