from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User, Question, Result, Answer, Answers
import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

engine = create_engine('sqlite:///quiz_game.db')
Session = sessionmaker(bind=engine)
session = Session()

# Game Functions eg. TOP 5, questions etc.
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
        results = session.query(Result).limit(5).all()
        if results:
            player_info = "\n".join(
                [f"ID: {result.user_id}. Vardas: {result.user_username}, Lygis: {result.level_id}, Taškai: {result.score}, Data: {result.data}" for
                 result in results])
            messagebox.showinfo("Top 5 Žaidėjai", player_info)
        else:
            messagebox.showinfo("Top 5 Žaidėjai", "Šiuo metu sąrašas yra tuščias. Būk pirmas!")
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
                score=self.user_score,
                data=datetime.strptime(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), "%Y/%m/%d, %H:%M:%S")
            )
            session.add(user_result)
            session.commit()

        for answer_widget in self.new_answers:
            answer_widget.pack_forget()
        for answer_widget in self.answer_buttons:
            answer_widget.pack_forget()
        if self.lose:
            messagebox.showinfo('Žaidimas baigtas',f'Žaidimas baigėsi\nSurinkote taškų: {int(self.user_score)}')
        else:
            (messagebox.showinfo
             ('Sveikinimai!', f'Sveikiname laimėjus žaidimą!\nSurinkote taškų: {int(self.user_score)}'))

label = None
level_label = None
name_exists = None
name_entry = None
is_correct_answer = None
root = None
remaining_time_label = None