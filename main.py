from tkinter import *
from async_tkinter_loop import async_handler, async_mainloop
import clipboard
from openai import AsyncOpenAI


#Заготовка окна
client = AsyncOpenAI(api_key="API-TOKEN")
ai_messages = []

window = Tk()
window.title("GPT") 
window.geometry('1080x720')
window.config(bg="#343541") #меняем цвет фона окна



@async_handler
async def Response():
    answer.configure(state="normal")
    answer.delete(1.0, END) 
    question = field.get("1.0", "end")

    answer.insert(1.0, "Thinking...")
    answer.configure(state="disabled")
    send_btn.config(state='disabled', background="#2A756A", foreground="#9CA0A6", cursor='')
    regenerate_btn.config(state='disabled', cursor='')

    ai_messages = [{"role": "user", "content": question}]
    completion = await client.chat.completions.create(model="gpt-3.5-turbo", messages=ai_messages)
    chat_response = completion.choices[0].message.content
    ai_messages.append({"role": "assistant", "content": chat_response})

    answer.delete(1.0, END)
    answer.insert(1.0, chat_response)
    answer.configure(state="disabled")

    send_btn.config(state='normal', background="#10A37F", foreground="WHITE", cursor='hand2')
    regenerate_btn.config(state='normal', cursor='hand2')


#поле ответа ChatGPT
#создаём объект answer, задаём шрифт, задний фон текста, цвет букв и перенос текста по словам (wrap=WORD)
answer = Text(window, font = ("Calibri", 15), background="#343541", bd = 0, fg = "white", selectbackground="#10A37F", wrap=WORD)
answer.place(width = 900, height = 400, x = 120, y = 47)
answer.configure(state="normal") 
answer.insert(1.0, "Waiting for your question") #добавляем текст (Waiting for your question)
answer.configure(state="disabled") #выключаем редактирование этого поля

#задний фон меню пользователя
user_frame = Label(window, background = "#444654", bd = 1, width = 220, height= 21)
user_frame.place(x = 0, y = 500) 

#поле для ввода. Задаём шрифт, задний фон текста, цвет букв и перенос текста по словам (wrap=WORD)
field = Text(window, font = ("Calibri", 15), background="#40414F", bd = 0, fg = "white", selectbackground="#10A37F", wrap=WORD)
field.place(width = 750, height = 50, x = 120, y = 590)
field.mark_set(INSERT, "1.7") #устанавливаем метку
field.configure(fg="#7A8EA0")
field.insert(1.0, "Send a message") #добавляем текст (Send a message)
field.configure(state='disabled') #выключаем редактирование этого поля

#иконка GPT
gpt_image_file = PhotoImage(file = "GPT.png")
gpt_icon = Label(window, image = gpt_image_file, bd = 0,)
gpt_icon.place(x = 50, y = 40)


#иконка User'а
user_image_file = PhotoImage(file = "User.png") 
user_icon = Label(window, image = user_image_file, bd = 0)
user_icon.place(x = 50, y = 595)

#функции от кнопок


#кнопки
send_btn = Button(
    window,
    background="#10A37F",
    foreground="WHITE",
    activebackground="#2A756A",
    activeforeground="#9CA0A6",
    width=15,
    height=1,
    border=0,
    cursor='hand2', #изменяем курсор
    text='Save & Submit',
    command = Response, # добавляем функцию при нажатии на кнопку
    font=('Calibri', 13)
)
send_btn.place(x = 910, y = 598)



def gpt_restart():
    ai_messages.clear()

def ai_copy():
    copy = answer.get(1.0, END)
    clipboard.copy(copy)

regen_btn_png = PhotoImage(file = "restart.png")
regenerate_btn = Button(
    window,
    background="#343541",
    activebackground="#343541",
    image = regen_btn_png,
    width=40,
    height=40,
    border=0,
    cursor='hand2',
    text='Regenerate',
    command = gpt_restart,
    font=('Calibri', 13)
)
regenerate_btn.place(x = 50, y = 90)

copy_btn_png = PhotoImage(file = "copy.png")
copy_ai_btn = Button(
    window,
    background="#343541",
    activebackground="#343541",
    image = copy_btn_png,
    width=30,
    height=30,
    border=0,
    cursor='hand2',
    text='Copy',
    command = ai_copy,
    font=('Calibri', 13)
)
copy_ai_btn.place(x = 55, y = 150)

#блоки биндов
def on_focus_in(entry):
    if entry.cget('state') == 'disabled':
        entry.configure(state='normal', fg = "white")
        entry.delete(1.0, 'end')
     
def on_focus_out(entry, placeholder):
    if entry.get(1.0) == "\n":
        entry.insert(1.0, placeholder)
        entry.configure(state='disabled', fg = "#7A8EA0")

field_focus_in = field.bind('<Button-1>', lambda f: on_focus_in(field))
field_focus_out = field.bind('<FocusOut>', lambda f: on_focus_out(field, 'Send a message'))



def text_copy(text_type):
    window.bind("<Control-KeyPress>", lambda e: keypress(e, text_type))

def keypress(e, text_type):
    if e.keycode == 86 and e.keysym != 'v':
       text_to_insert = clipboard.paste()
       field.insert("insert", text_to_insert) 
    elif e.keycode == 67 and e.keysym != 'c':
        selected_text = text_type.get('sel.first', 'sel.last')
        clipboard.copy(selected_text)
answer.bind("<FocusIn>", lambda c: text_copy(answer))
field.bind("<FocusIn>", lambda c: text_copy(field))

def response_enter():
    Response()
field.bind("<Return>", response_enter)





async_mainloop(window)