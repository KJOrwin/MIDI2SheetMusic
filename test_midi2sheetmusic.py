import unittest

class TestImportMIDI(unittest.TestCase):
    def test_midifile1(self):
        midifile1 = "4D 54 68 64 00 00 00 06 00 00 00 01 00 80 4D 54 72 6B 00 00 00 51 00 FF 58 04 04 02 18 08 00 FF 51 03 04 93 E0 00 C0 00 81 48 90 3E 7F 64 80 3E 00 00 90 40 7F 64 80 40 00 00 90 41 7F 64 80 41 00 00 90 43 7F 64 80 43 00 00 90 40 7F 81 48 80 40 00 00 90 3C 7F 64 80 3C 00 00 90 3E 7F 64 80 3E 00 81 48 80 3E 00 00 FF 2F 00".split()
        for i, element in enumerate(midifile1):
            midifile1[i] = int(element, 16)
        midifile1 = bytes(a)
        self.assertEqual(import_MIDI("midi_test1.mid"), midifile1)
    
    def test_midifile2(self):
        midifile2 = "4D 54 68 64 00 00 00 06 00 00 00 01 01 E0 4D 54 72 6B 00 00 00 32 00 FF 58 04 04 02 18 08 00 FF 51 03 08 7A 23 00 C0 4F 81 70 90 51 7F 3A 80 51 00 3A 90 51 7F 81 2E 80 51 00 82 2C 90 51 00 82 2C 80 51 00 00 FF 2F 00".split()
        for i, element in enumerate(midifile1):
            midifile1[i] = int(element, 16)
        midifile1 = bytes(a)
        self.assertEqual(import_MIDI("midi_test2.mid"), midifile2)
    
    def test_no_file(self):
        self.assertEqual(import_MIDI(), "Error: No file was entered")
    
    def test_invalid_file(self):
        self.assertEqual(import_MIDI("txt_test.mid"), "Error: File entered is not a midi file")

if __name__ == "__main__":
    unittest.main()