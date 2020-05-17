def voiceAssistant(commandList,globals,**kwargs):
    import VoiceAssistant
    voiceAssistant = VoiceAssistant.VoiceAssistant(globals,**kwargs)
    voiceAssistant.handleCommandList(commandList)

if __name__ == '__main__' :
    from domain.control import Globals
    globals = Globals.Globals(debugStatus = False)
    import SystemHelper
    SystemHelper.run(gitCommitter,globals)
