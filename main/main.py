# Import threading
import threading
import time
import sys
import ForceDetectorManual
# import ESPReader
import PosDetectorManual



# FOR FORCE DETECTOR USE 1 
# FOR POS DETECTOR USE 2
VERSION = 1



# # Run vis main in a thread
# vis_thread = threading.Thread(target=Vis.main)
# vis_thread.start()


# Define the function to run the main function
def run_main():
    # Get data from the ESP
    if VERSION == 1:
        force_detector = ForceDetectorManual.ForceDetector()
        # Run the inference 
        force_detector.run_inference()
    elif VERSION == 2:
        pos_detector = PosDetectorManual.PosDetector()
        # Run the inference 
        pos_detector.run_inference()
 

if __name__ == '__main__':
    run_main()