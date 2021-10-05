# Amplitude Compiler
Compiler for Amplitude 2016. A toolkit to help create fast and efficient new customs for Amplitude 2016. If Amplitude 2003 is figured out in the future, I may incorporate that too!

## Overview
Due to Amplitude requiring quite a bit of work to get customs going, this program handles a lot of the work, including:
* .mogg file creation
* Metadata creation into a .moggsong file
* Compiling all necessary files into a single folder (and renaming all files to be consistent and ready for immediate insertion into the game)

When loading the program you'll be greeted by the main screen:

![image](https://user-images.githubusercontent.com/74471839/136065771-e8e4ad01-0325-477e-bc94-0548dc75ed9e.png)

_MIDI Starter_ opens a GUI version of my previous program [_Amp Starter_](https://github.com/AddyMills/AmpStarter) allowing you to easily create a MIDI file with your instrument specifications:

![image](https://user-images.githubusercontent.com/74471839/136066076-789f4662-2ec2-4c28-bcf6-30fc94d7a666.png)

Clicking **Generate!** will open up a save prompt.

_Song Compiler_ opens up a window similar to Rock Band 3's Magma. This portion of the program consists of two windows.

The first is the **Meta Data** screen allowing you to fill in all the song's meta data:

![image](https://user-images.githubusercontent.com/74471839/136066272-48c362a5-697b-4add-9300-b472c2a2e79b.png)

By default, all values entered will be from the perspective of your MIDI creation program. If you want to the song to end at measure 113, you enter that in the length field. If you would prefer to use the values that are present in the .moggsong file instead, click on "Use Raw Values". This mode will require you to enter the data as the game wants it (i.e. have the end be 5 measures before the actual number). This is for advanced users and most people would use the values as you see in the MIDI file instead.

Clicking **Game Data** at the top will take you to the window allowing you to select your MIDI and Audio files:

![image](https://user-images.githubusercontent.com/74471839/136066494-08b9c0f5-eba9-4577-8188-a5c2f601e419.png)

Here you can search for all your audio files. Please be aware **all** fields must be filled in with something. If you are not using multitracks, you can right click the fields and select a silenced track based on your audio input.

Clicking on *Compiler* at the top and selecting *PS4 Mode* will enable the two disabled flow tracks.

Currently supported audio files are .wav, .mp3, .ogg, and .flac files. Please be aware they must already be in game condition to compile properly (similar to Magma).

All fields have tooltips if you're unsure what the field is for.

When hitting **Compile!**, the program will grab all fields as data and feed them into SoX to make a multitrack .ogg file. This step can take anywhere from 30 - 90 seconds (more or less depending on song length). Please be aware your files will be named after folder it's in. It's assumed that you want to play this right away, so please name the folder after your song (no spaces allowed, and should all be lowercase).

After the multitrack ogg is created, it will get fed into ogg2mogg and then placed into your folder.

Temporary files can take up to 70MB of space (can be larger for long, multitrack songs), but are deleted after every compile.

## Future content

* Allow dragging and dropping of files
* Keep settings similar between uses (i.e. remembering PS4 mode).
* One of my most wanted features to add are quick sanity checks for midi files. They will not be as verbose as the Magma Compiler, but more to check for notes that are too close together (like the "Crystal" double note), or to check for any chords present as Amplitude is single notes only.

## Licensing
Distributed under the GPLv3 license. Please see LICENSE for more information.

## Acknowledgements
Third-party software included in the release of this script are as follows:
### SoX
By the SoX Development Team

SoX source code is distributed under two main licenses. The two
licenses are in the files LICENSE.GPL and LICENSE.LGPL.

sox.c, and thus SoX-the user application, is distributed under the
GPL, while the files that make up libsox are licensed under the less
restrictive LGPL.

Note that some of the external packages that can be linked into libsox
are GPLed and/or may have licensing problems, so they can be disabled
at configure time with the relevant--with-* options. If libsox is built
with such libraries, it must be distributed under the GPL.

Included with SoX are files and/or code from the following group(s):

* FLAC - http://flac.sourceforge.net
* LADSPA - http://www.ladspa.org
* libid3tag - http://www.underbit.com/products/mad
* libltdl - http://www.gnu.org/software/libtool
* libsndfile - http://www.mega-nerd.com/libsndfile
* Ogg Vorbis - http://www.vorbis.com
* PNG - http://www.libpng.org/pub/png
* WavPack - http://www.wavpack.com

SoX source found at - http://sox.sourceforge.net

### ogg2mogg
By Michael Tolly

Included with ogg2mogg are files and/or code from the following group(s):

* Vorbis - Copyright (c) 2002-2020 Xiph.org Foundation
  * https://github.com/xiph/vorbis

ogg2mogg source found at - https://github.com/mtolly/ogg2mogg
