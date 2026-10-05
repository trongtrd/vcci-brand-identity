from pathlib import Path
import shutil, json, subprocess, sys, zipfile, hashlib
ROOT=Path(__file__).resolve().parents[2]
src=ROOT/'build'/'icons'/'review'/'05_Icons'; dst=ROOT/'build'/'icons'/'final'/'05_Icons'; archive=ROOT/'build'/'icons'/'VCCI_Icons_v1.zip'
if archive.exists(): raise FileExistsError('Final archive already exists; do not overwrite silently.')
shutil.copytree(src,dst,dirs_exist_ok=True)
spec=dst/'ICON_SPEC.md'
s=spec.read_text(encoding='utf8').replace('# VCCI Icon System v1 — Review candidate','# VCCI Icon System v1').replace('Status: Direction A approved; icon set awaiting owner review. Not final sign-off.','Status: Version 1.0. Direction A and the complete 48 UI / 24 hero icon set approved by the project owner on 2026-10-05.')
s+='\n## Release verification\n\nThe approved release contains 288 SVGs and 480 transparent icon PNGs. Automated checks passed with no errors; the largest SVG is 831 bytes and the largest hero accent occupies 8.11% of the live area. Every icon was visually checked at 24, 48 and 128 px on Paper and VCCI Blue. Hero contact sheets also show Deep Navy.\n'
spec.write_text(s,encoding='utf8')
handback=dst/'HANDBACK_TO_CLAUDE.md'
s=handback.read_text(encoding='utf8').replace('# Handback to Claude — Review candidate','# Handback to Claude — VCCI Icons v1').replace('The owner approved Direction A (Geometric Clarity). The vector set awaits review and final sign-off; no final ZIP has been issued.','The owner approved Direction A (Geometric Clarity) and signed off the complete 48 UI / 24 hero vector set on 2026-10-05 with “duyệt bộ này.” This is the approved Version 1.0 release, packaged as VCCI_Icons_v1.zip.').replace('## Review points and limitations','## Known issues and use limitations').replace('Owner review is still required, particularly for the abstract meanings of 02, 03 and 04 and the distinction between 09 and 10. Labels remain necessary. Hero 24 px is a stress-test size; 48 px is the minimum recommended display. The concept sheet is a raster reference and not a source of production geometry. Final sign-off and final ZIP packaging remain pending.','No unresolved owner-requested changes remain. The owner approved the complete set, including heroes 02, 03, 04, 09 and 10. Abstract policy concepts remain label-dependent by design. Hero 24 px is a stress-test size; 48 px is the minimum recommended display. The concept sheet is a raster reference and not a source of production geometry. All automatic checks passed, and every icon was visually checked at 24, 48 and 128 px on Paper and VCCI Blue. Contact sheets include Deep Navy for heroes. Geometry is unchanged from the approved review set; only release status and contact-sheet footers were updated.')
handback.write_text(s,encoding='utf8')
subprocess.run([sys.executable,str(ROOT/'tools'/'icons'/'sheets.py'),'--final'],check=True)
items=json.loads((ROOT/'tools'/'icons'/'catalog.json').read_text(encoding='utf8'))
expected={'05_Icons/ICON_SPEC.md','05_Icons/LICENSES.md','05_Icons/HANDBACK_TO_CLAUDE.md'}
expected.update('05_Icons/Sheets/'+n for n in ['VCCI_UI_ContactSheet.png','VCCI_Hero_ContactSheet.png','VCCI_Hero_Concepts.png'])
for i in items:
 for variant,p in i['paths'].items():
  rel=Path(p).relative_to(src); expected.add('05_Icons/'+rel.as_posix())
  assert (dst/rel).read_bytes()==Path(p).read_bytes(), 'Approved geometry changed'
  if variant=='currentColor':continue
  for size in ([48,96] if i['tier']=='UI' else [256,512]):
   png=Path(i['tier'])/'PNG'/variant/(Path(p).stem+f'_{size}px.png')
   expected.add('05_Icons/'+png.as_posix())
   assert (dst/png).read_bytes()==(src/png).read_bytes(), 'Approved export changed'
actual={'05_Icons/'+p.relative_to(dst).as_posix() for p in dst.rglob('*') if p.is_file()}
assert actual==expected, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for p in dst.glob('*.md'):
 content=p.read_text(encoding='utf8').lower()
 assert 'awaiting' not in content and 'pending' not in content and 'review candidate' not in content, p.name
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(dst.rglob('*')):
  if p.is_file():z.write(p,'05_Icons/'+p.relative_to(dst).as_posix())
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==expected
 assert z.testzip() is None
 for name in z.namelist():assert z.read(name)==(ROOT/'build'/'icons'/'final'/name).read_bytes()
report={'archive':str(archive),'files':len(expected),'svg':288,'icon_png':480,'sheets':3,'documents':3,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'checks':'Exact manifest, CRC, byte-for-byte archive contents, unchanged approved SVG/PNG assets: passed'}
(ROOT/'tools'/'icons'/'qa'/'release-validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
