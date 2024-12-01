#Import external libraries
import os

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