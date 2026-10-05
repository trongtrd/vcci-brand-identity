import struct, collections, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from env import build
D=open(build('cdr', 'data.bin'),'rb').read()
B=open(build('cdr', 'sizes.bin'),'rb').read()
SZ=struct.unpack('<%dI'%(len(B)//4),B[:len(B)//4*4])

def chunks(off,end):
    """yield (id, type_or_None, data_off, data_len, next)"""
    while off+8<=end:
        cid=D[off:off+4]; idx=struct.unpack('<I',D[off+4:off+8])[0]
        ln=SZ[idx] if idx<len(SZ) else idx
        if cid==b'LIST':
            typ=D[off+8:off+12]
            yield cid,typ,off+12,ln-4
        else:
            yield cid,None,off+8,ln
        off+=8+ln+(ln&1)

def tree(off,end,depth=0,out=None,path=()):
    for cid,typ,o,l in chunks(off,end):
        if cid==b'LIST':
            out.append((depth,b'LIST:'+typ,o,l,path))
            tree(o,o+l,depth+1,out,path+(typ,))
        else:
            out.append((depth,cid,o,l,path))
    return out

if __name__=='__main__':
    T=tree(0,len(D),0,[])
    c=collections.Counter(t[1] for t in T); print(c.most_common(50))
    for t in T[:80]: print('  '*t[0],t[1],t[3])
