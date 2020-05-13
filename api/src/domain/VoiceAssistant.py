import os, sys, re, speech_recognition, time, Levenshtein
import win32com.client as wincl

import GitCommitter

class VoiceAssistant:

    NO_CONTENT = '__NO_CONTENT__'

    DISPATCH_ARGUMENT = "SAPI.SpVoice"

    EXCEPTION = 'Exception'
    STOP_RUNNING = ['stop','quit','exit','shut up','quiet','sleep','thanks']

    def run(self):
        self.awake = True
        gitCommitter = self.gitCommitter
        globals = self.globals

        skip = False
        choosenCommandSoFar = None
        while self.awake :
            content = self.listen()
            if content == VoiceAssistant.NO_CONTENT :
                skip = True
            if choosenCommandSoFar :
                print('in execute rotine')
                skip = True
                if 'execute' == content :
                    print(f'choosenCommandSoFar = {choosenCommandSoFar}')
                    if choosenCommandSoFar == GitCommitter.COMMAND_ADD_COMMIT_PUSH_ALL :
                        branchName = input('type the branch name: ')
                        gitCommitter.handleSystemCommand([gitCommitter.GIT_COMMITTER,GitCommitter.COMMAND_ADD_COMMIT_PUSH_ALL,branchName])
            choosenCommandSoFar = None
            shortestDistanceSoFar = 1000000
            if content not in VoiceAssistant.STOP_RUNNING and not skip :
                self.speak(content)
                gitCommand = ''
                splittedContent = content.split()
                for command in self.commandList :
                    distance = Levenshtein.distance(content,globals.SPACE.join(command.split(globals.DASH)))
                    print(f'content = {content}, command = {command}, distance = {distance}')
                    if choosenCommandSoFar :
                        if distance < shortestDistanceSoFar :
                            choosenCommandSoFar = str(command)
                            shortestDistanceSoFar = distance * 1
                    else :
                        choosenCommandSoFar = str(command)
                        shortestDistanceSoFar = distance * 1
                choosenCommand = choosenCommandSoFar
                print(f'choosenCommand = {choosenCommand}')
            elif content in VoiceAssistant.STOP_RUNNING :
                self.awake = False
            else :
                skip = False

    def __init__(self,globals) :

        self.globals = globals
        self.brain = speech_recognition
        self.ears = self.brain.Microphone
        self.listenner = self.brain.Recognizer()
        self.speaker = wincl.Dispatch(VoiceAssistant.DISPATCH_ARGUMENT)

        self.gitCommitter = GitCommitter.GitCommitter(self.globals)
        self.commandList = self.gitCommitter.commandSet.keys()

        self.running = False

    def listen(self):
        debug = self.globals.debug
        with self.ears() as listenning :
            debug('Voice assistant ready')
            audioContent = self.listenner.listen(listenning)
            content = VoiceAssistant.NO_CONTENT
            try :
                debug('Voice assistant listenning')
                content = self.listenner.recognize_google(audioContent)
            except Exception as exception :
                debug(f'{VoiceAssistant.EXCEPTION} {str(exception)}')
        debug(f'content = {content}')
        return content

    def speak(self,content) :
        self.speaker.Speak(content)
