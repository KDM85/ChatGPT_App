import customtkinter as ctk
import openai
from settings import *

# import tkinter as tk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setup ChatGPT
        openai.api_key = "paste your api key here"
        self.messages = MESSAGES

        # Setup Window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("ChatGPT")

        # Draw Window
        self.chat_history = self.create_frame()
        self.text_input = self.create_input_textbox()
        self.text_input.bind("<Shift-Return>", self.ask_gpt)

    # Build Frames
    def create_frame(self):
        frame = ctk.CTkScrollableFrame(
            master=self, corner_radius=10, height=800, width=600
        )
        frame.pack(
            padx=10,
            pady=10,
            expand=True,
            fill="both",
        )
        return frame

    def create_input_textbox(self):
        textbox = ctk.CTkTextbox(master=self, font=FONT, wrap="word", height=100)
        textbox.pack(padx=10, pady=10, expand=True, fill="both")
        return textbox

    def create_message_textbox(self, frame):
        textbox = ctk.CTkTextbox(master=frame, font=FONT, wrap="word", height=1)
        textbox.pack(padx=10, pady=10, expand=True, fill="both")
        return textbox

    def inspect_wrapline(self, event, index1, index2, *args):
        args = [event._w, "count"] + ["-" + arg for arg in args] + [index1, index2]
        result = event.tk.call(*args)
        return result

    def resize_textbox(self, event):
        textbox = event.widget
        textbox.unbind("<Configure>")
        textbox.update_idletasks()
        count = self.inspect_wrapline(textbox, "1.0", "end", "displaylines")
        desired_height = count
        textbox.configure(height=desired_height)

    def ask_gpt(self, _):
        message = self.create_message_textbox(self.chat_history)
        prompt = "You: " + self.text_input.get("0.0", "end")
        message.insert("0.0", prompt)
        message.update_idletasks()
        message.bind("<Configure>", self.resize_textbox)
        message.configure(fg_color=USER_BG, state="disabled")
        self.text_input.delete("0.0", "end")

        reply = self.call_ChatGPT(prompt)
        response = self.create_message_textbox(self.chat_history)
        response.insert("0.0", "ChatGPT: " + reply)
        response.update_idletasks()
        response.bind("<Configure>", self.resize_textbox)
        response.configure(fg_color=BOT_BG, state="disabled")

    def call_ChatGPT(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        reply = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply


if __name__ == "__main__":
    app = App()
    app.mainloop()
