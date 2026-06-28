# Capitals Quiz
#### Description:
This project is a web-based geography game quiz built with Flask, SQLite, Jinja templates, and Bootstrap. In this game, you will be asked for the capitals of various countries, earn points for correct answers, and will be able to track your progress over time. Under the hood, the app manages user accounts, sessions, scoring, and a small history log.

The project is structured around a small set of routes and templates: you can register, log in, play a 10-question capitals quiz, and see feedback on which questions you got right. The app also stores cumulative points per user and records each game’s result in a history table. This project was inspired by an exercise from the CS50 course.

---

## Overall design and flow

At a high level, the application follows this pattern:

1. **Anonymous users** can visit the home page and choose to register or log in.
2. **Registered, logged-in users** can start a capitals game quiz.
3. The quiz displays **10 randomly selected countries** on a single page, and the user enters what they believe are the capitals.
4. After submitting, the app evaluates the answers, calculates how many were correct, updates the user’s cumulative score, and shows a detailed results page.
5. Additionally, the app can record each game in a history section, storing how many points the user gained in each round.

---

## How to run the game
Download the files from this repository. Once downloaded execute the command `flask run`. The application will then start running on a port in your machine; open it in your browser and you will be able to start with the game. If it is your first time, you will need to register as an user to keep a record of your games.

