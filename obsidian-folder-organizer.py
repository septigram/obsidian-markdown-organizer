"""Obsidian File Organizer Tool

This tool moves Obsidian Markdown files to folders based on tags.
"""
import os
import glob
import yaml
from lark import Lark, Transformer, v_args

# Grammar definition for rule expressions
RULE_GRAMMAR = r"""
    ?start: expr
    ?expr: expr "and" expr   -> and_expr
         | expr "or" expr    -> or_expr
         | "not" expr        -> not_expr
         | "(" expr ")"      -> paren_expr
         | tag_expr
    tag_expr: "tag:" TAGNAME
    TAGNAME: /[A-Za-z0-9_-]+/
    %import common.WS
    %ignore WS
"""

# Transformer for evaluating rule expressions
@v_args(inline=True)
class RuleEval(Transformer):
    def __init__(self, tags):
        self.tags = set(tags)
    def and_expr(self, a, b):
        return a and b
    def or_expr(self, a, b):
        return a or b
    def not_expr(self, a):
        return not a
    def paren_expr(self, a):
        return a
    def tag_expr(self, tagname):
        return str(tagname) in self.tags

def extract_yaml_block(md_path):
    """Extract the YAML block at the beginning of the file and return as a dict. Return None if not found."""
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()
    if not lines or lines[0].strip() != '---':
        return None
    yaml_lines = []
    for line in lines[1:]:
        if line.strip() == '---':
            break
        yaml_lines.append(line)
    if not yaml_lines:
        return None
    return yaml.safe_load(''.join(yaml_lines))

def load_rules(yaml_path):
    with open(yaml_path, encoding='utf-8') as f:
        return yaml.safe_load(f)['rules']

def main():
    rules = load_rules('rules.yaml')
    parser = Lark(RULE_GRAMMAR, parser='lalr')
    move_plan = []

    for md_path in glob.glob('*.md'):
        meta = extract_yaml_block(md_path)
        if not meta or 'tags' not in meta:
            continue
        tags = meta['tags']
        if not isinstance(tags, list):
            continue
        for rule in rules:
            tree = parser.parse(rule['when'])
            if RuleEval(tags).transform(tree):
                then = rule['then']
                if then.startswith('move to '):
                    folder = then[len('move to '):].strip()
                    move_plan.append({
                        'file': md_path,
                        'rule': rule['name'],
                        'dest': folder
                    })
                break

    if not move_plan:
        print('No files to move.')
        return

    print('The following files will be moved:')
    for plan in move_plan:
        print(f"  {plan['file']} → {plan['dest']} (Rule: {plan['rule']})")
    ans = input('Do you want to proceed? (y/N): ').strip().lower()
    if ans != 'y':
        print('Operation cancelled.')
        return

    for plan in move_plan:
        # Move using obsidian-cli command
        cmd = f'obsidian-cli "{plan["file"]}" "{plan["dest"]}"'
        ret = os.system(cmd)
        if ret == 0:
            print(f'{plan["file"]}: {plan["rule"]} → {plan["dest"]} moved (obsidian-cli executed)')
        else:
            print(f'Failed to move {plan["file"]} to {plan["dest"]} (obsidian-cli error)')

if __name__ == '__main__':
    main() 