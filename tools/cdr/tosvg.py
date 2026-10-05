import sys, struct, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from parse import D, tree, build

T=tree(0,len(D),0,[])

def fills():
    F={}
    for dep,cid,o,l,p in T:
        if cid==b'fild':
            fid=D[o:o+4].hex()
            if l<40: continue
            model=D[o+27]; v=D[o+35:o+39]
            if model==2: c,m,y,k=[x/100 for x in v]
            elif model in (3,0x11): c,m,y,k=[x/255 for x in v]
            elif model==5:
                F[fid]='#%02x%02x%02x'%(v[2],v[1],v[0]); continue
            else: continue
            r,g,b=[round(255*(1-a)*(1-k)) for a in (c,m,y)]
            F[fid]=('#%02x%02x%02x'%(r,g,b), f'CMYK {round(c*100)}/{round(m*100)}/{round(y*100)}/{round(k*100)} (model {model})')
    return F

def objects():
    """yield dicts with points/types/fill/matrix in document order"""
    objs=[]; cur=None
    for i,(dep,cid,o,l,p) in enumerate(T):
        if cid==b'loda':
            n,so,sto,ctype=struct.unpack('<4I',D[o+4:o+20])
            offs=struct.unpack('<%dI'%n,D[o+so:o+so+4*n])
            types=struct.unpack('<%dI'%n,D[o+sto:o+sto+4*n])[::-1]
            a=dict(zip(types,offs))
            cur={'ctype':ctype,'depth':dep}
            if ctype==3:
                ci=o+a[0x1e]; N=struct.unpack('<I',D[ci:ci+4])[0]
                pts=struct.unpack('<%di'%(2*N),D[ci+4:ci+4+8*N])
                cur['pts']=[(pts[2*j],pts[2*j+1]) for j in range(N)]
                cur['types']=list(D[ci+4+8*N:ci+4+9*N])
                cur['fill']=D[o+a[0x14]:o+a[0x14]+4].hex()
            objs.append(cur)
        elif cid==b'trfd' and cur is not None:
            b=D[o+24:o+l]; cur['m']=struct.unpack('<6d',b[16:64])
    return objs

def pathd(pts,types,m):
    a,b,tx,c,d,ty=m
    P=[(a*x+b*y+tx, c*x+d*y+ty) for x,y in pts]
    out=[]; ctrl=[]
    f=lambda q:f'{q[0]:.1f},{-q[1]:.1f}'
    for q,t in zip(P,types):
        closed=t&0x08
        if not (t&0x40) and not (t&0x80):
            out.append('M'+f(q)); ctrl=[]
        elif (t&0x40) and not (t&0x80):
            out.append('L'+f(q))
            if closed: out.append('Z')
        elif not (t&0x40) and (t&0x80):
            if len(ctrl)>=2: out.append('C'+f(ctrl[0])+' '+f(ctrl[1])+' '+f(q))
            else: out.append('L'+f(q))
            if closed: out.append('Z')
            ctrl=[]
        else:
            ctrl.append(q)
    return ''.join(out), P

if __name__=='__main__':
    F=fills(); print(json.dumps(F,indent=1))
    O=objects()
    paths=[]; allp=[]
    for ob in O:
        if ob['ctype']!=3: continue
        d,P=pathd(ob['pts'],ob['types'],ob['m']); allp+=P
        col=F.get(ob['fill'],('#f0f',''))[0]
        paths.append((d,col,ob['fill'],len(ob['pts'])))
        print(ob['fill'],F.get(ob['fill']),len(ob['pts']))
    xs=[p[0] for p in allp]; ys=[-p[1] for p in allp]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    print('bbox',x0,x1,y0,y1,'aspect',(x1-x0)/(y1-y0))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {x1-x0:.1f} {y1-y0:.1f}">'
    for d,col,fid,n in paths[::-1]: svg+=f'<path fill-rule="evenodd" fill="{col}" data-fill="{fid}" d="{d}"/>'
    svg+='</svg>'
    open(build('cdr', 'raw.svg'),'w').write(svg)
