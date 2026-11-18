#!/usr/bin/env python3
"""Converts the TOML behavior rules into rule library YAML files.

Reads src/behavior/rules/<folder>/<name>.toml and writes rules/<folder>/<name>.yml, one
{ id, type: "security-rule", attributes } document per file. Python 3.11+, standard library only.
"""

import argparse
import json
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

RESERVED_WORDS = {'true', 'false', 'yes', 'no', 'on', 'off', 'y', 'n', 'null', '~'}
PLAIN_STRING = re.compile(r'^[A-Za-z_][A-Za-z0-9 _./()-]*$')
LINE_SEPARATORS = {'\u0085': '\\u0085', ' ': '\\u2028', ' ': '\\u2029'}
INDENT = '  '


def quote(text: str) -> str:
    quoted = json.dumps(text, ensure_ascii=False)
    for char, escape in LINE_SEPARATORS.items():
        quoted = quoted.replace(char, escape)
    return quoted


def is_literal_safe(text: str) -> bool:
    if '\n' not in text or text.endswith('\n\n') or text[0] in ' \t\n':
        return False
    if not all(char == '\n' or char == '\t' or char.isprintable() for char in text):
        return False
    return not any(line != line.rstrip() for line in text.split('\n'))


def format_scalar(value) -> str:
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return json.dumps(value)
    if value and PLAIN_STRING.match(value) and value.lower() not in RESERVED_WORDS and value == value.strip():
        return value
    return quote(value)


def emit(value, depth: int) -> list:
    pad = INDENT * depth
    if isinstance(value, dict):
        if not value:
            return [pad + '{}']
        lines = []
        for key in value:
            lines.extend(emit_entry(pad + format_scalar(key) + ':', value[key], depth))
        return lines
    if isinstance(value, list):
        if not value:
            return [pad + '[]']
        lines = []
        for item in value:
            if isinstance(item, (dict, list)) and item:
                nested = emit(item, depth + 1)
                lines.append(pad + '- ' + nested[0].lstrip())
                lines.extend(nested[1:])
            else:
                lines.extend(emit_entry(pad + '-', item, depth))
        return lines
    return [pad + format_scalar(value)]


def emit_entry(head: str, value, depth: int) -> list:
    if isinstance(value, (dict, list)) and value:
        return [head] + emit(value, depth + 1)
    if isinstance(value, (dict, list)):
        return [head + ' ' + ('{}' if isinstance(value, dict) else '[]')]
    if isinstance(value, str) and is_literal_safe(value):
        chomp = '|' if value.endswith('\n') else '|-'
        body = value[:-1] if value.endswith('\n') else value
        block_pad = INDENT * (depth + 1)
        return [head + ' ' + chomp] + [(block_pad + line) if line else '' for line in body.split('\n')]
    return [head + ' ' + format_scalar(value)]


def to_document(toml_data: dict) -> dict:
    attributes = {('rule_id' if key == 'id' else key): value for key, value in toml_data['rule'].items()}
    attributes.update({key: value for key, value in toml_data.items() if key != 'rule'})
    return {
        'id': f"{attributes['rule_id']}_{attributes['version']}",
        'type': 'security-rule',
        'attributes': attributes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default='src/behavior/rules', type=Path)
    parser.add_argument('--out', default='rules', type=Path)
    args = parser.parse_args()

    sources = sorted(args.source.glob('*/*.toml'))
    if not sources:
        print(f'no .toml files under {args.source}', file=sys.stderr)
        return 1

    folders = {path.parent.name for path in sources}
    for folder in folders:
        for stale in (args.out / folder).glob('*.yml'):
            stale.unlink()

    locations = defaultdict(list)
    for path in sources:
        with path.open('rb') as handle:
            document = to_document(tomllib.load(handle))
        target = args.out / path.parent.name / (path.stem + '.yml')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('\n'.join(emit(document, 0)) + '\n', encoding='utf-8', newline='\n')
        locations[document['id']].append(target)

    print(f'wrote {len(sources)} rules to {args.out}')
    for rule_id, targets in sorted(locations.items()):
        if len(targets) > 1:
            print(f'warning: {rule_id} is in {len(targets)} files: ' + ', '.join(str(t) for t in targets))
    return 0


if __name__ == '__main__':
    sys.exit(main())
