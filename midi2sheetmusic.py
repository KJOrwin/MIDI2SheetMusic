def import_MIDI(filename):
    with open(filename, "rb") as file:
        return file.read()

input_file = input("Enter the midi file name: ")
import_MIDI(input_file)