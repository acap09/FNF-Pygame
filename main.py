import pygame
import psutil, os #lllllll
import shutil
import sys
import tkinter as tk
from tkinter import scrolledtext
import traceback
from pathlib import Path

root = tk.Tk()
root.withdraw()

def cleanup():
    pygame.display.quit()
    pygame.quit()
    root.destroy()

    if v.temp_path.exists() and v.temp_path.is_dir():
        shutil.rmtree(v.temp_path)

def handle_exception(exc_type, exc_value, exc_traceback):
    import colorama as cr
    cr.init()
    err = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f'{cr.Fore.RED}{err}{cr.Style.RESET_ALL}')
    #messagebox.showerror('An error has occurred!', f'An error has occurred! Please copy the error (CTRL+C) and report '
    #                                               f'to the GitHub '
    #                                               f'page (https://github.com/acap09/FNF-Pygame/issues) as an '
    #                                               f'issue!\n\n{err}')
    window = tk.Toplevel()
    window.title('Error Report')
    window.geometry("800x600")  # width x height

    if Path('github_link.txt').exists():
        with open('github_link.txt', 'r') as f:
            link = f.read().strip()
    else:
        link = 'https://github.com/acap09/FNF-Pygame/issues'

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    text_area.pack(expand=True, fill='both')
    text_area.insert(tk.END, f'An error has occured! Please copy the error and report to the GitHub page ({link})!\n\n{err}')
    text_area.config(state='disabled')

    def on_close():
        window.destroy()
        cleanup()
        sys.exit(1)

    # Optional: add a close button
    close_btn = tk.Button(window, width = 10, height = 2, text='OK', font=('Arial', 10, 'bold'), command=on_close)
    close_btn.pack(pady=10)
    window.protocol('WM_DELETE_WINDOW', on_close)
    root.bell()
    root.mainloop()
sys.excepthook = handle_exception

pygame.init()
from source import variables as v
from source import ClientPrefs as cp

icon = pygame.image.load(v.source_path/'placeholder_icon.png')
pygame.display.set_icon(icon)

v.screen = pygame.display.set_mode((1000, 1000*(9/16)), pygame.RESIZABLE)
pygame.display.set_caption('Friday Night Funkin\': Pie Engine')
v.mainSurface = pygame.Surface(v.screen.get_size(), pygame.SRCALPHA, 32)
v.mainSurfaceSize = v.mainSurface.get_size()
v.clock = pygame.time.Clock()

from source.backend.loops import fps_render, render, backend_stuff, state



font = pygame.font.Font(None, 20)
process = psutil.Process(os.getpid())

import source.backend.initialize
fpsDisp = 0
v.clock.tick()
try:
    while v.running:
        #v.dt = v.clock.tick()/1000
        v.elapsed += v.dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v.running = False
                break
            elif event.type == pygame.WINDOWSIZECHANGED:
                dim = v.screen.get_size()
                #print(dim)
                dim = (int(min(dim[0], int(dim[1]*cp.aspectRatio))), int(min(dim[1], int(dim[0]*cp.invAspectRatio))))

                #v.mainSurface = pygame.Surface(dim, pygame.SRCALPHA, 32)
                #print(v.mainSurface.get_size())
                print('RESIZED')
                v.mainSurface = pygame.transform.scale(v.mainSurface, dim)
                v.mainSurfaceSize = v.mainSurface.get_size()
                if 'WindowResizeDependencies' in v.registry:
                    for idx, val in v.registry['WindowResizeDependencies'].items():
                        if hasattr(val, 'windowResize') and callable(val.windowResize):
                            val.windowResize(dim)
                state.windowResize(dim)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    v.screenshot = True


        fpsDisp, daSurface = fps_render.update(process, font, fpsDisp)
        state.updatePre()
        backend_stuff.update()
        state.update()

        #v.screen.fill((0, 0, 0))
        render.screen_clear()
        render.render()
        state.render()
        render.update_disp(daSurface)

        v.dt = v.clock.tick(0 if cp.fpsLimiter == -1 else cp.fpsLimiter)/1000
except Exception as exc:
    handle_exception(type(exc), exc, exc.__traceback__)

cleanup()