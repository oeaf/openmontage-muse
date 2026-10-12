#!/usr/bin/env python3
"""查询 Fish Audio 公开音色库。Key 通过 --api-key 参数或 FISH_API_KEY 环境变量传入。

用法:
  export FISH_API_KEY="your-key-here"
  python3 voices.py                      # 中文音色（默认 zh，按点赞排序）
  python3 voices.py --language en        # 英文音色
  python3 voices.py --language zh --limit 10
  python3 voices.py --title 董宇辉        # 按标题搜索
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def make_key_header(key: str) -> dict:
    return {"Authorization": f"Bearer {key}"}


def main() -> int:
    p = argparse.ArgumentParser(description="查询 Fish Audio 音色库")
    p.add_argument("--language", default="zh", help="语言过滤，如 zh/en，默认 zh")
    p.add_argument("--title", default="", help="按标题搜索")
    p.add_argument("--limit", type=int, default=30, help="返回条数，默认 30")
    p.add_argument("--api-key", default="", help="Fish Audio API key（或设 FISH_API_KEY）")
    args = p.parse_args()

    key = args.api_key or os.environ.get("FISH_API_KEY", "")
    if not key:
        print("缺少 Fish Audio key：用 --api-key 传入，或设置 FISH_API_KEY 环境变量。",
              file=sys.stderr)
        return 2
    headers = make_key_header(key)

    seen = {}
    offset = 0
    try:
        while len(seen) < args.limit and offset < 1000:
            q = urllib.parse.urlencode({
                "language": args.language,
                "offset": offset,
                "page_size": 50,
                "sort_by": "task_count",
                **({"title": args.title} if args.title else {}),
            })
            req = urllib.request.Request(
                f"https://api.fish.audio/model?{q}", headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=60) as resp:
                d = json.loads(resp.read().decode("utf-8"))
            items = d.get("items", [])
            if not items:
                break
            for m in items:
                seen[m["_id"]] = m
            offset += 50
            if offset >= (d.get("total") or 0):
                break
    except Exception as e:
        print(f"查询失败: {e}", file=sys.stderr)
        return 1

    voices = sorted(seen.values(), key=lambda m: m.get("like_count", 0), reverse=True)
    print(f"找到 {len(voices)} 个音色（language={args.language}）：")
    for m in voices[:args.limit]:
        tags = ",".join(m.get("tags", [])[:8])
        print(f"- {m['title']} | 点赞 {m.get('like_count')} | 标签 {tags}")
        print(f"    id={m['_id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
