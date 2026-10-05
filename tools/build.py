"""Run the build pipeline, or selected steps of it, from the repository root.

    python tools/build.py all
    python tools/build.py assets board guide      # any subset, in pipeline order

Steps
  logo    decode source/logo/Logo_VCCI.cdr into the master SVG (build/logo/)
  assets  brand-assets/01_Logo, 02_Colour, 04_Graphics          (needs Microsoft Edge)
  board   board/export/*  + card positions for the guide           (needs Microsoft Edge)
  word    brand-assets/06_Templates/Word/*.dotx + PDF previews    (needs Microsoft Word, Node.js)
  ppt     brand-assets/06_Templates/PowerPoint/*.potx + preview   (needs Microsoft PowerPoint, Node.js)
  guide   brand-assets/07_Guidelines/*.pdf                         (needs Microsoft Edge, Poppler)
The icon set (brand-assets/05_Icons) has its own pipeline in tools/icons/ (see tools/README.md).
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY, NODE = [sys.executable], ['node']
STEPS = {
    'logo':   [PY + ['tools/cdr/decompress.py'], PY + ['tools/cdr/mkvector.py']],
    'assets': [PY + ['tools/assets/build_assets.py']],
    'board':  [PY + ['tools/board/render.py']],
    'word':   [PY + ['tools/word/make_art.py'], NODE + ['tools/word/make_templates.js'], PY + ['tools/word/finalize.py']],
    'ppt':    [PY + ['tools/ppt/make_art.py'], NODE + ['tools/ppt/make_pptx.js'], PY + ['tools/ppt/finalize.py']],
    'guide':  [PY + ['tools/guide/prepare_images.py'], PY + ['tools/guide/make_guide.py']],
}

if __name__ == '__main__':
    want = sys.argv[1:] or ['--help']
    if want == ['--help'] or any(w not in STEPS and w != 'all' for w in want):
        print(__doc__); sys.exit(0 if want == ['--help'] else 1)
    order = list(STEPS) if 'all' in want else [s for s in STEPS if s in want]
    for step in order:
        for cmd in STEPS[step]:
            print(f'\n[{step}] ' + ' '.join(cmd[1:] if cmd[0] == sys.executable else cmd), flush=True)
            subprocess.run(cmd, cwd=ROOT, check=True)
    print('\ndone:', ', '.join(order))
