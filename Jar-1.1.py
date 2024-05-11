import pyttsx3
import speech_recognition as sr
import os 
OPENAI_KEY = ""
import openai
openai_key = OPENAI_KEY

def SpeekText (command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
r = sr.Recognizer()
def record_text():
    while(1):
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration = 0.2 )
                audio = r.listen(source)
                MyText = r.recognize_google(audio)
                return MyText
        except sr.RequestError as e :
            print("Could not request result; {0}". format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")   

def send_to_ChatGPT(messages, model="gpt-3.5-turbo"):  
    response = openai.completion.create(model = model,
            messages = messages,
            max_tokens = 100,
            n=1,
            stop = None,
            temperature = 0.5,)
            
                                        
    
    messages = response.choices[0].messages.content
    messages.append(response.chpices[0].messages)
    return messages
messages = [{"role": "user","content": "act like jarvis from ironman"}]
while(1):
    text =record_text()
    messages.append({"role": "user","content": text})
    response = send_to_ChatGPT(messages)
    SpeekText(response)
    print(response)
