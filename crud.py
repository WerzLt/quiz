from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User, Question, Result, Answer, Answers
from database import insert_data
import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from main import Base

engine = create_engine('sqlite:///quiz_game.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
insert_data()

# Tkinter functions.


class Main(tk.Tk):
    def __init__(self):
        super().__init__()

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
        button1.pack_forget()
        button2.pack_forget()
        button3.pack_forget()
        confirm_button.pack_forget()
        name_exists.pack_forget()

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


# Game Functions eg. TOP 5, questions etc..
class QuizGame:
    def __init__(self):
        self.user_score = 0
        self.level = 1
        self.correct_answers = 0
        self.current_question = None
        self.current_user = None
        self.answer_buttons = []
        self.new_answers = []
        self.streak = False
        self.lose = False

    def get_question(self):
        available_questions = session.query(Question).filter(Question.level_id == self.level).all()
        return random.choice(available_questions)

    def time_question(self, remaining_time=30):
        if remaining_time > 0:
            remaining_time_label['text'] = f"Laikas: {remaining_time}"
            remaining_time_label.pack()
            self.after_function = root.after(1000, self.time_question, remaining_time-1)
        else:
            self.lose = True
            self.end_game()

    def update_question(self):
        available_question = self.get_question()
        self.current_question = available_question
        label.config(text=available_question.text)
        label.pack(pady=20)
        return available_question

    def update_level(self):
        if self.correct_answers > 1:
            level_label.config(text=f"Lygis {self.level} Taškai: {int(self.user_score)} Teisingi iš eilės: {self.correct_answers}", bg="Orange", fg="White")
            level_label.pack(pady=20)
            self.streak = True
        else:
            level_label.config(text=f"Lygis {self.level} Taškai: {int(self.user_score)}", bg="Yellow", fg="Red")
            level_label.pack(pady=20)
            self.streak = False

    def update_answers(self):
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons = []
        questions_answers = session.query(Answers).filter_by(question_id=self.current_question.id).all()
        for i, answer in enumerate(questions_answers):
            split_answers = answer.answers.split(',')
            for j, answer_text in enumerate(split_answers):
                new_button = tk.Button(root, text=answer_text,
                                       command=lambda idx=i, j=j: self.correct_answer(str(j + 1)))
                new_button.configure(bg="black", fg="white")
                new_button.pack(pady=10)
                self.answer_buttons.append(new_button)
                self.new_answers.append(new_button)
    def correct_answer(self, user_answers):
        correct = None
        if self.current_question:
            correct = session.query(Answer).filter_by(question_id=self.current_question.id).first()
            if user_answers == correct.correct_answer:
                self.update_question()
                is_correct_answer.config(text="Teisingas atsakymas!", bg="Green", fg="White")
                is_correct_answer.pack(pady=10)
                self.update_answers()
                root.after_cancel(self.after_function)
                self.time_question()
                if self.streak:
                    self.user_score += 20*1.5
                else:
                    self.user_score += 20
                self.correct_answers += 1
                if self.user_score > 2000:
                    self.end_game()
                elif self.user_score > 1000:
                    self.level = 7
                elif self.user_score > 700:
                    self.level = 6
                elif self.user_score > 500:
                    self.level = 5
                elif self.user_score > 360:
                    self.level = 4
                elif self.user_score > 200:
                    self.level = 3
                elif self.user_score > 80:
                    self.level = 2
                self.update_level()
            else:
                self.update_question()
                is_correct_answer.config(text="Neteisingas atsakymas :(", bg="Red", fg="White")
                is_correct_answer.pack(pady=10)
                self.update_answers()
                root.after_cancel(self.after_function)
                self.time_question()
                self.user_score -= 15
                self.correct_answers = 0
                self.update_level()
                if self.user_score < 0:
                    self.lose = True
                    self.end_game()
        else:
            print("Nėra klausimų")

        return user_answers == correct.correct_answer

    def register(self, nickname):
        user = session.query(User).filter_by(username=nickname).first()
        if not user:
            new_user = User(username=nickname)
            session.add(new_user)
            session.commit()
            root.hide_elements()
            self.current_user = new_user
            self.start_game()
        else:
            name_exists.config(text="Vartotojas jau yra užimtas. Bandykite dar kartą.", bg="Red", fg="White")
            name_exists.pack(pady=20)

    def show_top_players(self):
        root.hide_elements()
        results = session.query(Result).limit(5).all()

        scrollbaras = Scrollbar(root)
        boksas = Listbox(root, width=80, height=0, yscrollcommand=scrollbaras.set)

        boksas.pack(side="left", fill="both", expand=True)
        scrollbaras.pack(side="right", fill="y")
        boksas.delete(0, END)

        for result in results:
            player_info = f"{result.user_id}. {result.user_username}, {result.level_id}, {result.score}, {result.data}"
            boksas.insert(END, player_info)
        back_button = tk.Button(root, text="Atgal", command=root.input_window)
        back_button.pack(pady=10)

    def start_game(self):
        root.hide_elements()
        self.update_question()
        self.update_level()
        self.time_question()
        root.create_answers()

    def end_game(self):
        root.hide_elements()
        label.pack_forget()
        level_label.pack_forget()
        is_correct_answer.pack_forget()
        remaining_time_label.pack_forget()
        root.after_cancel(self.after_function)

        end_game_label = tk.Label(root, text="Žaidimas baigtas :(", font=("Helvetica", 16), bg="Red", fg="White")
        end_game_label.pack()

        end_game_button = tk.Button(root, text="Pradėti iš naujo", pady=20, command=root.input_window)
        end_game_button.pack()

        if self.current_user:
            user_result = Result(
                user_id=self.current_user.id,
                user_username=self.current_user.username,
                level_id=self.level,
                score=self.user_score
            )
            session.add(user_result)
            session.commit()

        for answer_widget in self.new_answers:
            answer_widget.pack_forget()
        for answer_widget in self.answer_buttons:
            answer_widget.pack_forget()
        if self.lose:
            messagebox.showinfo('Žaidimas baigtas',f'Žaidimas baigėsi\nSurinkote taškų: {int(quiz_obj.user_score)}')
        else:
            (messagebox.showinfo
             ('Sveikinimai!', f'Sveikiname laimėjus žaidimą!\nSurinkote taškų: {int(quiz_obj.user_score)}'))





root = Main()
root.title("Quiz žaidimas")
root.iconbitmap(r'assets/icon.ico')

quiz_obj = QuizGame()

root.center_window(root, 1440, 900)
root.configure(bg="#34495e")

root.logocreation()
label = tk.Label(root, text="", font=("Helvetica", 16))
level_label = tk.Label(root, text="", font=("Helvetica", 20))
name_exists = tk.Label(root, text="", font=("Helvetica", 16))
name_entry = tk.Entry(root, bd=3)
is_correct_answer = tk.Label(root, text="", font=("Helvetica", 16))
remaining_time_label = tk.Label(root, text="", font=("Helvetica", 20))

button1 = tk.Button(root, text="Pradėti žaidimą", command=root.input_window)
button1.configure(bg="black", fg="white")
button2 = tk.Button(root, text="TOP 5 Žaidėjai", command=quiz_obj.start_game)
button2.configure(bg="black", fg="white")
button3 = tk.Button(root, text="Išeiti iš žaidimo", command=root.destroy)
button3.configure(bg="black", fg="white")
confirm_button = tk.Button(root, text="Registruotis", command=lambda: quiz_obj.register(name_entry.get()))
confirm_button.configure(bg="black", fg="red")
name_entry.bind("<Return>", lambda event: quiz_obj.register(name_entry.get()))

button1.pack(pady=10)
button2.pack(pady=10)
button3.pack(pady=10)

root.mainloop()
#                 question_id = input("Nurodykite klausimo ID, kurį norite pakeisti ")
#                 question = session.get(Question, question_id)
#                 if question:
#                     question_update = input("Ką norite keisti? \n1 - Lygį \n2 - Klausimą \n3 - Atsakymą \nĮvestis: ")
#                     question_level_range = 0
#                     if question_update == "1":
#                         while not int(question_level_range) in range(1, 7):
#                             question_level_range = input("Pasirinkite lygį tarp 1 ir 7. ")
#                             question.level_id = int(question_level_range)
#                     if question_update == "2":
#                         question_name = input("Įveskite naują lygio pavadinimą ")
#                         question.text = question_name
#                     if question_update == "3":
#                         question_answer = input("Įveskite naują lygio atsakymą ")
#                         question.correct_answer = question_answer
#                     print(f"Pakeistas klausimas, kurio ID: {question_id}")
#                     session.commit()
#                 else:
#                     print(f"Klausimas, kurio ID: {question_id} nerastas...")
#             if admin_choice == "4":
#                 Players_list()
#                 player_id = input("Nurodykite žaidėjo ID, kurio taškus norite pakeisti ")
#                 player = session.get(Result, player_id)
#                 if player:
#                     player_update = input("Įveskite naują taškų kiekį: ")
#                     try:
#                         player.score = int(player_update)
#                         session.commit()
#                         print(f"Pakeitėte žaidėjo, kurio ID: {player_id} taškus į {player_update}")
#                     except ValueError:
#                         print("Įvestas netinkamas taškų kiekis. Įveskite skaičių.")
#                 else:
#                     Players_list()
#                     print("Žaidėjas nerastas!")
#         except ValueError:
#             print("Veskite tik skaičius!")
#     else:
#         print("Galbūt įvedėte ne tą slapyvardį?")
# else:
#     try:
#         user = session.query(User).filter_by(username=name).first()
#         user_choice = input("1 - Pradėti žaidimą\n2 - TOP 3 žaidėjai ")
#         if user_choice == "1":
#             print("Žaidimas prasidėjo DEMO režimu. Duomenų bazė nepildoma. :)")
#             while True:
#                 question = root.get_question()
#                 print(f"---- {root.level} lygis ---- ")
#                 print(f"Klausimas: {question.text}")
#                 user_answer = input("Pasirinkite atsakymą (veskite skaičius, pvz. 1): ")
#                 if root.correct_answer(user_answer, question):
#                     print("Atsakymas teisingas")
#                     root.user_score += 50
#                     root.correct_answers += 1
#                     if root.correct_answers == 5:
#                         level = 2
#                         print("Sveikiname jus pasiekėte antrą lygį!")
#                 else:
#                     print("Atsakymas neteisingas. Žaidimas baigtas.")
#                     user_result = Result(
#                         user_id=user.id,  # Use the user's id
#                         user_username=name,
#                         level_id=root.level,  # You might want to dynamically update this based on the user's progress
#                         score=root.user_score
#                     )
#                     session.add(user_result)
#                     session.commit()
#                     break
#         if user_choice == "2":
#             Top_List()
#     except ValueError:
#         print("Veskite tik skaičius!")
