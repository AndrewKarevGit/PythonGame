from pygame import mixer

mixer.init()


def start_window():
    mixer.music.load("music/start.mp3")
    mixer.music.play(-1)


def end_window():
    mixer.music.load("music/end.mp3")
    mixer.music.play(-1)


def beginner():
    mixer.music.load("music/beginner.mp3")
    mixer.music.play(-1)


def intermediate():
    mixer.music.load("music/intermediate.mp3")
    mixer.music.play(-1)


def hard():
    mixer.music.load("music/hard.mp3")
    mixer.music.play(-1)


def stop():
    mixer.music.stop()
