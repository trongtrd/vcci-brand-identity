"""Build clean SVG logo assets from the decoded CDR geometry."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tosvg import objects, pathd, build
import numpy as np

O=[o for o in objects() if o['ctype']==3]
# palette (FOGRA39 sRGB of the CDR CMYK values)
MASTER={'88be4f04':'#264896','182f5104':'#FFCD00','782e5104':'#CC713C','b82e5104':'#1C1B18'}

paths=[]; allp=[]
for o in O:
    d,P=pathd(o['pts'],o['types'],o['m']); allp+=P; paths.append((o['fill'],d))
P=np.array(allp); P[:,1]*=-1
x0,y0=P.min(0); x1,y1=P.max(0)
S=1000/(y1-y0)   # normalise: cap height = 1000 units
def norm(d):
    import re
    def f(m):
        x=float(m.group(1)); y=float(m.group(2))
        return f'{(x-x0)*S:.2f},{(y-y0)*S:.2f}'
    return re.sub(r'(-?[\d.]+),(-?[\d.]+)',f,d)
W=(x1-x0)*S
def svg(pal,only=None,pad=0):
    s=''
    for fid,d in paths[::-1]:
        if only and fid not in only: continue
        s+=f'<path fill="{pal.get(fid,"#f0f")}" fill-rule="evenodd" d="{norm(d)}"/>'
    return s
if __name__=='__main__':
    open(build('logo', 'vcci-logo.svg'),'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} 1000">{svg(MASTER)}</svg>')
    # drum only, cropped square
    drum=[np.array(pathd(o['pts'],o['types'],o['m'])[1]) for o in O if o['fill']!='88be4f04']
    D=np.vstack(drum); D[:,1]*=-1; dx0,dy0=(D.min(0)-[x0,y0])*S; dx1,dy1=(D.max(0)-[x0,y0])*S
    open(build('logo', 'vcci-drum.svg'),'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{dx0:.2f} {dy0:.2f} {dx1-dx0:.2f} {dy1-dy0:.2f}">{svg(MASTER,only=set(MASTER)-{"88be4f04"})}</svg>')
    print('W/H',W/1000,'drum box',dx0,dy0,dx1-dx0,dy1-dy0)
