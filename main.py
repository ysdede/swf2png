import os
import glob
import ffmpeg
import win32con
import win32gui
import subprocess
from time import sleep
from win32con import (WS_CAPTION, WS_THICKFRAME, WS_MINIMIZE, WS_MAXIMIZE, WS_SYSMENU, WS_POPUP)


border_style_flags = (
    WS_CAPTION | WS_THICKFRAME | WS_MINIMIZE | WS_MAXIMIZE | WS_SYSMENU | WS_POPUP)

width = 750
root_folder = os.path.dirname(os.path.abspath(__file__))
swf_folder = root_folder + '/swf'
glob_filter = swf_folder + '/*.swf'
output_folder = 'png/'
RECURSIVE = False


def runplayer(fname):
    cmd_player = 'util/flashplayer_32_sa.exe {}'.format(fname)
    process = subprocess.Popen(cmd_player, shell=False)
    return process


def killall():
    while True:
        trash = win32gui.FindWindow(None, r'Adobe Flash Player 32')
        if trash:
            print('process found: ', trash)
            win32gui.PostMessage(trash, win32con.WM_CLOSE, 0, 0)
            sleep(1)
        else:
            print('no more process!')
            break


def modifywindow():
    hwnd = win32gui.FindWindow(None, r'Adobe Flash Player 32')
    win32gui.SetForegroundWindow(hwnd)

    dimensions = win32gui.GetClientRect(hwnd)
    print('dimensions', dimensions)
    w = dimensions[2] - dimensions[0]
    h = dimensions[3] - dimensions[1]
    print('w: {}, h: {}'.format(w, h))
    setw = width
    seth = int((setw / w) * h)

    # Make borderless
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style & ~border_style_flags)
    win32gui.SetMenu(hwnd, None)

    win32gui.MoveWindow(hwnd, 100, 100, setw, seth, True)

    print('NEW w: {}, h: {}'.format(setw, seth))


def renderpng(outputfname):
    (
        ffmpeg
        .input(format='gdigrab', framerate=5, draw_mouse=0, filename="title=Adobe Flash Player 32")
        .output(outputfname, vframes=1)
        .run(quiet=True, overwrite_output=True)
    )


print('Looking for files in:', swf_folder)
dirList = glob.glob(glob_filter, recursive=RECURSIVE)
print('Found {} swf files...'.format(len(dirList)))

if dirList:
    for swffile in dirList:
        print('File name:', swffile)
        outputfilename = os.path.basename(swffile.replace('.swf', '.png'))
        print('finalfile name: ', outputfilename)

        killall()
        processhandler = runplayer(swffile)
        sleep(2)
        modifywindow()
        renderpng(output_folder + outputfilename)
        processhandler.terminate()
else:
    print('done...')
