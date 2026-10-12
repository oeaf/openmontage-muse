#!/usr/bin/env bash
# openmontage-muse 环境预检：换环境 / 隔段时间后先跑这个
# 用法: preflight.sh
set -uo pipefail

ok=1
check() { # check <描述> <命令...>
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "✓ $desc"; else echo "✗ $desc"; ok=0; fi
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "== 基础依赖 =="
check "ffmpeg 可用" command -v ffmpeg
check "ffprobe 可用" command -v ffprobe
check "python3 可用" command -v python3
if ffmpeg -hide_banner -h filter=subtitles 2>/dev/null | grep -q libass; then
  echo "✓ 字幕支持 (libass)"
else
  echo "✗ 字幕支持 (libass) —— compose.sh 会自动跳过字幕"; ok=0
fi

echo "== 脚本 =="
check "speak.sh 可执行" test -x "$SCRIPT_DIR/speak.sh"
check "compose.sh 可执行" test -x "$SCRIPT_DIR/compose.sh"

echo "== Fish Audio =="
if [ -f "$SCRIPT_DIR/../fish-audio/bin/tts.py" ]; then
  echo "✓ tts.py（包内自带）"
elif [ -f "$HOME/workspace/skills/fish-audio/bin/tts.py" ]; then
  echo "✓ tts.py（skills 目录已安装）"
else
  echo "✗ 找不到 tts.py"; ok=0
fi

echo "== 链接分析（可选：reference 流程用） =="
if command -v yt-dlp >/dev/null 2>&1; then
  echo "✓ yt-dlp 可用（可抓链接元数据/自动字幕）"
else
  echo "· 未装 yt-dlp —— 只有接到视频链接任务时才需要（pip install yt-dlp）；不影响正常生产"
fi

echo "== 结论 =="
if [ "$ok" -eq 1 ]; then echo "全部通过，可以生产"; else echo "有未通过项，先修好再生产"; fi
exit $((1 - ok))
