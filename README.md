# OpenMontage-Muse

> ⭐ **Support This Project**
>
> [![GitHub stars](https://img.shields.io/github/stars/oeaf/openmontage-muse?style=social)](https://github.com/oeaf/openmontage-muse)
> [![GitHub forks](https://img.shields.io/github/forks/oeaf/openmontage-muse?style=social)](https://github.com/oeaf/openmontage-muse)
> [![GitHub issues](https://img.shields.io/github/issues/oeaf/openmontage-muse)](https://github.com/oeaf/openmontage-muse/issues)
>
> 如果这个项目对你有用，欢迎点个 ⭐ Star！你的支持是我持续更新的动力。

把 [OpenMontage](https://github.com/calesthio/OpenMontage) 的 agentic 视频生产思想，跑在 AI 助手原生工具链上：自带视频生成做片段、Fish Audio 配音、ffmpeg 合成——不走 Veo/Kling 等付费 API。

## 快速上手

```sh
# 1. 环境预检（换环境或隔段时间后必跑）
bash scripts/preflight.sh

# 2. 新建一个任务目录
bash scripts/new_run.sh <主题>

# 3. 配音（一行搞定，自动走免费档）
bash scripts/speak.sh "旁白文案" 温柔动听女声 narration.mp3

# 4. 合成终版
bash scripts/compose.sh
```

完整生产流程（idea → 分镜 → **必做样片** → 素材 → 合成 → 审片）见 `SKILL.md`，这是给 AI Agent 用的 skill 说明。

## 文件结构

```
.
├── SKILL.md                 # 给 AI Agent 的完整生产手册（分镜/配额/硬约束）
├── scripts/
│   ├── preflight.sh         # 环境预检：ffmpeg/ffprobe/libass/脚本权限/tts.py
│   ├── new_run.sh           # 任务脚手架：shots.json 镜头状态 + DECISIONS.md
│   ├── speak.sh             # 配音：按音色名调 Fish Audio 免费档
│   └── compose.sh           # ffmpeg 合成：规格统一→拼接→混音→字幕→终版 mp4
└── fish-audio/
    ├── SKILL.md             # Fish Audio TTS 与音色库查询说明
    └── bin/
        ├── tts.py           # 文字转语音（--api-key 或 FISH_API_KEY 传 key）
        └── voices.py        # 查公开音色库
```

## 说明

- 视频/图片片段走 AI 助手原生生成能力，**计入订阅配额**（不是无限免费）；配音走 Fish Audio `s2.1-pro-free` **免费档（限时免费至 2026-11-30）**；ffmpeg 本地合成真正零费用。
- 配音 key 通过 `--api-key` 参数或 `FISH_API_KEY` 环境变量传入，不要写进仓库。
- 给用户配音前先让用户选音色（AD学姐 / 贾小军 / 温柔动听女声 / 宣传片大气浑厚 / 女大学生）；真人克隆类音色商用有肖像权风险。
- 参考视频只做风格拆解、不做 1:1 搬运。
