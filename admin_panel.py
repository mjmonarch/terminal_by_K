import tkinter as tk
from datetime import datetime
import uuid as uuid2

from tkinter import ttk

import requests

### CONSTANTS ###
# URL = "https://rest-access-scope.herokuapp.com"
URL = "http://127.0.0.1:5000"


### GUI part, build using tkinter framework ###
# setting up main window frame

root = tk.Tk()
root.title("WAGA service terminal - admin panel")
root.config(bg="#DDDDDD")
root.geometry("1200x900")
root.minsize(width=1200, height=900)
root.maxsize(width=1200, height=900)


# helper functions
def is_valid_uuid(uuid_to_test):

    try:
        uuid_obj = uuid2.UUID(uuid_to_test)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


# functions definition
def auth():
    global password, user_token

    body = {"username": "admin", "password": password.get()}
    response = requests.post(URL + "/auth", json=body)
    if response.status_code == 200:
        user_token = response.json()["access_token"]
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: Autentification was succesfull\n",
        )

        for item in entry_2, button_auth:
            item.config(state=tk.DISABLED)

        for item in (
            button_add_user,
            button_edit_user,
            button_show_users,
            button_delete_user,
        ):
            item.config(state=tk.NORMAL)

        for item in (
            button_add_wim,
            button_edit_wim,
            button_show_wims,
            button_delete_wim,
        ):
            item.config(state=tk.NORMAL)

    else:
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: Autentification was unsuccesfull\n",
            "failure",
        )


def show_associated_wims_full(self):
    global user_token
    user_id = str(self.widget["text"])

    headers = {"Authorization": "JWT " + user_token}
    response = requests.get(URL + "/user/id/" + user_id, headers=headers)

    if response.status_code == 200:
        wims = response.json()["wims"]

        if len(frame_2.winfo_children()) == 3:
            frame_2.winfo_children()[2].destroy()

        frame_2_2 = tk.Frame(frame_2, bg="#FFFFFF", width=590)
        for i in range(1, 4):
            frame_2_2.grid_columnconfigure(i, weight=1)
        frame_2_2.grid_columnconfigure(4, weight=3)

        row = 1
        label_t0 = tk.Label(
            frame_2_2,
            text=f"WIMS associated with User with id={user_id}",
            font=("Arial", "12", "normal"),
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
            justify=tk.CENTER,
        )
        label_t1 = tk.Label(
            frame_2_2,
            text="id",
            font=("Arial", "12", "normal"),
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t2 = tk.Label(
            frame_2_2,
            text="  name",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t3 = tk.Label(
            frame_2_2,
            text="  device_id",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t4 = tk.Label(
            frame_2_2,
            text="  UUID",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t0.grid(row=row, column=1, columnspan=4, sticky=tk.W + tk.E)
        row += 1
        label_t1.grid(row=row, column=1, sticky=tk.W + tk.E)
        label_t2.grid(row=row, column=2, sticky=tk.W + tk.E)
        label_t3.grid(row=row, column=3, sticky=tk.W + tk.E)
        label_t4.grid(row=row, column=4, sticky=tk.W + tk.E)

        row += 1
        for wim in wims:
            label_t1 = tk.Label(
                frame_2_2,
                text=wim["id"],
                font=("Arial", "12", "normal"),
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t2 = tk.Label(
                frame_2_2,
                text="  " + wim["name"],
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )
            label_t3 = tk.Label(
                frame_2_2,
                text="  " + str(wim["device_id"]),
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )
            label_t4 = tk.Label(
                frame_2_2,
                text="  " + wim["uuid"],
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )

            label_t1.grid(row=row, column=1, sticky=tk.W + tk.E)
            label_t2.grid(row=row, column=2, sticky=tk.W + tk.E)
            label_t3.grid(row=row, column=3, ipadx=10, sticky=tk.W + tk.E)
            label_t4.grid(row=row, column=4, ipadx=10, sticky=tk.W + tk.E)
            row += 1

        frame_2_2.pack(side=tk.TOP, fill=tk.X)


def show_users():
    global user_token

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    headers = {"Authorization": "JWT " + user_token}
    response = requests.get(URL + "/users", headers=headers)

    if response.status_code == 200:
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: query for 'Users' endpoint\n",
        )
        users = response.json()["Users"]

        frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", width=590)

        for i in range(1, 4):
            frame_2_1.grid_columnconfigure(i, weight=1)
        stab_t = ttk.Separator(frame_2, orient=tk.HORIZONTAL)

        row = 1
        label_t1 = tk.Label(
            frame_2_1,
            text="id",
            font=("Arial", "12", "normal"),
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t2 = tk.Label(
            frame_2_1,
            text="  username",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t3 = tk.Label(
            frame_2_1,
            text="  password",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t1.grid(row=row, column=1, sticky=tk.W + tk.E)
        label_t2.grid(row=row, column=2, sticky=tk.W + tk.E)
        label_t3.grid(row=row, column=3, sticky=tk.W + tk.E)
        row += 1
        label_id_list_t = list()
        for user in users:
            label_t1 = tk.Label(
                frame_2_1,
                text=user["id"],
                font=("Arial", "12", "normal"),
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_id_list_t.append(label_t1)
            label_t2 = tk.Label(
                frame_2_1,
                text="  " + user["username"],
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )
            label_t3 = tk.Label(
                frame_2_1,
                text="  " + user["password"],
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )

            label_t1.grid(row=row, column=1, sticky=tk.W + tk.E)
            label_t2.grid(row=row, column=2, sticky=tk.W + tk.E)
            label_t3.grid(row=row, column=3, ipadx=10, sticky=tk.W + tk.E)
            row += 1
        for label in label_id_list_t:
            label.bind("<Button-1>", show_associated_wims_full)
        frame_2_1.pack(side=tk.TOP, fill=tk.X)
        stab_t.pack(side=tk.TOP, pady=12, fill=tk.X)

    else:
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: Failed show users\n",
            "failure",
        )

    frame_1.focus_set()


def show_wims():
    global user_token

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    for i in range(1, 4):
        frame_2.grid_columnconfigure(i, weight=1)
    frame_2.grid_columnconfigure(4, weight=3)

    headers = {"Authorization": "JWT " + user_token}
    response = requests.get(URL + "/wims", headers=headers)

    if response.status_code == 200:
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: query for 'WIMs' endpoint\n",
        )
        wims = response.json()["WIMs"]

        row = 1
        label_t1 = tk.Label(
            frame_2,
            text="id",
            font=("Arial", "12", "normal"),
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t2 = tk.Label(
            frame_2,
            text="  name",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t3 = tk.Label(
            frame_2,
            text="  device_id",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t4 = tk.Label(
            frame_2,
            text="  UUID",
            font=("Arial", "12", "normal"),
            anchor=tk.W,
            fg="#FFFFFF",
            bg="#4B006E",
            height=2,
        )
        label_t1.grid(row=row, column=1, sticky=tk.W + tk.E)
        label_t2.grid(row=row, column=2, sticky=tk.W + tk.E)
        label_t3.grid(row=row, column=3, sticky=tk.W + tk.E)
        label_t4.grid(row=row, column=4, sticky=tk.W + tk.E)
        row += 1
        for wim in wims:
            label_t1 = tk.Label(
                frame_2,
                text=wim["id"],
                font=("Arial", "12", "normal"),
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t2 = tk.Label(
                frame_2,
                text="  " + wim["name"],
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )
            label_t3 = tk.Label(
                frame_2,
                text="  " + str(wim["device_id"]),
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )
            label_t4 = tk.Label(
                frame_2,
                text="  " + wim["uuid"],
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                bg="#DDDDDD",
                height=2,
            )

            label_t1.grid(row=row, column=1, sticky=tk.W + tk.E)
            label_t2.grid(row=row, column=2, sticky=tk.W + tk.E)
            label_t3.grid(row=row, column=3, ipadx=10, sticky=tk.W + tk.E)
            label_t4.grid(row=row, column=4, ipadx=10, sticky=tk.W + tk.E)
            row += 1

    else:
        console.insert(
            tk.END,
            f"{datetime.now().strftime('%H:%M:%S')}: Failed show wims\n",
            "failure",
        )

    frame_1.focus_set()


def edit_user():

    for i in range(1, 3):
        frame_2.grid_columnconfigure(i, weight=1)
    frame_2.grid_columnconfigure(3, weight=0)
    frame_2.grid_columnconfigure(4, weight=0)

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    def edit_user_REST():
        global user_token, user_id, username, pswd

        def save_changes_REST():
            global user_token, user_id, username, pswd

            headers = {"Authorization": "JWT " + user_token}
            body = {"username": username.get(), "password": pswd.get()}
            response = requests.put(
                URL + "/user/id/" + str(user_id.get()), json=body, headers=headers
            )

            if response.status_code == 201:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: User {username.get()} successfully added\n",
                    "success",
                )
            elif response.status_code == 200:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: User {username.get()} successfully changed\n",
                    "success",
                )
            elif response.status_code == 400:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: User with {username.get()} username already exists\n",
                    "failure",
                )
            elif response.status_code == 403:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Admin can't be modified!\n",
                    "failure",
                )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Failed changing {username.get()}\n",
                    "failure",
                )

        def bind_WIM_REST():
            global user_token, user_id
            headers = {"Authorization": "JWT " + user_token}
            response = requests.put(
                URL + "/user/" + str(user_id.get()) + "/" + str(device_id_add.get()),
                headers=headers,
            )

            if response.status_code == 200:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: WIM {device_id_add.get()} successfully added to {username.get()}\n",
                    "success",
                )
            elif response.status_code == 400:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: WIM {device_id_add.get()} is already binded to {username.get()}\n",
                    "failure",
                )
            elif response.status_code == 404:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: WIM {device_id_add.get()} or {username.get()} doesn't exist\n",
                    "failure",
                )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Failed adding WIM {device_id_add.get()} to {username.get()}\n",
                    "failure",
                )
            edit_user_REST()

        def unbind_WIM_REST():
            global user_token, user_id
            headers = {"Authorization": "JWT " + user_token}
            response = requests.delete(
                URL + "/user/" + str(user_id.get()) + "/" + str(device_id_delete.get()),
                headers=headers,
            )

            if response.status_code == 200:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: WIM {device_id_delete.get()} successfully deleted from {username.get()}\n",
                    "success",
                )
            elif response.status_code == 400:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: WIM {device_id_delete.get()} was not binded to {username.get()}\n",
                    "failure",
                )
            elif response.status_code == 404:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: {device_id_delete.get()} doesn't exist\n",
                    "failure",
                )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Failed deleting WIM {device_id_delete.get()} from {username.get()}\n",
                    "failure",
                )
            edit_user_REST()

        headers = {"Authorization": "JWT " + user_token}
        if entry_t1.get() == "" and entry_t2.get() == "":
            console.insert(
                tk.END,
                f"{datetime.now().strftime('%H:%M:%S')}: Enter user_id or username first\n",
                "failure",
            )
        elif entry_t1.get() != "":
            if entry_t1.get().isdigit():
                response = requests.get(
                    URL + "/user/id/" + entry_t1.get(), headers=headers
                )
                by_id = True
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Editing user: user_id should be posititive number",
                    "failure",
                )
        else:
            response = requests.get(
                URL + "/user/name/" + entry_t2.get(), headers=headers
            )
            by_id = False

        user = response.json()
        if response.status_code == 200:
            # create frame containing text labels with user info
            frame_2_2 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=10)
            for i in range(1, 4):
                frame_2_2.grid_columnconfigure(i, weight=1)
            frame_2_3 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=10)
            for i in range(1, 3):
                frame_2_3.grid_columnconfigure(i, weight=1)
            frame_2_3_1 = tk.Frame(frame_2_3, bg="#FFFFFF")
            frame_2_3_1.grid_columnconfigure(1, weight=1)
            frame_2_3_1.grid_columnconfigure(2, weight=2)
            frame_2_3_2 = tk.Frame(frame_2_3, bg="#FFFFFF")
            frame_2_3_2.grid_columnconfigure(1, weight=1)
            frame_2_3_2.grid_columnconfigure(2, weight=1)

            user_id = tk.IntVar()
            username = tk.StringVar()
            pswd = tk.StringVar()
            device_id_add = tk.StringVar()
            device_id_delete = tk.StringVar()
            label_t4 = tk.Label(
                frame_2_2,
                text="id",
                font=("Arial", "12", "normal"),
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t5 = tk.Label(
                frame_2_2,
                text="  username",
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t6 = tk.Label(
                frame_2_2,
                text="  password",
                font=("Arial", "12", "normal"),
                anchor=tk.W,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t7 = tk.Label(
                frame_2_2,
                textvariable=user_id,
                font=("Arial", "12", "normal"),
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            user_id.set(user["id"])
            entry_t3 = tk.Entry(
                frame_2_2,
                textvariable=username,
                font=("Arial", "12", "normal"),
                bg="#DDDDDD",
            )
            username.set(user["username"])
            entry_t4 = tk.Entry(
                frame_2_2,
                textvariable=pswd,
                font=("Arial", "12", "normal"),
                bg="#DDDDDD",
            )
            pswd.set(user["password"])
            button_t2 = tk.Button(
                frame_2_2,
                text="Save changes",
                font=("Arial", "12", "bold"),
                justify=tk.CENTER,
                command=save_changes_REST,
            )

            label_t4.grid(row=1, column=1, sticky=tk.W + tk.E)
            label_t5.grid(row=1, column=2, sticky=tk.W + tk.E)
            label_t6.grid(row=1, column=3, sticky=tk.W + tk.E)
            label_t7.grid(row=2, column=1, sticky=tk.W + tk.E)
            entry_t3.grid(row=2, column=2, sticky=tk.W + tk.E)
            entry_t4.grid(row=2, column=3, sticky=tk.W + tk.E)
            button_t2.grid(row=3, column=1, columnspan=3, sticky=tk.W + tk.E)
            frame_2_2.grid(row=2, column=1, columnspan=2, sticky=tk.W + tk.E)

            label_t8 = tk.Label(
                frame_2_3_1,
                text="Associated WIMS:",
                font=("Arial", "12", "bold"),
                anchor=tk.CENTER,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t9 = tk.Label(
                frame_2_3_1,
                text="device_id:",
                font=("Arial", "12", "bold"),
                anchor=tk.CENTER,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t10 = tk.Label(
                frame_2_3_1,
                text="WIM name:",
                font=("Arial", "12", "bold"),
                anchor=tk.CENTER,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t8.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)
            label_t9.grid(row=2, column=1, sticky=tk.W + tk.E)
            label_t10.grid(row=2, column=2, sticky=tk.W + tk.E)
            row = 3
            for wim in user["wims"]:
                label_t11 = tk.Label(
                    frame_2_3_1,
                    text=wim["device_id"],
                    font=("Arial", "12", "normal"),
                    anchor=tk.W,
                    bg="#FFFFFF",
                )
                label_t12 = tk.Label(
                    frame_2_3_1,
                    text=wim["name"],
                    font=("Arial", "12", "normal"),
                    anchor=tk.W,
                    bg="#FFFFFF",
                )
                label_t11.grid(row=row, column=1, sticky=tk.W + tk.E)
                label_t12.grid(row=row, column=2, sticky=tk.W + tk.E)
                row += 1
            label_t13 = tk.Label(
                frame_2_3_2,
                text="Bind/unbind WIM to User:",
                font=("Arial", "12", "bold"),
                anchor=tk.CENTER,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t14 = tk.Label(
                frame_2_3_2,
                text="device_id:",
                font=("Arial", "12", "bold"),
                anchor=tk.CENTER,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t15 = tk.Label(
                frame_2_3_2,
                text="command:",
                font=("Arial", "12", "bold"),
                anchor=tk.CENTER,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            label_t15 = tk.Label(
                frame_2_3_2,
                text="command:",
                font=("Arial", "12", "bold"),
                anchor=tk.CENTER,
                fg="#FFFFFF",
                bg="#4B006E",
                height=2,
            )
            entry_t5 = tk.Entry(
                frame_2_3_2,
                textvariable=device_id_add,
                font=("Arial", "12", "normal"),
                bg="#DDDDDD",
            )
            entry_t6 = tk.Entry(
                frame_2_3_2,
                textvariable=device_id_delete,
                font=("Arial", "12", "normal"),
                bg="#DDDDDD",
            )
            button_t3 = tk.Button(
                frame_2_3_2,
                text="Bind WIM",
                font=("Arial", "12", "bold"),
                justify=tk.CENTER,
                command=bind_WIM_REST,
            )
            button_t4 = tk.Button(
                frame_2_3_2,
                text="Unbind WIM",
                font=("Arial", "12", "bold"),
                justify=tk.CENTER,
                command=unbind_WIM_REST,
            )

            label_t13.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)
            label_t14.grid(row=2, column=1, sticky=tk.W + tk.E)
            label_t15.grid(row=2, column=2, sticky=tk.W + tk.E)
            entry_t5.grid(row=3, column=1, sticky=tk.W + tk.E)
            button_t3.grid(row=3, column=2, sticky=tk.W + tk.E)
            entry_t6.grid(row=4, column=1, sticky=tk.W + tk.E)
            button_t4.grid(row=4, column=2, sticky=tk.W + tk.E)
            frame_2_3.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)
            frame_2_3_1.grid(row=1, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
            frame_2_3_2.grid(row=1, column=2, sticky=tk.W + tk.E + tk.N + tk.S)

        elif response.status_code == 404:
            text = (
                f"{datetime.now().strftime('%H:%M:%S')}: User with user_id={entry_t1.get()} was not found\n"
                if by_id
                else f"{datetime.now().strftime('%H:%M:%S')}: User with username={entry_t2.get()} was not found\n"
            )
            console.insert(tk.END, text, "failure")
        else:
            text = (
                f"{datetime.now().strftime('%H:%M:%S')}: Failed editing user with user_id={entry_t1.get()}\n"
                if by_id
                else f"{datetime.now().strftime('%H:%M:%S')}: Failed editing user with username={entry_t2.get()}\n"
            )
            console.insert(tk.END, text, "failure")

        frame_1.focus_set()

    # create necessary widgets
    frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=10)
    for i in range(1, 4):
        frame_2_1.grid_columnconfigure(i, weight=1)
    label_t0 = tk.Label(
        frame_2_1,
        text="Enter user id or username",
        font=("Arial", "12", "bold"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t1 = tk.Label(
        frame_2_1,
        text="user_id:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t2 = tk.Label(
        frame_2_1,
        text="username:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    entry_t1 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    entry_t2 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    button_t1 = tk.Button(
        frame_2_1,
        text="Edit",
        font=("Arial", "12", "bold"),
        justify=tk.CENTER,
        command=edit_user_REST,
    )

    label_t0.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)
    label_t1.grid(row=2, column=1, sticky=tk.W + tk.E)
    label_t2.grid(row=3, column=1, sticky=tk.W + tk.E)
    entry_t1.grid(row=2, column=2, sticky=tk.W + tk.E)
    entry_t2.grid(row=3, column=2, sticky=tk.W + tk.E)
    button_t1.grid(row=4, column=1, columnspan=2, sticky=tk.W + tk.E)
    frame_2_1.grid(row=1, column=1, sticky=tk.W + tk.E)


def edit_wim():

    for i in range(1, 3):
        frame_2.grid_columnconfigure(i, weight=1)
    frame_2.grid_columnconfigure(3, weight=0)
    frame_2.grid_columnconfigure(4, weight=0)

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    def edit_wim_REST():
        global user_token, device_id, name, uuid

        def save_changes_REST():
            # global user_token, device_id, name, uuid

            if is_valid_uuid(uuid.get()):
                headers = {"Authorization": "JWT " + user_token}
                body = {"name": name.get(), "uuid": uuid.get()}
                response = requests.put(
                    URL + "/wim/" + str(device_id.get()), json=body, headers=headers
                )

                if response.status_code == 201:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM {name.get()} successfully added\n",
                        "success",
                    )
                elif response.status_code == 200:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM {name.get()} successfully changed\n",
                        "success",
                    )
                elif response.status_code == 400:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM with {name.get()} username  or {uuid.get()} UUID already exists\n",
                        "failure",
                    )
                else:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: Failed changing {username.get()}\n",
                        "failure",
                    )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Not valid UUID: {uuid.get()}\n",
                    "failure",
                )

        headers = {"Authorization": "JWT " + user_token}
        if entry_t1.get() != "":
            if entry_t1.get().isdigit():
                response = requests.get(URL + "/wim/" + entry_t1.get(), headers=headers)

                wim = response.json()
                if response.status_code == 200:
                    # create frame containing text labels with wim info
                    frame_2_2 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=10)
                    for i in range(1, 3):
                        frame_2_2.grid_columnconfigure(i, weight=1)
                    frame_2_2.grid_columnconfigure(3, weight=2)

                    name = tk.StringVar()
                    device_id = tk.IntVar()
                    uuid = tk.StringVar()
                    label_t4 = tk.Label(
                        frame_2_2,
                        text="  name",
                        font=("Arial", "12", "normal"),
                        anchor=tk.W,
                        fg="#FFFFFF",
                        bg="#4B006E",
                        height=2,
                    )
                    label_t5 = tk.Label(
                        frame_2_2,
                        text="  device_id",
                        font=("Arial", "12", "normal"),
                        anchor=tk.W,
                        fg="#FFFFFF",
                        bg="#4B006E",
                        height=2,
                    )
                    label_t6 = tk.Label(
                        frame_2_2,
                        text="  UUID",
                        font=("Arial", "12", "normal"),
                        anchor=tk.W,
                        fg="#FFFFFF",
                        bg="#4B006E",
                        height=2,
                    )
                    label_t7 = tk.Label(
                        frame_2_2,
                        textvariable=device_id,
                        font=("Arial", "12", "normal"),
                        fg="#FFFFFF",
                        bg="#4B006E",
                        height=2,
                    )
                    device_id.set(wim["device_id"])
                    entry_t3 = tk.Entry(
                        frame_2_2,
                        textvariable=name,
                        font=("Arial", "12", "normal"),
                        bg="#DDDDDD",
                    )
                    name.set(wim["name"])
                    entry_t4 = tk.Entry(
                        frame_2_2,
                        textvariable=uuid,
                        font=("Arial", "12", "normal"),
                        bg="#DDDDDD",
                    )
                    uuid.set(wim["uuid"])
                    button_t2 = tk.Button(
                        frame_2_2,
                        text="Save changes",
                        font=("Arial", "12", "bold"),
                        justify=tk.CENTER,
                        command=save_changes_REST,
                    )

                    label_t4.grid(row=1, column=1, sticky=tk.W + tk.E)
                    label_t5.grid(row=1, column=2, sticky=tk.W + tk.E)
                    label_t6.grid(row=1, column=3, sticky=tk.W + tk.E)
                    label_t7.grid(row=2, column=1, sticky=tk.W + tk.E)
                    entry_t3.grid(row=2, column=2, sticky=tk.W + tk.E)
                    entry_t4.grid(row=2, column=3, sticky=tk.W + tk.E)
                    button_t2.grid(row=3, column=1, columnspan=3, sticky=tk.W + tk.E)
                    frame_2_2.grid(row=2, column=1, columnspan=2, sticky=tk.W + tk.E)

                elif response.status_code == 404:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM with device_id={entry_t1.get()} was not found\n",
                        "failure",
                    )
                else:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: Failed editing WIM with device_id={entry_t1.get()}\n",
                        "failure",
                    )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Editing WIM: device_id should be posititive number",
                    "failure",
                )
        else:
            console.insert(
                tk.END,
                f"{datetime.now().strftime('%H:%M:%S')}: Enter WIM device_id first\n",
                "failure",
            )

        frame_1.focus_set()

    # create necessary widgets
    frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=10)
    for i in range(1, 4):
        frame_2_1.grid_columnconfigure(i, weight=1)
    label_t0 = tk.Label(
        frame_2_1,
        text="Enter WIM device_id",
        font=("Arial", "12", "bold"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t1 = tk.Label(
        frame_2_1,
        text="device_id:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    entry_t1 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    button_t1 = tk.Button(
        frame_2_1,
        text="Edit WIM",
        font=("Arial", "12", "bold"),
        justify=tk.CENTER,
        command=edit_wim_REST,
    )

    label_t0.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)
    label_t1.grid(row=2, column=1, sticky=tk.W + tk.E)
    entry_t1.grid(row=2, column=2, sticky=tk.W + tk.E)
    button_t1.grid(row=4, column=1, columnspan=2, sticky=tk.W + tk.E)
    frame_2_1.grid(row=1, column=1, sticky=tk.W + tk.E)


def add_user():

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    def add_user_REST():
        global user_token

        if entry_t1.get() != "" and entry_t2.get() != "":
            body = {"username": entry_t1.get(), "password": entry_t2.get()}
            headers = {"Authorization": "JWT " + user_token}
            response = requests.post(URL + "/register", json=body, headers=headers)

            if response.status_code == 201:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: User {entry_t1.get()} successfully added\n",
                    "success",
                )
            elif response.status_code == 400:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: User {entry_t1.get()} already exists\n",
                    "failure",
                )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Failed adding user {entry_t1.get()}\n",
                    "failure",
                )

        else:
            console.insert(
                tk.END,
                f"{datetime.now().strftime('%H:%M:%S')}: Empty username or login while adding user\n",
                "failure",
            )

        frame_1.focus_set()

    # create necessary widgets
    frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=1)
    label_t1 = tk.Label(
        frame_2_1,
        text="username:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t2 = tk.Label(
        frame_2_1,
        text="password:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    entry_t1 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    entry_t2 = tk.Entry(
        frame_2_1, font=("Arial", "12", "normal"), show="*", state=tk.NORMAL
    )
    button_t1 = tk.Button(
        frame_2_1,
        text="Create user",
        font=("Arial", "12", "bold"),
        justify=tk.CENTER,
        command=add_user_REST,
    )

    label_t1.grid(row=1, column=1, sticky=tk.W + tk.E)
    label_t2.grid(row=2, column=1, sticky=tk.W + tk.E)
    entry_t1.grid(row=1, column=2, sticky=tk.W + tk.E)
    entry_t2.grid(row=2, column=2, sticky=tk.W + tk.E)
    button_t1.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)
    # frame_2_1.grid(padx=10, pady=10)
    frame_2_1.pack(side=tk.TOP, fill=tk.X)

    frame_1.focus_set()


def add_wim():

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    def add_wim_REST():
        global user_token

        if entry_t1.get() != "" and entry_t2.get() != "" and entry_t3.get() != "":
            if is_valid_uuid(entry_t3.get()):
                body = {
                    "name": entry_t1.get(),
                    "uuid": entry_t3.get(),
                }
                headers = {"Authorization": "JWT " + user_token}
                response = requests.post(
                    URL + "/wim/" + entry_t2.get(), json=body, headers=headers
                )

                if response.status_code == 201:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM {entry_t1.get()} successfully added\n",
                        "success",
                    )
                elif response.status_code == 400:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM with some of given parameters already exists\n",
                        "failure",
                    )
                else:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: Failed adding WIM {entry_t1.get()}\n",
                        "failure",
                    )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Not valid UUID: {entry_t3.get()}\n",
                    "failure",
                )
        else:
            console.insert(
                tk.END,
                f"{datetime.now().strftime('%H:%M:%S')}: Empty WIM name or WIM device_id or WIM UUID while adding WIM\n",
                "failure",
            )

        frame_1.focus_set()

    # create necessary widgets
    frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=1)
    label_t1 = tk.Label(
        frame_2_1,
        text="name:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t2 = tk.Label(
        frame_2_1,
        text="device_id:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t3 = tk.Label(
        frame_2_1,
        text="UUID:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    entry_t1 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    entry_t2 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    entry_t3 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)

    button_t1 = tk.Button(
        frame_2_1,
        text="Create WIM",
        font=("Arial", "12", "bold"),
        justify=tk.CENTER,
        command=add_wim_REST,
    )

    label_t1.grid(row=1, column=1, sticky=tk.W + tk.E)
    label_t2.grid(row=2, column=1, sticky=tk.W + tk.E)
    label_t3.grid(row=3, column=1, sticky=tk.W + tk.E)
    entry_t1.grid(row=1, column=2, sticky=tk.W + tk.E)
    entry_t2.grid(row=2, column=2, sticky=tk.W + tk.E)
    entry_t3.grid(row=3, column=2, sticky=tk.W + tk.E)
    button_t1.grid(row=4, column=1, columnspan=2, sticky=tk.W + tk.E)
    frame_2_1.grid(padx=10, pady=10)

    frame_1.focus_set()


def delete_user():

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    def delete_user_REST():
        global user_token

        headers = {"Authorization": "JWT " + user_token}
        if entry_t1.get() != "":
            if entry_t1.get().isdigit():
                response = requests.delete(
                    URL + "/user/id/" + entry_t1.get(), headers=headers
                )

                if response.status_code == 200:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: User with user_id={entry_t1.get()} successfully deleted\n",
                        "success",
                    )
                elif response.status_code == 404:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: User with user_id={entry_t1.get()} was not found\n",
                        "failure",
                    )
                else:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: Failed deleting user with user_id={entry_t1.get()}\n",
                        "failure",
                    )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Deleting user: user_id should be posititive number",
                    "failure",
                )
        elif entry_t2.get() != "":
            response = requests.delete(
                URL + "/user/name/" + entry_t2.get(), headers=headers
            )

            if response.status_code == 200:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: User with username={entry_t2.get()} successfully deleted\n",
                    "success",
                )
            if response.status_code == 404:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: User with username={entry_t2.get()} was not found\n",
                    "failure",
                )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Failed deleting user with username={entry_t2.get()}\n",
                    "failure",
                )

        else:
            console.insert(
                tk.END,
                f"{datetime.now().strftime('%H:%M:%S')}: Enter user_id or username first\n",
                "failure",
            )

        frame_1.focus_set()

    # create necessary widgets
    frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=1)
    label_t0 = tk.Label(
        frame_2_1,
        text="Enter user id or username",
        font=("Arial", "12", "bold"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t1 = tk.Label(
        frame_2_1,
        text="user_id:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t2 = tk.Label(
        frame_2_1,
        text="username:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    entry_t1 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    entry_t2 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    button_t1 = tk.Button(
        frame_2_1,
        text="Delete",
        font=("Arial", "12", "bold"),
        justify=tk.CENTER,
        command=delete_user_REST,
    )

    label_t0.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)
    label_t1.grid(row=2, column=1, sticky=tk.W + tk.E)
    label_t2.grid(row=3, column=1, sticky=tk.W + tk.E)
    entry_t1.grid(row=2, column=2, sticky=tk.W + tk.E)
    entry_t2.grid(row=3, column=2, sticky=tk.W + tk.E)
    button_t1.grid(row=4, column=1, columnspan=2, sticky=tk.W + tk.E)
    frame_2_1.grid(padx=10, pady=10)


def delete_wim():

    # delete all widgets on frame 2
    for widget in frame_2.winfo_children():
        widget.destroy()

    def delete_wim_REST():
        global user_token

        headers = {"Authorization": "JWT " + user_token}
        if entry_t1.get() != "":
            if entry_t1.get().isdigit():
                response = requests.delete(
                    URL + "/wim/" + entry_t1.get(), headers=headers
                )

                if response.status_code == 200:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM with device_id={entry_t1.get()} successfully deleted\n",
                        "success",
                    )
                elif response.status_code == 404:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: WIM with device_id={entry_t1.get()} was not found\n",
                        "failure",
                    )
                else:
                    console.insert(
                        tk.END,
                        f"{datetime.now().strftime('%H:%M:%S')}: Failed deleting WIM with device_id={entry_t1.get()}\n",
                        "failure",
                    )
            else:
                console.insert(
                    tk.END,
                    f"{datetime.now().strftime('%H:%M:%S')}: Deleting WIM: device_id should be posititive number",
                    "failure",
                )

        else:
            console.insert(
                tk.END,
                f"{datetime.now().strftime('%H:%M:%S')}: Enter WIM device_id first\n",
                "failure",
            )

        frame_1.focus_set()

    # create necessary widgets
    frame_2_1 = tk.Frame(frame_2, bg="#FFFFFF", padx=1, pady=1)
    label_t0 = tk.Label(
        frame_2_1,
        text="Enter WIM device_id",
        font=("Arial", "12", "bold"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    label_t1 = tk.Label(
        frame_2_1,
        text="device_id:",
        font=("Arial", "12", "normal"),
        anchor=tk.W,
        bg="#FFFFFF",
    )
    # label_t2 = tk.Label(frame_2_1, text="username:", font=("Arial", "12", "normal"), anchor=tk.W, bg="#FFFFFF")
    entry_t1 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    # entry_t2 = tk.Entry(frame_2_1, font=("Arial", "12", "normal"), state=tk.NORMAL)
    button_t1 = tk.Button(
        frame_2_1,
        text="Delete",
        font=("Arial", "12", "bold"),
        justify=tk.CENTER,
        command=delete_wim_REST,
    )

    label_t0.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)
    label_t1.grid(row=2, column=1, sticky=tk.W + tk.E)
    # label_t2.grid(row=3, column=1, sticky=tk.W+tk.E)
    entry_t1.grid(row=2, column=2, sticky=tk.W + tk.E)
    # entry_t2.grid(row=3, column=2, sticky=tk.W+tk.E)
    button_t1.grid(row=4, column=1, columnspan=2, sticky=tk.W + tk.E)
    frame_2_1.grid(padx=10, pady=10)


### __________________________________________________________________________________________________________________________________________
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

stab_t1 = ttk.Separator(frame_1, orient=tk.HORIZONTAL)
frame_1_1 = tk.Frame(frame_1, bg="#FFFFFF", padx=1, pady=1)
label_1 = tk.Label(
    frame_1_1,
    text="Enter password for administrator:",
    font=("Arial", "12", "normal"),
    anchor=tk.W,
    bg="#FFFFFF",
)
label_2 = tk.Label(
    frame_1_1,
    text="password:",
    font=("Arial", "12", "normal"),
    anchor=tk.W,
    bg="#FFFFFF",
)
entry_2 = tk.Entry(
    frame_1_1, textvariable=password, font=("Arial", "12", "normal"), width=19, show="*"
)
button_auth = tk.Button(
    frame_1_1,
    text="Connect",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=auth,
)
stab_t2 = ttk.Separator(frame_1, orient=tk.HORIZONTAL)
label_user = tk.Label(
    frame_1, text="USERS", font=("Arial", "12", "bold"), bg="#FFFFFF", anchor=tk.CENTER
)

button_show_users = tk.Button(
    frame_1,
    text="Show users",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=show_users,
    state=tk.DISABLED,
)
button_edit_user = tk.Button(
    frame_1,
    text="Edit user",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=edit_user,
    state=tk.DISABLED,
)
button_add_user = tk.Button(
    frame_1,
    text="Add user",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=add_user,
    state=tk.DISABLED,
)
button_delete_user = tk.Button(
    frame_1,
    text="Delete user",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=delete_user,
    state=tk.DISABLED,
)
stab_t3 = ttk.Separator(frame_1, orient=tk.HORIZONTAL)
label_wim = tk.Label(
    frame_1, text="WIMS", font=("Arial", "12", "bold"), bg="#FFFFFF", anchor=tk.CENTER
)
button_show_wims = tk.Button(
    frame_1,
    text="Show WIMs",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=show_wims,
    state=tk.DISABLED,
)
button_edit_wim = tk.Button(
    frame_1,
    text="Edit WIM",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=edit_wim,
    state=tk.DISABLED,
)
button_add_wim = tk.Button(
    frame_1,
    text="Add WIM",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=add_wim,
    state=tk.DISABLED,
)
button_delete_wim = tk.Button(
    frame_1,
    text="Delete WIM",
    font=("Arial", "12", "bold"),
    justify=tk.CENTER,
    command=delete_wim,
    state=tk.DISABLED,
)

button_quit = tk.Button(
    frame_1, text="Exit", font=("Arial", "12", "bold"), justify=tk.CENTER, command=quit
)

label_1.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)
label_2.grid(row=2, column=1, sticky=tk.W + tk.E)
entry_2.grid(row=2, column=2, sticky=tk.W + tk.E)
button_auth.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)

stab_t1.pack(side=tk.TOP, pady=20, fill=tk.X)
frame_1_1.pack(side=tk.TOP, padx=1, pady=5, ipady=5, fill=tk.X)
stab_t2.pack(side=tk.TOP, pady=20, fill=tk.X)
label_user.pack(side=tk.TOP, padx=1, pady=5, ipady=5, fill=tk.X)

button_show_users.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_edit_user.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_add_user.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_delete_user.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
stab_t3.pack(side=tk.TOP, pady=20, fill=tk.X)
label_wim.pack(side=tk.TOP, padx=1, pady=5, ipady=5, fill=tk.X)

button_show_wims.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_edit_wim.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_add_wim.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
button_delete_wim.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)


button_quit.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)

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
