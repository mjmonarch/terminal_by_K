import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime


### CONSTANTS ###
URL = "https://rest-access-scope.herokuapp.com/"


### GUI part, build using tkinter framework ###
# setting up main window frame

root = tk.Tk()
root.title("WAGA service terminal - admin panel")
root.config(bg="#DDDDDD")
root.geometry("1200x900")
root.minsize(width=1200, height=900)
root.maxsize(width=1200, height=900)


# setting up observing variables
password = tk.StringVar()

# functions definition
def auth():
    global password, user_token

    body = {
        "username": "admin",
        "password": password.get()
    }
    response = requests.post(URL+'auth', json=body)
    if response.status_code == 200:
        user_token = response.json()['access_token']
        console.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')}: Autentification was succesfull\n")
   
        entry_2.config(state=tk.DISABLED)
        button_auth.config(state=tk.DISABLED)
        button_add_user.config(state=tk.NORMAL)
    else:
        console.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')}: Autentification was unsuccesfull\n", 'failure')
        messagebox.showerror(title="Authentification error", message=response.json()['description'] + '\n' + f'status code: {response.status_code}')

def show_users():
    pass

def show_user():
    pass

def add_user():
    global user_token

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    def add_user_REST():
        global user_token

        print(entry_t1.get(), entry_t2.get())
        if entry_t1.get() != '' and entry_t2.get() != '':
            body = {
                "username": entry_t1.get(),
                "password": entry_t2.get()
            }
            headers =  {"Authorization": "JWT " + user_token}
            response = requests.post(URL+'register', json=body, headers=headers)

            print(response.json())
            if response.status_code == 201:
                console.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')}: User {entry_t1.get()} successfully added\n", 'success')
                messagebox.showinfo(title="Add user", message=f"User {entry_t1.get()} successfully added")
            elif response.status_code == 400:
                console.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')}: User {entry_t1.get()} already exists\n", 'failure')
                messagebox.showerror(title="Add user", message=f"User {entry_t1.get()} already exists")
            else:
                console.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')}: Failed adding {entry_t1.get()}\n", 'failure')
                messagebox.showerror(title="Add user", message=f"Failed adding {entry_t1.get()}")
        
        else:
            console.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')}: Empty username or login while adding user\n", 'failure')
            messagebox.showerror(title="Error adding user", message="username ot password can't be empty")

    # create necessary widgets
    frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=1)
    label_t1 = tk.Label(frame_2_1, text="username:", font=("Arial", "12", "normal"), anchor=tk.W, bg="#FFFFFF") 
    label_t2 = tk.Label(frame_2_1, text="password:", font=("Arial", "12", "normal"), anchor=tk.W, bg="#FFFFFF")
    entry_t1 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    entry_t2 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), show="*", state=tk.NORMAL)
    button_t1 = tk.Button(frame_2_1, text="Create", font=("Arial", "12", "bold"), justify=tk.CENTER, command=add_user_REST)

    label_t1.grid(row=1, column=1, sticky=tk.W+tk.E)
    label_t2.grid(row=2, column=1, sticky=tk.W+tk.E)
    entry_t1.grid(row=1, column=2, sticky=tk.W+tk.E)
    entry_t2.grid(row=2, column=2, sticky=tk.W+tk.E)
    button_t1.grid(row=3, column=1, columnspan=2, sticky=tk.W+tk.E)
    frame_2_1.pack(side=tk.TOP, padx=10, pady=10)

    # for widget in frame_2.winfo_children():
    #     widget.grid_propagate(False)


def edit_user():
    pass
    

# setting up top-level elements
frame_1 = tk.Frame(root, width=210, height=840, bg="#FFFFFF")
frame_2 = tk.Frame(root, width=590, height=840, bg="#FFFFFF")
frame_4 = tk.Frame(root, width=500, height=840, bg="#FFFFFF")
for frame in frame_1, frame_2, frame_4:
    frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH)
    frame.pack_propagate(False)
    frame.grid_propagate(False)

# setting up first frame
password = tk.StringVar()

label_stab_1 = tk.Label(frame_1, text="_____________________________", font=("Arial", "12", "normal"), bg="#FFFFFF", anchor=tk.CENTER)
frame_1_1 = tk.Frame(frame_1, bg="#FFFFFF", padx=1, pady=1)
label_1 = tk.Label(frame_1_1, text="Enter password for administrator:", font=("Arial", "12", "normal"), anchor=tk.W, bg="#FFFFFF") 
label_2 = tk.Label(frame_1_1, text="password:", font=("Arial", "12", "normal"), anchor=tk.W, bg="#FFFFFF")
entry_2 = tk.Entry(frame_1_1, textvariable=password, font=("Arial", "12", "normal"), width=19, show="*")
button_auth = tk.Button(frame_1_1, text="Connect", font=("Arial", "12", "bold"), justify=tk.CENTER, command=auth)
label_stab_2 = tk.Label(frame_1, text="_____________________________", font=("Arial", "12", "normal"), bg="#FFFFFF", anchor=tk.CENTER)
label_user = tk.Label(frame_1, text="USERS", font=("Arial", "12", "bold"), bg="#FFFFFF", anchor=tk.CENTER)

button_show_users = tk.Button(frame_1, text="Show users", font=("Arial", "12", "bold"), justify=tk.CENTER, command=show_users, state=tk.DISABLED)
button_show_user = tk.Button(frame_1, text="Show user", font=("Arial", "12", "bold"), justify=tk.CENTER, command=show_user, state=tk.DISABLED)
button_add_user = tk.Button(frame_1, text="Add user", font=("Arial", "12", "bold"), justify=tk.CENTER, command=add_user, state=tk.DISABLED)
button_edit_user = tk.Button(frame_1, text="Show user", font=("Arial", "12", "bold"), justify=tk.CENTER, command=edit_user, state=tk.DISABLED)
label_stab_3 = tk.Label(frame_1, text="_____________________________", font=("Arial", "12", "normal"), bg="#FFFFFF", anchor=tk.CENTER)
label_wim = tk.Label(frame_1, text="WIMS", font=("Arial", "12", "bold"), bg="#FFFFFF", anchor=tk.CENTER)

button_quit = tk.Button(frame_1, text="Exit", font=("Arial", "12", "bold"), justify=tk.CENTER, command=quit)

label_1.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E)
label_2.grid(row=2, column=1, sticky=tk.W+tk.E)
# label_2.grid_propagate(False)
entry_2.grid(row=2, column=2, sticky=tk.W+tk.E)
button_auth.grid(row=3, column=1, columnspan=2, sticky=tk.W+tk.E)

label_stab_1.pack(side=tk.TOP, padx=1, pady=5, ipady=10, fill=tk.X)
frame_1_1.pack(side=tk.TOP, padx=1, pady=5, ipady=5, fill=tk.X)
label_stab_2.pack(side=tk.TOP, padx=1, pady=5, ipady=10, fill=tk.X)
label_user.pack(side=tk.TOP, padx=1, pady=5, ipady=5, fill=tk.X)

button_show_users.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_show_user.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_add_user.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_edit_user.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
label_stab_3.pack(side=tk.TOP, padx=1, pady=5, ipady=10, fill=tk.X)
label_wim.pack(side=tk.TOP, padx=1, pady=5, ipady=5, fill=tk.X)



button_quit.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)
 
# setting up second frame



# setting up third frame



# setting up fourth frame
console = tk.Text(frame_4, font=("Arial", "12", "normal"), height=61, yscrollcommand=set())
button_4 = tk.Button(frame_4, text="Clear", font=("Arial", "12", "bold"), justify=tk.CENTER, command=lambda: console.delete(1.0,tk.END))

console.pack_propagate(False)
console.pack(side=tk.TOP, fill=tk.BOTH)
console.tag_config('success', foreground='green')
console.tag_config('failure', foreground='red')
# make console read only
console.bind("<Key>", lambda e: 'break')
button_4.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)


root.mainloop()