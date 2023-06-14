from tkinter import*
from PIL import ImageTk, Image
root = Tk()
root.title('Tech Chatbot')
root.iconbitmap('C:\\Project\\chatbot\\chatbot\\bott.jpg')


my_img = ImageTk.PhotoImage(Image.open('C:\\Project\\chatbot\\chatbot\\bott.jpg'))
my_label = Label(root,image=my_img, height=100, width=1200)
my_label.pack(pady=10)

button_quit = Button(root, text="Exit program",command=root.quit)
button_quit.pack()

 
root.mainloop()