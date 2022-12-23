import os
from time import sleep
from PIL import ImageGrab, Image
from keyboard import on_release
from threading import Thread
from settings import *


def next_folder_number() -> None:
    counter = 1
    while True:
        folder_name = f"{counter:04d}"
        if not os.path.exists(CLIP_SAVING_PATH + folder_name):
            return counter
        counter += 1


class ClipMaker:
    def __init__(self, capture_interval: float, capture_past_time, hot_keys) -> None:
        self.capture_interval: float = capture_interval  # In seconds
        self.capture_past_time: float = capture_past_time  # In seconds
        self.hot_keys: dict = hot_keys
        self.buffer: list[Image.Image] = []
        self.clip: list[Image.Image] = []
        self.stop: bool = False
        
        # run the next_folder_number function before start the screen capture.
        # this way the program does not need to do a loop every time before save the clip; it only need to increase a counter
        self.next_folder_number = next_folder_number()

    def capture_screen(self) -> None:
        print('screen capture started')
        while not self.stop:
            # Capture a screenshoot
            screenshot = ImageGrab.grab()

            self.buffer.append(screenshot)

            # Remove older screenshots from buffer
            if len(self.buffer) > self.capture_past_time // self.capture_interval:
                self.buffer.pop(0)

            # Sleep for a time before capturing the next screen image
            sleep(self.capture_interval)
        print('screen capture stoped')
        return

    def get_clip(self) -> None:
        """save the actual state of the buffer"""
        self.clip = list(self.buffer)
        print('clip got')
        return

     def save_clip(self) -> None:
        """Save each image of the clip in a folder"""
        # create folder
        folder_name = f"{self.next_folder_number:04d}"
        os.makedirs(CLIP_SAVING_PATH + folder_name)  
        print('folder created')
        
        for i, image in enumerate(self.clip):  # oldest clip
            image.save(os.path.join(CLIP_SAVING_PATH + folder_name, f"image{i}.png"))
        self.next_folder_number += 1
        print('clip saved')
        return

    def on_key(self, key) -> None:
        """React to keyboard events"""
        if key.name == self.hot_keys['trigger']:
            print('trigger key pressed')
            self.get_clip()
            self.save_clip()
            return

        if key.name == self.hot_keys['quit']:
            print('end key pressed')
            self.stop = True
            return     


def main() -> int:
    print('main started')
    clipmaker = ClipMaker(CAPTURE_INTERVAL, CAPTURE_PAST_TIME, HOT_KEYS)
    Thread(target=clipmaker.capture_screen, name="capture_screen").start()

    print('started listening to keyboard')
    on_release(clipmaker.on_key)
    return 0


if __name__ == '__main__':
    print('starting program')
    main()
