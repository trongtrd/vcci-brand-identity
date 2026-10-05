"""Step 1 of the logo pipeline: unpack the zlib streams of the CorelDRAW X3 master (source/logo/Logo_VCCI.cdr).

CorelDRAW X3+ stores the document as a RIFF 'cmpr' list: one zlib stream with the chunk data and one with the
table of chunk sizes. Writes build/cdr/data.bin and build/cdr/sizes.bin, read by parse.py.
Run from the repository root:  python tools/cdr/decompress.py
"""
import os, re, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import ROOT, build

raw = open(os.path.join(ROOT, 'source', 'logo', 'Logo_VCCI.cdr'), 'rb').read()
streams = []
for m in re.finditer(rb'\x78[\x01\x5e\x9c\xda]', raw):
    try:
        out = zlib.decompressobj().decompress(raw[m.start():])
    except zlib.error:
        continue
    if len(out) > 100:
        streams.append(out)
assert len(streams) >= 2, 'expected a data stream and a block-size stream'
open(build('cdr', 'data.bin'), 'wb').write(streams[0])
open(build('cdr', 'sizes.bin'), 'wb').write(streams[1])
print('data', len(streams[0]), 'bytes; sizes', len(streams[1]), 'bytes')
