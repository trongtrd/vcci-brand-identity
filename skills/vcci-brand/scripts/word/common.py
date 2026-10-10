"""Shared helpers for the VCCI Word scripts: locating brand assets, OOXML namespaces, package I/O."""
import os, zipfile
from lxml import etree

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
}
W = '{%s}' % NS['w']
R = '{%s}' % NS['r']
REL_IMAGE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
REL_LINK = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink'
TEMPLATE_CT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml'
DOC_CT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'

_DECL = ' '.join(f'xmlns:{k}="{v}"' for k, v in NS.items() if k != 'rel')


def frag(xml):
    """Parse a WordprocessingML fragment written with the usual prefixes (w:, r:, wp:, a:, pic:)."""
    root = etree.fromstring(f'<root {_DECL}>{xml}</root>')
    return list(root)


def find_brand_root():
    """Directory that contains brand-assets/: $VCCI_BRAND_ROOT; else the folder named in brand-root.txt next to SKILL.md
    (written by tools/install_skill.py when the skill is installed outside the repository); else the nearest parent."""
    env = os.environ.get('VCCI_BRAND_ROOT')
    if env and os.path.isdir(os.path.join(env, 'brand-assets')):
        return env
    marker = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'brand-root.txt')
    if os.path.isfile(marker):
        root = open(marker, encoding='utf-8').read().strip()
        if os.path.isdir(os.path.join(root, 'brand-assets')):
            return root
        raise SystemExit(f'brand-root.txt points to {root}, which has no brand-assets/. Move the vcci-brand-identity clone back, '
                         'or reinstall the skill: python tools/install_skill.py <tool> (run from the clone).')
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(d, 'brand-assets')):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit('Cannot find brand-assets/. Set VCCI_BRAND_ROOT to the vcci-brand-identity repo folder.')
        d = parent


def template_path(name):
    return os.path.join(find_brand_root(), 'brand-assets', '06_Templates', 'Word', name)


def read_package(path):
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def write_package(files, path):
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in ['[Content_Types].xml'] + [n for n in files if n != '[Content_Types].xml']:
            z.writestr(n, files[n])
    os.replace(tmp, path)


def xml_bytes(tree):
    return etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
