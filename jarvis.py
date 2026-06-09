import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import subprocess
import time
import pygetwindow

# testing
a = 1

vscode = "C:\\Users\\Hp\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
capcut = "C:\\Users\\Hp\\AppData\\Local\\CapCut\\Apps\\CapCut.exe"
photoshop = "C:\\Program Files (x86)\\Adobe\\Photoshop 7.0\\Photoshop.exe"
simulide = "C:\\Users\\Hp\\Downloads\\SimulIDE_1.1.0-SR0_Win64\\SimulIDE_1.1.0-SR0_Win64\\simulide.exe"
arduinoide = "C:\\Users\\Hp\\AppData\\Local\\Programs\\Arduino IDE\\Arduino IDE.exe"
fileexplorer = "E:\\"
word = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Word 2007"
excel = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office Excel 2007"
powerpoint = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Microsoft Office PowerPoint 2007"
gmail = "https://mail.google.com/mail/u/0/#inbox"
chatgpt = "https://chatgpt.com/"
youtube = "https://www.youtube.com/results?search_query=sigma+web+development"


goodfeedback = ["thanks", "thankyou", "done", "resolving done","thank"]
graphicdesign = ["making thumbnail", "making banner", "making visiting card", "open photoshop", "making graphic design","graphic design"]
videoediting = ["edit video", "open capcut","edit a video", "video edit"]
websitemaking = ["making website", "design website", "making frontend", "making backend","folder my website"]
circuitprogramming = ["designing circuit", "making circuit", "circuit programming","circuit simulator", "circuit design"]
programming = ["write program", "open vs code", " write automation program"]
promode = ["pro mode", "pro mod"]

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('rate', 150)
engine.setProperty('voice',voices[0].id)
# print(voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("good morning zaid sir")
    elif hour >= 12 and hour < 18:
        speak("good after noon zaid sir")
    elif hour >= 18 and hour <= 24:
        speak("good evening zaid sir")
    speak("i am your virtual assistant")
    speak("how can i help you today")

def takecommand():
    # it takes input from microphine and output as string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("LISTENING....")
        r.pause_threshold = 2
        audio = r.listen(source)

    try:
        print("Recognising...")
        quiry = r.recognize_google(audio,language="en-in")
        print(f"user said {quiry} \n")
    except Exception as e:
        # print(e)
        print("Say that agin please")
        return "none"
    return quiry

def opener(key,condition):
    try:
        if condition == 0:
            os.startfile(key)
        elif condition == 1:
            webbrowser.open(key)
        elif condition == 2:
            subprocess.Popen(key)
        else:
            speak(".....oh no error detected condition is not found")
            speak("please zaid sir , resolve this problem")
    except Exception as e:
        speak("....oh no fetal error, wrong key detected")
        speak("please zaid sir , resolve this problem")


if __name__ == "__main__":
    wishme()
    while True:
        quiry = takecommand().lower()

        # logic for executing tasks based on quiry
        if "wikipedia" in quiry:
            try:

                speak("searching wikipedia...")
                quiry = quiry.replace("wikipedia" ,"")
                results = wikipedia.summary(quiry, sentences=2)
                speak("according to wikipedia")
                speak(results)
                print(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("The topic is too broad. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find anything on Wikipedia for that.")

        elif 'the time' in quiry:
            starttime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {starttime}")

        elif 'open youtube' in quiry :
            speak("opening youtube")
            opener(youtube,1)

        elif 'open google' in quiry :
            speak("opening google")
            opener("google.com",1)

        elif 'open file explorer' in quiry:
            speak("opening file explorer")
            opener(fileexplorer,0)

        elif 'open gmail' in quiry:
            speak("opening gmail")
            opener(gmail,1)

        elif 'open office' in quiry:
            speak("opening all office softwares")
            opener(word,0)
            opener(excel,0)
            opener(powerpoint,0)

        elif 'find youtube' in quiry:
            find = quiry.replace("find youtube", "")
            space = find.replace(" ","+")
            speak("running quiry on youtube")
            opener(f"https://www.youtube.com/results?search_query={space}",1)

        elif 'find google' in quiry:
            find = quiry.replace("find google", "")
            space = find.replace(" ","+")
            speak("running quiry on google")
            opener(f"https://www.google.com/search?q={space}",1)


        for item in videoediting:
            if item in quiry:
                speak("opening capcut for video editing because GPU is not found for premier pro")
                opener(capcut,0)

        for item in graphicdesign:
            if item in quiry:
                speak("opening adobe photoshop for graphic design")
                opener(photoshop,0)

        for item in websitemaking:
            if item in quiry:
                speak("opening my website folder in visual studio code ")
                opener([vscode, "E:\\WEB_DEVELOPMENT"],2)

        for item in circuitprogramming:
            if item in quiry:
                speak("opening simul IDE and arduino IDE for circuit design and compiling sketch binary")
                speak("And opening circuit programming folder in vs code for writting program")
                opener(simulide,0)
                opener(arduinoide,0)
                opener([vscode, "E:\\ELECTRICS\\PROGRAMS\\Arduino_UNO"],2)

        for item in programming:
            if item in quiry:
                opener([vscode, "E:\\MY_PROGRAMS"],2)

        for item in promode:
            if item in quiry:
                speak("     welcome back ! zaid sir! activating pro mode")
                opener(gmail,1)
                opener(youtube,1)
                opener(chatgpt,1)
                opener("https://github.com/CodeWithHarry/Sigma-Web-Dev-Course",1)
                opener([vscode, "E:\\WEB_DEVELOPMENT"],2)
                opener("E:\\OFFICE\\WORD\\WEBSITE_BACKEND_FROM_JAVASCRIPT.docx",0)
                 

        
        for good in goodfeedback:
            if good in quiry:
                speak(" thanks zaid sir i am happy")
                speak("and ask for more help")
                
        
        # elif 'play music' in quiry:
        #     music_dir = "E:\\Music\\☆}☆}"
        #     music = os.listdir(music_dir)
        #     print(music)
        #     os.startfile(os.path.join(music_dir, music[0]))

        # elif 'code' in quiry:
        #     code_path = "C:\\Users\\Hp\\Downloads\\SimulIDE_1.1.0-SR0_Win64\\SimulIDE_1.1.0-SR0_Win64\\simulide.exe"
        #     os.startfile(code_path)
