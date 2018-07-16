import sys
from pysndfx import AudioEffectsChain

fx = (
    AudioEffectsChain()
    .reverb()
    .delay()
)

infile = sys.argv[1]
outfile = sys.argv[2]

fx(infile, outfile)
