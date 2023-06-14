import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from tkinter import *
import sqlite3

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('C:\\Project\\chatbot\\chatbot\\intents2.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

# Create a connection to the database
conn1 = sqlite3.connect('history.db')
c = conn1.cursor()

# Create chat_history table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_response TEXT,
              bot_response TEXT)''')

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    print(ints)
    list_of_intents = intents_json['intents']
    total_count = len(ints)
    if total_count == 0:
        ChatLog.insert(END, " Bot: I don't understand you!\n\n")
        return 0
    count = 0
    result = ''
    while count < total_count:
        for i in list_of_intents:
            tag = ints[count]['intent']
            if i['tag'] == tag:
                result += (random.choice(i['responses']) if count == 0 else '') + (i['tag'] if count > 0 else '' ) + ( '' if count == total_count-1 else ', ')
                #result = random.choice(i['responses'])
                break
        count += 1
    return result

def save_chat_history(user_response, bot_response):
    c.execute("INSERT INTO chat_history (user_response, bot_response) VALUES (?, ?)", (user_response, bot_response))
    conn1.commit()


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    save_chat_history(msg, res)
    return res

#Creating GUI with tkinter
root = Tk()
root.title('Tech Chatbot')
root.iconbitmap('C:\\Project\\chatbot\\chatbot')

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

base = Tk()
base.title("Welcome to Tech Chatbot")
base.geometry("450x510")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="100", font="Arial")
ChatLog.config(state=DISABLED)

# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="10", height=4,
                    bd=0, bg="#661402", activebackground="#3c9d9b",fg='#ffffff',
                    command=send)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="50", height="5", font="Arial")

# Place all components on the screen
scrollbar.place(x=427, y=6, height=414)
ChatLog.place(x=6, y=6, height=414, width=420)
EntryBox.place(x=128, y=426, height=70, width=290)
SendButton.place(x=6, y=426, height=70)

base.mainloop()

# Close the connection to the database
conn1.close()
