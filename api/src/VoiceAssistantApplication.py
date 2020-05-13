import sys

if __name__ == '__main__' :

    from domain.control import Globals

    if len(sys.argv) > Globals.Globals.GIT_COMMITTER_INDEX and Globals.Globals.GIT_COMMITTER == sys.argv[Globals.Globals.GIT_COMMITTER_INDEX] :
        globals = Globals.Globals(debugStatus = True)
        import GitCommitter
        gitCommitter = GitCommitter.GitCommitter(globals)
        gitCommitter.handleSystemCommand(sys.argv[1:])

    else :
        globals = Globals.Globals(debugStatus = True)
        import VoiceAssistant
        voiceAssistant = VoiceAssistant.VoiceAssistant(globals)
        voiceAssistant.run()
