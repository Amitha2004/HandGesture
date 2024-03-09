##################################################
#### Written By: SATYAKI DE                   ####
#### Written On: 23-May-2022                  ####
#### Modified On 23-May-2022                  ####
####                                          ####
#### Objective: This is the main calling      ####
#### python script that will invoke the       ####
#### clsVideoZoom class to initiate           ####
#### the model to read the real-time          ####
#### hand movements gesture that enables      ####
#### video zoom control.                      ####
##################################################

import time
import clsVideoZoom as vz
from clsConfig import clsConfig as cf
import datetime
import logging

###############################################
###           Global Section                ###
###############################################
# Instantiating the base class

x1 = vz.clsVideoZoom()

###############################################
###    End of Global Section                ###
###############################################

def main():
    try:
        # Other useful variables
        debugInd = 'Y'
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        var1 = datetime.datetime.now()

        print('Start Time: ', str(var))
        # End of useful variables

        # Initiating Log Class
        general_log_path = str(cf.conf['LOG_PATH'])

        # Enabling Logging Info
        # logging.basicConfig(filename=general_log_path + 'visualZoom.log', level=logging.INFO)

        print('Started Visual-Zoom Emotions!')

        r1 = x1.runSensor()

        if (r1 == 0):
            print('Successfully identified visual zoom!')
        else:
            print('Failed to identify the visual zoom!')

        var2 = datetime.datetime.now()

        c = var2 - var1
        minutes = c.total_seconds() / 60
        print('Total difference in minutes: ', str(minutes))

        print('End Time: ', str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)


if __name__ == "__main__":
    main()
