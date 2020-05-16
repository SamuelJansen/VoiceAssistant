import os, sys, re, speech_recognition, time, Levenshtein, pyttsx3

import GitCommitter

class VoiceAssistant:

    NO_CONTENT = '__NO_CONTENT__'
    KEY_LANGUAGE = 'VoiceAssistant.api.language'

    KW_PYTTSX3_VOICE = 'voice'
    KW_PYTTSX3_VOICE_LIST = 'voices'

    EXCEPTION = 'Exception'
    STOP_RUNNING = ['stop','quit','exit','shut up','quiet','sleep','thanks']
    CONFIRM_COMMAND = ['execute']

    def run(self):
        self.awake = True
        gitCommitter = self.gitCommitter
        globals = self.globals
        while self.awake :
            content = self.listen()
            if content not in VoiceAssistant.STOP_RUNNING :
                if self.selectedCommand and content in VoiceAssistant.CONFIRM_COMMAND :
                    self.gitCommitter.handleSystemCommand([globals.GIT_COMMITTER,self.selectedCommand[0][1][0]])
                else :
                    self.selectedCommand = None
                    self.speak(content)
                    gradedCommandSet = {}
                    for command in self.commandSet.keys() :
                        commandScore = Levenshtein.distance(content,globals.SPACE.join(command.split(globals.DASH)))
                        if gradedCommandSet.get(commandScore) :
                            gradedCommandSet[commandScore].append(command)
                        else :
                            gradedCommandSet[commandScore] = [command]
                    self.selectedCommand = sorted(gradedCommandSet.items())
                    globals.debug(f'{globals.GIT_COMMITTER} {self.selectedCommand[0][1][0]}')
            elif content in VoiceAssistant.STOP_RUNNING :
                self.awake = False

    def __init__(self,globals) :
        self.globals = globals
        self.language = self.globals.getSetting(VoiceAssistant.KEY_LANGUAGE)
        self.brain = speech_recognition
        self.ears = self.brain.Microphone
        self.listenner = self.brain.Recognizer()
        self.speaker = pyttsx3.init()
        speakerList = self.speaker.getProperty(VoiceAssistant.KW_PYTTSX3_VOICE_LIST)
        for speaker in speakerList:
            if self.language in speaker.id :
                self.globals.debug(f'speaker = {speaker}')
                self.speaker.setProperty(VoiceAssistant.KW_PYTTSX3_VOICE,speaker.id)
        self.gitCommitter = GitCommitter.GitCommitter(self.globals)
        self.commandSet = self.gitCommitter.commandSet
        self.selectedCommand = None
        self.language
        self.running = False

    def listen(self):
        debug = self.globals.debug
        interpreted = False
        while not interpreted :
            with self.ears() as soundArround :
                debug('Voice assistant ready')
                self.listenner.adjust_for_ambient_noise(soundArround)
                debug('Voice assistant listenning')
                audioContent = self.listenner.listen(soundArround)
                content = VoiceAssistant.NO_CONTENT
                try :
                    debug('Voice assistant interpretting')
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
