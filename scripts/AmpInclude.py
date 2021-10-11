from mido import Message, MidiFile, MidiTrack, MetaMessage
import sys

#Initial release

class instCount:
  drums = 0
  bass = 0
  guitar = 0
  synth = 0
  vox = 0
  fx = 0
    

numInst = instCount() #Keep track of instruments. Drums, Bass, Guitar, Synth, Vocals

def countInst(inst):
    if inst.lower() == 'drums':
        numInst.drums += 1
        return numInst.drums
    elif inst.lower() == 'bass':
        numInst.bass += 1
        return numInst.bass
    elif inst.lower() == 'guitar':
        numInst.guitar += 1
        return numInst.guitar
    elif inst.lower() == 'synth':
        numInst.synth += 1
        return numInst.synth
    elif inst.lower() == 'vox':
        numInst.vox += 1
        return numInst.vox
    elif inst.lower() == 'fx':
        numInst.fx += 1
        return numInst.fx
    return -1

def createTrack(num, inst):
    if inst == "vocals":
        inst = 'vox'
    if inst == 'gtr':
        inst = 'guitar'
    x = countInst(inst) #Grab number of instruments present
    trackname = "T"+str(num)+" CATCH:"+inst[0].upper()+":"+inst[0].upper()+inst[1:].lower()
    if x > 1:
        trackname = trackname+str(x)
    return trackname

tracknum = 6

def createMIDIfile(playable, midiName):
    mid = MidiFile(type=1)
    mid.add_track()
    for y in range(0,tracknum):
        mid.add_track(name = createTrack(y+1,playable[y]))
    mid.add_track(name = "T7 FREESTYLE")
    mid.add_track(name = "BG_CLICK")
    mid.add_track(name = "WORLD")

    mid.tracks[7].append(Message('control_change', control = 0, value = 15))
    mid.tracks[7].append(Message('control_change', control = 7, value = 127))

    mid.save(midiName)

