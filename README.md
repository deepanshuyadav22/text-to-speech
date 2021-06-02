# Text to Speech

This software is developed mainly using some Python libraries and Tkinter framework. It supports text to speech (TTS) in 107 languages. It can perform TTS from on a letter to on a whole paragraph and it can also perform TTS on a text file.

### Requirements:
1. Python environment
2. Several libraries and modules

### Required libraries and modules:
1. **tkinter:** This library has been used to make GUI.
2. **askopenfilename:** This module has been used to open a dialogue box which contain text files in the opened/current directory, so that user can choose a text file for TTS.
3. **messagebox:** This module has been used to display a message (i.e. alert) box.
4. **detect:** Since this software supports 107 languages; so to detect the language in which user has been given the input and in which language user wants output, this detect module has been used.
5. **gTTS:** This is main module or we can say that this module is the soul of software. This module has been used to convert text to speech.
6. **Translator:** This module has been used to translate the entered text or the content of chosen text file in the language in which user wants output.
7. **playsound:** After converting the text to speech, we will save the speech file as an audio file with extension '.mp3'. Then to play that audio file, we will use this playsound module.
8. **os:** This library will be used to delete audio files which will be generated during TTS.
9. **emoji:** This module has been used to display 'heart' emoji at bottom right corner.

### Commands to install libraries and modules:
1. **langdetect:** pip install langdetect
2. **gtts:** pip install gtts
3. **googletrans:** pip install googletrans==4.0.0-rc1
4. **playsound:** pip install playsound
5. **emoji:** pip install emoji

### Happy Coding :blush:
