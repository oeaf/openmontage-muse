#!/usr/bin/env python3
"""Fish Audio TTS 合成。Key 通过 --api-key 参数或 FISH_API_KEY 环境变量传入。

用法:
  export FISH_API_KEY="your-key-here"
  python3 tts.py "要合成的文字" out.mp3
  python3 tts.py "要合成的文字" out.mp3 --reference-id <voice_id>
  python3 tts.py "要合成的文字" out.mp3 --model s2.1-pro
  python3 tts.py "要合成的文字" out.mp3 --api-key <key>
"""
import argparse
import json
import os
import sys
import urllib.request

FREE_MODEL = "s2.1-pro-free"


def resolve_key(args) -> str:
    key = args.api_key or os.environ.get("FISH_API_KEY", "")
    if not key:
        print("缺少 Fish Audio key：用 --api-key 传入，或设置 FISH_API_KEY 环境变量。",
              file=sys.stderr)
        sys.exit(2)
    return key


def read_body(resp) -> bytes:
    chunks = []
    while True:
        data = resp.read(65536)
        if not data:
            break
        chunks.append(data)
    return b"".join(chunks)


def main() -> int:
    p = argparse.ArgumentParser(description="Fish Audio TTS 合成")
    p.add_argument("text", help="要合成的文字")
    p.add_argument("output", help="输出音频路径")
    p.add_argument("--reference-id", default="", help="音色模型 id（留空用默认音色）")
    p.add_argument("--model", default=FREE_MODEL,
                   help=f"后端模型，默认 {FREE_MODEL}（免费档）")
    p.add_argument("--format", default="mp3", help="输出格式 mp3/wav/opus，默认 mp3")
    p.add_argument("--api-key", default="", help="Fish Audio API key（或设 FISH_API_KEY）")
    args = p.parse_args()
    key = resolve_key(args)

    body = {"text": args.text, "format": args.format}
    if args.reference_id:
        body["reference_id"] = args.reference_id
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        "https://api.fish.audio/v1/tts",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "model": args.model,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            audio = read_body(resp)
    except Exception as e:
        print(f"合成请求失败: {e}", file=sys.stderr)
        return 1

    with open(args.output, "wb") as f:
        f.write(audio)
    print(f"已保存: {args.output}（{len(audio)} 字节，模型 {args.model}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
