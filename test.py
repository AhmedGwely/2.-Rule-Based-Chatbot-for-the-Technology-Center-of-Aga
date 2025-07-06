import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageSequence
import speech_recognition as sr
from gtts import gTTS
import pyglet
import os
import tempfile
import threading

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech_from_mic():
    """Recognize speech from the microphone."""
    with sr.Microphone() as source:
        print("قل شيئًا:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ar-SA")
            print(f"لقد قلت: {text}")
            return text
        except sr.RequestError as e:
            print(f"تعذر طلب النتائج من خدمة التعرف على الكلام من Google؛ {e}")
            return ""
        except Exception as e:
            print(f"خطأ في التعرف على الكلام: {e}")
            return ""


# Function to generate responses
def get_rule_based_response(user_input):
    user_input = user_input.lower()

    if (("مرحبا" in user_input) or ("ازيك" in user_input)):
        return "مرحبًا! كيف يمكنني مساعدتك اليوم؟"
    elif ("كيف حالك" in user_input):
        return "انا بافضل حال الحمد لله،انا هنا لمساعدتك كيف يمكنني مساعدتك!"
    elif( ("ما اسمك" in user_input) or ("من صانعك" in user_input)):
        return "أنا روبوت دردشة بسيط تم إنشاؤه بواسطة المهندس احمد فتحى جويلى وهو اطلق عليا شات بوت "
    elif ( ("رخصة" in user_input) or ("بناء" in user_input) or ("رخصه" in user_input) or ("رخصه مباني" in user_input)):
        return """خطوات استخراج رخصة البناء تتضمن: تحضير عقد صحة التوقيع،
        ثم التأكد من أن الأرض المطلوب بناء عليها داخل الحيز العمراني،
        ثم الحصول على الترخيص من المجلس القروي، ثم الحصول على رخصة تعلية أو توسعة 
        أو زيادة المساحة، ثم معاينة الموقع من قبل اللجنة الهندسية، سواء كان المبنى قائمًا بالفعل أو كانت قطعة الأرض فقط."""
    elif (("طلب تصالح" in user_input )or ("مخالفات البناء" in user_input ) or ("ملف تصالح" in user_input )
          or ("طلب التصالح" in user_input) or ("صالح" in user_input) or ("طلب" in user_input)):
        return """يجب استخراج شهادة بيانات اولا. الاوراق المطلوبة: واحد صورة بطاقة الرقم القومي مع الاطلاع على الاصل.
        اثنين صورة فوتوغرافية للمبنى. ثالثا رسم كروكي للمبنى. رابعا سند ملكية المبنى.
        خامسا دفع الرسوم 517 جنيه يتم الدفع بفيزا كارت."""
    elif ("شكرا" in user_input):
        return "عفوا هل يمكننى مساعدتك فى شئ اخر"
    elif (("خروج" in user_input) or ("إنهاء" in user_input) or ("توقف" in user_input)):
        return "إنهاء الدردشة."
    elif (("شكوى" in user_input) or ("تقديم شكوى" in user_input)):
        return "يرجى ذكر شكواك، وسأقوم بتسجيلها."
    else:
        return "عذرًا، لم أفهم ذلك. هل يمكنك إعادة صياغة ذلك؟"


def record_complaint():
    """Record a complaint from the user and save it to a text file."""
    print("الرجاء تسجيل الشكوى بعد سماع هذا الرسالة.")
    speak_text("الرجاء تسجيل الشكوى بعد سماع هذا الرسالة.")

    complaint = recognize_speech_from_mic()

    if complaint:
        with open("complaints.txt", "a", encoding="utf-8") as file:
            file.write(f"شكوى جديدة: {complaint}\n")
        print("تم تسجيل شكواك بنجاح.")
        speak_text("تم تسجيل شكواك بنجاح.")
    else:
        print("لم يتم تسجيل أي شكوى.")
        speak_text("لم يتم تسجيل أي شكوى.")

# Function to handle voice input and responses
def handle_speech_input():
    while True:
        user_input = recognize_speech_from_mic()
        add_text_to_chatbox(user_input, sender="User")

        response = get_rule_based_response(user_input)
        add_text_to_chatbox(response, sender="Bot")
        speak_text(response)

        if user_input.lower() in ["خروج", "إنهاء", "توقف"]:
            root.quit()
            break

# Function to convert text to speech
def speak_text(te):
    try:
        language = 'ar'
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            speech = gTTS(text=te, lang=language, slow=False)
            speech.save(fp.name)
            play_audio(fp.name)
            fp.close()
        os.remove(fp.name)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

# Function to play the generated speech
def play_audio(file):
    music = pyglet.media.load(file, streaming=False)
    music.play()
    pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), music.duration)
    pyglet.app.run()

# Function to add text to the chatbox
def add_text_to_chatbox(message, sender="User"):
    if sender == "User":
        chatbox.insert(tk.END, f"أنت: {message}\n", "user")
    else:
        chatbox.insert(tk.END, f"الروبوت: {message}\n", "bot")
    chatbox.see(tk.END)

# Function to handle input via text
def handle_text_input():
    user_input = text_entry.get()
    text_entry.delete(0, tk.END)
    add_text_to_chatbox(user_input, sender="User")
    response = get_rule_based_response(user_input)
    add_text_to_chatbox(response, sender="Bot")
    speak_text(response)
    if user_input.lower() in ["خروج", "إنهاء", "توقف"]:
        root.quit()

# Start the speech input in a separate thread to prevent blocking the GUI
def start_speech_input_thread():
    speech_thread = threading.Thread(target=handle_speech_input)
    speech_thread.daemon = True
    speech_thread.start()

# Function to update the animated GIF
def update_gif():
    try:
        frame = next(gif_frames)
        photo = ImageTk.PhotoImage(frame)
        gif_label.config(image=photo)
        gif_label.image = photo  # Keep a reference to avoid garbage collection
        root.after(100, update_gif)  # Update every 100ms
    except StopIteration:
        pass

# Create the GUI window
root = tk.Tk()
root.title("Chatbot")

# Set the full-screen mode
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# Apply a background color
root.configure(bg="#f0f0f5")

# Create a grid layout
root.columnconfigure(0, weight=1)  # Chatbox column
root.columnconfigure(1, weight=0)  # GIF column
root.rowconfigure(0, weight=1)  # Allow chatbox to expand

# Create and place the title label at the top
title_label = tk.Label(root, text="روبوت خدمة المواطنين بالمركز التكنولوجى بمدينة اجا", font=("Arial", 20, "bold"), bg="#315ea2")
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky='ew')

# Create and style the chatbox
chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 16), bg="#f7f7f7", fg="#333333", state='normal')
chatbox.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')  # Use grid instead of pack
chatbox.tag_config("user", foreground="#3498db")
chatbox.tag_config("bot", foreground="#2ecc71")

# Create a frame for the input and buttons
input_frame = tk.Frame(root, bg="#f0f0f5")
input_frame.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

# Create the text input field
text_entry = tk.Entry(input_frame, font=("Arial", 16), bg="#ffffff", fg="#333333")
text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

# Create the send button
