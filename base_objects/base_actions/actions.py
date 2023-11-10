import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

logger = logging.getLogger(__name__)

class Actions:

    def __init__(self, driver):
        self.driver = driver
        self.video = None

    def get_video(self, url):
        self.video = self.driver.get(url)
        self.driver.set_window_size(980, 760)

    def get_duration(self):
        return self.driver.execute_script(r"""return document.querySelector('video').duration""")

    def play(self):
        time.sleep(5)
        self.driver.find_element(By.ID,"movie_player").send_keys(Keys.SPACE)
        time.sleep(1)
        self.driver.find_element(By.ID, "movie_player").click()
        #self.driver.execute_script(r"""return document.querySelector('video').play()""")

    def pause(self):
        self.driver.execute_script(r"""return document.querySelector('video').pause()""")

    def is_paused(self):
        return self.driver.execute_script(r"""return document.querySelector('video').paused""")

    def is_played(self):
        return self.driver.execute_script(r"""return document.querySelector('video').played""")

    def get_volume(self):
        return self.driver.execute_script(r"""return document.querySelector('video').volume""")

    def set_volume(self, val):
        return self.driver.execute_script(f"""return document.querySelector('video').volume={val}""")

    def get_current_time(self):
        return self.driver.execute_script(r"""return document.querySelector('video').currentTime""")

    def set_current_time(self, val):
        self.driver.execute_script(f"""return document.querySelector('video').currentTime={val}""")