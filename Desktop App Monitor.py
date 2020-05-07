import psutil
import time
import win32api
import win32process
import win32con
import sys
import ctypes.wintypes
import database
from process import Proc

# nohup python /path/to/test.py &"
# nohup python /path/to/test.py &

# Declarations of global variables
time_started = 0
time_ended = 0
time_in_foreground = 0
prev_process = Proc (0, "0", "0", 0, 0)

## Get statistics of process given name
# PROCNAME = "python.exe"
# for proc in psutil.process_iter(): # look through all current processes
#     if proc.name() == PROCNAME: # once the process is found,
#         print(proc) # returns pid, name, start_time
#         print(proc.exe())  # returns path
#         print(proc.cmdline())  # returns exe path, and all other processes that have been called with it
#         print(proc.name())  # returns process name
#         print(proc.create_time()) # returns process create time in epoch time
#         print(time.ctime(proc.create_time())) # converts epoch time to date time
#         print(time.ctime(time.time())) # gets current time
#         print(time.time() - proc.create_time()) # obtains the amount of time since the process started in a float
#         print(proc.pid) # obtains process id


## How to get pid from foreground window and get current process id
# string1 = win32gui.GetWindowText(win32gui.GetForegroundWindow())
# print(win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]) # [1] in tuple is processID

## Getting name from current process window
# p2 = psutil.Process(win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1])
# print(p2.name())

# Get process name given pid
def getCurrentProcessName(curr_pid):
    curr_process = psutil.Process(curr_pid)
    return curr_process.name()

# Get process create_time given pid
def getCurrentProcessCreateTime(curr_pid):
    curr_process = psutil.Process(curr_pid)
    return time.ctime(curr_process.create_time())

# Get Application Name from exe path
def getFileDescription(windows_exe):
    try:
        language, codepage = win32api.GetFileVersionInfo(windows_exe, '\\VarFileInfo\\Translation')[0]
        stringFileInfo = u'\\StringFileInfo\\%04X%04X\\%s' % (language, codepage, "FileDescription")
        description = win32api.GetFileVersionInfo(windows_exe, stringFileInfo)
    except:
        description = "unknown"

    return description
# print(getFileDescription(r"C:\Program Files\Internet Explorer\iexplore.exe")) # for some reason the r must be present

# Get process Application name given windows handle
def getCurrentProcessAppName(handle):
    pid = win32process.GetWindowThreadProcessId(handle)[1]
    hndl = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
    return getFileDescription(win32process.GetModuleFileNameEx(hndl, 0))


# SetWinEventHook in Python with ctypes and wintypes
EVENT_SYSTEM_FOREGROUND = 0x0003
WINEVENT_OUTOFCONTEXT = 0x0000

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32

ole32.CoInitialize(0)

WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)

# Callback function to obtain process attributes from process.py from the foreground window
def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global time_started
    global time_ended
    global time_in_foreground
    global prev_process
    conn = database.create_connecton('database.db')

    # Calculates the time in seconds that previous process was in foreground
    time_ended = time.time()
    time_in_foreground = time_ended - time_started
    prev_process.time_used = time_in_foreground

    # Checks if the previous process still exists in the database and if it does, update its time_used
    if prev_process.id != 0:
         database.update_entry(conn, prev_process)

    # Passes the window handle of foreground window to win32 functions to get pid
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]

    # Inserts the process attributes into a the database as an entry if it does not already exist
    process = Proc(pid, getCurrentProcessName(pid), getCurrentProcessAppName(hwnd), getCurrentProcessCreateTime(pid), 0)
    database.insert_entry(conn, process)

    database.show_all(conn)
    prev_process = process
    time_started = time.time()

    conn.commit()
    conn.close()

WinEventProc = WinEventProcType(callback)

user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
hook = user32.SetWinEventHook(
    EVENT_SYSTEM_FOREGROUND,
    EVENT_SYSTEM_FOREGROUND,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)

if hook == 0:
    print('SetWinEventHook failed')
    sys.exit(1)

if hook != 0:
    print('SetWinEventHook succeeded')

msg = ctypes.wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
    user32.TranslateMessageW(msg)
    user32.DispatchMessageW(msg)

user32.UnhookWinEvent(hook)
ole32.CoUninitialize()

