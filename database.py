from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User, Level, Question, Result, Answer, Answers

engine = create_engine('sqlite:///quiz_game.db')
Session = sessionmaker(bind=engine)
session = Session()

def insert_data():
    if session.query(Level).count() == 0:
        levels = [
            Level(name='I Lygis'),
            Level(name='II Lygis'),
            Level(name='III Lygis'),
            Level(name='IV Lygis'),
            Level(name='V Lygis'),
            Level(name='VI Lygis'),
            Level(name='Paskutinis Lygis'),
        ]
        session.add_all(levels)
        session.commit()
    if session.query(Question).count() == 0:
        questions = [
            Question(level_id=1, question_type='0', text='Kokia yra Prancūzijos sostinė?'),
            Question(level_id=1, question_type='0', text='Kiek iš viso yra pasaulyje žemynų?'),
            Question(level_id=1, question_type='0', text='Kokioje šalyje įvyko Černobilio avarija?'),
            Question(level_id=1, question_type='0', text='Kiek sekundžių turi viena valanda?'),
            Question(level_id=1, question_type='0', text='Kas buvo Lietuvos prezidentas prieš D.Grabauskaitę?'),
            Question(level_id=1, question_type='0', text='Kokia šalis turi daugiausiai gyventojų?'),
            Question(level_id=1, question_type='0', text='Kiek "Snieguolė" pasakoje buvo nykštukų?'),
            Question(level_id=1, question_type='0', text='Kas nutapė Moną Lizą?'),

            Question(level_id=2, question_type='0', text='Kelintais metais įvyko pirmasis pasaulinis karas?'),
            Question(level_id=2, question_type='0', text='Koks yra sidabro cheminis elementas?'),
            Question(level_id=2, question_type='0', text='Kiek vaivorykštė turi spalvų?'),
            Question(level_id=2, question_type='0', text='Koks naminis gyvūnas sugeba atkartoti žodžiius?'),
            Question(level_id=2, question_type='0', text='Kokia mygtukų kombinacija yra kopijuoti?'),
            Question(level_id=2, question_type='0', text='Kuri planeta yra karščiausia Saulės sistemoje?'),
            Question(level_id=2, question_type='0',
                     text='Kokiai kompanijai priklauso Bugatti, Lamborghini, Audi, Porsche?'),
            Question(level_id=2, question_type='0', text='Kokia šalis pagamina daugiausiai kavos?'),

            Question(level_id=3, question_type='0', text='Kurioje šalyje ilgiausiai gyvena žmonės?'),
            Question(level_id=3, question_type='0', text='Kiek minučių turi viena savaitė?'),
            Question(level_id=3, question_type='0', text='Kas buvo paskutinis Rusijos caras?'),
            Question(level_id=3, question_type='0',
                     text='Kurioje Europos šalyje 2015-2020m. sumažėjo didžiausias gyventojų skaičius?'),
            Question(level_id=3, question_type='0', text='Kiek žvaigždžių yra pavaizduota ant Kinijos vėliavos?'),
            Question(level_id=3, question_type='0', text='Kokioje šalyje atsirado patiekalas Sushi?'),
            Question(level_id=3, question_type='0', text='Koks yra ilgiausias angliškas žodis?'),
            Question(level_id=3, question_type='0', text='Kiek metų yra seniausiai pasaulyje kramtomai gumai?'),

            Question(level_id=4, question_type='0', text='Koks yra didžiausias socialinis tinklas?'),
            Question(level_id=4, question_type='0', text='Kuri šalis išrado Cezario salotas?'),
            Question(level_id=4, question_type='0',
                     text='Koks greito maisto restoranas turi daugiausiai restoranų pasaulyje?'),
            Question(level_id=4, question_type='0', text='Kuri šalis turi daugiausiai vegetarų?'),
            Question(level_id=4, question_type='0', text='Kuri šalis išrado šachmatų žaidimą?'),
            Question(level_id=4, question_type='0', text='Koks buvo Matrica pagrindinio veikėjo vardas?'),
            Question(level_id=4, question_type='0', text='Kada pirmą kartą buvo išleistas Facebook?'),
            Question(level_id=4, question_type='0', text='Kokios spalvos yra nuodingiausia varlė pasaulyje?'),

            Question(level_id=5, question_type='0', text='Kas yra didžiausias sausumos plėšrūnas?'),
            Question(level_id=5, question_type='0', text='Kiek kaulų turi ryklys?'),
            Question(level_id=5, question_type='0', text='Koks maistas yra labiausiai vogiamas pasaulyje?'),
            Question(level_id=5, question_type='0',
                     text='Koks yra vienintelis valgomas maistas, kurio galiojimo laikas niekada nesibaigia?'),
            Question(level_id=5, question_type='0', text='Kiek lietuvių kalbos abėcėlėje yra raidžių?'),
            Question(level_id=5, question_type='0', text='Kiek metų nugyveno vyriausias žmogus pasaulyje?'),
            Question(level_id=5, question_type='0', text='Kurioje šalyje atsirado Olimpinės žaidynės?'),
            Question(level_id=5, question_type='0', text='Koks yra diždiausias pasaulyje žemynas?'),

            Question(level_id=6, question_type='0', text='Kiek oskarų apdovanojimų laimėjo filmas "Titanikas"?'),
            Question(level_id=6, question_type='0', text='Kelintais metais buvo išsiųsta pirmoji SMS žinutė?'),
            Question(level_id=6, question_type='0', text='Kurioje senovės civilizacijoje buvo išrastos žirklės?'),
            Question(level_id=6, question_type='0', text='Kiek žmonių vaikščiojo Mėnulyje?'),
            Question(level_id=6, question_type='0', text='Kokios spalvos yra saulėlydis Marse?'),
            Question(level_id=6, question_type='0', text='Kuri planeta yra turi 145 Mėnulius?'),
            Question(level_id=6, question_type='0', text='Ko negali daryti astronautas kosmose?'),
            Question(level_id=6, question_type='0', text='Kelintais metais nuskendo laivas "Titanikas"?'),

            Question(level_id=7, question_type='0', text='Kiek dienų per savaitę buvo Senovės Romoje?'),
            Question(level_id=7, question_type='0', text='Kiek kartų buvo pavogtas "Mona Liza" paveikslas?'),
            Question(level_id=7, question_type='0', text='Kelintais metais buvo nugriauta Berlyno siena?'),
            Question(level_id=7, question_type='0', text='Kiek žvaigždžių yra pavaizduota ant Amerikos vėliavos?'),
            Question(level_id=7, question_type='0', text='Kuriame dešimtmetyje gimė Madonna?'),
            Question(level_id=7, question_type='0', text='Kas išrado bikinį?'),
            Question(level_id=7, question_type='0', text='Koks yra didžiausias žmogaus organas?'),
            Question(level_id=7, question_type='0', text='Kiek krabas iš viso turi kojų?'),
            Question(level_id=1, question_type='1', text='Ar žuvys gali mirksėti?'),
            Question(level_id=2, question_type='1', text='Ar žmogaus kūną sudaro 60% vandens?')
        ]

        session.add_all(questions)
        session.commit()  # Commit the Questions to get their IDs
    if session.query(Answer).count() == 0:
        answers = [
            Answer(question_id=1, correct_answer='1'),
            Answer(question_id=2, correct_answer='3'),
            Answer(question_id=3, correct_answer='2'),
            Answer(question_id=4, correct_answer='3'),
            Answer(question_id=5, correct_answer='1'),
            Answer(question_id=6, correct_answer='3'),
            Answer(question_id=7, correct_answer='2'),
            Answer(question_id=8, correct_answer='1'),
            Answer(question_id=9, correct_answer='1'),
            Answer(question_id=10, correct_answer='2'),
            Answer(question_id=11, correct_answer='2'),
            Answer(question_id=12, correct_answer='1'),
            Answer(question_id=13, correct_answer='2'),
            Answer(question_id=14, correct_answer='1'),
            Answer(question_id=15, correct_answer='1'),
            Answer(question_id=16, correct_answer='3'),

            Answer(question_id=17, correct_answer='3'),
            Answer(question_id=18, correct_answer='2'),
            Answer(question_id=19, correct_answer='2'),
            Answer(question_id=20, correct_answer='1'),
            Answer(question_id=21, correct_answer='3'),
            Answer(question_id=22, correct_answer='1'),
            Answer(question_id=23, correct_answer='1'),
            Answer(question_id=24, correct_answer='3'),

            Answer(question_id=25, correct_answer='2'),
            Answer(question_id=26, correct_answer='3'),
            Answer(question_id=27, correct_answer='3'),
            Answer(question_id=28, correct_answer='2'),
            Answer(question_id=29, correct_answer='1'),
            Answer(question_id=30, correct_answer='3'),
            Answer(question_id=31, correct_answer='2'),
            Answer(question_id=32, correct_answer='3'),

            Answer(question_id=33, correct_answer='1'),
            Answer(question_id=34, correct_answer='3'),
            Answer(question_id=35, correct_answer='2'),
            Answer(question_id=36, correct_answer='2'),
            Answer(question_id=37, correct_answer='3'),
            Answer(question_id=38, correct_answer='3'),
            Answer(question_id=39, correct_answer='1'),
            Answer(question_id=40, correct_answer='3'),

            Answer(question_id=41, correct_answer='1'),
            Answer(question_id=42, correct_answer='3'),
            Answer(question_id=43, correct_answer='1'),
            Answer(question_id=44, correct_answer='1'),
            Answer(question_id=45, correct_answer='3'),
            Answer(question_id=46, correct_answer='1'),
            Answer(question_id=47, correct_answer='2'),
            Answer(question_id=48, correct_answer='2'),

            Answer(question_id=49, correct_answer='3'),
            Answer(question_id=50, correct_answer='1'),
            Answer(question_id=51, correct_answer='2'),
            Answer(question_id=52, correct_answer='1'),
            Answer(question_id=53, correct_answer='1'),
            Answer(question_id=54, correct_answer='3'),
            Answer(question_id=55, correct_answer='1'),
            Answer(question_id=56, correct_answer='3'),
            Answer(question_id=57, correct_answer='2'),
            Answer(question_id=58, correct_answer='1'),
        ]

        session.add_all(answers)
        session.commit()  # Commit the Questions to get their IDs
    if session.query(Answers).count() == 0:
        question_answers = [
            Answers(question_id=1, answers='Paryžius, Orleanas, Dižonas'),
            Answers(question_id=2, answers='3, 12, 6'),
            Answers(question_id=3, answers='Amerika, Ukraina, Rusija'),
            Answers(question_id=4, answers='1800, 5800, 3600'),
            Answers(question_id=5, answers='Valdas Adamkus, Rolandas Paksas, Gitanas Nausėda'),
            Answers(question_id=6, answers='Amerika, Rusija, Indija'),
            Answers(question_id=7, answers='5, 7, 9'),
            Answers(question_id=8, answers='Leonardo Da Vinci, Albertas Einšteinas, Viljamas Šekspyras'),
            Answers(question_id=9, answers='1914m., 1891m., 1945m.'),
            Answers(question_id=10, answers='Fe, Ag, H'),
            Answers(question_id=11, answers='10, 7, 5'),
            Answers(question_id=12, answers='Papūga, Šuo, Katė'),
            Answers(question_id=13, answers='CTRL+V, CTRL+C, ALT+F4'),
            Answers(question_id=14, answers='Venera, Merkurijus, Marsas'),
            Answers(question_id=15, answers='Volkswagen, BMW, Mercedes'),
            Answers(question_id=16, answers='Prancūzija, Vokietija, Brazilija'),

            Answers(question_id=17, answers='Kinija, Japonija, Hong Kongas'),
            Answers(question_id=18, answers='7.200, 10.800, 12.600'),
            Answers(question_id=19, answers='Nikolajus Nikolaevičius, Nikolajus II, Aleksandras III'),
            Answers(question_id=20, answers='Lietuva, Vokietija, Italija'),
            Answers(question_id=21, answers='3, 6, 5'),
            Answers(question_id=22, answers='Japonija, Kinija, Šiaurės Korėja'),
            Answers(question_id=23,
                    answers='Antidisestablishmentarianism, Hippopotomonstrosesquippedaliophobia, Floccinaucinihilipilification'),
            Answers(question_id=24, answers='100, 2.500, 5.700'),
            Answers(question_id=25, answers='Twitter, Facebook, Instagram'),
            Answers(question_id=26, answers='Amerika, Lenkija, Meksika'),
            Answers(question_id=27, answers='McDonalds, KFC, Subway'),
            Answers(question_id=28, answers='Anglija, Indija, Brazilija'),
            Answers(question_id=29, answers='Indija, Kinija, Graikija'),
            Answers(question_id=30, answers='Niall, Neil, Neo'),
            Answers(question_id=31, answers='1988, 2004, 1995'),
            Answers(question_id=32, answers='Žalia, Mėlyna, Geltona'),

            Answers(question_id=33, answers='Baltoji meška, Puma, Vilkas'),
            Answers(question_id=34, answers='50, 24, 0'),
            Answers(question_id=35, answers='Žuvis, Sūris, Vištiena'),
            Answers(question_id=36, answers='Ryžiai, Medus, Makaronai'),
            Answers(question_id=37, answers='54, 30, 32'),
            Answers(question_id=38, answers='115, 125, 122'),
            Answers(question_id=39, answers='Graikija, Amerika, Rusija'),
            Answers(question_id=40, answers='Europa, Šiaurės Amerika, Azija'),

            Answers(question_id=41, answers='11, 15, 19'),
            Answers(question_id=42, answers='1987, 1990, 1992'),
            Answers(question_id=43, answers='Senovės Egiptas, Senovės Roma, Senovės Graikija'),
            Answers(question_id=44, answers='12, 14, 18'),
            Answers(question_id=45, answers='Raudona, Rožinė, Mėlyna'),
            Answers(question_id=46, answers='Saturnas, Marsas, Merkurijus'),
            Answers(question_id=47, answers='Skaityti, Verkti, Miegoti'),
            Answers(question_id=48, answers='1900m., 1912m., 1890m.'),

            Answers(question_id=49, answers='5, 6, 8'),
            Answers(question_id=50, answers='1, 5, 8'),
            Answers(question_id=51, answers='1987m., 1989m., 1990m.'),
            Answers(question_id=52, answers='50, 51, 48'),
            Answers(question_id=53, answers='1950-ieji, 1960-ieji, 1970-ieji'),
            Answers(question_id=54, answers='Louis Vuitton, Coco Chanel, Louis Reard'),
            Answers(question_id=55, answers='Oda, Širdis, Kepenys'),
            Answers(question_id=56, answers='8, 12, 10'),
            Answers(question_id=57, answers='Taip, Ne'),
            Answers(question_id=58, answers='Taip, Ne'),
        ]

        session.add_all(question_answers)
        session.commit()  # Commit the Questions to get their IDs