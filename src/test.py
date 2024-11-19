import customtkinter as ctk

app = ctk.CTk()

# Create the outer frame
outer_frame = ctk.CTkFrame(app)
outer_frame.grid(row=0, column=0, padx=20, pady=20)

# Create the inner frames
frame1 = ctk.CTkFrame(outer_frame)
frame1.grid(row=0, column=0, padx=10, pady=10)

frame2 = ctk.CTkFrame(outer_frame)
frame2.grid(row=0, column=1, padx=10, pady=10)

# Add widgets to the inner frames
label1 = ctk.CTkLabel(frame1, text="Frame 1")
label1.grid(row=0, column=0)

button1 = ctk.CTkButton(frame1, text="Button 1")
button1.grid(row=1, column=0)

label2 = ctk.CTkLabel(frame2, text="Frame 2")
label2.grid(row=0, column=0)

button2 = ctk.CTkButton(frame2, text="Button 2")
button2.grid(row=1, column=0)

app.mainloop()
