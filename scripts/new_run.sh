#!/usr/bin/env bash
# 新建一次生产任务的目录骨架：assets/ + shots.json（镜头状态） + DECISIONS.md（决策日志）
# 用法: new_run.sh <主题slug>   例: new_run.sh city-sunrise
set -euo pipefail

SLUG="${1:?usage: new_run.sh <主题slug>}"
RUN_DIR="$HOME/workspace/openmontage-muse/runs/$(date +%F)-${SLUG}"
mkdir -p "$RUN_DIR/assets"

cat > "$RUN_DIR/shots.json" <<EOF
{
  "topic": "${SLUG}",
  "created": "$(date -Iseconds)",
  "quota": {"video_limit": 6, "image_limit": 4, "videos_used": 0, "images_used": 0},
  "note": "quota 记账含样片和重生成；每次成功生成后更新 videos_used/images_used",
  "shots": []
}
EOF

cat > "$RUN_DIR/DECISIONS.md" <<EOF
# 决策日志（append-only，只追加不修改历史）

- $(date -Iseconds) run 创建：${SLUG}
EOF

echo "run 目录已创建: $RUN_DIR"
echo "往 shots.json 的 shots 数组里追加镜头条目，格式:"
echo '  {"id":1,"scene":"画面描述","status":"pending","clip":null,"narration":null,"snapshot_id":null,"note":""}'
echo 'status 取值: pending / sample / done / failed（失败只重做对应镜头）'
