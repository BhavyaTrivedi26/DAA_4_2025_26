import tkinter as tk
import random
import time
import json
import os

root = tk.Tk()
root.title("Memory Match Battle")
root.geometry("500x700")
root.configure(bg="#121212")

FILE = "scores.json"

symbols_base = list("ABCDEFGHIJKL")

buttons = []
symbols = []

first_card = -1
second_card = -1
lock = False

score = 0
pairs = 8
level = "Medium"

start_time = 0
timer_running = False

def load_scores():
    if not os.path.exists(FILE):
        data = {
            "Easy": {"best_time": 9999, "best_score": 0},
            "Medium": {"best_time": 9999, "best_score": 0},
            "Hard": {"best_time": 9999, "best_score": 0},
        }
        with open(FILE, "w") as f:
            json.dump(data, f)
        return data
    with open(FILE, "r") as f:
        return json.load(f)

def save_scores():
    with open(FILE, "w") as f:
        json.dump(scores, f)

scores = load_scores()

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def start_screen():
    clear_screen()

    tk.Label(root, text="Memory Match Battle",
             font=("Arial", 20, "bold"),
             fg="white", bg="#121212").pack(pady=100)

    tk.Button(root, text="PLAY",
              font=("Arial", 16),
              bg="#03dac6",
              command=level_screen).pack(pady=20)

def level_screen():
    clear_screen()

    tk.Label(root, text="Select Difficulty",
             font=("Arial", 18),
             fg="white", bg="#121212").pack(pady=30)

    tk.Label(root, text=f"Easy → Time: {scores['Easy']['best_time']} | Score: {scores['Easy']['best_score']}",
             fg="lightgreen", bg="#121212").pack()

    tk.Label(root, text=f"Medium → Time: {scores['Medium']['best_time']} | Score: {scores['Medium']['best_score']}",
             fg="lightblue", bg="#121212").pack()

    tk.Label(root, text=f"Hard → Time: {scores['Hard']['best_time']} | Score: {scores['Hard']['best_score']}",
             fg="pink", bg="#121212").pack()

    tk.Button(root, text="Easy", width=15,
              command=lambda: setup_game("Easy")).pack(pady=10)

    tk.Button(root, text="Medium", width=15,
              command=lambda: setup_game("Medium")).pack(pady=10)

    tk.Button(root, text="Hard", width=15,
              command=lambda: setup_game("Hard")).pack(pady=10)

def setup_game(lvl):
    global symbols, pairs, score, start_time, level, timer_running
    global first_card, second_card

    clear_screen()

    level = lvl

    if lvl == "Easy":
        pairs = 6
    elif lvl == "Medium":
        pairs = 8
    else:
        pairs = 10

    symbols = symbols_base[:pairs] * 2
    random.shuffle(symbols)

    score = 100
    first_card = -1
    second_card = -1

    start_time = time.time()
    timer_running = True

    # Top UI
    global score_label, timer_label

    score_label = tk.Label(root, text="Score: 100",
                           fg="white", bg="#121212", font=("Arial", 12))
    score_label.pack()

    timer_label = tk.Label(root, text="Time: 0s",
                           fg="white", bg="#121212", font=("Arial", 12))
    timer_label.pack()

    best_time = scores[level]["best_time"]
    best_score = scores[level]["best_score"]

    tk.Label(root,
             text=f"Best Time: {best_time}s | High Score: {best_score}",
             fg="yellow", bg="#121212").pack()

    # Board
    board = tk.Frame(root, bg="#121212")
    board.pack(pady=20)

    buttons.clear()

    for i in range(len(symbols)):
        btn = tk.Button(board, text="", width=7, height=3,
                        bg="#333", fg="white",
                        command=lambda i=i: on_click(i))
        btn.grid(row=i//4, column=i%4, padx=5, pady=5)
        buttons.append(btn)

    update_timer()

def on_click(i):
    global first_card, second_card, lock

    if lock:
        return

    btn = buttons[i]

    if btn["text"] != "":
        return

    btn.config(text=symbols[i], bg="#00bcd4")

    if first_card == -1:
        first_card = i
    else:
        second_card = i
        lock = True
        root.after(500, check_match)

def check_match():
    global first_card, second_card, lock, score

    if symbols[first_card] == symbols[second_card]:
        buttons[first_card].config(bg="#4caf50")
        buttons[second_card].config(bg="#4caf50")
        score += 10
    else:
        buttons[first_card].config(text="", bg="#333")
        buttons[second_card].config(text="", bg="#333")
        score -= 5

    score_label.config(text=f"Score: {score}")

    first_card = -1
    second_card = -1
    lock = False

    if all(b["text"] != "" for b in buttons):
        end_game()

def end_game():
    global timer_running

    timer_running = False
    elapsed = int(time.time() - start_time)

    old_time = scores[level]["best_time"]
    old_score = scores[level]["best_score"]

    new_record = False

    if elapsed < old_time:
        scores[level]["best_time"] = elapsed
        new_record = True

    if score > old_score:
        scores[level]["best_score"] = score
        new_record = True

    save_scores()

    # FUNKY POPUP
    win = tk.Toplevel(root)
    win.title("Result")
    win.geometry("350x300")
    win.configure(bg="#222244")

    if new_record:
        title = "🔥 YOU BROKE THE RECORD! 🔥"
        sub = "Vuhuuu! You're on fire 🚀"
        color = "#00ffcc"
    else:
        title = "🎉 WELL PLAYED!"
        sub = "Try again to beat the record 💪"
        color = "#ffcc00"

    tk.Label(win, text=title,
             font=("Arial", 16, "bold"),
             fg=color, bg="#222244").pack(pady=10)

    tk.Label(win,
             text=f"Time: {elapsed}s\nScore: {score}",
             font=("Arial", 13),
             fg="white", bg="#222244").pack(pady=10)

    tk.Label(win, text=sub,
             font=("Arial", 11),
             fg="lightgreen", bg="#222244").pack(pady=5)

    if not new_record:
        tk.Label(win,
                 text=f"Best Time: {old_time}s\nHigh Score: {old_score}",
                 fg="lightblue", bg="#222244").pack()

    tk.Button(win, text="Play Again",
              bg="#00c853", fg="white",
              command=lambda: [win.destroy(), level_screen()]).pack(pady=10)

    tk.Button(win, text="Home",
              bg="#ff1744", fg="white",
              command=lambda: [win.destroy(), start_screen()]).pack()

def update_timer():
    if timer_running:
        elapsed = int(time.time() - start_time)
        timer_label.config(text=f"Time: {elapsed}s")
        root.after(1000, update_timer)

start_screen()
root.mainloop()