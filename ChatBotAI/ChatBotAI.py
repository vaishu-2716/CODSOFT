import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import difflib

print("Loading AI model... Please wait...")

MODEL_NAME = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(MODEL_NAME)
model = BlenderbotForConditionalGeneration.from_pretrained(MODEL_NAME)

SYSTEM_PROMPT = (
    "You are a friendly conversational AI. "
    "Always respond directly to the user's latest message only. "
    "Keep replies short (1–2 sentences). "
)

chat_history = []

def similar(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def generate_reply(user_msg):
    global chat_history
    if len(chat_history) >= 1:
        if similar(user_msg, chat_history[-1]) < 0.25:
            chat_history.clear()

    conversation = SYSTEM_PROMPT + "\nUser: " + user_msg + "\nAI:"
    inputs = tokenizer(conversation, return_tensors="pt")
    reply_ids = model.generate(
        **inputs,
        max_length=80,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_p=0.90,
        temperature=0.65
    )
    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True).strip()
    if "." in reply:
        reply = reply.split(".")[0] + "."
    if len(reply) < 2:
        reply = "Okay!"

    chat_history.append(user_msg)
    chat_history.append(reply)

    return reply


class LocalChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chatbot")
        self.window.geometry("420x580")
        self.window.configure(bg="#1f2c34")

        # Heading Label
        heading = tk.Label(self.window,
                           text="💬 AI CHAT ASSISTANT",
                           font=("Segoe UI", 18, "bold"),
                           fg="#00f2ff",
                           bg="#1f2c34")
        heading.pack(pady=8)

        # Chat Area
        self.chat_box = scrolledtext.ScrolledText(
            self.window, wrap=tk.WORD, state="disabled",
            font=("Segoe UI", 11),
            bg="#121b22", fg="white",
            relief="flat"
        )
        self.chat_box.pack(expand=True, fill="both", padx=8, pady=8)

        # Input Frame
        input_frame = tk.Frame(self.window, bg="#1f2c34")
        input_frame.pack(pady=4, fill="x")

        self.entry = tk.Entry(
            input_frame, font=("Segoe UI", 12),
            bg="#2a3942", fg="white",
            relief="flat", insertbackground="white"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(8, 4), ipady=10)
        self.entry.bind("<Return>", self._handle_enter)

        send_btn = ttk.Button(input_frame, text="➤", width=4, command=self.send_message)
        send_btn.pack(side="right", padx=(4, 8))

        self._style_buttons()

    def _style_buttons(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 14, "bold"),
                        foreground="white",
                        background="#00a884",
                        padding=5)
        style.map("TButton", background=[("active", "#008f72")])

    def _handle_enter(self, event):
        self.send_message()
        return "break"

    def add_message_bubble(self, message, is_user=True):
        self.chat_box.configure(state="normal")

        # bubble container
        frame = tk.Frame(self.chat_box, bg="#121b22")

        bubble_bg = "#005c4b" if is_user else "#202c33"
        bubble = tk.Label(
            frame, text=message, wraplength=260,
            bg=bubble_bg, fg="white",
            padx=10, pady=6, justify="left",
            font=("Segoe UI", 11), anchor="w"
        )
        # Align right for user, left for AI
        bubble.pack(anchor="e" if is_user else "w", pady=3, padx=6)
        frame.pack(anchor="e" if is_user else "w", fill="x")

        self.chat_box.window_create(tk.END, window=frame)
        self.chat_box.insert(tk.END, "\n")

        self.chat_box.configure(state="disabled")
        self.chat_box.yview(tk.END)

    def send_message(self):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return

        self.entry.delete(0, tk.END)
        self.add_message_bubble(user_msg, is_user=True)

        threading.Thread(target=self.get_reply, args=(user_msg,), daemon=True).start()

    def get_reply(self, user_msg):
        ai_reply = generate_reply(user_msg)
        self.add_message_bubble(ai_reply, is_user=False)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = LocalChatbotGUI()
    app.run()
