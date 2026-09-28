#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成済み Vault に Obsidian 設定（.obsidian）を書き込む.

- Dataview / Spaced Repetition を最新リリースから取得して導入・有効化。
- Spaced Repetition の Flashcard tags を #SC に設定（CAMS/<sc> がサブデッキになる）。
使い方: python3 build/obsidian_setup.py [VAULT_DIR]
（初回に開くと Obsidian が「作者を信頼しますか？」と聞くので信頼を選ぶ）
"""
import os, sys, json, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "output", "SC_Obsidian_Vault")
CONF = os.path.join(VAULT, ".obsidian")

PLUGINS = {  # plugin id -> GitHub repo
    "dataview": "blacksmithgu/obsidian-dataview",
    "obsidian-spaced-repetition": "st3v3nmw/obsidian-spaced-repetition",
}
PLUGIN_DATA = {
    "obsidian-spaced-repetition": {"settings": {"flashcardTags": ["#SC"]}},
}

def fetch(url, dest):
    with urllib.request.urlopen(url, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())

for pid, repo in PLUGINS.items():
    d = os.path.join(CONF, "plugins", pid)
    os.makedirs(d, exist_ok=True)
    for fn in ("main.js", "manifest.json", "styles.css"):
        fetch(f"https://github.com/{repo}/releases/latest/download/{fn}", os.path.join(d, fn))
    if pid in PLUGIN_DATA:
        json.dump(PLUGIN_DATA[pid], open(os.path.join(d, "data.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    ver = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))["version"]
    print(f"{pid} {ver}")

json.dump(list(PLUGINS), open(os.path.join(CONF, "community-plugins.json"), "w", encoding="utf-8"), indent=2)
print(f".obsidian -> {CONF}")
