"""Install the vcci-brand skill for an AI agent, from this clone of vcci-brand-identity.

    python tools/install_skill.py codex                 ~/.agents/skills/vcci-brand          (OpenAI Codex)
    python tools/install_skill.py antigravity           ~/.gemini/config/skills/vcci-brand   (Google Antigravity)
    python tools/install_skill.py antigravity-cli       ~/.gemini/antigravity-cli/skills/vcci-brand
    python tools/install_skill.py claude                ~/.claude/skills/vcci-brand          (Claude Code, without the plugin)
    python tools/install_skill.py --project <folder>    <folder>/.agents/skills/vcci-brand   (one project; Codex and Antigravity)
    python tools/install_skill.py --dest <folder>       exactly <folder>
    add --uninstall to remove the skill from that place

The skill is copied (Windows cannot symlink without administrator rights), with brand-root.txt naming this clone, so its
scripts find the templates and icons in brand-assets/ without VCCI_BRAND_ROOT. Run it again after `git pull`.
Skill folders as documented by OpenAI (developers.openai.com/codex/skills) and Google (Antigravity skills codelab), 10/2026.
"""
import argparse, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, 'skills', 'vcci-brand')
HOME = os.path.expanduser('~')
TOOLS = {
    'codex': os.path.join(HOME, '.agents', 'skills'),
    'antigravity': os.path.join(HOME, '.gemini', 'config', 'skills'),
    'antigravity-cli': os.path.join(HOME, '.gemini', 'antigravity-cli', 'skills'),
    'claude': os.path.join(HOME, '.claude', 'skills'),
}


def is_vcci_skill(folder):
    p = os.path.join(folder, 'SKILL.md')
    return os.path.isfile(p) and re.search(r'^name:\s*vcci-brand\s*$', open(p, encoding='utf-8').read(), re.M)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('tool', nargs='?', choices=sorted(TOOLS))
    ap.add_argument('--project', help='install for one project: <folder>/.agents/skills/vcci-brand')
    ap.add_argument('--dest', help='install into exactly this folder')
    ap.add_argument('--uninstall', action='store_true')
    a = ap.parse_args()
    if sum(x is not None for x in (a.tool, a.project, a.dest)) != 1:
        ap.error('give one of: a tool name, --project <folder>, --dest <folder>')
    dest = (os.path.abspath(a.dest) if a.dest else
            os.path.join(os.path.abspath(a.project), '.agents', 'skills', 'vcci-brand') if a.project else
            os.path.join(TOOLS[a.tool], 'vcci-brand'))
    if os.path.normcase(os.path.abspath(dest)).startswith(os.path.normcase(SKILL)):
        sys.exit('The destination is the skill in this repository itself.')
    if os.path.exists(dest) and os.listdir(dest) and not is_vcci_skill(dest):
        sys.exit(f'{dest} exists and is not the vcci-brand skill; not touching it.')
    if a.uninstall:
        if not os.path.exists(dest): sys.exit(f'Nothing installed at {dest}.')
        shutil.rmtree(dest)
        print(f'Removed {dest}')
        return
    if os.path.exists(dest): shutil.rmtree(dest)   # an earlier copy of this skill
    shutil.copytree(SKILL, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'brand-root.txt'))
    open(os.path.join(dest, 'brand-root.txt'), 'w', encoding='utf-8').write(ROOT + '\n')
    print(f'Installed vcci-brand -> {dest}')
    print(f'Templates and icons are read from {ROOT}; keep this clone there and run this command again after git pull.')
    print('The scripts need Python 3.9+ with: pip install lxml pillow python-pptx')
    if a.tool or a.project: print('Restart the agent if the skill does not appear.')


if __name__ == '__main__':
    main()
