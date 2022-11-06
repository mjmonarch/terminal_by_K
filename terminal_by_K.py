import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime


### CONSTANTS ###
URL = "https://rest-access-scope.herokuapp.com/"


### GUI part, build using tkinter framework ###
# setting up main window frame

root = tk.Tk()
root.title("WAGA service terminal")
root.config(bg="#DDDDDD")
# root.geometry("1680x900")
root.minsize(width=1680, height=900)
root.maxsize(width=1680, height=900)


# setting up observing variables
# status = tk.StringVar()
login = tk.StringVar()
password = tk.StringVar()

# functions definition
def auth():
    global login, password, user_token

    # memo_2.config(text=login.get())

    body = {"username": login.get(), "password": password.get()}
    response = requests.post(URL + "auth", json=body)
    if response.status_code == 200:
        user_token = response.json()["access_token"]
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: Autentification for {login.get()} was succesfull\n",
            "success",
        )
        if login.get() == "admin":
            pass

        entry_1.config(state=tk.DISABLED)
        entry_2.config(state=tk.DISABLED)
        button_3.config(state=tk.DISABLED)
        # memo_2.config(fg="dark green")
    else:
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: Autentification for {login.get()} was unsuccesfull\n",
            "failure",
        )
        messagebox.showerror(
            title="Authentification error",
            message=response.json()["description"]
            + "\n"
            + f"status code: {response.status_code}",
        )


# setting up top-level elements
frame_1 = tk.Frame(root, width=280, height=840, bg="#FFFFFF")
frame_2 = tk.Frame(root, width=600, height=840, bg="#FFFFFF")
frame_3 = tk.Frame(root, width=500, height=840, bg="#FFFFFF")
frame_4 = tk.Frame(root, width=300, height=840, bg="#FFFFFF")
for frame in frame_1, frame_2, frame_3, frame_4:
    frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH)


# memo_1 = tk.Message(frame_4, textvariable=status, font=("Arial", "12", "bold"), bg="#FFFFFF", anchor=tk.W)
# memo_2 = tk.Message(frame_4, font=("Arial", "16", "bold"), bg="#FFFFFF", fg="red", anchor=tk.CENTER, aspect=1000)

frame_1_1 = tk.Frame(
    frame_1,
    highlightbackground="#171717",
    highlightthickness=1,
    bg="#FFFFFF",
    padx=1,
    pady=1,
)
label_1 = tk.Label(
    frame_1_1, text="login:", font=("Arial", "12", "normal"), anchor=tk.W, bg="#FFFFFF"
)
label_2 = tk.Label(
    frame_1_1,
    text="password:",
    font=("Arial", "12", "normal"),
    anchor=tk.W,
    bg="#FFFFFF",
)
entry_1 = tk.Entry(frame_1_1, textvariable=login, font=("Arial", "12", "normal"))
entry_2 = tk.Entry(
    frame_1_1, textvariable=password, font=("Arial", "12", "normal"), show="*"
)
button_3 = tk.Button(
    frame_1_1,
    text="Connect",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=auth,
)

button_1 = tk.Button(
    frame_1,
    text="Start",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    state=tk.DISABLED,
)
button_2 = tk.Button(
    frame_1, text="Exit", font=("Arial", "12", "bold"), justify=tk.CENTER, command=quit
)

label_1.grid(row=1, column=1, sticky=tk.W + tk.E)
label_2.grid(row=2, column=1, sticky=tk.W + tk.E)
label_2.grid_propagate(False)
entry_1.grid(row=1, column=2, sticky=tk.W + tk.E)
entry_2.grid(row=2, column=2, sticky=tk.W + tk.E)
button_3.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)

frame_1_1.pack_propagate(False)
frame_1_1.pack(side=tk.TOP, padx=1, pady=1, fill=tk.X)
button_1.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)
button_2.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)


# setting up second frame


# setting up third frame


# setting up fourth frame
console = tk.Text(
    frame_4, font=("Arial", "12", "normal"), height=61, yscrollcommand=set()
)
button_4 = tk.Button(
    frame_4,
    text="Clear",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=lambda: console.delete(1.0, tk.END),
)

console.pack_propagate(False)
console.pack(side=tk.TOP, fill=tk.BOTH)
console.tag_config("success", foreground="green")
console.tag_config("failure", foreground="red")
# make console read only
console.bind("<Key>", lambda e: "break")
button_4.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)


root.mainloop()
