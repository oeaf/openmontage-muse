---
name: "fish_audio"
description: "Fish Audio 语音合成与音色库查询：用户提到 Fish Audio、要合成语音/配音、或要查 Fish 音色时使用。"
---

# Fish Audio

## Purpose
通过 Fish Audio API key 调用 Fish Audio TTS：把文字合成为语音（支持中文及 80+ 语言、声音克隆音色），以及查询官方公开音色库。

## Tooling
`bin/tts.py` — 文字转语音：
```sh
python3 bin/tts.py "要合成的文字" out.mp3
python3 bin/tts.py "文字" out.mp3 --reference-id <音色id>
python3 bin/tts.py "文字" out.mp3 --model s2.1-pro
```
默认走 `s2.1-pro-free` 免费模型（$0，限时免费至 2026-11-30）。合成成功打印输出路径与字节数，输出即音频文件本身。

`bin/voices.py` — 查音色库：
```sh
python3 bin/voices.py                 # 中文音色，按人气排序
python3 bin/voices.py --language en  # 英文音色
python3 bin/voices.py --title 董宇辉  # 按标题搜索
```

## Auth
Key 通过 `--api-key` 参数或 `FISH_API_KEY` 环境变量传入，两个 CLI 用它拼 `Authorization: Bearer` 头。不要把 key 写进仓库文件或日志。

401/403 先检查请求是否真的带上了凭证（没走 helper 的请求就是没带）；确认带上仍被拒绝，才调用 `credentials.request_api_access`（带 `reconnect`）更换凭证。

## Operating Rules
1. 用户要合成语音、配音、读文案，或提到 Fish Audio 时用本 skill。
2. 已认证请求只发往 `api.fish.audio`。
3. 不打印、不记录、不持久化任何原始凭证。
4. 合成中文时确保文本为中文（免费模型自动识别语言，无需传语言参数）。
5. 长文案先分段再逐段合成，避免单次请求过长；合成后按需用 ffmpeg 拼接。
6. 商用前提醒：真人克隆类音色（名人/UP 主）有肖像权风险，官方可能下架；免费档无 SLA、请求可能被用于改进模型，不适合生产环境。
