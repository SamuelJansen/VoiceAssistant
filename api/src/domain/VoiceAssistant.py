import os, sys, re, speech_recognition, time
import win32com.client as wincl

import GitCommitter

class VoiceAssistant:

    EXCEPTION = 'Exception'
    STOP_RUNNING = ['stop','quit','exit','shut up','quiet','sleep','thanks']

    def run(self):
        self.speaking = True
        while self.speaking :
            content = self.listen()
            if content not in VoiceAssistant.STOP_RUNNING :
                self.speak(content)
                gitCommand = ''
                splittedContent = content.split()
                if 'git committer' in splittedContent :
                    gitCommand += 'git-committer '
                    splittedContent.remove('git committer')
                if 'git add all' in splittedContent :
                    gitCommand += 'add-all '
                    splittedContent.remove('add all')
            else :
                # sys.argv = 'git-committer git-add-commit-push-all "feat(git-clone-all-command-run)"'.split()
                # self.gitCommitter.handleSystemCommand()
                self.speaking = False

    def __init__(self,globals) :

        self.globals = globals
        self.brain = speech_recognition
        self.ears = self.brain.Microphone
        self.listenner = self.brain.Recognizer()
        self.speaker = wincl.Dispatch("SAPI.SpVoice")

        self.gitCommitter = GitCommitter.GitCommitter(self.globals)

        self.running = False

    def listen(self):
        debug = self.globals.debug
        with self.ears() as listenning :
            debug('ready')
            audioContent = self.listenner.listen(listenning)
            content = ''
            try :
                debug('listenning')
                content = self.listenner.recognize_google(audioContent)
            except Exception as exception :
                debug(f'{VoiceAssistant.EXCEPTION} {str(exception)}')
        debug(f'content = {content}')
        return content

    def speak(self,content) :
        self.speaker.Speak(content)
