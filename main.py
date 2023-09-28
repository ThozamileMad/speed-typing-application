from tkinter import *
from tkinter import messagebox, TclError
from PIL import ImageTk, Image
from random import choice


def destroy_window():
    try:
        window.destroy()
    except TclError:
        pass


def restart_end(title, message, message2):
    global wps_count, seconds, random_story
    if stories != []:
        restart = messagebox.askokcancel(title=title,
                                         message=message)
        if restart:
            textbox.delete("1.0", "end")
            seconds = 0
            wps_count = 0
            countdown(60)
            random_story = choice(stories)
            test_label["text"] = random_story
            stories.remove(random_story)
        else:
            destroy_window()
    else:
        messagebox.showinfo(title=title, message=message2)
        destroy_window()


def countdown(count):
    global seconds, timer
    start_but.destroy()
    seconds = count
    wps_countdown["text"] = f"WPS: {wps_count}       Countdown: {seconds}"
    if count > 0:
        timer = window.after(1000, countdown, count - 1)
    else:
        restart_end("Test Failed",
                    "The user was unable to finish the test under the allocated time. Do you wish to restart the speed typing test.",
                    "The user was unable to finish the test under the allocated time.")


def text_counter(e):
    global wps_count
    let_sym_num = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!~@#$%^&*()_-+=[{]}|\:;'?/>.<,")
    user_input = textbox.get(1.0, END + "-1c") + e.char
    writing = test_label["text"]
    try:
        if user_input[-1] not in let_sym_num and user_input[-1] != " ":
            user_input = user_input[:-2]
        elif user_input.split() != writing.split():
            count = sum(
                [1 for num in range(len(user_input)) if user_input[num] != " " and user_input[num] == writing[num]])
            wps_count = count
        else:
            striped_user_input = "".join(user_input.split())
            wps_count = len(striped_user_input)
            if seconds != 0:
                wps_countdown["text"] = f"WPS: {wps_count}       Countdown: {seconds}"
                window.after_cancel(timer)
                restart_end("Success",
                            f"Congratulations Speed Typer!!! you have typed {wps_count} words in the span of 60 seconds!!! Do you wish to restart the speed typing test.",
                            f"Congratulations Speed Typer!!! you have typed {wps_count} words in the span of 60 seconds!!!")

    except IndexError:
        pass

    try:
        wps_countdown["text"] = f"WPS: {wps_count}       Countdown: {seconds}"
    except TclError:
        pass


window = Tk()
window.title("Speed Typing Test")
window.config(width=700, height=500)

seconds = 0
wps_count = 0
timer = None

help_but = Button(text="Help?", command=lambda: messagebox.showinfo(title="Speed Typing",
                                                                    message="Type the words below as fast as you can!!! Click the start button below the textbox to start the speed test."))
help_but.place(x=10, y=10)

speed_img = ImageTk.PhotoImage(Image.open("speed.png").resize((70, 70)))
image_lab = Label(image=speed_img)
image_lab.grid(row=0, column=1)

wps_countdown = Label(font=("Helvetica", 16))
wps_countdown.grid(row=1, column=1)

with open("stories.txt") as file:
    stories = [story.strip() for story in file.read().split("#")]
    random_story = choice(stories)
    stories.remove(random_story)

test_label = Label(text=random_story, font=("", 15))
test_label.grid(row=2, column=1)

textbox = Text(font=("Helvetica", 0), height=5, state="disabled")
textbox.grid(row=3, column=1)

start_but = Button(text="Start Speed Test", command=lambda : [countdown(60), textbox.config(state="normal")], width=15)
start_but.grid(row=4, column=1)

textbox.bind("<Key>", text_counter)

window.mainloop()

textbox.bind("<Key>", text_counter)

window.mainloop()
