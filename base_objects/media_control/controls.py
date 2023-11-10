from pyautogui import press

class Controls:

    def stop(self):
        press('q')

    def pause(self):
        press("space")

    def forward(self):
        press("d")

    def rewind(self):
        press("a")

    def seek(self):
        press("s")

    def details(self):
        press("c")