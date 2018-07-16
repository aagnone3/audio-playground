import os
from os import path
import shutil
import numpy as np
from numpy import sin, pi, dot, linspace
from librosa.output import write_wav
from subprocess import check_call

from audio_helpers import play_audio

TWOPI = 2*pi
SR = 8000
BASE_FN = "song.wav"


def gen_tone(x, f1, f2):
    return dot([1, 1], [sin(TWOPI*f1*x), sin(TWOPI*f2*x)])


def make_tone(x, f1, f2):
    y = gen_tone(x, f1, f2)
    tmpfn = "tmp.wav"

    tone_fn = path.join('wavs', 'tone%i.wav' % i)
    write_wav(tone_fn, y, SR, norm=True)

    reverbed_fn = path.join('wavs', 'reverbed_tone%i.wav' % i)
    cmd = "sox {} {} gain -3 reverb".format(tone_fn, reverbed_fn)
    check_call(cmd, shell=True)

    combined_fn = path.join('wavs', 'combined_tone%i.wav' % i)
    cmd = "sox {} {} pad 1 0".format(tone_fn, tmpfn)
    check_call(cmd, shell=True)
    cmd = "sox -m {} {} {}".format(BASE_FN, tmpfn, combined_fn)
    check_call(cmd, shell=True)


def mix(s1, s2):
    return dot([0.5, 0.5], [s1, s2])


dtmf_freqs = {
    1: [697, 1209],
    2: [697, 1336],
    3: [697, 1477],
    4: [770, 1209],
    5: [770, 1336],
    6: [770, 1477],
    7: [852, 1209],
    8: [852, 1336],
    9: [852, 1477]
}


t = linspace(0, 5, SR)
tones = [
    make_tone(t, *dtmf_freqs[i + 1])
    for i in range(len(dtmf_freqs))
]
