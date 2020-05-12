import sys

GIT_COMMITTER = 1
if __name__ == '__main__' :
    from domain.control import Globals
    if len(sys.argv) > GIT_COMMITTER and Globals.Globals.GIT_COMMITTER == sys.argv[GIT_COMMITTER] :
        globals = Globals.Globals(debugStatus = False)
        import GitCommitter
        gitCommitter = GitCommitter.GitCommitter(globals)
        gitCommitter.handleSystemCommand()
    else :
        globals = Globals.Globals(debugStatus = True)
        import VoiceAssistant
        voiceAssistant = VoiceAssistant.VoiceAssistant(globals)
        voiceAssistant.run()
