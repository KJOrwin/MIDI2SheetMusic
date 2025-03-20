import os
import unittest
from time import strftime, gmtime

#Import main program
from midi2sheetmusic import *

import sys
sys.path.append("tests")
import tests

def manager():
    #Print output of unittest.main()
    unittest.main(verbosity=2, exit=False)
    while True:
        #Ask user if they would like to save the result of the test
        save = input("Save test (y/n)? ").lower()
        if save == "y" or save == "yes":
            #Creates a logs directory to store the log files if it doesn't exist already
            if not os.path.exists("logs"):
                os.makedirs("logs")
            log_filepath = f"logs/{strftime('%Y.%m.%d %H;%M;%S', gmtime())} log.txt"
            #Write output of unittest.main() to a log file
            with open(log_filepath, "w") as log_file:
                runner = unittest.TextTestRunner(stream=log_file, verbosity=2)
                unittest.main(testRunner=runner, exit=False)
            break
        elif save == "n" or save == "no":
            break
        else:
            print("I didn't understand")
            continue

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)