'''
1. TTS = text-to-speech
2. GUI = Graphical User Interface
3. input = Entered texts or chosen input files

NOTE: If the text field is filled and also a text-file is chosen, then this tkinter-app will perform TTS only for entered texts i.e. the app will ignore chosen file.
'''

#Imported Modules and Libraries-------------------------------------------

#to implement GUI
from tkinter import *

#to choose a text-file for TTS
from tkinter.filedialog import askopenfilename

#to display alert messages
from tkinter import messagebox

#to detect input language of entered texts or chosen text-file
from langdetect import detect

#TTS API
from gtts import gTTS

#to speak the given input in the language user want
from googletrans import Translator

#to play audio file of TTS
from playsound import playsound

#to delete saved audio files when tkinter-app closes
#(EXCEPT FILES SAVED WITH 'SAVE AS MP3' BUTTON)
import os

#to display heart at bottom right corner
import emoji

#Designing Main Window----------------------------------------------------

#creating main window
w = Tk()

#title of main window
w.title("Text to Speech")

#size of main window
w.geometry("930x600")

#background colour of main window
w.configure(background = '#fff')

#Functions Section--------------------------------------------------------

#stores texts of a text-file
file_content = []

#counts how many times user used TTS in one session
tts_count = []

#function to choose a text-file to TTS
def choose_file(event):
    try:
        file_name = askopenfilename(title = "Open a text file", filetypes = [("Text files", "*.txt")])

        #if the content of a text-file is already saved in 'file-content',
        # then delete the content
        if len(file_content) > 0:
            file_content.pop()

        #storing content of the chosen text-file in 'file-content'
        file_content.append(open(file_name, 'r', encoding='utf-8').read())

        #setting states to Normal to write path,
        #name and content of the chosen text-file
        entry_displayFilePath.config(state = "normal")
        entry_displayFilename.config(state = "normal")
        text_displayFileContent.config(state = "normal")

        #removing the line "No file chosen"
        entry_displayFilePath.delete(0, END)

        #and writing the path of chosen text-file
        entry_displayFilePath.insert(END, file_name)

        #getting the name of chosen text-file
        for i in range(0, len(file_name)):
            if file_name[i] == '/':
                file_name_ind = i + 1;

        #removing the line "No file chosen"
        entry_displayFilename.delete(0, END)

        #and writing the name of chosen text-file
        entry_displayFilename.insert(END, file_name[file_name_ind:])

        #removing the line "No file chosen"
        text_displayFileContent.delete("1.0", "end")

        #and writing the content of chosen text-file
        text_displayFileContent.insert(END, file_content[0])

        #setting states to Readonly & Disabled to prevent
        #manual editing of path, name and content of the chosen text-file
        entry_displayFilePath.config(state = "readonly")
        entry_displayFilename.config(state = "readonly")
        text_displayFileContent.config(state = "disabled")
    except:
        print(end = "")

#function to perform TTS as SAY NOW or SAVE AS MP3
def speech_or_save(speech_content, ss):
    try:
        #creating an object to translate input
        translator = Translator()

        #detecting language of entered text
        text_lang = detect(speech_content)

        #getting language in which user want TTS
        speech_lang = speech_in.get()

        #if language of output voice is set to 'Default',
        #then speak in detected language of entered text
        if speech_lang == "Default":
            speech_lang = text_lang

        #translating texts from detected language to output language
        text_to_translate = translator.translate(speech_content, src=text_lang, dest = speech_lang)

        #storing translated texts
        speech_content = text_to_translate.text

        #determining speed of output voice
        if speech_speed == 0:
            speech_speed_bool = False #speak in default speed
        else:
            speech_speed_bool = True #speak in slow speed

        tts = gTTS(text = speech_content, slow = speech_speed_bool) #initialized TTS

        #if clicked on 'Order to Say'
        if ss == 0:
            #to get number of times TTS used in one session to give filename
            #to audio file which will be spoken by this tkiner-app
            tts_count.append(0)

            #generating filename for the audio file
            #(naming format - 'Audio-N', where N is a natural number)
            tts_audio = "Audio-" + str(len(tts_count)) + ".mp3"

            tts.save(tts_audio) #saving the audio
            playsound(tts_audio) #playing the audio
            os.remove(tts_audio) #removing the saved audio file

        #if clicked on 'Save as MP3'
        else:
            #getting the list of name of files in current directry
            #to avoid naming conflicts
            tts_audio_list = os.listdir()

            #variable to give different name to each audio file while saving
            i = 1

            while True:
                #generating filename for the audio file
                #(naming format - 'TTS-N', where N is a natural number)
                tts_audio = "TTS-" + str(i) + ".mp3"

                #if generated filename has no naming conflicts
                #with the files in current directry
                if tts_audio not in tts_audio_list:
                    #then save the audio file with generated name
                    tts.save(tts_audio)

                    #a message-box to display that the file has been saved
                    messagebox.showinfo("File saved", "The file has been saved with name " + tts_audio)

                    break
                else:
                    i += 1
    except:
        messagebox.showinfo("Error!", "Oops! An error occurred.")

#function to speak entered texts or content of chosen text-file
def order_to_speech(event):
    text_displayFileContent = str(entry_inputText.get()) #getting entered texts

    if text_displayFileContent != "": 
        #if text field is filled
        speech_or_save(text_displayFileContent, 0)

    elif len(file_content) > 0:
        #if text field is empty but a text-file has been chosen
        speech_or_save(file_content[0], 0)

    else:
        #if both the fields are empty
        messagebox.showinfo("Incomplete action!", "Please enter a text or choose a text-file.")

#function to save input as an audio file
def save_as_mp3(event):
    text_displayFileContent = str(entry_inputText.get())

    if text_displayFileContent != "":
        speech_or_save(text_displayFileContent, 1)

    elif len(file_content) > 0:
        speech_or_save(file_content[0], 1)
        
    else:
        #if both the fields are empty
        messagebox.showinfo("Incomplete action!", "Please enter a text or choose a text-file.")

#function to reset everything
def reset(event):
    file_content = []
    tts_count = []

    entry_displayFilePath.config(state = "normal")
    entry_displayFilename.config(state = "normal")
    text_displayFileContent.config(state = "normal")

    entry_inputText.delete(0, END)
    entry_displayFilePath.delete(0, END)
    entry_displayFilePath.insert(END, "No file chosen")

    speech_in.set("Default")

    speech_speed_dflt.select()
    speech_speed_slow.deselect()

    entry_displayFilename.delete(0, END)
    text_displayFileContent.delete("1.0", "end")
    entry_displayFilename.insert(END, "No file chosen")
    text_displayFileContent.insert(END, "No file chosen")

    entry_displayFilePath.config(state = "readonly")
    entry_displayFilename.config(state = "readonly")
    text_displayFileContent.config(state = "disabled")

#Heading Section----------------------------------------------------------

heading = Label(w, text = "Text  to  Speech", bg = '#fff', font = ('algerian', 25))
heading.config(pady = 15)
heading.pack()

#Input Section-------------------------------------------------------

label_enterText = Label(w, text = "Enter the text:", bg = '#fff', font = ('segoeui', 14))
label_displayOR = Label(w, text = "OR", bg = '#fff', font = ('segoeui', 14))
button_chooseFile = Button(w, text = "Choose a text file", width = 15, height = 1, bg = '#077bff', fg = '#fff', activebackground = 'blue', activeforeground = '#fff', font = ('segoeui', 14), bd = 0)
label_filename = Label(w, text = "Content of the chosen text file:", bg = '#fff', font = ('segoeui', 14))

entry_inputText = Entry(width = '43', bg = '#f1f1f1', bd = '0', font = ('calibri', 14))
entry_displayFilePath = Entry(width = '37', bg = '#f1f1f1', bd = '0', font = ('calibri', 14))
entry_displayFilename = Entry(width = '29', bg = '#f1f1f1', bd = '0', font = ('calibri', 14))
text_displayFileContent = Text(w, width = '57', height = '12', bg = '#f1f1f1', wrap = WORD, bd = '0', font = ('calibri', 14))

#when tkinter-app starts, below three will display "No file chosen"
entry_displayFilePath.insert(END, "No file chosen")
entry_displayFilename.insert(END, "No file chosen")
text_displayFileContent.insert(END, "No file chosen")

#setting states to Readonly & Disabled to prevent
#manual editing of path, name and content of the chosen text-file
entry_displayFilePath.config(state = "readonly")
entry_displayFilename.config(state = "readonly")
text_displayFileContent.config(state = "disabled")

label_enterText.pack()
label_displayOR.pack()
button_chooseFile.pack()
label_filename.pack()
text_displayFileContent.pack()

button_chooseFile.bind('<Button-1>', choose_file)

label_enterText.place(x = 50, y = 100)
label_displayOR.place(x = 100, y = 140)
button_chooseFile.place(x = 50, y = 180)
label_filename.place(x = 50, y = 255)

entry_inputText.place(x = 190, y = 100)
entry_displayFilePath.place(x = 247, y = 185)
entry_displayFilename.place(x = 330, y = 255)
text_displayFileContent.place(x = 50, y = 295)

#Choose the Language for Output Voice-------------------------------------

label_chooseLang = Label(w, text = "Speech in:", bg = '#fff', font = ('segoeui', 14))
label_chooseLang.pack()
label_chooseLang.place(x = 675, y = 98)

langs = ["Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chichewa", "Chinese (simplified)", "Chinese (traditional)", "Corsican", "Croatian", "Czech", "Danish", "Default", "Dutch", "English", "Esperanto", "Estonian", "Filipino", "Finnish", "French", "Frisian", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian creole", "Hausa", "Hawaiian", "Hebrew", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Kurdish (kurmanji)", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar (burmese)", "Nepali", "Norwegian", "Odia", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scots gaelic", "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"]

speech_in = StringVar()

#language of output voice will be same as language of entered texts
speech_in.set("Default")

lang_list = OptionMenu(w , speech_in, *langs)
lang_list.config(bg = "#f2f2f2", bd = 0, font = ('calibri', 12))
lang_list["menu"].config(bg = '#f5f5f5', bd = 0, font = ('calibri', 12))
lang_list.pack()
lang_list.place(x = 790, y = 98)

#Speed Control Section for Output Voice-----------------------------------

label_chooseRate = Label(w, text = "Speed of speech:", bg = '#fff', font = ('segoeui', 14))
label_chooseRate.pack()
label_chooseRate.place(x = 675, y = 180)

speech_speed = IntVar()

speech_speed_dflt = Radiobutton(w, text = "Default", variable = speech_speed, value = 0, bg = '#fff', font = ('calibri', 14))
speech_speed_slow = Radiobutton(w, text = "Slow", variable = speech_speed, value = 1, bg = '#fff', font = ('calibri', 14))

#by default 'Default' speed (i.e. rate) is selected
speech_speed_dflt.select()
speech_speed_slow.deselect()

speech_speed_dflt.pack()
speech_speed_slow.pack()

speech_speed_dflt.place(x = 675, y = 220)
speech_speed_slow.place(x = 765, y = 220)

#Buttons to Do Tasks------------------------------------------------------

button_OrderToSpeech = Button(w, text = "Order to Speech", width = 15, height = 2, bg = '#077bff', fg = '#fff', activebackground = 'blue', activeforeground = '#fff', font = ('centurygothic', 14), bd = 0)
button_SaveAsMP3 = Button(w, text = "Save as MP3", width = 15, height = 2, bg = '#077bff', fg = '#fff', activebackground = 'blue', activeforeground = '#fff', font = ('centurygothic', 14), bd = 0)
button_Reset = Button(w, text = "Reset", width = 15, height = 2, bg = 'red', fg = '#fff', activebackground = 'darkred', activeforeground = '#fff', font = ('centurygothic', 14), bd = 0)

button_OrderToSpeech.pack()
button_SaveAsMP3.pack()
button_Reset.pack()

button_OrderToSpeech.bind('<Button-1>', order_to_speech)
button_SaveAsMP3.bind('<Button-1>', save_as_mp3)
button_Reset.bind('<Button-1>', reset)

button_OrderToSpeech.place(x = 675, y = 310)
button_SaveAsMP3.place(x = 675, y = 390)
button_Reset.place(x = 675, y = 470)

#Developers---------------------------------------------------------------

label_developer = Label(w, text = emoji.emojize("Created with :red_heart: by Deepanshu"), bg = '#fff', font = ('verdana', 12))
label_developer.pack()
label_developer.place(x = 670, y = 570)

#-------------------------------------------------------------------------

w.mainloop()
