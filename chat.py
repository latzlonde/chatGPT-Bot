from tkinter import *
import customtkinter
import openai
import os
import pickle

#initiate app
root = customtkinter.CTk()
root.title("ChatGPT bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico') #https://tkinter.com/ai_lt.ico

#set color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


#submit to chatgpt

def speak():

	if chat_entry.get():
	
	
		filename = "api_key"

		try:

			if os.path.isfile(filename):

				input_file=open(filename,'rb')

				#load data from the file into a variable

				stuff = pickle.load(input_file)


				#Query chatGPT
				#my_text.insert(END, "Working...")
				openai.api_key = stuff


				#create instance
				openai.Model.list()

				#define our query/response
				response = openai.Completion.create(
					model = "text-davinci-003",
					prompt = chat_entry.get(),
					temperature = 0,
					max_tokens = 60,
					top_p = 1.0,
					frequency_penalty = 0.0,
					presence_penalty = 0.0)

				my_text.insert(END,(response["choices"][0]["text"]).strip())
				my_text.insert(END, "\n\n")

			else:

				input_file = open(filename,'wb')

				input_file.close()

				#Error message - Need API
				my_text.insert(END, "\n\n You Need an API Key to talk to chatGPT. Get one here! \nhttps://openai.com/account/api-keys")

		except Exception as e:
				my_text.insert(END, f"\n\n There was an error \n\n{e}")

	else:
		my_text.insert(END,"\n\nHey! You forgot to write anything!")

#clear the screens
def clear():
	
	#clear main text box
	my_text.delete(1.0,END)

	#clear query text entry
	chat_entry.delete(0,END)

#update API key
def key():

	filename = "api_key"

	try:

		if os.path.isfile(filename):

			input_file=open(filename,'rb')

			#load data from the file into a variable

			stuff = pickle.load(input_file)


			api_entry.insert(END,stuff)

		else:

			input_file = open(filename,'wb')

			input_file.close()

	except Exception as e:
			my_text.insert(END, f"\n\n There was an error \n\n{e}")

	#Resize app to larger
	root.geometry('600x750')

	#resize API frame
	api_frame.pack(pady=30)


#update save API key
def save_key():

	filename = "api_key"

	try:

		#open file
		output_file = open(filename,'wb')

		#add data to entry file
		pickle.dump(api_entry.get(),output_file)

		api_entry.delete(0,END)

		#Hide API frame
		api_frame.pack_forget()

		#Resize app smaller
		root.geometry('600x600')

	except Exception as e:
			my_text.insert(END, f"\n\n There was an error \n\n{e}")

#create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)


#Add text widget to get GPT Responses
my_text = Text(text_frame,
	bg="#343638",
	width=65,
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground="#1f538d")
my_text.grid(row=0,column=0)

#create text scroll for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0,column=1,sticky="ns")

#add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

#Entry widget to type stuff to chat with chatGPT
chat_entry=customtkinter.CTkEntry(root,
placeholder_text = "Type Something to chat with ChatGPT...",
width=535,
height=50,
border_width=1)

chat_entry.pack(pady=10)

#Create Button Frame
button_frame=customtkinter.CTkFrame(root,fg_color="#242424")
button_frame.pack(pady=10)

#create buttons

clear_button=customtkinter.CTkButton(button_frame,
	text="clear response",
	command=clear)

clear_button.grid(row=0, column=1, padx=35)


submit_button=customtkinter.CTkButton(button_frame,
	text="Speak to ChatGPT",
	command=speak)

submit_button.grid(row=0, column=2, padx=25)


api_button=customtkinter.CTkButton(button_frame,
	text="Update API key",
	command=key)

api_button.grid(row=0, column=0, padx=25)


#Add API key frame
api_frame=customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

#API Entry widget
api_entry=customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter Your API key here",
	width=350, height=50, border_width=1)

api_entry.grid(row=0,column=0,padx=20,pady=20)

#add API button
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save Key",
	command=save_key)
api_save_button.grid(row=0,column=1,padx=10)




root.mainloop()