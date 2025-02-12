#Import external libraries
import os
import sys

class MIDI_Metadata:
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
    def __init__(self, track_header: bytes, track_header_length: bytes, events: list):
        self.track_header = self.track_header_length = None
        self.events = events
        if len(track_header) == 4:
            self.track_header = track_header
        if len(track_header_length) == 4:
            self.track_header_length = track_header_length
        if not (self.track_header and self.track_header_length):
            raise StructureException("Invaild Input")
    
    def getTrackHeader(self):
        return self.track_header

    def getTrackHeaderLength(self):
        return self.track_header_length

    def getEvents(self):
        return self.events
    
class Event:
    def __init__(self, delta_time: bytes, event: bytes, data: bytes):
        self.delta_time = delta_time
        self.event = event
        self.data = data
    
    def getDeltaTime(self):
        return self.delta_time
    
    def getEvent(self):
        return self.event
    
    def getData(self):
        return self.data

class StructureException(Exception):
    def __init__(self, message):
        super().__init__(message)

#Reads an inputted midi file
def import_MIDI(filename):
    #Input sanitation
    if len(filename) == 0:
        return "Error: No file was entered"
    elif not os.path.exists(os.path.abspath(filename)):
        return "Error: File entered does not exist"
    elif not filename.endswith(".mid"):
        return "Error: File entered is not a midi file"
    #Read inputted midi file
    with open(filename, "rb") as file:
        return file.read()

if __name__ == "__main__":
    #Store inputted midi file
    input_file = input("Enter the midi file name: ")
    midifile = import_MIDI(input_file)
    mmetadata = MIDI_Metadata(midifile[0:4], midifile[4:8], midifile[8:10], midifile[10:12], midifile[12:14])
    startpos = 14
    endpos = 15
    tracks = []
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
            # for e in ["1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111", "11111111"]:
            #     if not format(midifile[startpos], "08b").startswith(e):
            #         if e == "11111111":
            #             print(temp_deltatime, midifile[startpos:startpos+8])
            #             print("no")
            if format(midifile[startpos], "08b") == "11111111":
                temp_event = midifile[startpos:startpos+3]
                startpos += 3
                temp_data = midifile[startpos:startpos+midifile[startpos-1]]
                temp_events.append(Event(temp_deltatime, temp_event, temp_data))
                startpos += midifile[startpos-1]
            #If the event starts with byte Cn or Dn then the event will always be 2 bytes long
            elif format(midifile[startpos], "08b").startswith("1100") or format(midifile[startpos], "08b").startswith("1101"):
                temp_events.append(Event(temp_deltatime, midifile[startpos:startpos+2], None))
                startpos += 2
            #Otherwise do the event will always be 3 bytes long
            else:
                temp_events.append(Event(temp_deltatime, midifile[startpos:startpos+3], None))
                startpos += 3
            endpos = startpos + 1

            print(f"{temp_events[-1].getDeltaTime()}\t{temp_events[-1].getEvent()}\t{temp_events[-1].getData()}")

        tracks.append(Track(temp_track_header, temp_track_header_length, temp_events))
    
    print(tracks)
    for element in tracks:
        print(element.getEvents())
    

#TO DO
#Change track metadata to track data and store the events assciated to the tracks in the class
#Allow for multiple tracks