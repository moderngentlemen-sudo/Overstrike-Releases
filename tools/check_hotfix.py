#!/usr/bin/env python3
"""Checks hotfix.txt the way the game reads it: the format, the @settings and that every value is a
number or true/false within range. Whether each path names a real value is checked in the Unity
editor (Sixfold > Hotfix > Check Hotfix File...), which knows the hero data.

Usage: python3 tools/check_hotfix.py [hotfix.txt]
"""
import math
import re
import sys

MAX_BYTES = 64 * 1024
MAX_LINES = 4000
MAX_MAGNITUDE = 100000
SETTINGS = {"id", "notes", "game", "latest", "download"}
PATH = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+$")
VERSION = re.compile(r"^\d+(\.\d+)*$")
BOOLS = {"true", "false", "1", "0", "on", "off", "yes", "no"}


def check(text):
    problems = []
    if len(text.encode("utf-8")) > MAX_BYTES:
        return [f"the file is larger than {MAX_BYTES // 1024} KB"]
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if len(lines) > MAX_LINES:
        return [f"the file has more than {MAX_LINES} lines"]
    seen, settings, values = {}, {}, 0
    for n, raw in enumerate(lines, 1):
        line = raw
        if "#" in line and not line.lstrip().lower().startswith("@download"):
            line = line[: line.index("#")]
        line = line.strip()
        if not line:
            continue
        if "=" not in line or line.index("=") == 0:
            problems.append(f"line {n}: expected 'name = value'")
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if key.startswith("@"):
            name = key[1:].lower()
            if name not in SETTINGS:
                problems.append(f"line {n}: unknown setting '{key}'")
            elif name in ("game", "latest") and value and not VERSION.match(value):
                problems.append(f"line {n}: '{value}' is not a version like 0.9.0")
            elif name == "download" and value and not value.startswith("https://"):
                problems.append(f"line {n}: the download link must start with https://")
            settings[name] = value
            continue
        if not value:
            problems.append(f"line {n}: '{key}' has no value")
            continue
        if not PATH.match(key):
            problems.append(f"line {n}: '{key}' is not a path like wisp.ReloadSeconds")
            continue
        if key.lower() in seen:
            problems.append(f"line {n}: '{key}' is already set on line {seen[key.lower()]} (the later line wins)")
        seen[key.lower()] = n
        values += 1
        if value.lower() in BOOLS:
            continue
        number = value[:-1] if value.lower().endswith("f") else value
        try:
            v = float(number)
        except ValueError:
            problems.append(f"line {n}: '{value}' is not a number or true/false")
            continue
        if math.isnan(v) or math.isinf(v) or abs(v) > MAX_MAGNITUDE:
            problems.append(f"line {n}: {value} is out of range")
    if not settings.get("id"):
        problems.append("@id is missing: players only see a hotfix as new when its id changes")
    return problems, settings, values


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "hotfix.txt"
    with open(path, encoding="utf-8") as f:
        result = check(f.read())
    if isinstance(result, list):
        problems, settings, values = result, {}, 0
    else:
        problems, settings, values = result
    for p in problems:
        print(f"{path}: {p}")
    print(f"{path}: hotfix '{settings.get('id', '')}' for game {settings.get('game') or 'any version'}: "
          f"{values} value line(s), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
