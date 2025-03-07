import os

def export_MIDI(file):
    file_format = input("Would you like to export as a pdf or png? ")
    if file_format == "pdf":
        file_format = "--pdf"
        print(file_format)
    elif file_format == "png":
        file_format = "--png"
    else:
        print("That is not a vaild file format!")
    os.system(f'"{os.path.dirname(__file__)}\\libs\\lilypond-binaries\\bin\\lilypond" {file_format} {file}')

export_MIDI("APBirdland.ly")