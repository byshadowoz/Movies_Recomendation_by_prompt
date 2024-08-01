from customtkinter import *

app = CTk()

app.geometry("500x600")

btn = CTkButton(master=app, text='Click me', corner_radius=10)
btn.place(relx=0.5, rely=0.5, anchor='center')

app.mainloop()