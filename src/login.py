# from pywinauto import application
# import win32gui
# import time

# app = application.Application()
# app.start("C:\\Users\\Lucas\\AppData\\Local\\Ankama\\zaap\\dofus\\Dofus.exe")
#input()
# class Login:

#     def open_game

# def windowEnumerationHandler(hwnd, top_windows):
#     top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

# if __name__ == "__main__":
#     results = []
#     top_windows = []
#     win32gui.EnumWindows(windowEnumerationHandler, top_windows)
#     for i in top_windows:
#         if "dofus" in i[1].lower():
#             print(i)
#             win32gui.ShowWindow(i[0],5)
#             win32gui.SetForegroundWindow(i[0])
#             break




import win32gui
def window_enum_handler(hwnd, resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_app_list(handles=[]):
    mlst=[]
    win32gui.EnumWindows(window_enum_handler, handles)
    for handle in handles:
        mlst.append(handle)
    return mlst

def bring_character_to_front(self, name:str):
    appwindows = get_app_list()
    for i in appwindows:
        if name in i[1].lower():
            win32gui.SetForegroundWindow(i[0])
#win32gui.SetForegroundWindow(198906)