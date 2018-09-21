import sys
import pickle

""" This File contains the classes for the FlightFile object.

    FlightFile:
        Overall flight File attributes
        LogFrame List:
            Attributes are the data from each logFrame during the flight ~20 logFrames per second
        Event List:
            Events during the flight
"""

class FlightFile():
    """ A FlightFile object

        Attributes:
            flightID (int): The flight ID of the file from Pyxida, either 0, 1, 2, or 3
            written (bool): Does the FlightFile contain Data? Should always be True
            length (int): number of logFrames in logFrames list
            time (int): The unix time when the flight data began being recorded
            rollup (int)
            numEvents (int)

            logFrames (LogFrame[]): A list of logFrame objects
            events (Event[]): A list of events stored.
    """

    def __init__(self, flightID, logInfo):
        """ Initiate a flightFile object from its logInfo tuple decoded from c++ struct
        and unpack the logInfo tuple

        Args:
            flightID (int)
            logInfo (tuple): Tuple from the decoding of the c++ logInfo struct
        """
        self.flightID = flightID
        self.written = logInfo[0]
        self.length = logInfo[1]
        self.time = logInfo[2]
        self.rollup = logInfo[3]
        self.numEvents = logInfo[4]

        self.logFrames = []
        self.events = []

    def __str__(self):
        """Returns a string representation of the Flight File attributes, excluding the logFrame and event lists
        """
        return "flightID: " + str(self.flightID) + ", length: " + str(self.length) + ", time: " + str(self.time) + ", rollup: " + str(self.rollup) + ", numEvents: " + str(self.numEvents)

    def calculateStats(self): # Should be called after all data has been loaded
        self.apogee = max([frame.altitude for frame in self.logFrames])
        self.maxVelocity = max([frame.vspeed for frame in self.logFrames])
        self.maxVelocity = max([frame.vaccel for frame in self.logFrames])
        self.startTime = min([frame.time for frame in self.logFrames])
        self.endTime = max([frame.time for frame in self.logFrames])
        self.flightTime = (self.endTime - self.startTime)/1000.0
        self.ascentTime = 0 # calc apogee time, subtract start time
        self.drogueRate = 0 # Average vspeed in droguedesc? (apogee-main)/droguedesc time?
        self.mainRate = 0 # Average vspeed in maindesc? main/maindesc time?

    def transformTime(self, time):
        return (time-self.startTime)/1000.0

    def getList(self, field):
        out = []

        if field == "Time":
            startTime = self.logFrames[0].time

        for frame in self.logFrames:
            if field == "Time":
                out.append((frame.time-startTime)/1000.0)

            elif field == "Altitude":
                out.append(frame.altitude)

            elif field == "Velocity":
                out.append(frame.vspeed)

            elif field == "Acceleration":
                out.append(frame.vaccel)

            elif field == "Temperature":
                out.append(frame.temp)

            elif field == "Pressure":
                out.append(frame.pressure)

            elif field == "Satellites":
                out.append(frame.sats)

            elif field == "Voltage":
                out.append(frame.voltage)

        return out

    def printFile(self):
        """ Prints the flight file, including all logFrames and events to the console
        """
        print("Flight File:")
        print(str(self))
        for frame in self.logFrames:
            print("logFrame:")
            print(frame)
        for event in self.events:
            print("Event:")
            print(event)
        sys.stdout.flush()

    #FIX THIS for new flight save and downlaod
    def save(self, fileSavePath):
        """ Saves the flightFile using pickle

        Args:
            fileSavePath (String): The location of where to save the file
        """
        pickle.dump(self, open(fileSavePath, "w"), 0)

    @classmethod
    def load(cls, fileLoadPath):
        """ Loads a FlightFile object using pickle and returns the object

        Note:
            This is a class method and FlightFile does not need to be instantiated
            to use

        Args:
            fileLoadPath (String): Location of where to load file from

        Returns:
            FlightFile object
        """
        return pickle.load(open(fileLoadPath))


class LogFrame():
    """ The Pyxida records a set of logFrames about 20 times second and stores
    flight data in it. A FlightFile object contains a list of LogFrame objects.

    Attributes:
        time (int): measured from start of the flight
        state (int)
        continuity (int)
        voltage (int)
        error (int)
        altitude (float)
        vspeed (float)
        vaccel (float)
        quatW (float)
        quatX (float)
        quatY (float)
        quatZ (float)
        pressure (float)
        temp (float)
        lat (float)
        lon (float)
        sats (int)
    """
    def __init__(self, logFrame):
        """ Initizes a logFrame from a tuple decoded from a c++ struct on Pyxida

            Args:
                logFrame (tuple)
        """
        self.time       = logFrame[0]
        self.state      = logFrame[1]
        self.continuity = logFrame[2]
        self.voltage    = logFrame[3]
        self.error      = logFrame[4]
        self.altitude   = logFrame[5]
        self.vspeed     = logFrame[6]
        self.vaccel     = logFrame[7]
        self.quatW      = logFrame[8]
        self.quatX      = logFrame[9]
        self.quatY      = logFrame[10]
        self.quatZ      = logFrame[11]
        self.pressure   = logFrame[12]
        self.temp       = logFrame[13]
        self.lat        = logFrame[14]
        self.lon        = logFrame[15]
        self.sats       = logFrame[16]

    def __str__(self):
        """ Creates a human readable string of the logFrame
        """
        return ("time: " + str(self.time) + ", state: " + str(self.state) + ", continuity: " + str(self.continuity) + ", voltage: " + str(self.voltage) + ", error: " + str(self.error)
                + ", altitude: " + str(self.altitude) + ", vspeed: " + str(self.vspeed) + ", vaccel: " + str(self.vaccel) + ", quatW: " + str(self.quatW) + ", quatX: " + str(self.quatX)
                + ", quatY: " + str(self.quatY) + ", quatZ: " + str(self.quatZ) + ", pressure: " + str(self.pressure) + ", temp: " + str(self.temp) + ", lat: " + str(self.lat)
                + ", lon: " + str(self.lon) + ", sats: " + str(self.sats))

class Event():
    """ The Pyxida records a set of logFrames about 20 times second and stores
    flight data in it. A FlightFile object contains a list of LogFrame objects.

    Attributes:
        time (int): Measured from the start of the flight
        id (int)
        details (int)
    """
    def __init__(self, event):
        """ Intitiates Event object and unpacks tuple decoded from a c++ struct

        Args:
            event (tuple)
        """
        self.time       = event[0]
        self.id         = event[1]
        self.details    = event[2]

    def __str__(self):
        """ Creates a human readable string of the logFrame
        """
        return "time: " + str(self.time) + ", id: " + str(self.id) + ", details: " + str(self.details)
