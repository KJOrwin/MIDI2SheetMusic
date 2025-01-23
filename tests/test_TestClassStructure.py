import unittest

import os.path
parent_path = os.path.dirname(__name__)
import sys
sys.path.append(parent_path)

from midi2sheetmusic import *
from testmanager import *

class TestClassStructure(unittest.TestCase):
    def test_MIDI_Metadata(self):
        #Bytes from midi_test1.mid are used here
        midifile = "4D 54 68 64 00 00 00 06 00 00 00 01 00 80".split()
        for i, element in enumerate(midifile):
            midifile[i] = int(element, 16)
        midifile = bytes(midifile)
        testing_class = MIDI_Metadata(midifile[0:4], midifile[4:8], midifile[8:10], midifile[10:12], midifile[12:14])
        self.assertEqual(testing_class.getMIDIHeader(), midifile[0:4])
        self.assertEqual(testing_class.getMIDIHeaderLength(), midifile[4:8])
        self.assertEqual(testing_class.getMIDIFormat(), midifile[8:10])
        self.assertEqual(testing_class.getNumTracks(), midifile[10:12])
        self.assertEqual(testing_class.getTimeDivision(), midifile[12:14])

    def test_MIDI_Metadata_Exception(self):
        """Test if the MIDI_Metadata class returns the correct exception if the incorrect length for each variable is inputted"""
        #Empty bytes objects are used as an example
        with self.assertRaises(StructureException):
            MIDI_Metadata(bytes(), bytes(), bytes(), bytes(), bytes())

    def test_Track_Metadata(self):
        #Bytes from midi_test1.mid are used here
        midifile = "4D 54 72 6B 00 00 00 51".split()
        for i, element in enumerate(midifile):
            midifile[i] = int(element, 16)
        midifile = bytes(midifile)
        testing_class = Track_Metadata(midifile[0:4], midifile[4:8])
        self.assertEqual(testing_class.getTrackHeader(), midifile[0:4])
        self.assertEqual(testing_class.getTrackHeaderLength(), midifile[4:8])

    def test_Track_Metadata_Exception(self):
        """Test if the Track_Metadata class returns the correct exception if the incorrect length for each variable is inputted"""
        #Empty bytes objects are used as an example
        with self.assertRaises(StructureException):
            Track_Metadata(bytes(), bytes())

    def test_Events(self):
        pass

if __name__ == "__main":
    manager()