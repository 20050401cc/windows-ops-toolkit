# Computer Use Lite

> 用任何多模态 API 实现 Claude Computer Use 的核心能力 — 截屏、识屏、操控，~100 行 Python。

## 这是什么

Claude 的 [Computer Use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) 功能让 AI 能看屏幕、点鼠标、敲键盘。但它需要 Claude Pro/Max 订阅。

这个项目用 **任何支持图片输入的多模态 API**（MiMo、GPT-4V、Claude API 等）复现了核心循环：

```
截屏 → 发给 AI → AI 决定操作 → 执行 → 截屏 → ...
```

## 快速开始

```bash
pip install -r requirements.txt

# 用 MiMo API
python agent.py --api-base https://your-api.com/v1 --api-key YOUR_KEY --model mimo-v2.5

# 用 OpenAI 兼容 API
python agent.py --api-base https://api.openai.com/v1 --api-key YOUR_KEY --model gpt-4o
```

## 工作原理

```
┌──────────┐     screenshot (base64)     ┌──────────────┐
│  Screen   │ ─────────────────────────→ │  Multimodal  │
│  Capture  │                            │     LLM      │
└──────────┘                              └──────┬───────┘
       ↑                                         │
       │          JSON action plan                │
       │    {"action":"click","x":100,"y":200}    │
       │                                         ↓
┌──────────┐                            ┌──────────────┐
│ Execute   │ ←──────────────────────── │  Parse JSON  │
│ pyautogui │                            │   Response   │
└──────────┘                              └──────────────┘
```

1. **截屏** — `mss` 库高速截屏，转 base64
2. **发给 AI** — OpenAI 兼容 API，图片作为 `image_url` content block
3. **解析响应** — AI 返回 JSON 格式的操作指令
4. **执行操作** — `pyautogui` 模拟鼠标/键盘
5. **循环** — 回到第 1 步，直到 AI 认为任务完成

## 支持的操作

| 操作 | 参数 | 说明 |
|------|------|------|
| `screenshot` | — | 截屏分析 |
| `click` | `x`, `y`, `button` | 鼠标点击 |
| `double_click` | `x`, `y` | 双击 |
| `right_click` | `x`, `y` | 右键 |
| `type` | `text` | 打字 |
| `key` | `key` | 按键（如 `enter`, `ctrl+s`） |
| `scroll` | `x`, `y`, `dx`, `dy` | 滚动 |
| `drag` | `x1`, `y1`, `x2`, `y2` | 拖拽 |
| `done` | `summary` | 任务完成 |

## 配置

```bash
python agent.py \
  --api-base https://your-api.com/v1 \
  --api-key YOUR_KEY \
  --model mimo-v2.5 \
  --task "打开浏览器搜索明日方舟" \
  --max-steps 20 \
  --screenshot-quality 80 \
  --resolution 1920x1080
```

## 安全提示

- 建议在虚拟机或沙箱中运行
- 不要在有敏感数据的环境使用
- AI 可能被网页上的 prompt injection 误导
- 始终保持人工监督

## 致谢

- [Anthropic Computer Use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) — 原始设计
- [mss](https://github.com/BoboTiG/python-mss) — 高速截屏
- [pyautogui](https://github.com/asweigart/pyautogui) — 鼠标键盘控制

## License

MIT
