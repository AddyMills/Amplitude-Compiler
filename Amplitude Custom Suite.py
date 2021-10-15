# GUI Test

import PySimpleGUI as sg
import scripts.AmpInclude as ampInclude
import scripts.CompFunctions as compF
import scripts.CompClasses as compC


songData = compC.defVal()


showWindow = 0
progEnd = 0

while progEnd != -1:  # Keep window open until program is closed
    if progEnd == 0:  # Program selection screen
        layout = compF.splashScreenGui()

        window = sg.Window('Amplitude Custom Song Suite', layout)

        event, values = window.read()

        if event == "Midi Starter":
            progEnd = 1
            window.close()
        elif event == "Song Compiler":
            progEnd = 2
            window.close()
        else:
            progEnd = -1
    elif progEnd == 1:  # Midi Starter Program
        layout = compF.midStartGui()

        window = sg.Window('Amplitude Midi Starter', layout)

        event, values = window.read()

        if event == "Close Program":
            progEnd = -1
        elif event == "Generate!":
            progEnd = -1
            argsMid = []
            for x in range(0, 6):
                curTrack = 'track'+str(x+1)
                argsMid.append(values[curTrack][0])
            ampInclude.createMIDIfile(argsMid, sg.popup_get_file("", save_as=True, no_window=True,
                                    file_types=(('MIDI Files', '*.mid'),)))
        elif event == "Metadata":
            progEnd = 2
            window.close()
        elif event == "Song Data":
            progEnd = 3
            window.close()
        else:
            progEnd = -1
            
    elif progEnd == 2: #Compiler: Metadata Screen
        layout = compF.compMetaDataGUI(songData)

        window = sg.Window('Amplitude 2016 Compiler', layout)

        event, values = window.read()

        songData = compF.modSongMetaData(songData, values)

        #print(event, values)

        #print(songData.preview_start)
        
        if event == "Game Data":
            progEnd = 3
            window.close()
        elif event == "Open":
            songData = compF.loadFile(songData)
            window.close()
        elif event == "Save":
            compF.saveFile(songData)
            window.close()
        elif event == "Save As":
            compF.saveFileAs(songData)
            window.close()
        elif event == "Compile Full Song":
            songData = compF.modSongMetaData(songData, values)
            compF.compGameData(songData)
            window.close()
            progEnd = -1
        elif event == "Export Moggsong":
            compF.exportMoggSong(songData)
            window.close()
        else:
            progEnd = -1
        
    elif progEnd == 3: #Compiler: Game Data Screen
        layout = compF.compSongDataGUI(songData)

        window = sg.Window('Amplitude 2016 Compiler', layout)

        event, values = window.read()

        songData = compF.modSongGameData(songData, values)

        print(event, values)

        #print(songData.preview_start)
        
        if event == "Metadata":
            progEnd = 2
            window.close()
        elif event == "PS4 Mode":
            songData.ps4mode = True
            songData.flow2_att = 0.0
            songData.flow3_att = 0.0
            window.close()
        elif event == "PS3 Mode":
            songData.ps4mode = False
            songData.flow2 = ""
            songData.flow2_att = ""
            songData.flow3 = ""
            songData.flow3_att = ""
            window.close()
        elif event == "Open":
            songData = compF.loadFile(songData)
            window.close()
        elif event == "Save":
            compF.saveFile(songData)
            window.close()
        elif event == "Save As":
            compF.saveFileAs(songData)
            window.close()
        elif event == "Compile Full Song":
            songData = compF.modSongGameData(songData, values)
            compF.compGameData(songData)
            window.close()
            progEnd = -1
        elif event == "Export Moggsong":
            compF.exportMoggSong(songData)
            window.close()
        else:
            progEnd = -1

        window.close()


window.close()
