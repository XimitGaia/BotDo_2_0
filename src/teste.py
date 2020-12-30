import win32gui
import re
aa = []

non_logged_screens = list()
def windowEnumerationHandler(hwnd, all_windows):
    all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
all_windows = list()
win32gui.EnumWindows(windowEnumerationHandler, all_windows)
for window in all_windows:
    print(window[1])
    if re.search(r'(^D?d?ofus \d+?.?\d+)',window[1]):
        non_logged_screens.append(window[0])

print(non_logged_screens)
