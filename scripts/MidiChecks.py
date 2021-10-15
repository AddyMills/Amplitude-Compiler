from mido import tick2second, MidiFile

expertNotes = {114, 116, 118}
hardNotes = {108, 110, 112}
mediumNotes = {102, 104, 106}
easyNotes = {96, 98, 100}  # Also used for notes found in WORLD track
bg_clickNotes = {28, 29}
worldEvents = {"[blacklit]", "[blackout]", "[default]", "[end]", "[high_01]", "[high_02]", "[low_01]", "[low_02]",
               "[mid_01]", "[mid_02]", "[neutral]", "[pulse]", "[silhouette_01]", "[silhouette_02]", "[strobe]",
               "[transition_1_beat]", "[transition_2_beat]", "[transition_3_beat]", "[transition_4_beat]",
               "[transition_8_beat]", "[whiteout]"}


def diffCheck(time, diff, msg, mid, diffName, tempo, timeSigNum, x):
    issue = ""
    timeSecs, timeMinSec, timeMBT = timeConvert(time, mid.ticks_per_beat, tempo, timeSigNum)
    if time not in diff:
        try:
            if time - diff[-1] < 30:
                issue = "Track {2}: Note {0} at {1} (MBT {3}) is less than 1/64th note from previous note.".format(
                    msg.note, timeMinSec, mid.tracks[x].name, timeMBT)
            diff.append(time)
        except:
            diff.append(time)
    elif time == diff[-1]:
        issue = "Track {2}: More than 1 note found on {0} difficulty at {1} (MBT {3}).".format(diffName, timeMinSec,
                                                                                             mid.tracks[x].name, timeMBT)

    return issue


def timeConvert(time, tpb, tempo, tsNum):
    timeSecs = tick2second(time, tpb, tempo)
    timeMinSec = secs2Mins(timeSecs)
    timeMBT = ticks2MBT(time, tpb, tsNum)
    return timeSecs, timeMinSec, timeMBT


def unsupportedNote(time, msg, mid, song_tempo, timeSigNum, x):
    timeSecs, timeMinSec, timeMBT = timeConvert(time, mid.ticks_per_beat, song_tempo, timeSigNum)
    unString = "Track {2}: Unsupported note {0} found at {1} (MBT {3}).".format(msg.note, timeMinSec,
                                                                                mid.tracks[x].name, timeMBT)
    return unString


def unsupportedEvent(time, msg, mid, song_tempo, timeSigNum, x):
    timeSecs, timeMinSec, timeMBT = timeConvert(time, mid.ticks_per_beat, song_tempo, timeSigNum)
    unString = "Track {2}: Unsupported text event {0} found at {1} (MBT {3}).".format(msg.text, timeMinSec,
                                                                                      mid.tracks[x].name, timeMBT)
    return unString


def secs2Mins(time):
    mins, secs = divmod(time, 60)
    secsTemp = str(secs).split(".")
    mills = "{0:.3f}".format(float(".{0}".format(secsTemp[1]))).lstrip('0')
    secs = int(secsTemp[0])
    timeString = "{0:.0f}:{1:02d}{2}".format(mins, secs, mills)
    return timeString


def ticks2MBT(time, tpb, timeSigNum):
    measure, beat = divmod(time, tpb * timeSigNum)
    measure += 1
    beat, tick = divmod(beat, tpb)
    beat += 1
    mbtString = "{0}.{1}.{2:03d}".format(measure, beat, tick)
    return mbtString


def midiSanityCheck(midPath):
    issues = []
    mid = MidiFile(midPath, clip=True)
    tempos = 0
    ts = 0
    song_tempo = 500000
    timeSigNum = 4
    trackNotes = {
        "T1": [],
        "T2": [],
        "T3": [],
        "T4": [],
        "T5": [],
        "T6": []
    }
    totalNotes = []
    #print(mid.tracks[0].name)
    for x in range(0, len(mid.tracks)):
        totalTime = 0
        diffEasy = []
        diffMedium = []
        diffHard = []
        diffExpert = []
        for msg in mid.tracks[x]:
            totalTime += msg.time
            if x == 0:
                if msg.type == "set_tempo":
                    if tempos == 0:
                        song_tempo = msg.tempo
                    tempos += 1
                    # print(msg)
                if msg.type == "time_signature":
                    ts += 1
                    timeSigNum = msg.numerator
                    # print(timeSigNum)
            elif mid.tracks[x].name.startswith(("T1", "T2", "T3", "T4", "T5", "T6")):
                if msg.type == "note_on":
                    if msg.note in expertNotes:
                        issues.append(diffCheck(totalTime, diffExpert, msg, mid, "Expert", song_tempo, timeSigNum, x))
                    elif msg.note in hardNotes:
                        issues.append(diffCheck(totalTime, diffHard, msg, mid, "Advanced", song_tempo, timeSigNum, x))
                    elif msg.note in mediumNotes:
                        issues.append(diffCheck(totalTime, diffMedium, msg, mid, "Intermediate", song_tempo, timeSigNum, x))
                    elif msg.note in easyNotes:
                        issues.append(diffCheck(totalTime, diffEasy, msg, mid, "Beginner", song_tempo, timeSigNum, x))
                    elif msg.note < 80:
                        pass
                    else:
                        issues.append(unsupportedNote(totalTime, msg, mid, song_tempo,
                                              timeSigNum, x))

            elif mid.tracks[x].name.startswith("T7"):
                pass
            elif mid.tracks[x].name == "BG_CLICK":
                if msg.type == "note_on":
                    if msg.note not in bg_clickNotes:
                        issues.append(unsupportedNote(totalTime, msg, mid, song_tempo,
                                              timeSigNum, x))
            elif mid.tracks[x].name == "WORLD":
                if msg.type == "note_on":
                    if msg.note not in easyNotes:
                        issues.append(unsupportedNote(totalTime, msg, mid, song_tempo,
                                              timeSigNum, x))
                if msg.type == "text":
                    if msg.text not in worldEvents:
                        issues.append(unsupportedEvent(totalTime, msg, mid, song_tempo,
                                               timeSigNum, x))
            try:
                if issues[-1] == "":
                    issues.pop()
            except:
                pass
        if mid.tracks[x].name.startswith(("T1", "T2", "T3", "T4", "T5", "T6")):
            if mid.tracks[x].name.startswith("T1"):
                trackNotes["T1"] = [len(diffExpert), len(diffHard), len(diffMedium), len(diffEasy)]
            elif mid.tracks[x].name.startswith("T2"):
                trackNotes["T2"] = [len(diffExpert), len(diffHard), len(diffMedium), len(diffEasy)]
            elif mid.tracks[x].name.startswith("T3"):
                trackNotes["T3"] = [len(diffExpert), len(diffHard), len(diffMedium), len(diffEasy)]
            elif mid.tracks[x].name.startswith("T4"):
                trackNotes["T4"] = [len(diffExpert), len(diffHard), len(diffMedium), len(diffEasy)]
            elif mid.tracks[x].name.startswith("T5"):
                trackNotes["T5"] = [len(diffExpert), len(diffHard), len(diffMedium), len(diffEasy)]
            else:
                trackNotes["T6"] = [len(diffExpert), len(diffHard), len(diffMedium), len(diffEasy)]

    for key in trackNotes.keys():
        for notes in range(0, len(trackNotes[key])):
            try:
                totalNotes[notes] += trackNotes[key][notes]
            except:
                totalNotes.append(trackNotes[key][notes])

    #print(trackNotes)
    #print(totalNotes)
    #print(len(diffExpert))
    #print(song_tempo)

    if ts > 1:
        issues.append(
            "{0} time signature events found. Please be aware time signature changes are ignored by Amplitude.".format(
                ts))
    elif ts == 0:
        issues.append("No time signature events found. Please double check your MIDI file exported correctly.")
    else:
        pass

    if tempos > 1:
        issues.append("{0} tempo change events found. Please be aware tempo changes are not supported by Amplitude.".format(
            tempos))
    elif tempos == 0:
        issues.append(
            "No tempo change events found. Although tempo is set by the moggsong file, please double check your MIDI file for completeness.")
    else:
        pass
    return totalNotes, issues