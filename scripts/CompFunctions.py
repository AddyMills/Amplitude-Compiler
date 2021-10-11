from collections import namedtuple
from mido import Message, MidiFile, MidiTrack, MetaMessage
import PySimpleGUI as sg
import json
import os
import shutil
import soundfile
import subprocess
import sys

listboxSize = (6, 5)
numBoxSize = (4, 1)
prevBoxSize = (7, 1)
instrumentsList = ['bass', 'drums', 'guitar', 'synth', 'vocals']
defaultList = [None, None, None, None, None, None]
compile_text = "Compile!"
open_text = "Browse"
#inputRightClick = ['&Right', ['Insert 16-bit 44,100 Hz', 'Insert 24-bit 44,100 Hz', 'Insert 16-bit 48,000 Hz', 'Insert 24-bit 48,000 Hz']]


def customDataDecoder(songData):
    return namedtuple('songData', songData.keys())(*songData.values())


def modSongMetaData(songData, values):
    songData.title = values['title']
    songData.title_short = values['title_short']
    songData.artist = values['artist']
    songData.artist_short = values['artist_short']
    songData.desc = values['desc']
    songData.length = values['length']
    songData.countin = values['countin']
    songData.bpm = values['bpm']
    songData.true_values = values['true_values']
    songData.gates = [values['gate1'], values['gate2'], values['gate3']]
    songData.game_speed = values['game_speed']
    songData.preview_start = values['preview_start']
    songData.preview_end = values['preview_end']
    songData.save_path = values['save_path']
    return songData


def modSongGameData(songData, values):
    songData.midi_file = values['midi_file']
    songData.track1 = values['track1']
    songData.track2 = values['track2']
    songData.track3 = values['track3']
    songData.track4 = values['track4']
    songData.track5 = values['track5']
    songData.track6 = values['track6']
    songData.bg_track = values['bg_track']
    songData.flow1 = values['flow1']
    songData.flow2 = values['flow2']
    songData.flow3 = values['flow3']
    songData.track1_att = values['track1_att']
    songData.track2_att = values['track2_att']
    songData.track3_att = values['track3_att']
    songData.track4_att = values['track4_att']
    songData.track5_att = values['track5_att']
    songData.track6_att = values['track6_att']
    songData.bg_track_att = values['bg_track_att']
    songData.flow1_att = values['flow1_att']
    songData.flow2_att = values['flow2_att']
    songData.flow3_att = values['flow3_att']
    songData.save_path = values['save_path']
    return songData


def loadAmpFile(songData, infile):
    songData.title = infile.title
    songData.title_short = infile.title_short
    songData.artist = infile.artist
    songData.artist_short = infile.artist_short
    songData.desc = infile.desc
    songData.bpm = infile.bpm
    songData.preview_start = infile.preview_start
    songData.preview_end = infile.preview_end
    songData.length = infile.length
    songData.countin = infile.countin
    songData.gates = infile.gates
    songData.game_speed = infile.game_speed
    songData.true_values = infile.true_values
    songData.midi_file = infile.midi_file
    songData.track1 = infile.track1
    songData.track2 = infile.track2
    songData.track3 = infile.track3
    songData.track4 = infile.track4
    songData.track5 = infile.track5
    songData.track6 = infile.track6
    songData.bg_track = infile.bg_track
    songData.flow1 = infile.flow1
    songData.flow2 = infile.flow2
    songData.flow3 = infile.flow3
    songData.ps4mode = infile.ps4mode
    songData.track1_att = infile.track1_att
    songData.track2_att = infile.track2_att
    songData.track3_att = infile.track3_att
    songData.track4_att = infile.track4_att
    songData.track5_att = infile.track5_att
    songData.track6_att = infile.track6_att
    songData.bg_track_att = infile.bg_track_att
    songData.flow1_att = infile.flow1_att
    songData.flow2_att = infile.flow2_att
    songData.flow3_att = infile.flow3_att
    songData.save_path = infile.save_path
    songData.save_file = infile.save_file
    return songData


def splashScreenGui():
    layout = [[sg.Menu(menu_definition=[['&File', ['&!Properties', 'E&xit']]])],
              [sg.Text('Please select the program you\'d like to use today:', expand_x=True, justification='center')],
              [sg.Button(button_text="Midi Starter",
                         tooltip="Create a midi customized to your song's instrument layout.", size=(20, 10)),
               sg.Button(button_text="Song Compiler", tooltip="Create a custom song folder by creating game data.",
                         size=(20, 10))]
              ]
    return layout


def midStartGui():
    textSize = (5, 1)
    layout = [[sg.Menu(menu_definition=[['&File', ['&Open', '&Save', '---', '&!Properties', 'E&xit']],
                                        ['&Song Compiler', ['&Metadata', 'Song &Data']]])],
              [sg.Text('Tracks', expand_x=True, justification='center')],
              [sg.Text('1', size=textSize, justification='center'),
               sg.Text('2', size=textSize, justification='center'),
               sg.Text('3', size=textSize, justification='center'),
               sg.Text('4', size=textSize, justification='center'),
               sg.Text('5', size=textSize, justification='center'),
               sg.Text('6', size=textSize, justification='center'),],
              [sg.Listbox(values=instrumentsList, default_values=defaultList[0], key='track1', size=listboxSize,
                          no_scrollbar=True),
               sg.Listbox(values=instrumentsList, default_values=defaultList[1], key='track2', size=listboxSize,
                          no_scrollbar=True),
               sg.Listbox(values=instrumentsList, default_values=defaultList[2], key='track3', size=listboxSize,
                          no_scrollbar=True),
               sg.Listbox(values=instrumentsList, default_values=defaultList[3], key='track4', size=listboxSize,
                          no_scrollbar=True),
               sg.Listbox(values=instrumentsList, default_values=defaultList[4], key='track5', size=listboxSize,
                          no_scrollbar=True),
               sg.Listbox(values=instrumentsList, default_values=defaultList[5], key='track6', size=listboxSize,
                          no_scrollbar=True)],
              [sg.Button(button_text="Generate!", expand_x=True)]]
    return layout


def compMetaDataGUI(songData):
    textSize = (12, 1)
    layout = [[sg.Menu(menu_definition=[['&File', ['&Open', '&Save', "Save &As", '---', '&!Properties', 'E&xit']]])],
              [sg.Button(button_text='Metadata', disabled=True, expand_x=True),
               sg.Button(button_text='Game Data', expand_x=True)],
              [sg.Text('Metadata', expand_x=True, justification='center')],
              [sg.Text('Title', size=textSize, justification='right'),
               sg.Input(default_text=songData.title, expand_x=True, key='title', tooltip="The full name of the song.")],
              [sg.Text('Leaderboard Title', size=textSize, justification='right'),
               sg.Input(default_text=songData.title_short, expand_x=True, key='title_short',
                        tooltip="A modified title. This only shows up above the leaderboards portion during song selection. Leave blank if it would be the same as the \"Title\" field.")],
              [sg.HorizontalSeparator()],
              [sg.Text('Artist', size=textSize, justification='right'),
               sg.Input(default_text=songData.artist, expand_x=True, key='artist',
                        tooltip="The full artist name (include featuring guests here to maintain consistency).")],
              [sg.Text('\"Short\" Artist', size=textSize, justification='right'),
               sg.Input(default_text=songData.artist_short, expand_x=True, key='artist_short',
                        tooltip="This doesn't seem to be used anywhere, but it's present for artists that have a featured guest.\nThis field would contain just the main artist.\nPerhaps a \"Sort by Artist\" algorithm was planned at some point.\nLeave blank if both this and \"Artist\" are the same.")],
              [sg.HorizontalSeparator()],
              [sg.Text('Description', size=textSize, justification='right'),
               sg.Input(default_text=songData.desc, expand_x=True, key='desc',
                        tooltip="A short description of the song or artist. Shows up during song selection.")],
              [sg.HorizontalSeparator()],
              [sg.Text('Length', size=textSize, justification='right'),
               sg.Input(default_text=songData.length, key='length', size=numBoxSize,
                        tooltip="The end of the song. This field should have the measure where you want the song to end. The final gate."),
               sg.Text('Count In', expand_x=True, justification='right'),
               sg.Input(default_text=songData.countin, key='countin', size=numBoxSize,
                        tooltip="How many measures of count in before notes start playing. Default is 4."),
               sg.Text('BPM', expand_x=True, justification='right'),
               sg.Input(default_text=songData.bpm, key='bpm', size=numBoxSize,
                        tooltip="Tempo of the song. This should match your MIDI's tempo exactly."),
               sg.Checkbox(text="Use raw values", key='true_values',
                           tooltip='Use values found in moggsong file instead of in MIDI\n(i.e. End measure value is 4 less than what it is in the midi).')],
              [sg.HorizontalSeparator()],
              [sg.Text('Energy Gates', size=textSize, justification='right')],
              [sg.Text('Gate 1', size=textSize, justification='right'),
               sg.Input(default_text=songData.gates[0], key='gate1', size=numBoxSize,
                        tooltip="Insert the measures where you'd like energy gates to appear."),
               sg.Text('Gate 2', size=textSize, justification='right'),
               sg.Input(default_text=songData.gates[1], key='gate2', size=numBoxSize,
                        tooltip="Insert the measures where you'd like energy gates to appear."),
               sg.Text('Gate 3', size=textSize, justification='right'),
               sg.Input(default_text=songData.gates[2], key='gate3', size=numBoxSize,
                        tooltip="Insert the measures where you'd like energy gates to appear.")],
              [sg.HorizontalSeparator()],
              [sg.Text('Tunnel Scale', size=textSize, justification='right'),
               sg.Input(default_text=songData.game_speed, size=numBoxSize, key='game_speed',
                        tooltip="Speed of the note highway. Lower number is faster. Default is 1."),
               sg.Text('Preview Start', size=textSize, justification='right'),
               sg.Input(default_text=songData.preview_start, size=prevBoxSize, key='preview_start',
                        tooltip="Start of preview in milliseconds."),
               sg.Text('Preview End', size=textSize, justification='right'),
               sg.Input(default_text=songData.preview_end, size=prevBoxSize, key='preview_end',
                        tooltip="End of preview in milliseconds.")],
              [sg.HorizontalSeparator()],
              [sg.Text('Compile Folder', size=textSize, justification='right'),
               sg.Input(default_text=songData.save_path, expand_x=True, key='save_path'),
               sg.FolderBrowse(button_text=open_text)],
              [sg.Button(button_text=compile_text, expand_x=True)]
              ]
    return layout


def compSongDataGUI(songData):
    textSize = (12, 1)
    audio_files = ".flac .ogg .mp3 .wav"
    layout = [[sg.Menu(menu_definition=[['&File', ['&Open', '&Save', "Save &As", '---', '&!Properties', 'E&xit']],
                                        ['&Compiler', ['PS&3 Mode', 'PS&4 Mode']]])],
              [sg.Button(button_text='Metadata', expand_x=True),
               sg.Button(button_text='Game Data', disabled=True, expand_x=True)],
              [sg.Text('MIDI Data', expand_x=True, justification='center')],
              [sg.Text('MIDI file', size=textSize, justification='right'),
               sg.Input(default_text=songData.midi_file, expand_x=True, key='midi_file'),
               sg.FileBrowse(button_text=open_text, file_types=(('Midi Files', '*.mid'),))],
              [sg.HorizontalSeparator()],
              [sg.Text('Audio Data', expand_x=True, justification='center')],
              [sg.Text('Location', expand_x=True, justification='right'),
               sg.Text('Att. ', expand_x=True, justification='right')],
              [sg.Text('Track 1', size=textSize, justification='right'),
               sg.Input(default_text=songData.track1, expand_x=True, key='track1'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.track1_att, size=numBoxSize, key='track1_att')],
              [sg.Text('Track 2', size=textSize, justification='right'),
               sg.Input(default_text=songData.track2, expand_x=True, key='track2'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.track2_att, size=numBoxSize, key='track2_att')],
              [sg.Text('Track 3', size=textSize, justification='right'),
               sg.Input(default_text=songData.track3, expand_x=True, key='track3'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.track3_att, size=numBoxSize, key='track3_att')],
              [sg.Text('Track 4', size=textSize, justification='right'),
               sg.Input(default_text=songData.track4, expand_x=True, key='track4'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.track4_att, size=numBoxSize, key='track4_att')],
              [sg.Text('Track 5', size=textSize, justification='right'),
               sg.Input(default_text=songData.track5, expand_x=True, key='track5'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.track5_att, size=numBoxSize, key='track5_att')],
              [sg.Text('Track 6', size=textSize, justification='right'),
               sg.Input(default_text=songData.track6, expand_x=True, key='track6'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.track6_att, size=numBoxSize, key='track6_att')],
              [sg.Text('BG/Click Track', size=textSize, justification='right'),
               sg.Input(default_text=songData.bg_track, expand_x=True, key='bg_track'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.bg_track_att, size=numBoxSize, key='bg_track_att')],
              [sg.Text("Flow Track 1", size=textSize, justification='right'),
               sg.Input(default_text=songData.flow1, expand_x=True, key='flow1'),
               sg.FileBrowse(button_text=open_text, file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.flow1_att, size=numBoxSize, key='flow1_att')],
              [sg.Text("Flow Track 2", size=textSize, justification='right'),
               sg.Input(default_text=songData.flow2, expand_x=True, disabled=not songData.ps4mode, key='flow2'),
               sg.FileBrowse(button_text=open_text, disabled=not songData.ps4mode,
                             file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.flow2_att, disabled=not songData.ps4mode, size=numBoxSize,
                        key='flow2_att')],
              [sg.Text("Flow Track 3", size=textSize, justification='right'),
               sg.Input(default_text=songData.flow3, expand_x=True, disabled=not songData.ps4mode, key='flow3'),
               sg.FileBrowse(button_text=open_text, disabled=not songData.ps4mode,
                             file_types=(('Audio Files', audio_files),)),
               sg.Input(default_text=songData.flow3_att, disabled=not songData.ps4mode, size=numBoxSize,
                        key='flow3_att')],
              [sg.HorizontalSeparator()],
              [sg.Text('Compile Folder', size=textSize, justification='right'),
               sg.Input(default_text=songData.save_path, expand_x=True, key='save_path'),
               sg.FolderBrowse(button_text=open_text)],
              [sg.Button(button_text=compile_text, expand_x=True)]
              ]
    return layout


def lessCountin(attribute, countin):
    return str(int(attribute) - int(countin))


def saveFile(songData):
    if songData.save_file == "":
        ampproj = sg.popup_get_file("", save_as=True, no_window=True,
                                    file_types=(('Amp Project File', '*.ampproj'),))
        songData.save_file = ampproj
    else:
        ampproj = songData.save_file
    try:
        with open(ampproj, 'w') as outfile:
            json.dump(vars(songData), outfile)
    except:
        print("Save failed! Invalid save location.")
    return


def saveFileAs(songData):
    ampproj = sg.popup_get_file("", save_as=True, no_window=True,
                                file_types=(('Amp Project File', '*.ampproj'),))
    try:
        songData.save_file = ampproj
        with open(ampproj, 'w') as outfile:
            json.dump(vars(songData), outfile)
    except:
        print("Save failed! Invalid save location.")
    return


def loadFile(songData):
    ampproj = sg.popup_get_file("", no_window=True, file_types=(('Amp Project', '*.ampproj'), ('ALL Files', '*.*')))
    try:
        with open(ampproj, 'r') as infile:
            songData_dummy = json.loads(infile.read(), object_hook=customDataDecoder)
            songData = loadAmpFile(songData, songData_dummy)
            songData_dummy = None
        if ampproj != songData.save_file:
            songData.save_file = ampproj
    except:
        print("File not loaded! Could not locate .ampproj file.")
    return songData


def compMidiPart(mid):
    tracknames_dict = {
        "T1": "",
        "T2": "",
        "T3": "",
        "T4": "",
        "T5": "",
        "T6": ""
    }

    tracknames = []

    for x in mid.tracks:
        colons = []
        for y in range(0, len(x.name)):
            if x.name[y] == ":":
                colons.append(y)
        if x.name[0:2] == "T1":
            tracknames_dict["T1"] = (x.name[colons[-1] + 1:])
        elif x.name[0:2] == "T2":
            tracknames_dict["T2"] = (x.name[colons[-1] + 1:])
        elif x.name[0:2] == "T3":
            tracknames_dict["T3"] = (x.name[colons[-1] + 1:])
        elif x.name[0:2] == "T4":
            tracknames_dict["T4"] = (x.name[colons[-1] + 1:])
        elif x.name[0:2] == "T5":
            tracknames_dict["T5"] = (x.name[colons[-1] + 1:])
        elif x.name[0:2] == "T6":
            tracknames_dict["T6"] = (x.name[colons[-1] + 1:])
    for x in tracknames_dict.keys():
        tracknames.append(tracknames_dict[x])
    return tracknames


def getAudioData(songData):
    tracksData = [songData.track1, songData.track2, songData.track3, songData.track4, songData.track5, songData.track6,
                  songData.flow1, songData.flow2, songData.flow3, songData.bg_track]
    attData = [songData.track1_att, songData.track2_att, songData.track3_att, songData.track4_att, songData.track5_att,
               songData.track6_att, songData.flow1_att, songData.flow2_att, songData.flow3_att, songData.bg_track_att]
    tracks = []
    att = []
    channels = 0
    for x in range(0, len(tracksData)):
        try:
            data = soundfile.SoundFile(tracksData[x])
            tracks.append(data)
            att.append(attData[x])
            channels += data.channels
        except:
            pass
            #print("Track not found... Continuing")
    return tracks, att, channels


def channelCount(x, tData):
    y = str(x)
    if tData.channels == 1:
        return y
    elif tData.channels == 2:
        y += " " + str(x + 1)
    return y


def makeMoggSong(songData):
    original_stdout = sys.stdout  # Save a reference to the original standard output
    forward_slash = []

    song_name = getSongName(songData)
    save_file = getSaveFilePath(songData, ".moggsong")
    print("\nSaving .moggsong file to " + save_file)
    with open(save_file, "w") as f:
        sys.stdout = f
        countinraw = songData.countin
        if songData.true_values == True:
            countin = '0'
        else:
            countin = countinraw
        mid = MidiFile(songData.midi_file, clip=True)
        tracknames = compMidiPart(mid)
        trackData, attData, channels = getAudioData(songData)
        print("(mogg_path " + song_name + ".mogg)")
        print("(midi_path " + song_name + ".mid)")
        if songData.true_values == True:
            print("(song_info\n\t(length " + lessCountin(songData.length,
                                                         int(countin)) + ":0:0)\n\t(countin " + countinraw + ")\n)")
        else:
            print("(song_info\n\t(length " + lessCountin(songData.length,
                                                         int(countin) + 1) + ":0:0)\n\t(countin " + countinraw + ")\n)")
        print("")
        print("(tracks\n   (")
        channel_counter = 0
        track_counter = 0
        flow_counter = 0
        pans = ""
        vols = ""
        for x in trackData:
            if track_counter < 6:
                print("      (" + tracknames[track_counter].lower(),
                      "(" + channelCount(channel_counter, x) + ") event:/SONG_BUS)")
            else:
                if songData.ps4mode == True:
                    if flow_counter < 3:
                        print("      (" + "freestyle",
                              "(" + channelCount(channel_counter, x) + ") event:/FREESTYLE_FX_1)")
                        flow_counter += 1
                    else:
                        print("      (" + "bg_click", "(" + channelCount(channel_counter, x) + ") event:/SONG_BUS)")
                else:
                    if flow_counter < 1:
                        print("      (" + "freestyle",
                              "(" + channelCount(channel_counter, x) + ") event:/FREESTYLE_FX_1)")
                        flow_counter += 1
                    else:
                        print("      (" + "bg_click", "(" + channelCount(channel_counter, x) + ") event:/SONG_BUS)")
            if x.channels == 2:
                pans += "-1.0 1.0   "
                vols += ((str(attData[track_counter]) + " ") * 2 + "  ")
            elif x.channels == 1:
                pans += "   0.0   "
                vols += ("  " + str(attData[track_counter]) + "   ")
            track_counter += 1
            channel_counter += x.channels
        print("\t)")
        print(")\n")
        print(";-------------------  MIXER --------------------")
        if songData.ps4mode == True:
            print(
                ";        1TRK1      2TRK2      3TRK3     4TRK4      5TRK5      6TRK6      7FREE1    7FREE2    7FREE3      8BG")
        else:
            print(";        1TRK1      2TRK2      3TRK3     4TRK4      5TRK5      6TRK6      7FREE1      8BG")
        print("(pans (" + pans.strip() + "))")
        print("(vols (" + vols.strip() + "))")
        print("\n;-------------------- ATTENUATION --------------")
        if songData.ps4mode == True:
            print("(active_track_db 0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0)")
        else:
            print("(active_track_db 0.0  0.0  0.0  0.0  0.0  0.0  0.0)")
        print("\n; Amplitude settings\n(arena_path ConstructoP2)")
        # Insert score_goal algorithm here
        print(
            "\n(tunnel_scale 1.0)  ; fudge factor controlling speed of arena travel \n(enable_order (1 2 3 4 5 6)) ; 1-based")
        print("\n; first bar of each section \n(section_start_bars", lessCountin(songData.gates[0], countin),
              lessCountin(songData.gates[1], countin), lessCountin(songData.gates[2], countin) + ")")
        print(";; META DATA")
        print("(title \"{}\")".format(songData.title))
        if songData.title_short != '':
            print("(title_short \"" + songData.title_short + "\")")
        print("(artist \"" + songData.artist + "\")")
        if songData.artist_short == "":
            print("(artist_short \"" + songData.artist + "\")")
        else:
            print("(artist_short \"" + songData.artist_short + "\")")
        print("(desc \"" + songData.desc + "\")")
        print("(unlock_requirement unlock_requirement_playcount)")
        print("(bpm " + songData.bpm + ")\n")

        print("(preview_start_ms " + songData.preview_start + ")")
        print("(preview_length_ms " + lessCountin(songData.preview_end, songData.preview_start) + ")")
    sys.stdout = original_stdout
    print("Save Complete")
    return

def getSongName(songData):
    forward_slash = []
    for x in range(0, len(songData.save_path)):
        if songData.save_path[x] == "/":
            forward_slash.append(x)
    song_name = songData.save_path[forward_slash[-1] + 1:]
    return song_name

def getSaveFilePath(songData, filetype):
    song_name = getSongName(songData)
    if songData.save_path[-1] == "/":
        save_file = songData.save_path + song_name + filetype
    else:
        save_file = songData.save_path + "/" + song_name + filetype
    return save_file

def moveMidi(songData):
    mid = MidiFile(songData.midi_file, clip=True)
    save_file = getSaveFilePath(songData, ".mid")
    print("\nSaving Midi File to " + save_file)
    mid.save(save_file)
    print("Save Complete")
    return

def copyAudioToTemp(tracksData):
    for x in tracksData:
        try:
            shutil.copy(x, "./temp")
        except:
            pass
            
def programProgress(childProg, seconds):
    print(seconds,"seconds elapsed.")
    try:
        childProg.wait(timeout = 5)
    except subprocess.TimeoutExpired:
        seconds += 5
        programProgress(childProg, seconds)
    except:
        print("Failed to make multitrack OGG file.")
    return

def createMoggAudio(songData):
    tracksData = [songData.track1, songData.track2, songData.track3, songData.track4, songData.track5, songData.track6,
                  songData.flow1, songData.flow2, songData.flow3, songData.bg_track]
    print("\nCreating single multitrack ogg file")
    if songData.ps4mode == True:
        makeogg = subprocess.Popen(['./executables/sox-14.4.2/sox.exe','-M',tracksData[0],tracksData[1],tracksData[2],tracksData[3],tracksData[4],tracksData[5],tracksData[6],tracksData[7],tracksData[8],tracksData[9],'-C 5', './temp/temp.ogg'])
    else:
        makeogg = subprocess.Popen(['./executables/sox-14.4.2/sox.exe','-M',tracksData[0],tracksData[1],tracksData[2],tracksData[3],tracksData[4],tracksData[5],tracksData[6],tracksData[9],'-C 5', './temp/temp.ogg'])
    programProgress(makeogg, 0)
    if makeogg.returncode == 0:
        print("Success!")

    print("\nConverting ogg to mogg file")
    makemogg = subprocess.Popen(['./executables/ogg2mogg/ogg2mogg.exe', './temp/temp.ogg', getSaveFilePath(songData, ".mogg")])
    makemogg.wait()
    if makemogg.returncode == 0:
        print("Success!")
        
    print("\nCleaning temporary files.")
    for root, dirs, files in os.walk('./temp'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    return

def compGameData(songData):
    makeMoggSong(songData)
    moveMidi(songData)
    createMoggAudio(songData)
    return
