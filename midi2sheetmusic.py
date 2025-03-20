#Import external libraries
import os
import sys
import subprocess
import json
import ctypes
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import ttk, filedialog

#If LilyPond doesn't exist locally then try to install it locally
if not os.path.exists(f"libs\\lilypond-binaries\\bin\\lilypond.exe"):
    import_warning = tkmb.askokcancel(title="MIDI2SheetMusic", icon="error", message="Lilypond is required to be locally installed to run this program.\n\nIf you want to continue click 'OK' and lilypond will be installed locally to your computer so that it can be easily removed later if you wish.\n\nClicking 'Cancel' will close the program and not install lilypond.")
    if not import_warning:
        sys.exit()
    subprocess.call("pip install lilypond --target=libs")
    subprocess.call("python midi2sheetmusic.py")
    sys.exit()

class MIDI_Metadata:
    """
    Stores the metadata of the midifile (first 14 bytes) ensuring that each attribute is the correct length of bytes.

    Attributes:
        midi_header (bytes)         Shows that the file is a MIDI file - should always be 4D 54 68 64 (MThd).
        midi_header_length (bytes)  Shows the length of the midi header (referring to the length of midi_format, num_tracks and time_division) - should always be 00 00 00 06 (6).
        midi_format (bytes)         Shows if the MIDI file has one or more tracks if they are simultaneous or sequentially independent.
        num_tracks (bytes)          Shows how many tracks are in the MIDI file - will be 00 01 (1) is the midi_format is 00 00 (0).
        time_division (bytes)       Shows if the MIDI file uses metrical time or time-code-based time to either determine the no. of beats per crotchet or per frame.
    """
    def __init__(self, midi_header: bytes, midi_header_length: bytes, midi_format: bytes, num_tracks: bytes, time_division: bytes):
        self.midi_header = self.midi_header_length = self.midi_format = self.num_tracks = self.time_division = None
        if len(midi_header) == 4:
            self.midi_header = midi_header
        if len(midi_header_length) == 4:
            self.midi_header_length = midi_header_length
        if len(midi_format) == 2:
            self.midi_format = midi_format
        if len(num_tracks) == 2:
            self.num_tracks = num_tracks
        if len(time_division) == 2:
            self.time_division = time_division
        if not (self.midi_header and self.midi_header_length and self.midi_format and self.num_tracks and self.time_division):
            raise StructureException("Invaild Input")

    #MIDI_Metadata get methods
    def getMIDIHeader(self):
        return self.midi_header

    def getMIDIHeaderLength(self):
        return self.midi_header_length
    
    def getMIDIFormat(self):
        return self.midi_format
    
    def getNumTracks(self):
        return self.num_tracks
    
    def getTimeDivision(self):
        return self.time_division

class Track:
    """
    Stores each track of the midifile ensuring that the metadata is the correct length of bytes.

    Attributes:
        track_header (bytes)        Shows the beginning of a new track - should always be 4D 54 72 6B (MTrk).
        track_header_length (bytes) Shows the length of all the events in the track (WILL NOT INCLUDE THE END OF TRACK EVENT FF 2F 00).
        events (list)               Stores a list of all the events in the track as __main__.Event objects.
    """
    def __init__(self, track_header: bytes, track_header_length: bytes, events: list):
        self.track_header = self.track_header_length = None
        self.events = events
        if len(track_header) == 4:
            self.track_header = track_header
        if len(track_header_length) == 4:
            self.track_header_length = track_header_length
        if not (self.track_header and self.track_header_length):
            raise StructureException("Invaild Input")
    
    #Track get methods
    def getTrackHeader(self):
        return self.track_header

    def getTrackHeaderLength(self):
        return self.track_header_length

    def getEvents(self):
        return self.events
    
class Event:
    """
    Stores each event by splitting it into its deltatime, event and data.

    Attributes:
        delta_time (bytes)  Stores the amount of time before the next event 
        event (bytes)       Stores the action to be performed - list of possible events can be found here:
                            https://www.mobilefish.com/tutorials/midi/midi_quickguide_specification.html#:~:text=u3-,Event,-byte%20range%3A%20variable
        data (bytes)        Some events require extra data outside of the initial action which is stored here.
    """
    def __init__(self, delta_time: bytes, event: bytes, data: bytes):
        self.delta_time = delta_time
        self.event = event
        self.data = data
    
    #Event get methods
    def getDeltaTime(self):
        return self.delta_time
    
    def getEvent(self):
        return self.event
    
    def getData(self):
        return self.data

#Custom exception. Only triggered if the class structure fails due to incorrect file input or length of events.
class StructureException(Exception):
    def __init__(self, message):
        super().__init__(message)

#Creates a tkinter window with a title, icon and stops it from being resized by the user.
root = tk.Tk()
root.title("MIDI2SheetMusic")
root.resizable(False, False)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("midi2sheetmusic")
root.iconbitmap("midi2sheetmusic icon.ico")

#Reads an inputted MIDI file
def import_MIDI(filename):
    #Input sanitation
    if len(filename) == 0:
        return "Error: No file was entered"
    elif not os.path.exists(os.path.abspath(filename)):
        return "Error: File entered does not exist"
    elif not filename.endswith((".mid", ".midi")):
        return "Error: File entered is not a midi file"
    #Read inputted MIDI file
    with open(filename, "rb") as file:
        return file.read()

#Takes the inputted midifile and transplants it into the class structure
def instantiate_MIDI(midifile):
    json_list = []
    #Extract the metadata from the MIDI file
    mmetadata = MIDI_Metadata(midifile[0:4], midifile[4:8], midifile[8:10], midifile[10:12], midifile[12:14])
    global tracks
    startpos = 14
    endpos = 15
    #SYSTEM EXCULSIVE EVENTS AND SOME META EVENTS ARE NOT ACCOUNTED FOR
    #Repeat the process for all the tracks in the MIDI file
    for i in range(int.from_bytes(mmetadata.getNumTracks())):
        temp_track_header = midifile[startpos:startpos+4]
        temp_track_header_length = midifile[startpos+4:startpos+8]
        startpos += 8
        endpos += 8
        temp_events = []
        while True:
            #Calulating deltatime
            #If the first bit of the final byte is zero then it is the final byte in deltatime, if not continue
            while True:
                if format(midifile[endpos - 1], "08b").startswith("0"):
                    temp_deltatime = midifile[startpos:endpos]
                    break
                elif format(midifile[endpos - 1], "08b").startswith("1"):
                    endpos += 1
            startpos = endpos
            endpos += 1
            #Check if at the end of file
            if bytes(midifile[startpos:startpos+3]) == b'\xff/\x00':
                temp_events.append(Event(temp_deltatime, b'\xff/\x00', None))
                startpos += 3
                endpos += 3
                break
            #Calculate length of event
            #If the event starts with byte FF then the event will have data
            if format(midifile[startpos], "08b") == "11111111":
                temp_event = midifile[startpos:startpos+3]
                startpos += 3
                temp_data = midifile[startpos:startpos+midifile[startpos-1]]
                temp_events.append(Event(temp_deltatime, temp_event, temp_data))
                startpos += midifile[startpos-1]
            #If the event starts with byte 8n, 9n, An, Bn or En then the event will always be 3 bytes long
            elif format(midifile[startpos], "08b").startswith(("1000", "1001", "1010", "1011", "1110")):
                temp_events.append(Event(temp_deltatime, midifile[startpos:startpos+3], None))
                startpos += 3
            #If the event starts with byte Cn or Dn or anything else then the event will always be 2 bytes long
            else:
                temp_events.append(Event(temp_deltatime, midifile[startpos:startpos+2], None))
                startpos += 2

            endpos = startpos + 1
            
            #Append each event to a list for json exporting
            json_list.append({"delta_time": str(temp_events[-1].getDeltaTime()), "event": str(temp_events[-1].getEvent()), "data": str(temp_events[-1].getData())})
            #print(f"{temp_events[-1].getDeltaTime()}\t{temp_events[-1].getEvent()}\t{temp_events[-1].getData()}")

        #Append the track to a list with all of its events 
        tracks.append(Track(temp_track_header, temp_track_header_length, temp_events))
    
    #Create the json file with all the events
    with open(f"{os.path.splitext(os.path.basename(file_entry_var.get()))[0]}.json", "w", encoding="utf-8") as f:
        json.dump(json_list, f, ensure_ascii=False, indent=4)
    print("Done")

#Takes a LilyPond file as an input and runs it through the LilyPond parser
def export_MIDI(lyfile):
    #Ask the user for what file format the exported file should be
    file_format = input("Would you like to export as a pdf, png or svg? ").lower()
    if file_format == "pdf":
        file_format = "--pdf"
    elif file_format == "png":
        file_format = "--png"
    elif file_format == "svg":
        file_format = "--svg"
    else:
        print("That is not a vaild file format!")
        return
    #Run the LilyPond parser
    subprocess.call(f'"libs\\lilypond-binaries\\bin\\lilypond" {file_format} {lyfile}')

#Used by the tkinter browse button to open a filedialog box (file explorer) and ask the user to find the correct file/directory
def browse_files(file_entry, type, dir_entry=None):
    #Check if the user input should be a file or a directory
    if type == "file":
        path = filedialog.askopenfilename(initialdir=".", title="Select a file", filetypes=(("Midi files", "*.mid *.midi"),))
    elif type == "directory":
        path = filedialog.askdirectory(initialdir=".", title="Select a folder")    
    #Check if something was inputted in the filedialog box
    #Without this, if the user didn't input anything the path would be cleared.
    if path:
        file_entry.set(path)
        if dir_entry and not dir_entry.get():
            dir_entry.set(os.path.dirname(path))

#Main function to export the MIDI file
def export(midifile):
    global tracks
    #Get the bytes from the midifile
    midifile = import_MIDI(midifile)
    tracks = []
    #Insert the bytes into the class structure
    instantiate_MIDI(midifile)
    
    #Output the track objects and event objects
    #print(tracks)
    #for element in tracks:
    #    print(element.getEvents())

#root widgets

title = tk.Label(root, text="MIDI2SheetMusic", font=("TkDefaultFont", 12, "bold"))
title.grid(row=1, column=1, columnspan=3, pady=(10, 5))

file_label = tk.Label(root, text="File:")
file_label.grid(row=2, column=1, padx=(10, 5), pady=(5, 5), sticky="E")
file_entry_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_entry_var, width=50, state="readonly")
file_entry.grid(row=2, column=2, padx=(5, 5), pady=(5, 5))
file_browse = tk.Button(root, text="Browse", command=lambda: browse_files(file_entry_var, "file", destn_entry_var))
file_browse.grid(row=2, column=3, padx=(5, 10), pady=(5, 5))

destn_label = tk.Label(root, text="Destination:")
destn_label.grid(row=3, column=1, padx=(10, 5), pady=(5, 5), sticky="E")
destn_entry_var = tk.StringVar()
destn_entry = tk.Entry(root, textvariable=destn_entry_var, width=50, state="readonly")
destn_entry.grid(row=3, column=2, padx=(5, 5), pady=(5, 5))
destn_browse = tk.Button(root, text="Browse", command=lambda: browse_files(destn_entry_var, "directory"))
destn_browse.grid(row=3, column=3, padx=(5, 10), pady=(5, 5))

format_label = tk.Label(root, text="File Format:")
format_label.grid(row=4, column=1, padx=(10, 5), pady=(5, 5), sticky="E")
format_cb_var = tk.StringVar()
format_cb = ttk.Combobox(root, textvariable=format_cb_var, values=["pdf", "png", "svg"], state="readonly")
format_cb.grid(row=4, column=2, padx=(5, 10), pady=(5, 5), sticky="W")

export_button = tk.Button(root, text="Export", command=lambda: export(file_entry_var.get()))
export_button.grid(row=5, column=1, columnspan=2, padx=(10, 5), pady=(5, 10))
test_ly2sm = tk.Button(root, text="ly2sm", command=lambda: export_MIDI("APBirdland.ly"))
test_ly2sm.grid(row=5, column=3, padx=(5, 10), pady=(5, 10))

#------------

#Tkinter main loop
root.mainloop()