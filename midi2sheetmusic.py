#Import external libraries
import os

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

class Track_Metadata:
    def __init__(self, track_header: bytes, track_header_length: bytes):
        self.track_header = self.track_header_length = None
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
    
class Events:
    def __init__(self, delta_time: bytes, event: bytes):
        self.delta_time = delta_time
        self.event = event
    
    def getDeltaTime(self):
        return self.delta_time
    
    def getEvent(self):
        return self.event

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
