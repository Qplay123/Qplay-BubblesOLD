# coding=utf-8
# !usr/local/bin/python
"""
Bubble Blaster 5 game.
Version = 5.2
"""

import os

from _tkinter import TclError
from math import sqrt
from pickle import *
from random import randint, shuffle
from threading import Thread
from time import sleep, time
# from winsound import *
from threadsafe_tkinter import *
# from PIL import Image
# from PIL import ImageTk

S = 0

time1 = time()


class Logging:
    """
    Logging class for logs
    """

    def __init__(self, save_path="", stdout=True, stderr=False):
        from time import strftime
        import os
        self.os = os
        self.tme = strftime
        self.save_file = save_path + self.tme("/log_%d_%m_%Y_-_%H_%M_%S.log")
        self.pos = 1
        self.log_var = ""
        self.stdout = stdout
        self.stderr = stderr

    def log(self, priority, cmd, msg):
        """
        Logs a message
        :param priority:
        :param cmd:
        :param msg:
        :return:
        """
        priority = str(priority)
        cmd = str(cmd)
        msg = str(msg)
        out = "[" + self.tme("%H:%M:%S") + "] - [" + priority.upper() + "] [" + cmd + "]: " + msg + "\n"
        if self.stdout:
            print(out[0:-1])
        self.log_var += out

    def save(self):
        """
        saves the log
        :return:
        """
        fa = open(self.save_file, "w+")
        fa.write(self.log_var)
        fa.close()


class LogException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


log = Logging("logs", True, True)
log.log("info", "define", "Logging class and log method defined.")


def load_data_int(file_path, if_none=0.0):
    """
    Loading data in int format
    :param file_path:
    :param if_none:
    :return:
    """
    fo = open(file_path, "r+")
    data = fo.read(100)
    fo.close()
    if data == "":
        return if_none
    try:
        data2 = int(data)
    except ValueError:
        try:
            data2 = float(data)
        except ValueError:
            data2 = if_none
    return data2


def load_data_str(file_path):
    """
    Load data in string-format
    :param file_path:
    :return:
    """
    fo = open(file_path, "r+")
    data = fo.read(1024)
    fo.close()
    return data


def load_data_bool(file_path, if_none=False):
    """
    Load data in boolean-format
    :param file_path:
    :param if_none:
    :return:
    """
    try:
        fo = open(file_path, "r+")
        data = fo.read(10)
        fo.close()
        if data == "True":
            data = True
        elif data == "False":
            data = False
        else:
            raise ValueError("Can't convert '" + data + "' to Boolean!")
    except ValueError:
        data = if_none
    return data


def load_data_bytes(file_path):
    """
    Load data in bytes-format
    :param file_path:
    :return:
    """
    fo = open(file_path, "r+")
    data = fo.read(100).encode()
    fo.close()
    return data


log.log("info", "define", "File loaders defined")

# Screen Settings

SaveName = "save"

button = dict()

Res = load_data_str("data/Resolution.cfg")
Res = Res.split(sep="x")
WIDTH = int(Res[0])
HEIGHT = int(Res[1])

MID_X = WIDTH / 2
MID_Y = HEIGHT / 2

# Ship Settings
SHIP_R = load_data_int("data/ShipRadius.cfg", 15)
SHIP_SPD = load_data_int("data/ShipSpeed.cfg", 10)
# Bubble Settings
# BubID = list()

BubID = list()
BubAct = list()
BubRad = list()
BubSpd = list()
BubPos = list()
BubHard = list()

bub = dict()
bub["Normal"] = dict()

ShotID = list()
ShotSpd = list()
ShotPos = list()
ShotDmge = list()

ShotRad = 5
ShotSpeed = 5

MinBubRad = load_data_int("data/BubMinRadius.cfg", 10)
MaxBubRad = load_data_int("data/BubMaxRadius.cfg", 30)
MaxBubSpd = load_data_int("data/BubMaxSpeed.cfg", 4.8)
ScreenGap = load_data_int("data/BubScreenGap.cfg", 100)

# Game Settings
BubChance = load_data_int("data/BubChance.cfg", 10)
TimeLimit = load_data_int("data/GameTimeLimit.cfg", 30)
LevelScore = load_data_int("data/GameLevelScore.cfg", 10000)

# Game setup
Score = load_data_int("data/GameResetScore.cfg", 0)
Level = load_data_int("data/GameResetLevel.cfg", 1)
Lives = load_data_int("data/GameResetLives.cfg", 7)
HiScore = load_data_int("data/GameResetHiScore.cfg", 0)
end = time() + TimeLimit

# Player States
ScoreState = load_data_int("data/StateResetScore.cfg", 1)
ScoreStateTime = load_data_int("data/StateResetScoreTime.cfg", 0)
SecureState = load_data_bool("data/StateResetSecure.cfg", False)
SecureStateTime = load_data_int("data/StateResetSecureTime.cfg", 0)
SlowMoState = load_data_bool("data/StateResetSlowMotion.cfg", False)
SlowMoStateTime = load_data_int("data/StateResetSlowMotionTime.cfg", 0)
ConfusState = load_data_bool("data/StateResetConfusion.cfg", False)
ConfusStateTime = load_data_int("data/StateResetConfusionTime.cfg", 0)
TimeBreak = load_data_bool("data/StateResetTimeBreak.cfg", False)
TimeBreakTime = load_data_int("data/StateResetTimeBreakTime.cfg", 0)
SpdBoost = load_data_bool("data/StateResetSpeedBoost.cfg", False)
SpdBoostTime = load_data_int("data/StateResetSpeedBoostTime.cfg", 0)
Paralized = load_data_bool("data/StateResetParalized.cfg", False)
ParalizedTime = load_data_int("data/StateResetParalizedTime.cfg", 0)
StateTime = load_data_int("data/StateResetTime.cfg", 0)
ShotSpeedTime = load_data_int("data/StateResetShotSpeedTime.cfg", 0)
NoTouchTime = 0.0
NoTouch = False
Action = load_data_str("data/StateResetAction.cfg")

# Game Modes
pause = load_data_bool("data/Pause.cfg", False)
tpmode = False
storemode = False
windowmode = False
presentmode = False
cheatmode = False
KeyActive = False

# Debugging modes
DEBUG = False
DEBUG_KEY = False

# ???
ReturnMain = True

# Money, coins, diamonds etc.
Coins = 0
Diamond = 0

# ???
S = 1

# This is nonsens
wait = True

# Teleport points
TP = 0

log.log("info", "var", "Variables successful defined or readed")


# Error Definitions


class ShipError(Exception):
    """
    Exception
    """

    def __init__(self, text="<Undefined>"):
        Exception.__init__(self, text)


class CmdNotCompatible(Exception):
    """
    A CmdNotCompatible Excpeption
    """

    def __init__(self, text=""):
        Exception.__init__(self, "The command '" + text + "' isn't compatible with Ubuntu")


# Extras


class Extra:
    """
    Extras for the game.
    """

    @staticmethod
    def bool_convert(boolean):
        """
        Boolean convertion tp ON/OFF string.
        :param boolean:
        :return:
        """
        if type(boolean) != bool:
            return "ERROR"
        if boolean:
            return "ON"
        elif not boolean:
            return "OFF"
        else:
            return "ERROR"

    @staticmethod
    def wave_sound(file):
        """
        Plays a .wav sound.
        :param file:
        :return:
        """
        Thread(None, lambda: PlaySound(file, 0))


log.log("debug", "test", "Extra.BoolConvert(True) returns:" + Extra.bool_convert(True))
log.log("debug", "test", "Extra.BoolConvert(False) returns:" + Extra.bool_convert(False))
log.log("debug", "test", "Extra.BoolConvert(\"Error\") returns:" + Extra.bool_convert("Error"))

Extra.wave_sound("data/Sounds/GameOver.wav")


def play(event):
    """
    Unexpected function:
    Does nothing.
    """
    global wait
    if event.keysym == "Return":
        wait = True


# Game Definitions


def replace_list(list_name=list, index=int, item=None):
    """
    Replacelist function
    :param list_name:
    :param index:
    :param item:
    """
    if type(list_name) == tuple:
        list_name = list(list_name)
    list_name.pop(index)
    list_name.insert(index, item)


list1 = ["Windows", "Ubuntu", "Mac OS X"]
log.log("debug", "replacelist", "list is now:" + str(list1))
replace_list(list_name=list1, index=1, item="Linux")
log.log("debug", "replacelist", "list after replace index 1 to Linux:" + str(list1))
if list1[1] == "Linux":
    log.log("info", "replacelist", "Method working well")
else:
    log.log("fatal", "replacelist", "Method have an important issue")
    log.save()
    sys.exit(1)


def move_ship(event):
    """
    Ship-motion event
    :param event:
    """
    global Paralized
    global pause
    global S
    global StateTime
    global TP
    global tpmode
    global storemode
    global store
    global windowmode
    global ScoreStateS
    global ScoreStateTime
    global SecureStateS
    global SecureStateTime
    global TimeBreakS
    global TimeBreakTime
    global ConfusStateS
    global ConfusStateTime
    global SlowMoStateS
    global SlowMoStateTime
    global ParalizedS
    global ParalizedTime
    global ShotSpeedS
    global ShotSpeedTime
    global KeyActive
    global NoTouchS
    global NoTouchTime
    global presentmode
    global cheatmode
    global Cheater
    # print("Event")
    if (not tpmode) and (not storemode) and (not windowmode):
        # print("No Modes")
        if not pause:
            # print("No Pause")
            if not Paralized:
                # print("Not Paralized")
                x, y = get_coords(ship_id2)
                if event.keysym == 'Up':
                    if y > 72 + SHIP_R:
                        c.move(ship_id, 0, -SHIP_SPD)
                        c.move(ship_id2, 0, -SHIP_SPD)
                        Root.update()
                elif event.keysym == 'Down':
                    if y < HEIGHT - 105 - SHIP_R:
                        c.move(ship_id, 0, SHIP_SPD)
                        c.move(ship_id2, 0, SHIP_SPD)
                        Root.update()
                elif event.keysym == 'Left':
                    if x > 0 + SHIP_R:
                        c.move(ship_id, -SHIP_SPD, 0)
                        c.move(ship_id2, -SHIP_SPD, 0)
                        Root.update()
                elif event.keysym == 'Right':
                    if x < WIDTH - SHIP_R:
                        c.move(ship_id, SHIP_SPD, 0)
                        c.move(ship_id2, SHIP_SPD, 0)
                        Root.update()
                if event.keysym == "space":
                    create_shot()
                c.update()
                c.update_idletasks()
                Root.update()
                Root.update_idletasks()
    if storemode:
        if event.keysym == "Up":
            store.set_selected(-1)
        if event.keysym == "Down":
            store.set_selected(1)
        if event.keysym == "space":
            store.buy_selected()
        if event.keysym == "BackSpace":
            store.exit()
            del store
        if event.keysym == "Escape":
            store.exit()
            del store
    if presentmode:
        if event.keysym == "space":
            P.exit()
            pause = False
            presentmode = False
            ScoreStateTime = ScoreStateS + time()
            SecureStateTime = SecureStateS + time()
            TimeBreakTime = TimeBreakS + time()
            ConfusStateTime = ConfusStateS + time()
            SlowMoStateTime = SlowMoStateS + time()
            ParalizedTime = ParalizedS + time()
            ShotSpeedTime = ShotSpeedS + time()
            NoTouchTime = NoTouchS + time()
    if tpmode:
        x, y = get_coords(TP_id1)
        if event.keysym == 'Up':
            if y > 72 + 5:
                c.move(TP_id1, 0, -5)
                c.move(TP_id2, 0, -5)
                c.move(TP_id3, 0, -5)
                c.move(TP_id4, 0, -5)
        if event.keysym == "Down":
            if y < HEIGHT - 105 - 5:
                c.move(TP_id1, 0, 5)
                c.move(TP_id2, 0, 5)
                c.move(TP_id3, 0, 5)
                c.move(TP_id4, 0, 5)
        if event.keysym == "Left":
            if x > 0 + 5:
                c.move(TP_id1, -5, 0)
                c.move(TP_id2, -5, 0)
                c.move(TP_id3, -5, 0)
                c.move(TP_id4, -5, 0)
        if event.keysym == "Right":
            if x < WIDTH - 5:
                c.move(TP_id1, 5, 0)
                c.move(TP_id2, 5, 0)
                c.move(TP_id3, 5, 0)
                c.move(TP_id4, 5, 0)
        if event.keysym == "BackSpace":
            pause = False
            ScoreStateTime = ScoreStateS + time()
            SecureStateTime = SecureStateS + time()
            TimeBreakTime = TimeBreakS + time()
            ConfusStateTime = ConfusStateS + time()
            SlowMoStateTime = SlowMoStateS + time()
            ParalizedTime = ParalizedS + time()
            ShotSpeedTime = ShotSpeedS + time()
            NoTouchTime = NoTouchS + time()
            teleport(ship_id, ship_id)
        if event.keysym == "Escape":
            pause = False
            ScoreStateTime = ScoreStateS + time()
            SecureStateTime = SecureStateS + time()
            TimeBreakTime = TimeBreakS + time()
            ConfusStateTime = ConfusStateS + time()
            SlowMoStateTime = SlowMoStateS + time()
            ParalizedTime = ParalizedS + time()
            ShotSpeedTime = ShotSpeedS + time()
            NoTouchTime = NoTouchS + time()
            teleport(ship_id, ship_id)
        if event.keysym == "Return":
            pause = False
            ScoreStateTime = ScoreStateS + time()
            SecureStateTime = SecureStateS + time()
            TimeBreakTime = TimeBreakS + time()
            ConfusStateTime = ConfusStateS + time()
            SlowMoStateTime = SlowMoStateS + time()
            ParalizedTime = ParalizedS + time()
            ShotSpeedTime = ShotSpeedS + time()
            NoTouchTime = NoTouchS + time()
            TP -= 1
            teleport(ship_id, TP_id1)
    if event.keysym == "Shift_L" and (not pause):
        pause = True
        c.itemconfig(pause_icon, state=NORMAL)
        c.itemconfig(pause_text, text="PAUZE")
        Root.update()
        ScoreStateS = ScoreStateTime - time()
        SecureStateS = SecureStateTime - time()
        TimeBreakS = TimeBreakTime - time()
        ConfusStateS = ConfusStateTime - time()
        SlowMoStateS = SlowMoStateTime - time()
        ParalizedS = ParalizedTime - time()
        ShotSpeedS = ShotSpeedTime - time()
        NoTouchS = NoTouchTime - time()
    elif event.keysym == "Shift_R" and pause and (not storemode) and (not tpmode) and (not windowmode) and (not presentmode) and not(cheatmode):
        pause = False
        c.itemconfig(pause_icon, state=HIDDEN)
        c.itemconfig(pause_text, text="")
        Root.update()
        ScoreStateTime = ScoreStateS + time()
        SecureStateTime = SecureStateS + time()
        TimeBreakTime = TimeBreakS + time()
        ConfusStateTime = ConfusStateS + time()
        SlowMoStateTime = SlowMoStateS + time()
        ParalizedTime = ParalizedS + time()
        ShotSpeedTime = ShotSpeedS + time()
        NoTouchTime = NoTouchS + time()
        # Spacebar = "space"
    if event.keysym == "F1" and TP > 0 and (not tpmode):
        pause = True
        ScoreStateS = ScoreStateTime - time()
        SecureStateS = SecureStateTime - time()
        TimeBreakS = TimeBreakTime - time()
        ConfusStateS = ConfusStateTime - time()
        SlowMoStateS = SlowMoStateTime - time()
        ParalizedS = ParalizedTime - time()
        ShotSpeedS = ShotSpeedTime - time()
        NoTouchS = NoTouchTime - time()
        tpmode = True
        tp_mode()
    if event.keysym == "F2" and (not storemode):
        pause = True
        ScoreStateS = ScoreStateTime - time()
        SecureStateS = SecureStateTime - time()
        TimeBreakS = TimeBreakTime - time()
        ConfusStateS = ConfusStateTime - time()
        SlowMoStateS = SlowMoStateTime - time()
        ParalizedS = ParalizedTime - time()
        ShotSpeedS = ShotSpeedTime - time()
        NoTouchS = NoTouchTime - time()
        storemode = True
        log.log("DEBUG", "Motion", "Creating Store() to variable \"store\"")
        log.log("DEBUG", "Motion", "storemode="+str(storemode))
        store = Store()
    if event.char == "/":
        Cheater.EventHandler(event)
    if cheatmode:
        Cheater.InputEventHandler(event)

    if event.keysym == "Control":
        global ReturnMain
        ReturnMain = True
    if event.keysym == "F12" and DEBUG:
        # print(LevelScore, KeyActive)
        pass
    if DEBUG_KEY or DEBUG:
        log.log("DEBUG", "EventHandler", "Key Pressed: " + event.keysym)
    Root.update()


log.log("info", "main", "move_ship command has been created")


class State:
    """
    Status for the game
    """
    global StateTime
    global ScoreState
    global SecureState
    global SlowMoState
    global ConfusState
    global TimeBreak
    global SpdBoost
    global ScoreStateTime

    @staticmethod
    def set_state(act):
        """
        Sets the status by Bubble-Action
        :param act:
        :return:
        """
        global ScoreState
        global StateTime
        global SecureState
        global SlowMoState
        global ConfusState
        global TimeBreak
        global SpdBoost
        global Paralized
        global ShotSpeed
        global ScoreStateTime
        global SecureStateTime
        global SlowMoStateTime
        global ConfusStateTime
        global TimeBreakTime
        global SpdBoostTime
        global ParalizedTime
        global ShotSpeedTime
        global NoTouch
        global NoTouchTime
        log.log("info", "State", "Give the player, status: '" + act + "'.")
        if act == "DoubleState":
            ScoreState = 2
            ScoreStateTime = time() + randint(5, 20)
        if act == "Protect":
            SecureState = True
            SecureStateTime = time() + randint(10, 15)
        if act == "SlowMotion":
            SlowMoState = True
            SlowMoStateTime = time() + randint(15, 23)
        if act == "Confusion":
            ConfusState = True
            ConfusStateTime = time() + randint(5, 10)
        if act == "TimeBreak":
            TimeBreak = True
            TimeBreakTime = time() + randint(10, 20)
        if act == "SpeedBoost":
            SpdBoost = True
            SpdBoostTime = time() + randint(10, 20)
        if act == "Paralis":
            Paralized = True
            ParalizedTime = time() + randint(5, 7)
        if act == "HyperMode":
            ConfusState = False
            ConfusStateTime = time()
            Paralized = False
            ParalizedTime = time()
            TimeBreak = True
            ScoreState = 10
            TimeBreakTime = time() + randint(24, 32)
            ScoreStateTime = time() + randint(24, 32)
        if act == "ShotSpdStat":
            ShotSpeed = 10
            ShotSpeedTime = time() + randint(13, 15)
        if act == "NoTouch":
            NoTouch = True
            NoTouchTime = time() + randint(10, 15)
        if act == "Ultimate":
            ScoreState = 10
            ScoreStateTime = time() + 10
            SlowMoState = True
            SlowMoStateTime = time() + randint(7, 10)

    @staticmethod
    def del_state(act):
        """
        Removes a status
        *This is for future game
        :param act:
        :return:
        """
        # State and time globals
        global ScoreState
        global StateTime
        global SecureState
        global SlowMoState
        global ConfusState
        global TimeBreak
        global SpdBoost
        global Paralized
        global ShotSpeed
        global ScoreStateTime

        # Set the status of the player
        if act == "DoubleState":
            ScoreState = 1
            ScoreStateTime = time()
        if act == "Protect":
            SecureState = False
            StateTime = time()
        if act == "SlowMotion":
            SlowMoState = False
            StateTime = time()
        if act == "Confusion":
            ConfusState = False
            StateTime = time()
        if act == "TimeBreak":
            TimeBreak = False
            StateTime = time()
        if act == "SpeedBoost":
            SpdBoost = False
            StateTime = time()

        if act == "Paralis":
            Paralized = False
            StateTime = time()
        if act == "HyperMode":
            TimeBreak = False
            ScoreState = 10
            StateTime = time()
        if act == "ShotSpdStat":
            ShotSpeed = 25
            StateTime = time()


log.log("info", "main", "State-class has been created succesfully")


# (Incompatible) It's was used for a saved start positions of the bubbles
def old_start():
    """
    *It's not the old start.
    Start positions for bubbles in coords x and y.
    """
    for tyru in range(int((WIDTH + 105 - 72) / 10)):
        x = randint(0, WIDTH + ScreenGap * 8)
        r = randint(MinBubRad, MaxBubRad)
        y = randint(72 + r, (HEIGHT - 105 - r))
        i = randint(0, 1000)
        hardness = 1
        if 0 <= i < 800:
            ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
            act = "Normal"
            spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
            hardness = 1
        elif 800 <= i < 830:
            ids = [c.create_image(x, y, image=bub["Double"][r * 2])]
            act = "Double"
            spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
            hardness = 1
        elif 830 <= i < 930:
            ids = [c.create_image(x, y, image=bub["Kill"][r * 2])]
            act = "Kill"
            spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
            hardness = 1
        elif 930 <= i < 940:
            ids = [c.create_image(x, y, image=bub["Triple"][r * 2])]
            act = "Triple"
            spd = randint(int(MaxBubSpd) + 2, int(MaxBubSpd) + 6)
            hardness = 1
        elif 940 <= i < 950:
            ids = [c.create_image(x, y, image=bub["SpeedUp"][r * 2])]
            act = "SpeedUp"
            spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 3)
            hardness = 1
        elif 950 <= i < 960:
            ids = [c.create_image(x, y, image=bub["SpeedDown"][r * 2])]
            act = "SpeedDown"
            spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 3)
            hardness = 1
        elif 960 <= i < 965:
            if Lives < 7:
                ids = [c.create_image(x, y, image=bub["Up"][r * 2])]
                act = "Up"
                spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 3)
                hardness = 1
            else:
                ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
                act = "Normal"
                spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
                hardness = 1
        elif 973 <= i < 974:
            ids = [c.create_image(x, y, image=bub["Ultimate"][r * 2])]
            act = "Ultimate"
            spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
            hardness = 1
        elif 974 <= i < 976:
            ids = [c.create_image(x, y, image=bub["DoubleState"][r*2])]
            act = "DoubleState"
            spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        elif 979 <= i < 981:
            ids = [c.create_image(x, y, image=bub["Protect"][r*2])]
            act = "Protect"
            spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        elif 981 <= i < 984:
            ids = [c.create_image(x, y, image=bub["SlowMotion"][r*2])]
            act = "SlowMotion"
            spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        elif 984 <= i < 985:
            ids = [c.create_image(x, y, image=bub["TimeBreak"][r*2])]
            act = "TimeBreak"
            spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        elif 1100 <= i < 1101:
            ids = [c.create_image(x, y, image=bub["HyperMode"][r*2])]
            act = "HyperMode"
            spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        elif 1101 <= i < 1120:
            ids = [c.create_image(x, y, image=bub["ShotSpdStat"][r*2])]
            act = "ShotSpdStat"
            spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        elif 1120 <= i < 1121 and Level > 19:
            ids = [c.create_image(x, y, image=bub["Teleporter"][r*2])]
            act = "Teleporter"
            spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 2)
        elif 1121 <= i < 1124 and Level > 4:
            ids = [c.create_image(x, y, image=DmdBub),
                   c.create_image(x, y, image=bub["Normal"][36])]
            r = 36
            act = "Diamond"
            spd = randint(int(MaxBubSpd) + 2, int(MaxBubSpd) + 4)
        elif 1124 <= i < 1130 and Level > 4:
            ids = [c.create_image(x, y, image=BubCoin)]
            r = 40
            act = "Coin"
            spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 2)
        else:
            ids = [c.create_image(x, y, image=bub["Normal"][r*2])]
            act = "Normal"
            spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        BubHard.append(hardness)
        BubPos.append(get_coords(ids[0]))
        BubAct.append(act)
        BubID.append(ids)
        BubRad.append(r)
        BubSpd.append(spd)


log.log("info", "main", "The old start has been created")


def start():
    """
    Starts the bubbles on random positions x and y.
    :return:
    """
    old_start()
    return


log.log("info", "main", "New start has been created")


def place_bubble(x, y, r, act):
    """
    Places a bubble.
    The bubble can't moving or removed (only by closing game).
    :param x:
    :param y:
    :param r:
    :param act:
    """

    if act == "Normal":
        c.create_image(x, y, image=bub["Normal"][r*2])
    if act == "Double":
        c.create_image(x, y, image=bub["Double"][r*2])
    if act == "Kill":
        c.create_image(x, y, image=bub["Kill"][r*2])
    if act == "Triple":
        c.create_image(x, y, image=bub["Triple"][r*2])
    if act == "SpeedUp":
        c.create_image(x, y, image=bub["SpeedUp"][r*2])
    if act == "SpeedDown":
        c.create_image(x, y, image=bub["SpeedDown"][r*2])
    if act == "Up":
        c.create_image(x, y, image=bub["Up"][r*2])
    if act == "Ultimate":
        c.create_image(x, y, image=bub["Ultimate"][r*2])
    if act == "DoubleState":
        c.create_image(x, y, image=bub["DoubleState"][r*2])
    if act == "Protect":
        c.create_image(x, y, image=bub["Protect"][r*2])
    if act == "SlowMotion":
        c.create_image(x, y, image=bub["SlowMotion"][r*2])
    if act == "TimeBreak":
        c.create_image(x, y, image=bub["TimeBreak"][r*2])
    if act == "Confusion":
        c.create_image(x, y, image=bub["Confusion"][r*2])
    if act == "HyperMode":
        c.create_image(x, y, image=bub["HyperMode"][r*2])
    if act == "ShotSpdStat":
        c.create_image(x, y, image=bub["ShotSpdStat"][r*2])
    if act == "Teleporter":
        c.create_image(x, y, image=bub["Teleporter"][r*2])
    if act == "Coin":
        c.create_image(x, y, image=BubCoin)
    if act == "NoTouch":
        c.create_image(x, y, image=bub["NoTouch"][r*2])
    if act == "LevelKey":
        c.create_image(x, y, image=bub["Double"][25*2])
        c.create_image(x, y, image=Key)


log.log("info", "main", "Bubble placer created")


def create_bubble(j=None, xx=None, yy=None, rr=None, ss=None):
    """
    Creates a bubble that can moving and removing by touching with the ship
    :param j:
    :param xx:
    :param yy:
    :param rr:
    :param ss:
    Todo: Add more bubbles. Bad Stone Bubble
    """
    global BubPos
    if (not xx) or (not yy) or (not rr):
        x = WIDTH + ScreenGap
        r = randint(int(MinBubRad), int(MaxBubRad))
        y = randint(72 + r, (HEIGHT - 105 - r))
    else:
        x = xx
        y = yy
        r = rr
    if not j:
        i = randint(0, 1600)
    else:
        i = j
    if Level <= 100:
        level_dat = Level
    else:
        level_dat = 100
    if 0 <= i < 800:
        ids = [c.create_image(x, y, image = bub["Normal"][r*2])]
        act = "Normal"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 800 <= i < 830:
        ids = [c.create_image(x, y, image=bub["Double"][r*2])]
        act = "Double"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 830 <= i < 930:
        ids = [c.create_image(x, y, image=bub["Kill"][r*2])]
        act = "Kill"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 930 <= i < 940:
        ids = [c.create_image(x, y, image=bub["Triple"][r*2])]
        act = "Triple"
        spd = randint(int(MaxBubSpd) + 2, int(MaxBubSpd) + 6)
        hardness = 1
    elif 940 <= i < 950:
        ids = [c.create_image(x, y, image=bub["SpeedUp"][r*2])]
        act = "SpeedUp"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 3)
        hardness = 1
    elif 950 <= i < 960:
        ids = [c.create_image(x, y, image=bub["SpeedDown"][r*2])]
        act = "SpeedDown"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 3)
        hardness = 1
    elif 960 <= i < 965:
        if Lives < 7:
            ids = [c.create_image(x, y, image=bub["Up"][r*2])]
            act = "Up"
            spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 3)
            hardness = 1
        else:
            ids = [c.create_image(x, y, image=bub["Normal"][r*2])]
            act = "Normal"
            spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
            hardness = 1
    elif 973 <= i < 974:
        ids = [c.create_image(x, y, image=bub["Ultimate"][r*2])]
        act = "Ultimate"
        spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        hardness = 1
    elif 974 <= i < 976:
        ids = [c.create_image(x, y, image=bub["DoubleState"][r*2])]
        act = "DoubleState"
        spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        hardness = 1
    elif 979 <= i < 981:
        ids = [c.create_image(x, y, image=bub["Protect"][r*2])]
        act = "Protect"
        spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        hardness = 1
    elif 981 <= i < 984:
        ids = [c.create_image(x, y, image=bub["SlowMotion"][r*2])]
        act = "SlowMotion"
        spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        hardness = 1
    elif 984 <= i < 985:
        ids = [c.create_image(x, y, image=bub["TimeBreak"][r*2])]
        act = "TimeBreak"
        spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        hardness = 1
    elif 1100 <= i < 1101:
        ids = [c.create_image(x, y, image=bub["HyperMode"][r*2])]
        act = "HyperMode"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 1101 <= i < 1120:
        ids = [c.create_image(x, y, image=bub["ShotSpdStat"][r*2])]
        act = "ShotSpdStat"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 985 <= i < 1085:
        ids = [c.create_image(x, y, image=bub["Confusion"][r*2])]
        act = "Confusion"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 1085 <= i < 1100:
        ids = [c.create_image(x, y, image=bub["Paralis"][r*2])]
        act = "Paralis"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 1100 <= i < 1101:
        ids = [c.create_image(x, y, image=bub["HyperMode"][r*2])]
        act = "HyperMode"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 1101 <= i < 1120:
        ids = [c.create_image(x, y, image=bub["ShotSpdStat"][r*2])]
        act = "ShotSpdStat"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    elif 1120 <= i < 1121 and Level > 19:
        ids = [c.create_image(x, y, image=bub["Teleporter"][r*2])]
        act = "Teleporter"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 2)
        hardness = 1
    elif 1121 <= i < 1124 and Level > 4:
        ids = [c.create_image(x, y, image=Dmd),
               c.create_image(x, y, image=bub["Normal"][36])]
        r = 18
        act = "Diamond"
        spd = randint(int(MaxBubSpd) + 2, int(MaxBubSpd) + 4)
        hardness = 1
    elif 1124 <= i < 1130 and Level > 4:
        ids = [c.create_image(x, y, image=BubCoin)]
        r = 20
        act = "Coin"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 2)
        hardness = 2
    elif 1130 <= i < 1150 and Level > 4:
        r = 20
        ids = [c.create_image(x, y, image=bub["NoTouch"][r*2])]
        act = "NoTouch"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 2)
        hardness = 1
    elif 1150 <= i < 1160 and Level > 4:
        r = 20
        ids = [c.create_image(x, y, image=bub["Normal"][40]),
               c.create_text(x, y, text="?", font=("helvetica", 32), fill="white")]
        act = "Present"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 2)
        hardness = 1
    elif 1160 <= i < 1263+(197*level_dat/100):
        ids = [c.create_image(x, y, image=bub["StoneBub"][r*2])]
        act = "StoneBub"
        spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        hardness = 3 + int(level_dat/2)
        # elif 1360 <= i < ???:
    elif 1460 <= i < 1491:
        ids = [c.create_image(x, y, image=BubCoin)]
        r = 20
        act = "Coin"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 2)
        hardness = 2
    elif i == -1:
        ids = [c.create_image(x, y, image=bub["Double"][26*2]),
               c.create_image(x, y, image=Key)]
        r = 26
        act = "LevelKey"
        spd = randint(int(MaxBubSpd) + 4, int(MaxBubSpd) + 8)
        hardness = 1
    elif i == -2:
        ids = [c.create_image(x, y, image=bub["Up"][r * 2])]
        act = "Up"
        spd = randint(int(MaxBubSpd), int(MaxBubSpd) + 3)
        hardness = 1
    else:
        ids = [c.create_image(x, y, image=bub["Normal"][r*2])]
        act = "Normal"
        spd = randint(int(MaxBubSpd) - 3, int(MaxBubSpd))
        hardness = 1
    if not ss:
        pass
    else:
        spd = ss
    BubHard.append(hardness)
    BubAct.append(act)
    BubID.append(ids)
    BubRad.append(r)
    BubSpd.append(spd)


log.log("info", "main", "Bubble creator created")


def create_shot():
    """
    Creates Shooting ammo
    """
    global new
    if new < time():
        x, y = get_coords(ship_id2)
        ShotID.append(c.create_line(10 + x + SHIP_R / 2, y, 15 + x + SHIP_R / 2, y, fill="yellow"))
        ShotSpd.append(ShotSpeed)
        ShotDmge.append(0)
        new = time() + 5


def get_coords(id_num):
    """
    Gets the coords by id number of item.
    :param id_num:
    :return:
    """
    pos = c.coords(id_num)
    # print(pos, id_num, c.itemcget(id_num, "fill"))
    if len(pos) == 2:
        x = pos[0]
        y = pos[1]
    else:
        x = (pos[0] + pos[2]) / 2
        y = (pos[1] + pos[3]) / 2
    return x, y


def move_bubbles():
    """
    The base of motion for the bubbles
    """
    global BubPos
    try:
        for i in range(len(BubID)):
            for j in range(len(BubID[i])):
                if not BubAct == "Null":
                    if SlowMoState:
                        c.move(BubID[i][j], -BubSpd[i]/10, 0)
                    else:
                        c.move(BubID[i][j], -BubSpd[i], 0)
                    Root.update()
    except IndexError:
        pass


def move_shoots():
    """
    Motion for ammo.
    """
    global ShotPos
    for i in range(len(ShotID)):
        try:
            c.move(ShotID[i], ShotSpd[i], 0)
        except IndexError:
            log.log("WARNING", "Move Ammo", "Can't move ammo index '"+str(i)+"'.")
        Root.update()


log.log("info", "main", "Sprite movers created")


def del_bubble(i):
    """
    Removes a bubble.
    :param i:
    """
    if not BubAct == "Null":
        if len(BubPos) != 0:
            del BubRad[i]
            del BubSpd[i]
            for j in BubID[i]:
                c.delete(j)
            del BubID[i]
            if BubAct[i] == "LevelKey":
                global KeyActive
                KeyActive = False
            del BubAct[i]
            del BubHard[i]
            # pop.play()


def del_shoot(i):
    """
    Deletes ammo by request.
    :param i:
    :return:
    """
    c.delete(ShotID[i])
    del ShotID[i]
    del ShotSpd[i]
    del ShotDmge[i]


log.log("info", "main", "Sprite deleters created")


def clean_up_bubs():
    """
    Removes bubbles that's out of screen. If x is lower than -100
    """
    try:
        for i in range(len(BubID) - 1, -1, -1):
            x, y = get_coords(BubID[i][0])
            if x < -ScreenGap:
                # Checks if the Level-key is active.
                # If it's active then sets it the variable
                # for the key-bubble to off.
                if BubAct[i] == "LevelKey":
                    global KeyActive
                    KeyActive = False
                del_bubble(i)
    except IndexError:
        pass


def clean_up_shots():
    """
    Removes ammo if it's off screen.
    :return:
    """
    for i in range(len(ShotID) - 1, -1, -1):
        x, y = get_coords(ShotID[i][0])
        if x > WIDTH + ScreenGap:
            del_shoot(i)


log.log("info", "main", "Sprite cleaners created")


def distance(id1, id2):
    """
    Calculates the distance of the ids.
    :param id1:
    :param id2:
    :return:
    """
    try:
        x1, y1 = get_coords(id1)
        x2, y2 = get_coords(id2)
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    except IndexError:
        # print(id1, id2)
        # print(get_coords(id1))
        # print(get_coords(id2))
        log.log("ERROR", "Distance", "IndexError excepted in distance()-module")
        LogException("IndexError excepted in distance()-module")


def clean_level_keys():
    """
    Removes all Level-Keybubble.
    :return:
    """
    for i in range(len(BubAct) - 1, -1, -1):
        if BubAct[i] == "LevelKey":
            del_bubble(i)

class Collision:
    def __init__(self):
        pass

    def coll_func(self, act, normal_score, hardness, accept_negative):
        """
        Collision.
        All bubbles have a function.
        This Method sets a state or sets a variable.
        :param act:
        :param normal_score:
        :param hardness:
        :param accept_negative:
        :return:
        """
        global Score
        global Lives
        global SHIP_SPD
        global ScoreState
        global Level
        global TP
        global Diamond
        global LevelScore
        global Coins
        global KeyActive
        if act == "Normal":
            Score += normal_score * ScoreState
        if act == "Double":
            Score += normal_score * 2 * ScoreState
        if act == "Triple":
            Score += normal_score * 3 * ScoreState
        if (not SecureState) and accept_negative:
            if act == "Kill":
                Lives -= 1
            if act == "Min":
                Score -= normal_score
            if act == "SpeedDown":
                if SHIP_SPD == 5:
                    return
                SHIP_SPD -= 5
            if act == "Confusion":
                State.set_state("Confusion")
            if act == "Paralis":
                State.set_state("Paralis")
            if act == "NoTouch":
                Score += normal_score * ScoreState
                State.set_state(act)
        if act == "DoubleState":
            State.set_state(act)
        if act == "TripleState":
            State.set_state(act)
        if act == "SpeedUp":
            if SHIP_SPD == 20:
                return
            elif SHIP_SPD == 25:
                return
            SHIP_SPD += 5
        if act == "Up":
            Lives += 1
        if act == "Protect":
            State.set_state(act)
        if act == "SlowMotion":
            State.set_state(act)
        if act == "TimeBreak":
            State.set_state(act)
        if act == "Ultimate":
            if Lives < 7:
                Lives += 1
            SHIP_SPD = 25
            Score += normal_score * 10 * ScoreState
        if act == "HyperMode":
            Lives += 2
            SHIP_SPD = 25
            Score += normal_score * 30 * ScoreState
            State.set_state(act)
        if act == "ShotSpdStat":
            Score += normal_score * ScoreState
            State.set_state(act)
        if act == "Diamond":
            Diamond += 1
        if act == "Coin":
            Coins += 1
        if act == "Teleporter":
            TP += 1
        if act == "Teleporter":
            Score += (normal_score * (hardness/9))
        if act == "LevelKey":
            Level += 1
            clean_level_keys()
            KeyActive = False
            view_Level(Level)
        if act == "Present":
            global P
            P = Present()
        if act != "Present":
            PlaySound("data/bubpop.wav", 1)

    def check_collision(self):
        """
        Collision bubble by touching or shooting the bubble
        """
        for bub in range(len(BubID.copy()) - 1, -1, -1):
            # Collision with ship
            try:
                if distance(ship_id2, BubID[bub][0]) < (SHIP_R + BubRad[bub]):
                    log.log("INFO", "Bubble",
                            "Bubble collised: " + BubAct[bub] + "| Radius: " + str(BubRad[bub]) + "| Hardness: " + str(
                                BubHard[bub]) + "| Speed: " + str(BubSpd[bub]) + "| len BubAct: " + str(
                                len(BubAct)) + "| len BubHard: " + str(len(BubHard)))
                    if not NoTouch:
                        # Sets score / status etc. and deletes bubble
                        if BubHard[bub] == 1:
                            Thread(None, lambda: self.coll_func(BubAct[bub], (BubRad[bub] + BubSpd[bub]), BubHard[bub], True)).start()
                            del_bubble(bub)
                        elif BubHard[bub] > 1:
                            replace_list(BubHard, bub, BubHard[bub] - 1)
            except IndexError:
                pass

        # Collision with ammo
        for shot in range(len(ShotID.copy()) - 1, -1, -1):
            # print(ShotID[shot], shot)
            try:
                if distance(ShotID[shot], BubID[bub][0]) < (1 + BubRad[bub]):
                    log.log("INFO", "Bubble",
                            "Bubble collised: " + BubAct[bub] + "| Radius: " + str(BubRad[bub]) + "| Hardness: " + str(
                                BubHard[bub]) + "| Speed: " + str(BubSpd[bub]) + "| len BubAct: "+str(len(BubAct)) + "| len BubHard: " + str(len(BubHard)))
                    if BubHard[bub] == 1:
                        Thread(None, lambda: self.coll_func(BubAct[bub], (BubRad[bub] + BubSpd[bub]), BubHard[bub], False)).start()
                        del_bubble(bub)
                        replace_list(ShotDmge, shot, ShotDmge[shot] + 1)
                        if ShotDmge[shot] > 4:
                            del_shoot(shot)
                        PlaySound("data/bubpop.wav", 1)
                    elif BubHard[bub] > 1:
                        replace_list(BubHard, bub, BubHard[bub] - 1)
                        replace_list(ShotDmge, shot, ShotDmge[shot] + 1)
                        if ShotDmge[shot] > 4:
                            del_shoot(shot)
            except IndexError:
                pass


log.log("info", "main", "Collision and check_collision-func created")


def tp_mode():
    """
    Teleport mode.
    Activated if you pressed F12, and have 1 or more TP's
    """
    global TimeBreak
    global tpmode
    TimeBreak = True
    tpmode = True
    global TP_id1
    global TP_id2
    global TP_id3
    global TP_id4

    # Creates Teleport-ID's
    TP_id1 = c.create_oval(0, 0, 20, 20, outline="black")
    TP_id2 = c.create_line(0, 10, 20, 10, fill="black")
    TP_id3 = c.create_line(10, 0, 10, 20, fill="black")
    TP_id4 = c.create_oval(7, 7, 13, 13, outline="black")

    # Moves teleport-ID's to mid.
    c.move(TP_id1, MID_X - 10, MID_Y - 10)
    c.move(TP_id2, MID_X - 10, MID_Y - 10)
    c.move(TP_id3, MID_X - 10, MID_Y - 10)
    c.move(TP_id4, MID_X - 10, MID_Y - 10)


def teleport(ship_id1, teleport_id):
    """
    Teleporting.
    Activating by TP_mode, if pressed on Spacebar.
    :param ship_id1:
    :param teleport_id:
    """

    # Globals
    global TimeBreak
    global tpmode
    TimeBreak = False
    tpmode = False

    # Setting up variables for teleporting.
    s_x, s_y = get_coords(ship_id1)
    t_x, t_y = get_coords(teleport_id)
    x_move = t_x - s_x
    y_move = t_y - s_y

    # Teleporting.
    c.move(ship_id1, x_move, y_move)
    c.move(ship_id2, x_move, y_move)

    # Deletes Teleport ID's
    c.delete(TP_id1)
    c.delete(TP_id2)
    c.delete(TP_id3)
    c.delete(TP_id4)

    # Updates the screen
    Root.update()


class Present:
    """
    Giving a present activated by a bubble
    """

    def __init__(self):
        global ScoreStateS
        global SecureStateS
        global TimeBreakS
        global ConfusStateS
        global SlowMoStateS
        global ParalizedS
        global ShotSpeedS
        global NoTouchS
        global pause
        global presentmode

        # Sets pause, and presentmode for controling information.
        pause = True
        presentmode = True

        # Sets pause save-variables.
        ScoreStateS = ScoreStateTime - time()
        SecureStateS = SecureStateTime - time()
        TimeBreakS = TimeBreakTime - time()
        ConfusStateS = ConfusStateTime - time()
        SlowMoStateS = SlowMoStateTime - time()
        ParalizedS = ParalizedTime - time()
        ShotSpeedS = ShotSpeedTime - time()
        NoTouchS = NoTouchTime - time()

        # Creating ID's for window and information.
        self.lineid = []
        self.bgid2 = c.create_rectangle(0, 0, 0, 0, fill="#002713")
        self.bgid = c.create_image(MID_X, MID_Y + 50, image=PresBG)
        self.LineImageLength = len(self.lineid)
        self.IconId1 = c.create_image(MID_X, 120, image=Circle)
        self.IconId2 = c.create_image(MID_X, 120, image=PrIcon)
        self.Diamonds = None
        self.Money = None
        self.textid = c.create_text(MID_X, MID_Y + 20, font=("Helvetica", 30), fill="black")
        self.fgid = c.create_image(MID_X, MID_Y, image=StrFG)

        # Ramdomizing Gifts for output
        self.randomize_gifts()

    def randomize_gifts(self, i=None):
        """
        Randomizing Gifts
        :param i:
        :return:
        """
        if i is None:
            # If variable "i" was not given.
            i = randint(0, 1000)
        if i == 0:
            # Master Bonus, huge pack of diamonds and coins
            a = randint(0, 44)
            if 0 <= a < 16:
                self.Diamonds = a
            elif 16 <= a < 24:
                self.Diamonds = a * 2
            elif 24 <= a < 32:
                self.Diamonds = a * 3
            elif 32 <= a < 36:
                self.Diamonds = a * 4
            elif 36 <= a < 40:
                self.Diamonds = a * 5
            elif 40 <= a < 42:
                self.Diamonds = a * 6
            elif 42 <= a < 44:
                self.Diamonds = a * 8
            elif 44 <= a < 45:
                self.Diamonds = a * 12

            a = randint(0, 44)
            if 0 <= a < 16:
                self.Money = a
            elif 16 <= a < 24:
                self.Money = a * 10
            elif 24 <= a < 32:
                self.Money = a * 15
            elif 32 <= a < 36:
                self.Money = a * 20
            elif 36 <= a < 40:
                self.Money = a * 25
            elif 40 <= a < 42:
                self.Money = a * 30
            elif 42 <= a < 44:
                self.Money = a * 40
            elif 44 <= a < 45:
                self.Money = a * 60
            text = "You earned:\n" + str(self.Diamonds) + \
                   "diamonds and " + str(self.Money) + " coins."
            c.itemconfig(self.textid, text=text)

            global Diamond, Coins
            Diamond += self.Diamonds
            Coins += self.Money
            PlaySound("data/Tadaa.wav", 1)
        elif 1 <= i < 100:
            # Teleport
            text = "You earned:\n1 Teleport"
            c.itemconfig(self.textid, text=text)
            PlaySound("data/Tadaa.wav", 1)
            global TP
            TP += 1
        elif 100 <= i < 180:
            # Giving a Protection
            # Text for information
            text = "You earned:\nA protection"
            c.itemconfig(self.textid, text=text)

            # Playing sound for gift.
            PlaySound("data/Tadaa.wav", 1)

            # Globals and status setup
            global SecureState, SecureStateTime
            global ConfusState, ConfusStateTime
            global Paralized, ParalizedTime
            global NoTouch, NoTouchTime
            SecureState = True
            SecureStateTime = time() + randint(10, 18)
            ConfusState = False
            ConfusStateTime = time()
            Paralized = False
            ParalizedTime = time()
            NoTouch = False
            NoTouchTime = time()
        else:
            # Nothing gives
            text = "O, oh. There's nothing"
            c.itemconfig(self.textid, text=text)

    def exit(self):
        """
        Exits present screen.
        :return:
        """
        # Deletes line background.
        for i in self.lineid:
            c.delete(i)
        c.delete(self.bgid)
        c.delete(self.textid)
        c.delete(self.IconId1)
        c.delete(self.IconId2)
        c.delete(self.bgid2)
        c.delete(self.fgid)


class Store:
    """
    Base Store Class.
    This class is for the in-game store.
    The store contains items to buy with
    virtual money (Coins and Diamonds).
    """

    def __init__(self):
        """
        Set store menu.
        Base of menu control

        (Used for creating bg, items and icons)
        :rtype: object
        """
        # Logging information for debug.
        log.log("info", "Store", "Player Opened the store")

        # Setup for store, the pause and controls.
        global storemode
        global pause
        global Diamond

        # Set storemode to ON (True)
        # and the pause ON (True). So the bubbles / ship can't moving.
        storemode = True
        pause = True

        # Background color (Can be changed by fill=<color-string>
        self.bg = c.create_rectangle(0, 0, WIDTH, HEIGHT, fill="coral")

        # Selection
        self.maximal = 3
        self.selected = 0

        # Info / icons dictionaries
        self.button = {}
        self.frame = {}
        self.item = {}
        self.name = {}
        self.d_icon = {}
        self.info = {}
        self.price = {}
        self.c_icon = {}
        self.coins = {}

        # Number of diamonds you have:
        self.vDiamonds = c.create_text(25, 25, text="Diamonds: " + str(Diamond), fill="white", anchor=W,
                                       font=("Helvetica", 18))

        # Setups items and price.
        fo = open("data/Store.cfg")
        self.maximal = int(next(fo))

        for i in range(self.maximal + 1):
            a = next(fo)
            b = a.split(sep=";")
            self.button[i] = c.create_rectangle(25, 50 + (100 * i), 200, 149 + (100 * i), outline="white", fill="coral")
            self.frame[i] = c.create_rectangle(50, 50 + (100 * i), 100, 100 + (100 * i), outline="white", fill="coral")
            self.item[i] = c.create_image(75, 75 + (100 * i), image=StoreIcon[i])
            self.name[i] = c.create_text(110, 75 + (100 * i), text=b[2], fill="white", anchor=W)
            self.d_icon[i] = c.create_image(188, 117 + (100 * i), image=Dmd, anchor=E)
            self.info[i] = c.create_text(148, 117 + (100 * i), text=b[1], fill="white", anchor=E)
            self.price[i] = int(b[1])
            self.c_icon[i] = c.create_image(30, 117 + (100 * i), image=StoreCoin, anchor=W)
            self.coins[i] = c.create_text(50, 117 + (100 * i), text=b[0], fill="white", anchor=W)

        # Sets up the selected, the first.
        c.itemconfig(self.button[self.selected], fill="red")
        c.itemconfig(self.frame[self.selected], fill="darkred")

        # Foreground for fade
        self.fg = c.create_image(MID_X, MID_Y, image=StrFG)
        self.w = None
        self.b = None
        self.b2 = None
        self.close = None

    def set_selected(self, i):
        """
        Set selected item
        i = select var to be moved
            if i is 1 then switch one down
            else if i is -1 then switch one up
            can't switch if i is out of range.
        :param i:
        :return:
        """

        # Sets slected item color.
        if self.maximal >= self.selected + i > -1:
            # Sets old color
            c.itemconfig(self.button[self.selected], fill="coral")
            c.itemconfig(self.frame[self.selected], fill="coral")

            # Sets selected variable
            self.selected += i

            # Sets new selected color
            c.itemconfig(self.button[self.selected], fill="red")
            c.itemconfig(self.frame[self.selected], fill="darkred")

    def buy(self):
        """
        Buying a item and accepting buying the item
        activates the last phase.
        This phase sets the Diamonds and the Coins variables
        by buying a item.
        If you have no coins / diamonds it does nothing.
        """
        global Diamond
        global Coins
        global pause
        global windowmode
        global storemode
        global Lives

        # Sets storemode controls
        storemode = True

        # Deletes window
        self.w.destroy()
        self.b.destroy()
        self.b2.destroy()
        self.close.destroy()
        # Log information
        log.log("info", "Store",
                "Player bought item nr. " + str(self.selected) + " for " + str(self.price[self.selected]) +
                "Diamonds, and" + c.itemcget(self.coins[self.selected], "text"))

        # Checking if you have enough money / diamonds
        if Diamond >= self.price[self.selected] and Coins >= int(c.itemcget(self.coins[self.selected], "text")):
            Diamond -= self.price[self.selected]
            Coins -= int(c.itemcget(self.coins[self.selected], "text"))
            if self.selected == 0:
                global Level
                Level += 1
            if self.selected == 1:
                global TP
                TP += 1
            if self.selected == 2:
                global StateTime
                global SecureState
                global ConfusState
                global Paralized
                StateTime = time()
                ConfusState = False
                Paralized = False
                State.set_state("Protect")
            if self.selected == 3:
                Diamond += 1
            if self.selected == 4:
                Lives += 1
            c.itemconfig(self.vDiamonds, text="Diamonds: " + str(Diamond))
            windowmode = False
        else:
            pass

    def buy_selected(self):
        """
        Creates a window for accepting to bought a item.
        """
        # Pause and control globals
        global pause
        global windowmode
        global storemode

        # Storemode controls off.
        storemode = False

        def StoremodeOn():
            global storemode
            storemode = True

        # Creates window
        self.w = Window(title="Continue?", height=50, width=200, parent_is_store=True)

        # Creates buttons
        a = log.log
        log.log("DEBUG", "Store", "MID_X - 80 = "+str(MID_X-80))
        self.b = Button2(MID_X - 80, MID_Y, text="Yes", command=lambda: self.buy())
        self.b2 = Button2(MID_X + 80, MID_Y, text="No",
                         command=lambda: (self.w.destroy(), self.b.destroy(), self.b2.destroy(), None,
                                          StoremodeOn()))
        # self.close = Button2(MID_X + 80, text="No",
        #                 command=lambda: self.close.storemode_destroy(self.w.destroy(), self.b.destroy(), self.b2.destroy(),
        #                                      self.close.destroy(), StoremodeOn()))

        # Places buttons
        self.w.child.append(self.b)
        self.w.child.append(self.b2)
        self.w.child.append(self.close)
        # self.b.place(y=MID_Y, x=MID_X - 80, anchor=W)
        # self.b2.place(y=MID_Y, x=MID_X + 80, anchor=E)

        # Sets windowmode controls
        windowmode = True

    def exit(self):
        """
        Exits the store

        Todo: Removing it's self by exit
        """

        # Pause and controls globals
        global storemode
        global pause
        global windowmode
        global ScoreStateTime
        global SecureStateTime
        global ConfusStateTime
        global TimeBreakTime
        global SlowMoStateTime
        global ParalizedTime
        global ShotSpeedTime
        global NoTouchTime

        # Sets windowmode off. If it isn't off.
        windowmode = False

        # Deletes item-boxes and items.
        for i in range(self.maximal + 1):
            log.log("DEBUG", "Store", "Del attributes: "+str((self.button[i], self.frame[i], self.item[i], self.info[i], self.d_icon[i], self.name[i], self.price[i], self.c_icon[i], self.coins[i])))
            c.delete(self.button[i])
            c.delete(self.frame[i])
            if c.option_get("image", self.item[i]) != None:
                c.delete(self.item[i])
            c.delete(self.info[i])
            c.delete(self.d_icon[i])
            c.delete(self.name[i])
            # c.delete(self.price[i])
            c.delete(self.c_icon[i])
            c.delete(self.coins[i])
        # Deletes back- and foreground.
        c.delete(self.bg)
        c.delete(self.fg)

        # Deletes the view of diamonds you have.
        c.delete(self.vDiamonds)
        #
        # # Globals for the pause of game and control of store-items.
        # global pause, storemode
        #
        # # Deletes self-variables
        # del self.button, self.frame, self.item, self.info
        # del self.name, self.price, self.c_icon, self.coins
        # del self.bg, self.fg, self.vDiamonds
        #
        # # Pause and store controls.
        pause = False
        storemode = False

        # Pause variables.
        ScoreStateTime = ScoreStateS + time()
        SecureStateTime = SecureStateS + time()
        TimeBreakTime = TimeBreakS + time()
        ConfusStateTime = ConfusStateS + time()
        SlowMoStateTime = SlowMoStateS + time()
        ParalizedTime = ParalizedS + time()
        ShotSpeedTime = ShotSpeedS + time()
        NoTouchTime = NoTouchS + time()

        # Log.
        self.__del__()
        log.log("info", "Store", "Player exited the store.")
    def __del__(self):
        pass



class Window:
    """
    Creates a virtual window in the canvas.
    """

    def __init__(self, title="window", height=600, width=800, parent_is_store = False):
        # Window variables
        self.x1 = MID_X - width / 2
        self.y1 = MID_Y - height / 2 - 20
        self.x2 = MID_X + width / 2
        self.y2 = MID_Y + height / 2
        t_x = MID_X
        t_y = MID_Y - height / 2 - 10
        self.selected_x = 0
        self.selected_y = 0
        self.id = list()
        self.is_store_parent = parent_is_store

        # Creates window.
        self.title_mid = PhotoImage(file="data/borders/titlebar-mid-focused.png")
        self.title_left = PhotoImage(file="data/borders/titlebar-left-focused.png")
        self.title_right = PhotoImage(file="data/borders/titlebar-right-focused.png")

        self.border_left = PhotoImage(file="data/borders/frame-left-focused.png")
        self.border_right = PhotoImage(file="data/borders/frame-right-focused.png")
        self.border_bottom_mid = PhotoImage(file="data/borders/frame-bottom-mid-focused.png")
        self.border_bottom_left = PhotoImage(file="data/borders/frame-bottom-left-focused.png")
        self.border_bottom_right = PhotoImage(file="data/borders/frame-bottom-right-focused.png")
        self.close = PhotoImage(file="data/borders/button-close.png")
        self.close_press = PhotoImage(file="data/borders/button-close-prelight.png")

        self.id.append(c.create_rectangle(self.x1-6, self.y1+14, self.x2+6, self.y2+6, fill="lightgray", outline="#272727"))

        self.id.append(c.create_image(self.x1-4, self.y1, image=self.title_left))
        self.id.append(c.create_image(self.x2+4, self.y1, image=self.title_right))

        for i in range(0, int(width), 8):
            self.id.append(c.create_image(self.x1+i, self.y1, image=self.title_mid))
            self.id.append(c.create_image(self.x1+i, self.y2+7, image=self.border_bottom_mid))

        self.id.append(c.create_image(self.x2-2, self.y1, image=self.title_mid))
        self.id.append(c.create_image(self.x2+2, self.y2+7, image=self.border_bottom_mid))

        for i in range(16, int(height), 16):
            self.id.append(c.create_image(self.x1-7, self.y1+i, image=self.border_left))
            self.id.append(c.create_image(self.x2+7, self.y1+i, image=self.border_right))

        self.id.append(c.create_image(self.x1-7, self.y2-6, image=self.border_left))
        self.id.append(c.create_image(self.x2+7, self.y2-6, image=self.border_right))

        self.id.append(c.create_image(self.x1-7, self.y2+7, image=self.border_bottom_left))
        self.id.append(c.create_image(self.x2+7, self.y2+7, image=self.border_bottom_right))
        self.id.append(c.create_image(self.x2-5, self.y1-3, image=self.close))
        c.bind("<ButtonPress-1>", self.closeButtonPressEvent)
        c.bind("<ButtonRelease-1>", self.closeButtonEvent)

        # self.id.append(c.create_rectangle(self.x1, self.y1, self.x2, self.y1 + 20, fill="#272727", outline="#272727"))

        # Creates Title
        self.id.append(c.create_text(t_x, t_y-12, text=title, fill="#D9D9D9", anchor=CENTER))

        # Sets child-variables.
        self.child = []

    def closeButtonPressEvent(self, event):
        if self.x2 - 5 - self.close.width()/2 < event.x < self.x2 - 5 + self.close.width()/2:
            if self.y1 - 3 - self.close.height()/2 < event.y < self.y1 - 3 + self.close.height()/2:
                c.itemconfig(self.id[-2], image=self.close_press)

    def closeButtonEvent(self, event):
        if self.x2 - 5 - self.close.width()/2 < event.x < self.x2 - 5 + self.close.width()/2:
            if self.y1 - 3 - self.close.height()/2 < event.y < self.y1 - 3 + self.close.height()/2:
                self.destroy()

    def destroy(self):
        """
        Destroys (deletes) virtual window and child modules.
        If the child-id isn't a child, it will raise a exception.
        """

        # Deletes window
        for i in self.id:
            try:
                i.destroy()
            except AttributeError:
                c.delete(i)

        # Deletes title

        # Deletes all childs.
        for i in self.child:
            try:
                c.delete(i)
            except TclError:
                    i.destroy()
                # except TclError:
                #     # If it isn't a Canvas-item.
                #     log.log("Fatal", "Window", "Child isn't a child. Id: " + str(i) + ".")
                # raise ChildProcessError("Child isn't a child. Id: " + str(i) + ".")
        global windowmode
        windowmode = False
        if self.is_store_parent:
            global storemode
            storemode = True

    class Label:
        """
        Label-child for the virtual window.
        """

        def __init__(self, parent, x, y, text="", color="black", font=("Helvetica", 9), anchor=CENTER):
            # Creates label.
            self.id = c.create_text(x, y, text=text, fill=color, font=font, anchor=anchor)

            # Creates label-configuraion variables
            self.__text = text
            self.__color = color
            self.__font = font
            self.__anchor = anchor

            # Creates a child by its parent.
            parent.child.append(self.id)

        def get(self):
            """
            Gets text value of the Label.
            :return:
            """

            # Gets text if the label.
            return c.itemcget(self.id, "text")

        def config(self, text=None, color=None, font=None, anchor=None):
            """
            Configure Label.
            :param text:
            :param color:
            :param font:
            :param anchor:
            """
            if text is None:
                text = self.__text
            if color is None:
                color = self.__color
            if font is None:
                font = self.__font
            if anchor is None:
                anchor = self.__anchor
            c.itemconfig(self.id, text=text, fill=color, font=font, anchor=anchor)
            self.__text = text
            self.__color = color
            self.__font = font
            self.__anchor = anchor

        def destroy(self):
            """
            Destroys Label
            """
            c.delete(self.id)


class Button2(Thread):
    def __init__(self, x, y, parent=None, command=None, text="", anchor=CENTER, font=("Helvetica", 9)):
        super().__init__()
        self.x = x
        self.y = y
        self.button_normal = PhotoImage(file="data/control/button/button-normal.png")
        self.button_pressed = PhotoImage(file="data/control/button/button-active-prelight.png")
        self.button_hover = PhotoImage(file="data/control/button/button-prelight.png")
        log.log("DEBUG", " Button2.__init__", "x="+str(x)+"| y="+str(y)+"| image="+str(self.button_normal))
        self.id = c.create_image(x, y, image=self.button_normal)
        self.command = command
        c.update()
        c.bind("<ButtonPress-1>", self.__press__)
        c.bind("<ButtonRelease-1>", self.__hover__)
        c.bind("<Motion>", self.__hover__)
        if parent:
            if parent == Window:
                parent.child.append(self.id)
        self.start()

    def __press__(self, event):
        if self.x - self.button_normal.width()/2 < event.x < self.x + self.button_normal.width()/2:
            if self.y - self.button_normal.height() / 2 < event.y < self.y + self.button_normal.height() / 2:
                log.log("DEBUG", "Button2.__pressed", "Pressed button.")
                c.itemconfig(self.id, image=self.button_pressed)
                self.command()

    def __hover__(self, event):
        print(event.x, event.y)
        print(self.x, self.y)
        print(self.button_normal.width())
        print(self.button_normal.height())
        print(self.x - self.button_normal.width()/2, self.x + self.button_normal.width()/2)
        print(self.y - self.button_normal.height() / 2, self.y + self.button_normal.height() / 2)
        if self.x - self.button_normal.width()/2 < event.x < self.x + self.button_normal.width()/2:
            if self.y - self.button_normal.height() / 2 < event.y < self.y + self.button_normal.height() / 2:
                c.itemconfig(self.id, image=self.button_hover)
                print("Hover")
            else:
                c.itemconfig(self.id, image=self.button_normal)
        else:
            c.itemconfig(self.id, image=self.button_normal)

    def storemode_destroy(self, w, b, b2, close, storemodeon):
        w()
        b()
        b2()
        close()
        storemodeon()

    def destroy(self):
        c.delete(self.id)


def color_bool(on_off):
    """
    Convert boolean to color.
    :param on_off:
    :return:
    """
    if on_off:
        return "cyan"
    else:
        return "black"


def show_Score(score):
    """
    Shows Score
    :param score:
    :return:
    """
    c.itemconfig(Score_text, text=str(score))


def show_Level(level):
    """
    Shows Level
    :param level:
    :return:
    """
    c.itemconfig(Level_text, text=str(level))


def show_Speed(speed):
    """
    Shows Speed
    :param speed:
    :return:
    """
    c.itemconfig(Speed_text, text=str(speed))


def show_Lives(lives):
    """
    Shows Lives
    :param lives:
    :return:
    """
    c.itemconfig(Lives_text, text=str(lives))


def show_S_Pnt(data):
    """
    Shows score status value
    :param data:
    :return:
    """
    c.itemconfig(S_Pnt_text, text=data)


def show_Secure(on_off):
    """
    shows security-state
    :param on_off:
    :return:
    """
    c.itemconfig(Secure_text, text=on_off)


def show_SlowMo(on_off):
    """
    shows slow motion state
    :param on_off:
    :return:
    """
    c.itemconfig(SlowMo_text, text=on_off)


def show_Confus(on_off):
    """
    shows confusion state
    :param on_off:
    :return:
    """
    c.itemconfig(Confus_text, text=on_off)


def show_TmeBrk(on_off):
    """
    shows timebreak state
    :param on_off:
    :return:
    """
    c.itemconfig(TmeBrk_text, text=on_off)


def show_SpdBst(on_off):
    """
    shows speedboost state
    :param on_off:
    :return:
    """
    c.itemconfig(SpdBst_text, text=on_off)


def show_Paralz(on_off):
    """
    shows paralis state
    :param on_off:
    :return:
    """
    c.itemconfig(Paralz_text, text=on_off)


def show_ShtSpd(integer):
    """
    Shows Shot-speed state
    :param integer:
    :return:
    """
    c.itemconfig(ShtSpd_text, text=integer)


def show_TPs(integer):
    """
    Shows Teleports
    :param integer:
    :return:
    """
    c.itemconfig(ShipTP_text, text=str(integer))


def show_NoTouch(integer):
    """
    Shows Teleports
    :param integer:
    :return:
    """
    c.itemconfig(NoTouch_text, text=str(integer))


def show_Diamond(integer):
    """
    Shows Diamonds
    :param integer:
    :return:
    """
    c.itemconfig(Diamond_text, text=str(integer))


def show_Coin(integer):
    """
    Shows Coins
    """
    c.itemconfig(Coin_text, text=str(integer))


def view_Level(level):
    """
    Viewes level
    """
    c.itemconfig(Level_view, text="Level " + str(level))
    Root.update()
    sleep(2)
    c.itemconfig(Level_view, text="")
    Root.update()


log.log("info", "main", "Game stats viewers created")


def cleanALL():
    """
    Deletes removes bubbles out of the game.
    """
    for i in len(BubID) - 1, -1, -1:
        del_bubble(i)


def Shuffling():
    """
    Shuffles the Bubble-actions.
    This is been used by aa confuse-bubble
    """
    shuffle(BubAct)


def AutoSave():
    """
    Saves the game. (For Auto-Save)
    """
    global StateTime
    global ScoreState
    global SecureState
    global SlowMoState
    global ConfusState
    global TimeBreak
    global Score
    global Level
    global SHIP_SPD
    global MaxBubSpd
    global Lives
    global HiScore
    global LevelScore
    global ShotSpeed
    global TP
    global Diamond
    global Coins
    global NoTouchTime
    global NoTouch
    global NoTouchS
    f = open("saves/" + SaveName + "/state/score.data", "w")
    f.write(str(ScoreState))
    f.close()
    f = open("saves/" + SaveName + "/state/scoretime.data", "w")
    if not pause:
        f.write(str(ScoreStateTime - time()))
    else:
        f.write(str(ScoreStateS))
    f.close()
    f = open("saves/" + SaveName + "/state/securetime.data", "w")
    if not pause:
        f.write(str(SecureStateTime - time()))
    else:
        f.write(str(SecureStateS))
    f.close()
    f = open("saves/" + SaveName + "/state/secure.data", "w")
    f.write(str(SecureState))
    f.close()
    f = open("saves/" + SaveName + "/state/slowmotime.data", "w")
    if not pause:
        f.write(str(SlowMoStateTime - time()))
    else:
        f.write(str(SlowMoStateS))
    f.close()
    f = open("saves/" + SaveName + "/state/slowmo.data", "w")
    f.write(str(SlowMoState))
    f.close()
    f = open("saves/" + SaveName + "/state/confusion.data", "w")
    if not pause:
        f.write(str(ConfusStateTime - time()))
    else:
        f.write(str(ConfusStateS))
    f.close()
    f = open("saves/" + SaveName + "/state/confusion.data", "w")
    f.write(str(ConfusState))
    f.close()
    f = open("saves/" + SaveName + "/state/timebreaktime.data", "w")
    if not pause:
        f.write(str(TimeBreakTime - time()))
    else:
        f.write(str(TimeBreakS))
    f.close()
    f = open("saves/" + SaveName + "/state/timebreak.data", "w")
    f.write(str(TimeBreak))
    f.close()
    f = open("saves/" + SaveName + "/state/shipspeed.data", "w")
    f.write(str(SHIP_SPD))
    f.close()
    f = open("saves/" + SaveName + "/state/bubspeed.data", "w")
    f.write(str(int(MaxBubSpd)))
    f.close()
    f = open("saves/" + SaveName + "/game/hiscore.data", "w")
    f.write(str(HiScore))
    f.close()
    f = open("saves/" + SaveName + "/game/lives.data", "w")
    f.write(str(Lives))
    f.close()
    f = open("saves/" + SaveName + "/game/score.data", "w")
    f.write(str(Score))
    f.close()
    f = open("saves/" + SaveName + "/game/level.data", "w")
    f.write(str(Level))
    f.close()
    f = open("saves/" + SaveName + "/game/levelscore.data", "w")
    f.write(str(LevelScore))
    f.close()
    f = open("saves/" + SaveName + "/state/shotspeed.data", "w")
    f.write(str(ShotSpeed))
    f.close()
    f = open("saves/" + SaveName + "/state/timebreaktime.data", "w")
    if not pause:
        f.write(str(ShotSpeedTime - time()))
    else:
        f.write(str(ShotSpeedS))
    f.close()
    f = open("saves/" + SaveName + "/state/notouch.data", "w")
    f.write(str(NoTouch))
    f.close()
    f = open("saves/" + SaveName + "/state/notouchtime.data", "w")
    if not pause:
        f.write(str(NoTouchTime - time()))
    else:
        f.write(str(NoTouchS))
    f.close()
    f = open("saves/" + SaveName + "/game/BubAct.data", "wb")
    dump(BubAct, f)
    f.close()
    f = open("saves/" + SaveName + "/game/BubRad.data", "wb")
    dump(BubRad, f)
    f.close()
    f = open("saves/" + SaveName + "/game/BubSpd.data", "wb")
    dump(BubSpd, f)
    f.close()
    f = open("saves/" + SaveName + "/game/BubPos.data", "wb")
    dump(BubPos, f)
    f.close()
    f = open("saves/" + SaveName + "/game/Teleports.data", "w")
    f.write(str(TP))
    f.close()
    f = open("saves/" + SaveName + "/game/Diamond.data", "w")
    f.write(str(Diamond))
    f.close()
    f = open("saves/" + SaveName + "/game/Coins.data", "w")
    f.write(str(Coins))
    f.close()


def AutoRestore():
    """
    Restoring. (For Auto-Restore)
    """
    global StateTime
    global ScoreState
    global SecureState
    global SlowMoState
    global ConfusState
    global TimeBreak
    global Score
    global Level
    global SHIP_SPD
    global MaxBubSpd
    global Lives
    global HiScore
    global LevelScore
    global ShotSpeed
    global TP
    global Diamond
    global Coins
    global TimeBreakTime
    global ConfusStateTime
    global SlowMoStateTime
    global SecureStateTime
    global ScoreStateTime
    global ShotSpeedTime
    global NoTouch
    global NoTouchTime
    f = open("saves/" + SaveName + "/state/score.data", "r")
    ScoreState = int(f.read(3))
    f.close()
    f = open("saves/" + SaveName + "/state/scoretime.data", "r")
    ScoreStateTime = float(f.read(3)) + time()
    f.close()
    f = open("saves/" + SaveName + "/state/secure.data", "r")
    SecureState = bool(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/securetime.data", "r")
    SecureStateTime = float(f.read(10)) + time()
    f.close()
    f = open("saves/" + SaveName + "/state/slowmo.data", "r")
    SlowMoState = bool(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/slowmotime.data", "r")
    SlowMoStateTime = float(f.read(10)) + time()
    f.close()
    f = open("saves/" + SaveName + "/state/confusion.data", "r")
    ConfusState = bool(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/confusiontime.data", "r")
    ConfusStateTime = float(f.read(10)) + time()
    f.close()
    f = open("saves/" + SaveName + "/state/timebreaktime.data", "r")
    TimeBreakTime = float(f.read(10)) + time()
    f.close()
    f = open("saves/" + SaveName + "/state/timebreak.data", "r")
    TimeBreak = bool(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/shipspeed.data", "r")
    SHIP_SPD = int(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/time.data", "r")
    StateTime = float(f.read(30)) + time()
    f.close()
    f = open("saves/" + SaveName + "/game/hiscore.data", "r")
    HiScore = int(f.read(30))
    f.close()
    f = open("saves/" + SaveName + "/game/lives.data", "r")
    Lives = int(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/game/score.data", "r")
    Score = int(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/game/level.data", "r")
    Level = int(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/bubspeed.data", "r")
    MaxBubSpd = float(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/shotspeed.data", "r")
    ShotSpeed = int(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/shotspeedtime.data", "r")
    ShotSpeedTime = int(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/notouch.data", "r")
    NoTouch = bool(f.read(10))
    f.close()
    f = open("saves/" + SaveName + "/state/notouchtime.data", "r")
    NoTouchTime = float(f.read(10))
    f.close()
    TP = load_data_int("saves/" + SaveName + "/game/Teleports.data", 0)
    Diamond = load_data_int("saves/" + SaveName + "/game/Diamond.data", 0)
    Coins = load_data_int("saves/" + SaveName + "/game/Coins.data", 0)


def Reset():
    """
    Resets the game fully
    """
    global StateTime
    global ScoreState
    global SecureState
    global SlowMoState
    global ConfusState
    global TimeBreak
    global Score
    global Level
    global SHIP_SPD
    global MaxBubSpd
    global Lives
    global HiScore
    global LevelScore
    global BubID
    global BubAct
    global BubSpd
    global BubRad
    global MinBubRad
    global MaxBubRad
    global ScreenGap
    global end
    global BubChance
    global SpdBoost
    global Paralized
    global Action
    global pause
    global TP
    global Diamond
    global Coins
    global TimeLimit
    # ShipSettings
    SHIP_SPD = load_data_int("data/ShipSpeed.cfg", 10)
    # Bubble Settings
    BubAct = list()
    BubID = list()
    BubRad = list()
    BubSpd = list()
    MinBubRad = load_data_int("data/BubMinRadius.cfg", 10)
    MaxBubRad = load_data_int("data/BubMaxRadius.cfg", 30)
    MaxBubSpd = load_data_int("data/BubMaxSpeed.cfg", 5)
    ScreenGap = load_data_int("data/BubScreenGap.cfg", 100)

    # Game Settings
    BubChance = load_data_int("data/BubChance.cfg", 10)
    TimeLimit = load_data_int("data/GameTimeLimit.cfg", 30)
    LevelScore = load_data_int("data/GameLevelScore.cfg", 3000)

    # Game setup
    Score = load_data_int("data/GameResetScore.cfg", 0)
    Level = load_data_int("data/GameResetLevel.cfg", 1)
    Lives = load_data_int("data/GameResetLives.cfg", 7)
    TP = load_data_int("data/GameResetTeleports.cfg", 0)
    end = time() + TimeLimit

    # Reset State
    ScoreState = load_data_int("data/StateResetScore.cfg", 1)
    SecureState = load_data_bool("data/StateResetSecure.cfg", False)
    SlowMoState = load_data_bool("data/StateResetSlowMotion.cfg", False)
    ConfusState = load_data_bool("data/StateResetConfusion.cfg", False)
    TimeBreak = load_data_bool("data/StateResetTimeBreak.cfg", False)
    SpdBoost = load_data_bool("data/StateResetSpeedBoost.cfg", False)
    Paralized = load_data_bool("data/StateResetParalized.cfg", False)
    StateTime = load_data_int("data/StateResetTime.cfg", 0)
    Action = load_data_str("data/StateResetAction.cfg")
    pause = load_data_bool("data/Pause.cfg", False)
    TP = load_data_int("data/GameResetTeleport.cfg", 0)
    Diamond = 0
    Coins = 0

    f = open("saves/" + SaveName + "/game/BubAct.data", "wb+")
    dump([], f)
    f.close()
    f = open("saves/" + SaveName + "/game/BubRad.data", "wb+")
    dump([], f)
    f.close()
    f = open("saves/" + SaveName + "/game/BubSpd.data", "wb+")
    dump([], f)
    f.close()
    f = open("saves/" + SaveName + "/game/BubPos.data", "wb+")
    dump([], f)
    f.close()

    # Reset Save
    AutoSave()


def show_info():
    """
    Shows all information:
    Score, Level, status-time etc.
    :return:
    """
    global Score
    global Level
    global ScoreState
    global SecureState
    global TimeBreak
    global ConfusState
    global SpdBoost
    global Paralized
    global ShotSpeed
    global ScoreStateTime
    global SecureStateTime
    global SlowMoStateTime
    global TimeBreakTime
    global ConfusStateTime
    global SpdBoostTime
    global ParalizedTime
    global ShotSpeedTime
    global SpdBoostTime
    global HiScore
    global NoTouch
    global NoTouchTime
    show_Score(Score)
    show_Level(Level)
    show_Speed(SHIP_SPD)
    show_Lives(Lives)
    show_S_Pnt(str(int(ScoreStateTime - time())))
    show_Secure(str(int(SecureStateTime - time())))
    show_SlowMo(str(int(SlowMoStateTime - time())))
    show_Confus(str(int(ConfusStateTime - time())))
    show_TmeBrk(str(int(TimeBreakTime - time())))
    show_SpdBst(str(int(SpdBoostTime - time())))
    show_Paralz(str(int(ParalizedTime - time())))
    show_ShtSpd(str(int(ShotSpeedTime - time())))
    show_NoTouch(str(int(NoTouchTime - time())))
    show_TPs(TP)
    show_Diamond(Diamond)
    show_Coin(Coins)

def refresh():
    global Root, FG, GLOSS, GameFG, GameFG_gloss

def refresh_state():
    global ScoreState, SecureState, SlowMoState, ConfusState, Paralized, NoTouch, TimeBreak, ShotSpeed, ShotSpeedTime
    global ScoreStateTime, SecureStateTime, SlowMoStateTime, ConfusStateTime, ParalizedTime, NoTouchTime, TimeBreakTime
    global SpdBoost, SpdBoostTime, HiScore, Score

    if SlowMoState:
        sleep(0.5)
    if ScoreStateTime <= time():
        ScoreState = 1
        ScoreStateTime = time()
    if SecureStateTime <= time():
        SecureState = False
        SecureStateTime = time()
    if SlowMoStateTime <= time():
        SlowMoState = False
        SlowMoStateTime = time()
    if TimeBreakTime <= time():
        TimeBreak = False
        TimeBreakTime = time()
    if ConfusStateTime <= time():
        ConfusState = False
        ConfusStateTime = time()
    if SpdBoostTime <= time():
        SpdBoost = False
        SpdBoostTime = time()
    if ParalizedTime <= time():
        Paralized = False
        ParalizedTime = time()
    if NoTouchTime <= time():
        NoTouch = False
        NoTouchTime = time()
    if ShotSpeedTime <= time():
        ShotSpeed = 15
        ShotSpeedTime = time()
    if Score < 0:
        log.log("error", "main", "The score var under zero.")
    if Score > HiScore:
        HiScore = Score
    if ConfusState and not SecureState:
        Shuffling()

class CheatEngine:
    def __init__(self):
        self.text = ""


    def EventHandler(self, event):
        global pause
        global S
        global StateTime
        global ScoreStateS
        global ScoreStateTime
        global SecureStateS
        global SecureStateTime
        global TimeBreakS
        global TimeBreakTime
        global ConfusStateS
        global ConfusStateTime
        global SlowMoStateS
        global SlowMoStateTime
        global ParalizedS
        global ParalizedTime
        global ShotSpeedS
        global ShotSpeedTime
        global KeyActive
        global NoTouchS
        global NoTouchTime
        global cheatmode
        pause = True
        cheatmode = True
        ScoreStateS = ScoreStateTime - time()
        SecureStateS = SecureStateTime - time()
        TimeBreakS = TimeBreakTime - time()
        ConfusStateS = ConfusStateTime - time()
        SlowMoStateS = SlowMoStateTime - time()
        ParalizedS = ParalizedTime - time()
        ShotSpeedS = ShotSpeedTime - time()
        NoTouchS = NoTouchTime - time()
        self.text = ""
        self.text_id = c.create_text(10, HEIGHT-100, text="> ", font=("Helvetica", 24), anchor=SW)
        self.a = c.bind("<Key>", self.InputEventHandler)
        # c.bind_all("<Return>", self.ExecuteEventHandler)

    def Close(self):
        c.delete(self.text_id)
        global cheatmode
        global pause
        global S
        global StateTime
        global ScoreStateS
        global ScoreStateTime
        global SecureStateS
        global SecureStateTime
        global TimeBreakS
        global TimeBreakTime
        global ConfusStateS
        global ConfusStateTime
        global SlowMoStateS
        global SlowMoStateTime
        global ParalizedS
        global ParalizedTime
        global ShotSpeedS
        global ShotSpeedTime
        global KeyActive
        global NoTouchS
        global NoTouchTime
        pause = False
        cheatmode = False
        ScoreStateTime = ScoreStateS + time()
        SecureStateTime = SecureStateS + time()
        TimeBreakTime = TimeBreakS + time()
        ConfusStateTime = ConfusStateS + time()
        SlowMoStateTime = SlowMoStateS + time()
        ParalizedTime = ParalizedS + time()
        ShotSpeedTime = ShotSpeedS + time()
        NoTouchTime = NoTouchS + time()

    def InputEventHandler(self, event):
        if event.keysym == "BackSpace":
            self.text = self.text[0:-1]
        if event.keysym == "space":
            self.text += " "
        if len(event.char) > 0:
            if 127 > ord(event.char) > 32:
                self.text += event.char
        if event.keysym == "Return":
            self.ExecuteEventHandler(event)
        print(event.char)
        c.itemconfig(self.text_id, text="> "+self.text)
        c.update()

    def AddLevelKey(self, params):
        if len(params) == 1:
            if params[0].isnumeric():
                if not "." in params[0]:
                    a = int(params[0])
                    if 0 <= a < 10:
                        for i in range(0, a):
                            create_bubble(-1)

    def CleanAllBubbles(self, params):
        pass

    def AddBubble(self, params):
        act = ["Double", "Kill", "Triple", "Normal", "SpeedDown", "SpeedUp", "Up", "Ultimate", "Teleporter",
               "SlowMotion", "HyperMode", "Protect", "ShotSpdStat", "TimeBreak", "DoubleState", "Confusion", "Paralis",
               "StoneBub", "NoTouch", "Coin", "Diamond"]
        if 2 >= len(params) >= 1:
            if params[0] in act:
                p = params[0]
                if p == "Normal":
                    i = 0
                elif p == "Double":
                    i = 800
                elif p == "Kill":
                    i = 830
                elif p == "Triple":
                    i = 930
                elif p == "SpeedUp":
                    i = 940
                elif p == "SpeedDown":
                    i = 950
                elif p == "Up":
                    i = -2
                elif p == "Ultimate":
                    i = 973
                elif p == "DoubleState":
                    i = 974
                elif p == "Protect":
                    i = 979
                elif p == "SlowMotion":
                    i = 981
                elif p == "TimeBreak":
                    i = 984
                elif p == "HyperMode":
                    i = 1100
                elif p == "ShotSpdStat":
                    i = 1101
                elif p == "Confusion":
                    i = 985
                elif p == "Paralis":
                    i = 1085
                elif p == "Teleporter":
                    i = 1120
                elif p == "Diamond":
                    i = 1121
                elif p == "Coin":
                    i = 1124
                elif p == "NoTouch":
                    i = 1130
            if len(params) == 2:
                p = params[1]
            else:
                p = "1"
            if p.isnumeric():
                if i:
                    for _ in range(int(float(p))):
                        create_bubble(float(i))
        if len(params) == 5:

            if params[0] in act:
                p = params[0]
                if p == "Normal":
                    i = 0
                elif p == "Double":
                    i = 800
                elif p == "Kill":
                    i = 830
                elif p == "Triple":
                    i = 930
                elif p == "SpeedUp":
                    i = 940
                elif p == "SpeedDown":
                    i = 950
                elif p == "Up":
                    i = -2
                elif p == "Ultimate":
                    i = 973
                elif p == "DoubleState":
                    i = 974
                elif p == "Protect":
                    i = 979
                elif p == "SlowMotion":
                    i = 981
                elif p == "TimeBreak":
                    i = 984
                elif p == "HyperMode":
                    i = 1100
                elif p == "ShotSpdStat":
                    i = 1101
                elif p == "Confusion":
                    i = 985
                elif p == "Paralis":
                    i = 1085
                elif p == "Teleporter":
                    i = 1120
                elif p == "Diamond":
                    i = 1121
                elif p == "Coin":
                    i = 1124
                elif p == "NoTouch":
                    i = 1130
            if params[1].isnumeric() and params[2].isnumeric() and params[3].isnumeric() and params[4].isnumeric():
                if i:
                    for _ in range(int(float(params[1]))):
                        create_bubble(i, float(params[2]), float(params[3]), float(params[4]))
    def AddLives(self, params):
        global Lives
        if len(params) == 1:
            if params[0].isnumeric():
                Lives += int(float(params[0]))

    def AddState(self, params):
        if len(params) == 1:
            State.set_state(params[0])

    def ExecuteEventHandler(self, event):
        cmdAndParamList = self.text.split(sep=" ")
        Command = cmdAndParamList[0]
        Params = cmdAndParamList[1:]
        print(Command)
        print(Params)
        if Command == "/AddLevelKey":
            self.AddLevelKey(params=Params)
        elif Command == "/CleanAllBubbles":
            cleanALL()
        elif Command == "/AddBubble":
            self.AddBubble(Params)
        elif Command == "/AddLives":
            self.AddLives(Params)
        else:
            pass
        self.Close()


class Game:
    """
    Main Game class.
    """

    def __init__(self):
        global ReturnMain
        ReturnMain = False
        """
        Saves loader engine
        Todo: Create panel, in darkcyan with flat relief
        """
        global c
        global Root
        Root = Tk()
        Root.title('Bubble Blaster 5')
        button["Normal"] = PhotoImage(file="data/control/button/button-normal.png")
        button["Hover"] = PhotoImage(file="data/control/button/button-prelight.png")
        button["Pressed"] = PhotoImage(file="data/control/button/button-active-prelight.png")
        bb_logo = PhotoImage(file="data/BB_logo.png")
        Root.wm_iconphoto(True, bb_logo)
        Root.wm_iconify()
        c = Canvas(Root, width=WIDTH, height=HEIGHT, bg='darkcyan')
        c.pack()
        self.mframe = Frame(Root, height=HEIGHT - 100, width=WIDTH - 240, bd=0, relief=FLAT, bg="#003f3f")
        self.mframe.place(x=MID_X, y=MID_Y, anchor=CENTER)
        self.scroll = Scrollbar(self.mframe, relief=FLAT, bg="Black")
        self.scroll.pack(side=RIGHT, fill=Y)
        self.frame = Frame(self.mframe, height=HEIGHT - 100, width=WIDTH - 240, bd=0, relief=FLAT, bg="#003f3f")
        self.frame.pack()
        self.canvas = Canvas(self.frame, width=WIDTH - 220, height=HEIGHT - 100, yscrollcommand=self.scroll.set, bd=0,
                             bg='#003f3f', relief=FLAT)
        self.canvas.pack()
        self.scroll.config(command=self.canvas.yview)

        list_saves_dir = os.listdir("saves")
        j = 20
        k = 0
        self.SavesID = []
        self.ButtonID = []
        b = []
        self.d = []
        a = [self.canvas.create_rectangle(200, j, WIDTH - 220 - 200, j + 99, outline="cyan")]
        if "icon.png" in os.listdir("saves/" + list_saves_dir[0]):
            pass
        else:
            b.append(PhotoImage(file="data/NoImage.png"))
            a.append(self.canvas.create_image(202, j + 2, image=b[-1], anchor=NW))
        a.append(
            self.canvas.create_text(310, j + 15, text=list_saves_dir[0], font=("helvetica", 22, "bold"), fill="white",
                                    anchor=W))
        self.ButtonID.append(Button(self.frame, text="Open", relief=FLAT, bd=0,
                                    command=lambda: self.opengame(list_saves_dir[0]), bg="#007f7f", fg="white",
                                    height=2, width=7, anchor=CENTER))
        self.ButtonID[0].place(x=WIDTH - 220 - 201, y=j + 98, anchor=SE)
        self.ButtonID.append(Button(self.frame, text="Rename", relief=FLAT, bd=0,
                                    command=lambda: self.renamgame(list_saves_dir[0], len(self.SavesID) - 1),
                                    bg="#007f7f", fg="white", height=2, width=7, anchor=CENTER))
        self.ButtonID[0].place(x=WIDTH - 220 - 263, y=j + 98, anchor=SE)
        self.SavesID.append(a)
        import time
        self.canvas.create_text(310, j + 75, text=time.strftime("%e %b. %G, %R", time.struct_time(
            time.localtime(os.stat("saves/" + list_saves_dir[0]).st_ctime))), anchor=W, fill="white")
        self.TextboxID = None
        j += 99
        k += 1
        a = [self.canvas.create_rectangle(200, j, WIDTH - 220 - 200, j + 99, outline="cyan")]
        if "icon.png" in os.listdir("saves/" + list_saves_dir[1]):
            pass
        else:
            b.append(PhotoImage(file="data/NoImage.png"))
            a.append(self.canvas.create_image(202, j + 2, image=b[-1], anchor=NW))
        a.append(
            self.canvas.create_text(310, j + 15, text=list_saves_dir[1], font=("helvetica", 22, "bold"), fill="white",
                                    anchor=W))
        self.ButtonID.append(Button(self.frame, text="Open", relief=FLAT, bd=0,
                                    command=lambda: self.opengame(list_saves_dir[1]), bg="#007f7f", fg="white",
                                    height=2, width=7, anchor=CENTER))
        self.ButtonID[1].place(x=WIDTH - 220 - 201, y=j + 98, anchor=SE)
        self.ButtonID.append(Button(self.frame, text="Rename", relief=FLAT, bd=0,
                                    command=lambda: self.renamgame(list_saves_dir[1], len(self.SavesID) - 1),
                                    bg="#007f7f", fg="white", height=2, width=7, anchor=CENTER))
        self.ButtonID[1].place(x=WIDTH - 220 - 263, y=j + 98, anchor=SE)
        self.SavesID.append(a)
        self.canvas.create_text(310, j + 75, text=time.strftime("%e %b. %G, %R", time.struct_time(
            time.localtime(os.stat("saves/" + list_saves_dir[1]).st_ctime))), anchor=W, fill="white")
        self.TextboxID = None
        j += 99
        k += 1
        a = [self.canvas.create_rectangle(200, j, WIDTH - 220 - 200, j + 99, outline="cyan")]
        if "icon.png" in os.listdir("saves/" + list_saves_dir[2]):
            pass
        else:
            b.append(PhotoImage(file="data/NoImage.png"))
            a.append(self.canvas.create_image(202, j + 2, image=b[-1], anchor=NW))
        a.append(
            self.canvas.create_text(310, j + 15, text=list_saves_dir[2], font=("helvetica", 22, "bold"), fill="white",
                                    anchor=W))
        self.ButtonID.append(Button(self.frame, text="Open", relief=FLAT, bd=0,
                                    command=lambda: self.opengame(list_saves_dir[2]), bg="#007f7f", fg="white",
                                    height=2, width=7, anchor=CENTER))
        self.ButtonID[2].place(x=WIDTH - 220 - 201, y=j + 98, anchor=SE)
        self.ButtonID.append(Button(self.frame, text="Rename", relief=FLAT, bd=0,
                                    command=lambda: self.renamgame(list_saves_dir[2], len(self.SavesID) - 1),
                                    bg="#007f7f", fg="white", height=2, width=7, anchor=CENTER))
        self.ButtonID[2].place(x=WIDTH - 220 - 263, y=j + 98, anchor=SE)
        self.SavesID.append(a)
        self.canvas.create_text(310, j + 75, text=time.strftime("%e %b. %G, %R", time.struct_time(
            time.localtime(os.stat("saves/" + list_saves_dir[2]).st_ctime))), anchor=W, fill="white")
        self.TextboxID = None
        j += 99
        k += 1
        a = [self.canvas.create_rectangle(200, j, WIDTH - 220 - 200, j + 99, outline="cyan")]
        if "icon.png" in os.listdir("saves/" + list_saves_dir[3]):
            pass
        else:
            b.append(PhotoImage(file="data/NoImage.png"))
            a.append(self.canvas.create_image(202, j + 2, image=b[-1], anchor=NW))
        a.append(
            self.canvas.create_text(310, j + 15, text=list_saves_dir[3], font=("helvetica", 22, "bold"), fill="white",
                                    anchor=W))
        self.ButtonID.append(Button(self.frame, text="Open", relief=FLAT, bd=0,
                                    command=lambda: self.opengame(list_saves_dir[3]), bg="#007f7f", fg="white",
                                    height=2, width=7, anchor=CENTER))
        self.ButtonID[3].place(x=WIDTH - 220 - 201, y=j + 98, anchor=SE)
        self.ButtonID.append(Button(self.frame, text="Rename", relief=FLAT, bd=0,
                                    command=lambda: self.renamgame(list_saves_dir[3], len(self.SavesID) - 1),
                                    bg="#007f7f", fg="white", height=2, width=7, anchor=CENTER))
        self.ButtonID[3].place(x=WIDTH - 220 - 263, y=j + 98, anchor=SE)
        self.SavesID.append(a)
        self.canvas.create_text(310, j + 75, text=time.strftime("%e %b. %G, %R", time.struct_time(
            time.localtime(os.stat("saves/" + list_saves_dir[3]).st_ctime))), anchor=W, fill="white")
        self.TextboxID = None
        j += 99
        k += 1
        a = [self.canvas.create_rectangle(200, j, WIDTH - 220 - 200, j + 99, outline="cyan")]
        if "icon.png" in os.listdir("saves/" + list_saves_dir[4]):
            pass
        else:
            b.append(PhotoImage(file="data/NoImage.png"))
            a.append(self.canvas.create_image(202, j + 2, image=b[-1], anchor=NW))
        import time
        a.append(
            self.canvas.create_text(310, j + 15, text=list_saves_dir[4], font=("helvetica", 22, "bold"), fill="white",
                                    anchor=W))
        self.ButtonID.append(Button(self.frame, text="Open", relief=FLAT, bd=0,
                                    command=lambda: self.opengame(list_saves_dir[4]), bg="#007f7f", fg="white",
                                    height=2, width=7, anchor=CENTER))
        self.ButtonID[4].place(x=WIDTH - 220 - 201, y=j + 98, anchor=SE)
        self.ButtonID.append(Button(self.frame, text="Rename", relief=FLAT, bd=0,
                                    command=lambda: self.renamgame(list_saves_dir[4], len(self.SavesID) - 1),
                                    bg="#007f7f", fg="white", height=2, width=7, anchor=CENTER))
        self.ButtonID[4].place(x=WIDTH - 220 - 263, y=j + 98, anchor=SE)
        self.SavesID.append(a)
        self.canvas.create_text(310, j + 75, text=time.strftime("%e %b. %G, %R", time.struct_time(

            time.localtime(os.stat("saves/" + list_saves_dir[4]).st_ctime))), anchor=W, fill="white")
        self.TextboxID = None
        j += 99
        k += 1
        # print(len(self.ButtonID))
        self.i = None
        Root.wm_deiconify()
        Root.mainloop()
        # self.game()

    def opengame(self, i):
        """
        Opens the game
        :param i:
        :return:
        """
        self.mframe.destroy()
        self.i = i
        self.game()

    def rename(self):
        """
        Renaming the game.
        """
        os.renames("saves/" + self.i[0], "saves/" + self.TextboxID.get())
        self.canvas.itemconfig(self.SavesID[self.i[1]][2], text=self.TextboxID.get())
        self.TextboxID.destroy()

    def renamgame(self, i, index):
        """
        renaming a game
        :param i:
        :param index:
        :return:
        """
        self.TextboxID = Entry(self.frame, relief=FLAT, bd=4, bg="#007f7f", fg="white")
        self.TextboxID.pack(side=BOTTOM, fill=X)
        self.TextboxID.bind("<Return>", self.rename)
        self.i = [i, index]
        self.TextboxID.focus_set()

    def game(self):
        """
        Main Game.
        :return:
        """
        global Root, Dmd, c, DmdBub, Key, StoreIcon, LineBG, PresBG, Circle, PrIcon, Str, StrFG, StoreCoin, BubCoin
        global PauseIcon, SlowMoIcon, Score_text, Level_text, Level_view, LevelScore, Score, SecureStateTime
        global SecureState, Paralized, ParalizedTime, Speed_text, SpdBoostTime, SpdBoost, SpdBst_text, ConfusStateTime
        global ConfusState, Confus_text, Lives, Lives_text, SlowMoStateTime, SlowMoState, SlowMo_text, Secure_text
        global TmeBrk_text, TimeBreakTime, TimeBreak, TimeLimit, Paralz_text, S_Pnt_text, Diamond, Coins, Diamond_text
        global Coin_text, ShotSpeed, ShtSpd_text, ship_id, ship_id2, NoTouch, NoTouchTime, NoTouch_text, ShipTP_text
        global TP, pause_text, pause_icon, BubID, BubPos, BubRad, BubSpd, BubAct, BubChance, BubCoin, ShotDmge, DmdBub
        global HiScore, StateTime, ScoreState, ScoreStateTime, ShotSpeedTime, ShotSpeed, ShotID, ShotPos
        global ShotRad, ShotSpd, new, time1, MinBubRad, MaxBubRad, MaxBubSpd, Level, pause, KeyActive, kzl
        global ScreenGap, end, Action, S, SHIP_SPD, SaveName, ReturnMain, FG, GLOSS, GameFG, GameFG_Gloss, bub

        SaveName = self.i

        bub["Triple"] = dict()
        bub["Double"] = dict()
        bub["Kill"] = dict()
        bub["SpeedUp"] = dict()
        bub["SpeedDown"] = dict()
        bub["Ultimate"] = dict()
        bub["Up"] = dict()
        bub["Teleporter"] = dict()
        bub["SlowMotion"] = dict()
        bub["DoubleState"] = dict()
        bub["Protect"] = dict()
        bub["ShotSpdStat"] = dict()
        bub["HyperMode"] = dict()
        bub["TimeBreak"] = dict()
        bub["Confusion"] = dict()
        bub["Paralis"] = dict()
        bub["StoneBub"] = dict()
        bub["NoTouch"] = dict()
        for i in range(9, 61):
            bub["Normal"][i] = PhotoImage(file="data/bubbles/Normal/" + str(i) + "px.png")
            bub["Triple"][i] = PhotoImage(file="data/bubbles/Triple/" + str(i) + "px.png")
            bub["Double"][i] = PhotoImage(file="data/bubbles/Double/" + str(i) + "px.png")
            bub["SpeedDown"][i] = PhotoImage(file="data/bubbles/SpeedDown/" + str(i) + "px.png")
            bub["SpeedUp"][i] = PhotoImage(file="data/bubbles/SpeedUp/" + str(i) + "px.png")
            bub["Up"][i] = PhotoImage(file="data/bubbles/Up/" + str(i) + "px.png")
            bub["Ultimate"][i] = PhotoImage(file="data/bubbles/Ultimate/" + str(i) + "px.png")
            bub["Kill"][i] = PhotoImage(file="data/bubbles/Kill/" + str(i) + "px.png")
            bub["Teleporter"][i] = PhotoImage(file="data/bubbles/Teleporter/" + str(i) + "px.png")
            bub["SlowMotion"][i] = PhotoImage(file="data/bubbles/SlowMotion/" + str(i) + "px.png")
            bub["DoubleState"][i] = PhotoImage(file="data/bubbles/DoubleState/" + str(i) + "px.png")
            bub["Protect"][i] = PhotoImage(file="data/bubbles/Protect/" + str(i) + "px.png")
            bub["ShotSpdStat"][i] = PhotoImage(file="data/bubbles/ShotSpdStat/" + str(i) + "px.png")
            bub["HyperMode"][i] = PhotoImage(file="data/bubbles/HyperMode/" + str(i) + "px.png")
            bub["TimeBreak"][i] = PhotoImage(file="data/bubbles/TimeBreak/" + str(i) + "px.png")
            bub["Confusion"][i] = PhotoImage(file="data/bubbles/Confusion/" + str(i) + "px.png")
            bub["Paralis"][i] = PhotoImage(file="data/bubbles/Paralis/" + str(i) + "px.png")
            bub["StoneBub"][i] = PhotoImage(file="data/bubbles/StoneBub/" + str(i) + "px.png")
            bub["NoTouch"][i] = PhotoImage(file="data/bubbles/NoTouch/" + str(i) + "px.png")
        ship = PhotoImage(file="data/Ship.png")

        AutoRestore()

        Coll = Collision()

        log.log("info", "main", "Save, restore and reset methods created")

        fi = open("saves/" + SaveName + "/game/lives.data", "r")
        dat = int(fi.read(10))
        fi.close()

        log.log("info", "tkinter", "Window and canvas created")
        log.log("debug", "tkinter", PhotoImage.__doc__)
        bg = PhotoImage(file="data/BackGround.png")
        Dmd = PhotoImage(file="data/Diamond.png")
        DmdBub = PhotoImage(file="data/DiamondBub.png")
        Key = PhotoImage(file="data/Key.png")
        StoreIcon = list()
        StoreIcon.append(PhotoImage(file="data/Images/StoreItems/Key.png"))
        StoreIcon.append(PhotoImage(file="data/Images/StoreItems/Teleport.png"))
        StoreIcon.append(PhotoImage(file="data/Images/StoreItems/Shield.png"))
        StoreIcon.append(PhotoImage(file="data/Images/StoreItems/DiamondBuy.png"))
        StoreIcon.append(PhotoImage(file="data/Images/StoreItems/BuyACake.png"))
        StoreIcon.append(PhotoImage(file="data/Images/StoreItems/Pop_3_bubs.png"))
        LineBG = PhotoImage(file="data/LineIcon.png")
        PresBG = PhotoImage(file="data/EventBackground.png")
        Circle = PhotoImage(file="data/Circle.png")
        PrIcon = PhotoImage(file="data/Present.png")
        Str = PhotoImage(file="data/StoreBG.png")
        StrFG = PhotoImage(file="data/FG.png")
        StoreCoin = PhotoImage(file="data/Coin.png")
        BubCoin = PhotoImage(file="data/CoinBub.png")
        PauseIcon = PhotoImage(file="data/PauseIcon.png")
        SlowMoIcon = PhotoImage(file="data/SlowMotionIcon.png")

        GameBG = PhotoImage(file="data/Images/Backgrounds/GameBG.png")
        GameFG = PhotoImage(file="data/Images/Foregrounds/GameFG.png")
        GameFG_Gloss = PhotoImage(file="data/Images/Foregrounds/Glossy.png")

        c.create_image(0, 0, anchor=NW, image=GameBG)

        # Sounds
        # mixer.init()
        # pop = mixer.Sound("bubpop")

        log.log("debug", "tkinter", "Background=" + str(bg))
        # c.create_image(MID_X, MID_Y, image=bg)
        ship_id = c.create_polygon(0, 0, 0, 0, 0, 0, outline=None)
        ship_id2 = c.create_image(7.5, 7.5, image=ship)

        c.move(ship_id, MID_X, MID_Y)
        c.move(ship_id2, MID_X, MID_Y)


        #c.create_rectangle(0, 0, WIDTH, 69, fill="#003f3f")
        #c.create_rectangle(0, HEIGHT, WIDTH, HEIGHT - 102, fill="#003f3f")

        c.create_text(55, 30, text='Score', fill='orange')
        c.create_text(110, 30, text='Level', fill='orange')
        c.create_text(165, 30, text='Speed', fill='orange')
        c.create_text(220, 30, text='Lives', fill='orange')
        c.create_text(330, 30, text="Stat Score", fill="gold")
        c.create_text(400, 30, text="Protection", fill="gold")
        c.create_text(490, 30, text="Slowmotion", fill="gold")
        c.create_text(580, 30, text="Confusion", fill="gold")
        c.create_text(670, 30, text="Time Break", fill="gold")
        c.create_text(760, 30, text="Spd. Boost", fill="gold")
        c.create_text(850, 30, text="Paralizing", fill="gold")
        c.create_text(940, 30, text="Shot spd. time", fill="gold")
        c.create_text(1030, 30, text="No-touch time", fill="gold")
        c.create_text(1120, 30, text='Teleports', fill='gold')
        c.create_image(1185, 30, image=Dmd)
        c.create_image(1185, 50, image=StoreCoin)
        Score_text = c.create_text(55, 50, fill='cyan')
        Level_text = c.create_text(110, 50, fill='cyan')
        Speed_text = c.create_text(165, 50, fill='cyan')
        Lives_text = c.create_text(220, 50, fill='cyan')
        S_Pnt_text = c.create_text(330, 50, fill='cyan')
        Secure_text = c.create_text(400, 50, fill='cyan')
        SlowMo_text = c.create_text(490, 50, fill='cyan')
        Confus_text = c.create_text(580, 50, fill='cyan')
        TmeBrk_text = c.create_text(670, 50, fill='cyan')
        SpdBst_text = c.create_text(760, 50, fill='cyan')
        Paralz_text = c.create_text(850, 50, fill='cyan')
        ShtSpd_text = c.create_text(940, 50, fill='cyan')
        NoTouch_text = c.create_text(1030, 50, fill='cyan')
        ShipTP_text = c.create_text(1120, 50, fill='cyan')
        Diamond_text = c.create_text(1210, 30, fill='cyan')
        Coin_text = c.create_text(1210, 50, fill='cyan')
        Level_view = c.create_text(MID_X, MID_Y, fill='Orange', font=("Helvetica", 50))

        pause_text = c.create_text(MID_X, MID_Y, fill='Orange', font=("Helvetica", 60, "bold"))
        pause_icon = c.create_image(MID_X, MID_Y - 128, image=PauseIcon, state=HIDDEN)

        c.create_text(50, HEIGHT - 30, text='1x Score', fill='cyan')
        c.create_text(130, HEIGHT - 30, text='2x Score', fill='cyan')
        c.create_text(210, HEIGHT - 30, text='3x Score', fill='cyan')
        c.create_text(290, HEIGHT - 30, text='-1 leven', fill='cyan')
        c.create_text(370, HEIGHT - 30, text='Slow Motion', fill='cyan')
        c.create_text(450, HEIGHT - 30, text='Verwarring', fill='cyan')
        c.create_text(530, HEIGHT - 30, text='NoBubMove', fill='cyan')
        c.create_text(610, HEIGHT - 30, text='Protectie', fill='cyan')
        c.create_text(690, HEIGHT - 30, text='2x Pnt Status', fill='cyan')
        c.create_text(770, HEIGHT - 30, text='Speed-up', fill='cyan')
        c.create_text(850, HEIGHT - 30, text='Speed-down', fill='cyan')
        c.create_text(930, HEIGHT - 30, text='Ultime Bubbel', fill='cyan')
        c.create_text(1010, HEIGHT - 30, text='Hyper Mode', fill='cyan')
        c.create_text(1090, HEIGHT - 30, text='Ammo speedup', fill='cyan')
        c.create_text(1170, HEIGHT - 30, text='Teleporter', fill='cyan')
        c.create_text(1250, HEIGHT - 30, text='No-touch', fill='cyan')
        c.create_text(1410, HEIGHT - 30, text='Level Sleutel', fill='cyan')

        #c.create_line(0, 70, WIDTH, 70, fill="lightblue")
        #c.create_line(0, 69, WIDTH, 69, fill="white")
        log.log("info", "game", "Lines 1")

        #c.create_line(0, HEIGHT - 103, WIDTH, HEIGHT - 103, fill="lightblue")
        #c.create_line(0, HEIGHT - 102, WIDTH, HEIGHT - 102, fill="White")
        log.log("info", "game", "Lines 2")

        c.create_line(-25 + (75 / 2), HEIGHT - 101, -25 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(55 + (75 / 2), HEIGHT - 101, 55 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(135 + (75 / 2), HEIGHT - 101, 135 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(215 + (75 / 2), HEIGHT - 101, 215 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(295 + (75 / 2), HEIGHT - 101, 295 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(375 + (75 / 2), HEIGHT - 101, 375 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(455 + (75 / 2), HEIGHT - 101, 455 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(535 + (75 / 2), HEIGHT - 101, 535 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(615 + (75 / 2), HEIGHT - 101, 615 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(695 + (75 / 2), HEIGHT - 101, 695 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(775 + (75 / 2), HEIGHT - 101, 775 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(855 + (75 / 2), HEIGHT - 101, 855 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(935 + (75 / 2), HEIGHT - 101, 935 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(1015 + (75 / 2), HEIGHT - 101, 1015 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(1095 + (75 / 2), HEIGHT - 101, 1095 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(1175 + (75 / 2), HEIGHT - 101, 1175 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(1255 + (75 / 2), HEIGHT - 101, 1255 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(1335 + (75 / 2), HEIGHT - 101, 1335 + (75 / 2), HEIGHT, fill="darkcyan")
        c.create_line(1415 + (75 / 2), HEIGHT - 101, 1415 + (75 / 2), HEIGHT, fill="darkcyan")
        log.log("info", "Canvas", "Lines for bubble info created.")

        place_bubble(50, HEIGHT - 75, 25, "Normal")
        place_bubble(130, HEIGHT - 75, 25, "Double")
        place_bubble(210, HEIGHT - 75, 25, "Triple")
        place_bubble(290, HEIGHT - 75, 25, "Kill")
        place_bubble(370, HEIGHT - 75, 25, "SlowMotion")
        place_bubble(450, HEIGHT - 75, 25, "Confusion")
        place_bubble(530, HEIGHT - 75, 25, "TimeBreak")
        place_bubble(610, HEIGHT - 75, 25, "Protect")
        place_bubble(690, HEIGHT - 75, 25, "DoubleState")
        place_bubble(770, HEIGHT - 75, 25, "SpeedUp")
        place_bubble(850, HEIGHT - 75, 25, "SpeedDown")
        place_bubble(930, HEIGHT - 75, 25, "Ultimate")
        place_bubble(1010, HEIGHT - 75, 25, "HyperMode")
        place_bubble(1090, HEIGHT - 75, 25, "ShotSpdStat")
        place_bubble(1170, HEIGHT - 75, 25, "Teleporter")
        place_bubble(1250, HEIGHT - 75, 25, "NoTouch")
        place_bubble(1410, HEIGHT - 75, 25, "LevelKey")
        log.log("info", "place_bubble", "Virtual bubbles for info created.")

        global Cheater
        Cheater = CheatEngine()
        c.bind_all('<Key>', move_ship)
        log.log("info", "Canvas", "Key-bindings binded to 'move_ship'")

        # Reset()
        if dat != 0:
            AutoRestore()
        # MAIN GAME LOOP

        # print(BubPos)
        # print
        # print(BubPos0)

        log.log("debug", "game", "Current Bubble pos. is '" + str(BubPos) + "'.")
        log.log("debug", "game", "__name__ variable is '" + str(__name__) + "'.")
        log.log("debug", "game", "'Lives' variable is '" + str(Lives) + "'.")
        log.log("debug", "game", "Score       =" + str(Score))
        log.log("debug", "game", "HiScore     =" + str(HiScore))
        log.log("debug", "game", "LevelScore  =" + str(LevelScore))
        log.log("debug", "game",
                "Ship ID's are '" + str(ship_id) + "' and '" + str(ship_id2) + "'. (Default = 1 and 2)")
        log.log("debug", "game", "TimeBreak=" + str(TimeBreak))
        log.log("debug", "game", "StateTime=" + str(StateTime))
        log.log("debug", "game", "S. Time  =" + str(int(StateTime - time())))

        old_start()

        BubChance = 1

        if len(BubID) == 0:
            log.log("warning", "game", "Bubbel-ID lijst is gelijk aan lengte nul.")

        if len(BubAct) == 0:
            log.log("warning", "game", "Bubble-actie lijst is gelijk aan lengte nul.")

        if len(BubSpd) == 0:
            log.log("warning", "game", "Bubbel-snelheid lijst is gelijk aan lengte nul.")

        if BubChance < 3:
            log.log("warning", "game",
                    "Bub-kans rate is behoorlijk laag. Dit kan problemen opleveren zoals te veel bubbels.")

        new = time()

        ScoreState = load_data_int("saves/" + SaveName + "/state/score.data", 1)
        SecureState = load_data_bool("saves/" + SaveName + "/state/secure.data", False)
        SlowMoState = load_data_bool("saves/" + SaveName + "/state/slowmo.data", False)
        TimeBreak = load_data_bool("saves/" + SaveName + "/state/timebreak.data", False)
        ConfusState = load_data_bool("saves/" + SaveName + "/state/confusion.data", False)
        SpdBoost = load_data_bool("saves/" + SaveName + "/state/speedboost.data", False)
        Paralized = load_data_bool("saves/" + SaveName + "/state/paralis.data", False)
        ShotSpeed = load_data_int("saves/" + SaveName + "/state/shotspeed.data", 5)

        if StateTime <= time():
            ScoreState = 1
            SecureState = False
            SlowMoState = False
            TimeBreak = False
            ConfusState = False
            SpdBoost = False
            Paralized = False
            ShotSpeed = 5
            StateTime = time()

        kzl = False

        if ScoreStateTime <= time():
            ScoreState = 1
            ScoreStateTime = time()
        if SecureStateTime <= time():
            SecureState = False
            SecureStateTime = time()
        if SlowMoStateTime <= time():
            SlowMoState = False
            SlowMoStateTime = time()
        if TimeBreakTime <= time():
            TimeBreak = False
            TimeBreakTime = time()
        if ConfusStateTime <= time():
            ConfusState = False
            ConfusStateTime = time()
        if SpdBoostTime <= time():
            SpdBoost = False
            SpdBoostTime = time()
        if ParalizedTime <= time():
            Paralized = False
            ParalizedTime = time()
        if ShotSpeedTime <= time():
            ShotSpeed = 5
            ShotSpeedTime = time()
        if Score < 0:
            log.log("error", "main", "The 'Score' variable under zero.")
        if Score > HiScore:
            HiScore = Score
        if ConfusState and not SecureState:
            Shuffling()

        FG = c.create_image(0, 0, anchor=NW, image=GameFG)
        GLOSS = c.create_image(0, 0, anchor=NW, image=GameFG_Gloss)

        # if 1:
        try:
            if __name__ == '__main__':
                while True:
                    AutoRestore()
                    while Lives > 0:
                        time2 = time()
                        try:
                            fps = int(1 / (time2 - time1))
                        except ZeroDivisionError:
                            fps = 0
                        time1 = time()
                        if not pause:
                            Root.title('Bubble Blaster 5 - ' + str(fps) + " fps.")
                            if not TimeBreak:
                                if len(BubID) < (WIDTH - 105 - 72) / 12:
                                    Thread(None, lambda: create_bubble()).start()
                                move_bubbles()
                                Thread(None, move_shoots).start()
                                clean_up_bubs()
                            Coll.check_collision()
                            if Score / LevelScore > Level - 1:
                                if randint(0, 125) == 0:
                                    if not KeyActive:
                                        create_bubble(j=-1)
                                        MaxBubSpd += 0.2
                                        KeyActive = True
                            if ReturnMain:
                                AutoSave()
                                for i in range(BubID - 1, -1, -1):
                                    del_bubble(i)
                                for i in range(ShotID - 1, -1, -1):
                                    del_shoot(i)
                                c.delete(ship_id)
                                c.delete(ship_id2)
                            Thread(None, refresh_state).start()
                            kzl = True
                            Thread(None, lambda: show_info()).start()
                            if not storemode:
                                c.delete(FG)
                                c.delete(GLOSS)
                                FG = c.create_image(0, 0, anchor=NW, image=GameFG)
                                GLOSS = c.create_image(0, 0, anchor=NW, image=GameFG_Gloss)
                        Root.update()
                        Root.update_idletasks()
                        # sleep(0.001)
                    Root.update()
                    g1 = c.create_text(MID_X, MID_Y, text='GAME OVER', fill='Red', font=('Helvetica', 60, "bold"))
                    g2 = c.create_text(MID_X, MID_Y + 60, text='Score: ' + str(Score), fill='white',
                                       font=('Helvetica', 30))
                    g3 = c.create_text(MID_X, MID_Y + 90, text='Level: ' + str(Level), fill='white',
                                       font=('Helvetica', 30))
                    Root.update()
                    sleep(4)
                    c.delete(g1)
                    c.delete(g2)
                    c.delete(g3)
                    del g1, g2, g3
                    cleanALL()
                    if len(BubID) != 0:
                        log.log("Fatal",
                                "Bubbles",
                                "Na schoonmaken van speelvlak zijn er nog steeds bubbels overgebleven. " +
                                "Vraag de eigenaar voor hulp en ondersteuning.")
                        log.save()
                        sys.exit(1)

                    # -----------#Reset Game --------------------------------------------------------------------

                    # ShipSettings
                    SHIP_SPD = load_data_int("data/ShipSpeed.cfg", 10)
                    # Bubble Settings
                    BubAct = list()
                    BubID = list()
                    BubRad = list()
                    BubSpd = list()
                    MinBubRad = load_data_int("data/BubMinRadius.cfg", 10)
                    MaxBubRad = load_data_int("data/BubMaxRadius.cfg", 30)
                    MaxBubSpd = load_data_int("data/BubMaxSpeed.cfg", 4.8)
                    ScreenGap = load_data_int("data/BubScreenGap.cfg", 100)

                    # Game Settings
                    BubChance = load_data_int("data/BubChance.cfg", 10)
                    TimeLimit = load_data_int("data/GameTimeLimit.cfg", 30)
                    LevelScore = load_data_int("data/GameLevelScore.cfg", 3000)

                    # Game setup
                    Score = load_data_int("data/GameResetScore.cfg", 0)
                    Level = load_data_int("data/GameResetLevel.cfg", 1)
                    Lives = load_data_int("data/GameResetLives.cfg", 7)
                    TP = load_data_int("data/GameResetTeleports.cfg", 0)
                    end = time() + TimeLimit

                    # Reset State
                    ScoreState = load_data_int("data/StateResetScore.cfg", 1)
                    SecureState = load_data_bool("data/StateResetSecure.cfg", False)
                    SlowMoState = load_data_bool("data/StateResetSlowMotion.cfg", False)
                    ConfusState = load_data_bool("data/StateResetConfusion.cfg", False)
                    TimeBreak = load_data_bool("data/StateResetTimeBreak.cfg", False)
                    SpdBoost = load_data_bool("data/StateResetSpeedBoost.cfg", False)
                    Paralized = load_data_bool("data/StateResetParalized.cfg", False)
                    StateTime = load_data_int("data/StateResetTime.cfg", 0)
                    Action = load_data_str("data/StateResetAction.cfg")
                    pause = load_data_bool("data/Pause.cfg", False)

                    f = open("saves/" + SaveName + "/game/BubID.data", "wb+")
                    dump([], f)
                    f.close()
                    f = open("saves/" + SaveName + "/game/BubAct.data", "wb+")
                    dump([], f)
                    f.close()
                    f = open("saves/" + SaveName + "/game/BubRad.data", "wb+")
                    dump([], f)
                    f.close()
                    f = open("saves/" + SaveName + "/game/BubSpd.data", "wb+")
                    dump([], f)
                    f.close()
                    f = open("saves/" + SaveName + "/game/BubPos.data", "wb+")
                    dump([], f)
                    f.close()

                    # Reset Save
                    AutoSave()
        except TclError:
            pass
            # Saves the game
            AutoSave()

            # Logging and save log.
            log.log("info", "game", "Exit...")
            log.save()


if __name__ == "__main__":
    Game()
