"""Test tools/install_skill.py:  python tools/test_install_skill.py
Installs outside the repository, runs the Word and PowerPoint pipelines from the copy (no VCCI_BRAND_ROOT), compares
them with the same pipelines run inside the repository, and checks the refusals."""
import os, subprocess, sys, tempfile, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALL = os.path.join(REPO, 'tools', 'install_skill.py')
env = {k: v for k, v in os.environ.items() if k != 'VCCI_BRAND_ROOT'}
env['PYTHONIOENCODING'] = 'utf-8'
results = []

def run(args, cwd):
    return subprocess.run([sys.executable] + args, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8')

def check(name, ok, detail=''):
    results.append(ok)
    print(f'[{"PASS" if ok else "FAIL"}] {name}' + (f': {detail}' if detail and not ok else ''))

def parts(path):
    with zipfile.ZipFile(path) as z:
        # docProps and the chart workbooks (ppt/embeddings, written by XlsxWriter) carry creation times
        return {n: z.read(n) for n in z.namelist() if not n.startswith(('docProps/', 'ppt/embeddings/'))}

def pipelines(skill, work):
    """Run render_report and render_deck on the skill's own examples; return the output paths."""
    out = {}
    for kind, script, src, ext in (('word', 'scripts/word/render_report.py', 'examples/sample-report.md', '.docx'),
                                   ('ppt', 'scripts/ppt/render_deck.py', 'examples/sample-deck.md', '.pptx')):
        dst = os.path.join(work, f'{kind}{ext}')
        r = run([os.path.join(skill, script), os.path.join(skill, src), '-o', dst], cwd=work)
        out[kind] = (r, dst)
    return out

with tempfile.TemporaryDirectory() as tmp:
    dest = os.path.join(tmp, 'agent', 'skills', 'vcci-brand')
    r = run([INSTALL, '--dest', dest], cwd=tmp)
    check('install --dest succeeds', r.returncode == 0, r.stderr[-300:])
    marker = os.path.join(dest, 'brand-root.txt')
    check('brand-root.txt names the clone', os.path.isfile(marker) and open(marker, encoding='utf-8').read().strip() == REPO)
    check('the copy has SKILL.md, scripts and references',
          all(os.path.exists(os.path.join(dest, p)) for p in ('SKILL.md', 'scripts/word/render_report.py', 'scripts/ppt/render_deck.py', 'references/word-markdown.md')))
    check('no __pycache__ copied', not any('__pycache__' in d for d, _, _ in os.walk(dest)))

    work_out, work_in = os.path.join(tmp, 'work-out'), os.path.join(tmp, 'work-in')
    os.makedirs(work_out); os.makedirs(work_in)
    installed = pipelines(dest, work_out)
    reference = pipelines(os.path.join(REPO, 'skills', 'vcci-brand'), work_in)
    for kind in ('word', 'ppt'):
        r, path = installed[kind]
        check(f'{kind}: the installed copy renders outside the repository, without VCCI_BRAND_ROOT',
              r.returncode == 0 and os.path.isfile(path), (r.stderr or r.stdout)[-300:])
        r2, path2 = reference[kind]
        same = os.path.isfile(path) and os.path.isfile(path2) and parts(path) == parts(path2)
        check(f'{kind}: output identical to the repository copy (same template, icons, media)', same)

    # a moved clone must give a clear message, not a traceback
    open(marker, 'w', encoding='utf-8').write(os.path.join(tmp, 'moved-away') + '\n')
    r = run([os.path.join(dest, 'scripts/word/render_report.py'), os.path.join(dest, 'examples/sample-report.md'), '-o', 'x.docx'], cwd=work_out)
    check('a stale brand-root.txt stops with an explanation', r.returncode != 0 and 'brand-root.txt points to' in r.stderr and 'Traceback' not in r.stderr, r.stderr[-300:])
    env['VCCI_BRAND_ROOT'] = REPO
    r = run([os.path.join(dest, 'scripts/word/render_report.py'), os.path.join(dest, 'examples/sample-report.md'), '-o', 'y.docx'], cwd=work_out)
    check('VCCI_BRAND_ROOT still takes precedence', r.returncode == 0, r.stderr[-300:])
    del env['VCCI_BRAND_ROOT']

    # reinstall replaces an earlier copy; foreign folders are never touched
    r = run([INSTALL, '--dest', dest], cwd=tmp)
    check('reinstall replaces the earlier copy and repairs brand-root.txt', r.returncode == 0 and open(marker, encoding='utf-8').read().strip() == REPO)
    foreign = os.path.join(tmp, 'someone-else')
    os.makedirs(foreign); open(os.path.join(foreign, 'notes.txt'), 'w').write('keep me')
    r = run([INSTALL, '--dest', foreign], cwd=tmp)
    check('refuses a folder that is not the vcci-brand skill', r.returncode != 0 and os.path.isfile(os.path.join(foreign, 'notes.txt')))
    r = run([INSTALL, '--dest', os.path.join(REPO, 'skills', 'vcci-brand')], cwd=tmp)
    check('refuses to install over the skill in the repository', r.returncode != 0)
    r = run([INSTALL, '--project', os.path.join(tmp, 'proj')], cwd=tmp)
    check('--project installs into <folder>/.agents/skills/vcci-brand',
          r.returncode == 0 and os.path.isfile(os.path.join(tmp, 'proj', '.agents', 'skills', 'vcci-brand', 'SKILL.md')))
    r = run([INSTALL, '--dest', dest, '--uninstall'], cwd=tmp)
    check('--uninstall removes it', r.returncode == 0 and not os.path.exists(dest))

print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
sys.exit(0 if all(results) else 1)
