import os, sys, re, speech_recognition, Levenshtein, pyttsx3

import GitCommitter

class VoiceAssistant:

    NO_CONTENT = '__NO_CONTENT__'
    API_KEY_LANGUAGE = 'api.language'

    KW_PYTTSX3_VOICE = 'voice'
    KW_PYTTSX3_VOICE_LIST = 'voices'

    EXCEPTION = 'Exception'
    SLEEP = ['stop','quit','exit','shut up','quiet','sleep','thanks']

    def handleCommandList(self,commandList):
        return self.run()

    def __init__(self,globals) :
        self.globals = globals
        self.language = self.globals.getApiSetting(VoiceAssistant.API_KEY_LANGUAGE)
        self.brain = speech_recognition
        self.sound = self.brain.Microphone
        self.listenner = self.brain.Recognizer()
        self.speaker = pyttsx3.init()
        speakerList = self.speaker.getProperty(VoiceAssistant.KW_PYTTSX3_VOICE_LIST)
        for speaker in speakerList:
            if self.language in speaker.id :
                self.globals.debug(f'speaker = {speaker}')
                self.speaker.setProperty(VoiceAssistant.KW_PYTTSX3_VOICE,speaker.id)
        self.language
        self.running = False

    def run(self):
        self.awake = True
        globals = self.globals
        while self.awake :
            content = self.listen()
            if content not in VoiceAssistant.SLEEP :
                self.speak(content)
            else :
                self.awake = False

    def listen(self):
        debug = self.globals.debug
        interpreted = False
        while not interpreted :
            with self.sound() as soundArround :
                print('Voice assistant ready')
                self.listenner.adjust_for_ambient_noise(soundArround)
                print('Voice assistant listenning')
                audioContent = self.listenner.listen(soundArround)
                content = VoiceAssistant.NO_CONTENT
                try :
                    print('Voice assistant interpretting')
                    content = self.listenner.recognize_google(audioContent,language=self.language)
                    if not content == VoiceAssistant.NO_CONTENT:
                        interpreted = True
                except Exception as exception :
                    debug(f'{VoiceAssistant.EXCEPTION} {str(exception)}')
        debug(f'content = {content}')
        return content

    def speak(self,content) :
        try :
            self.speaker.say(content)
            self.speaker.runAndWait()
        except Exception as exception :
            self.globals.debug(f'Speaker failed: {str(exception)}')
            import win32com.client as wincl
            speaker = wincl.Dispatch("SAPI.SpVoice")
            speaker = pyttsx3.init()
            speaker.Speak(content)
