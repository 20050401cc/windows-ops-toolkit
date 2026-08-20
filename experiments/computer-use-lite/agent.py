"""
Computer Use Lite — 用任何多模态 API 实现截屏→识屏→操控循环。

支持 OpenAI 兼容 API（MiMo、GPT-4V、Claude via proxy 等）。
"""

import argparse
import base64
import io
import json
import sys
import time
from typing import Any

import mss
import mss.tools
import pyautogui
import requests
from PIL import Image

# ---------------------------------------------------------------------------
# 截屏
# ---------------------------------------------------------------------------

def take_screenshot(region: tuple[int, int, int, int] | None = None, quality: int = 80) -> str:
    """截屏并返回 base64 编码的 JPEG。"""
    with mss.mss() as sct:
        monitor = sct.monitors[1] if region is None else {
            "left": region[0], "top": region[1],
            "width": region[2], "height": region[3],
        }
        raw = sct.grab(monitor)
        img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        return base64.b64encode(buf.getvalue()).decode()


def get_screen_size() -> tuple[int, int]:
    """获取主屏幕分辨率。"""
    with mss.mss() as sct:
        mon = sct.monitors[1]
        return mon["width"], mon["height"]

# ---------------------------------------------------------------------------
# 调用多模态 API（OpenAI 兼容格式）
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a computer-use agent. You can see the user's screen via screenshots and control it.

When you receive a screenshot, analyze it and decide the next action.
Respond with a JSON object (no markdown, no explanation outside JSON):

{
  "thought": "brief reasoning about what you see and what to do next",
  "action": "click|double_click|right_click|type|key|scroll|drag|done",
  "params": { ... }
}

Action parameters:
- click: {"x": int, "y": int, "button": "left"|"right"}
- double_click: {"x": int, "y": int}
- right_click: {"x": int, "y": int}
- type: {"text": "string to type"}
- key: {"key": "enter|tab|escape|backspace|delete|ctrl+c|ctrl+v|ctrl+s|alt+tab|..."}
- scroll: {"x": int, "y": int, "amount": int}  (positive=up, negative=down)
- drag: {"x1": int, "y1": int, "x2": int, "y2": int}
- done: {"summary": "what was accomplished"}

Always respond with valid JSON only. No markdown fences.
"""


def call_api(
    api_base: str,
    api_key: str,
    model: str,
    screenshot_b64: str,
    screen_w: int,
    screen_h: int,
    task: str,
    history: list[dict],
) -> dict:
    """调用 OpenAI 兼容的多模态 API。"""
    url = f"{api_base.rstrip('/')}/chat/completions"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Task: {task}\nScreen: {screen_w}x{screen_h}\nWhat should I do next?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{screenshot_b64}",
                        "detail": "low",
                    },
                },
            ],
        },
    ]

    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.1,
        },
        timeout=60,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]

    # 尝试解析 JSON（兼容 markdown fences）
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    return json.loads(content)

# ---------------------------------------------------------------------------
# 执行操作
# ---------------------------------------------------------------------------

# pyautogui 安全设置
pyautogui.FAILSAFE = True  # 鼠标移到左上角触发异常
pyautogui.PAUSE = 0.3

MOUSE_BUTTON_MAP = {"left": "left", "right": "right", "middle": "middle"}


def execute_action(action: dict) -> str:
    """执行 AI 返回的操作，返回描述。"""
    act = action.get("action", "")
    params = action.get("params", {})

    if act == "click":
        btn = MOUSE_BUTTON_MAP.get(params.get("button", "left"), "left")
        pyautogui.click(params["x"], params["y"], button=btn)
        return f"Clicked ({params['x']}, {params['y']}) {btn}"

    elif act == "double_click":
        pyautogui.doubleClick(params["x"], params["y"])
        return f"Double-clicked ({params['x']}, {params['y']})"

    elif act == "right_click":
        pyautogui.rightClick(params["x"], params["y"])
        return f"Right-clicked ({params['x']}, {params['y']})"

    elif act == "type":
        pyautogui.typewrite(params["text"], interval=0.03) if params["text"].isascii() else pyautogui.write(params["text"])
        return f"Typed: {params['text'][:50]}"

    elif act == "key":
        pyautogui.hotkey(*params["key"].split("+")) if "+" in params["key"] else pyautogui.press(params["key"])
        return f"Key: {params['key']}"

    elif act == "scroll":
        x, y = params.get("x", 960), params.get("y", 540)
        amount = params.get("amount", -3)
        pyautogui.scroll(amount, x=x, y=y)
        return f"Scrolled {amount} at ({x}, {y})"

    elif act == "drag":
        pyautogui.moveTo(params["x1"], params["y1"])
        pyautogui.drag(
            params["x2"] - params["x1"],
            params["y2"] - params["y1"],
            duration=0.5,
        )
        return f"Dragged ({params['x1']},{params['y1']}) → ({params['x2']},{params['y2']})"

    elif act == "done":
        return f"DONE: {params.get('summary', 'Task completed')}"

    else:
        return f"Unknown action: {act}"

# ---------------------------------------------------------------------------
# 主循环
# ---------------------------------------------------------------------------

def run_agent(
    api_base: str,
    api_key: str,
    model: str,
    task: str,
    max_steps: int = 20,
    screenshot_quality: int = 80,
    verbose: bool = True,
) -> str:
    """运行 agent loop：截屏→AI→执行→循环。"""
    screen_w, screen_h = get_screen_size()
    history: list[dict] = []

    print(f"🖥  Screen: {screen_w}x{screen_h}")
    print(f"🤖 Model: {model}")
    print(f"📋 Task: {task}")
    print(f"🔄 Max steps: {max_steps}")
    print("=" * 60)

    for step in range(1, max_steps + 1):
        print(f"\n--- Step {step}/{max_steps} ---")

        # 1. 截屏
        screenshot_b64 = take_screenshot(quality=screenshot_quality)
        if verbose:
            print(f"📸 Screenshot captured ({len(screenshot_b64) // 1024} KB)")

        # 2. 调用 AI
        try:
            action = call_api(api_base, api_key, model, screenshot_b64, screen_w, screen_h, task, history)
        except json.JSONDecodeError as e:
            print(f"⚠️  AI 返回了非 JSON 响应: {e}")
            # 重试一次
            history.append({"role": "assistant", "content": json.dumps(action) if 'action' in dir() else "{}"})
            history.append({"role": "user", "content": "Please respond with valid JSON only."})
            continue
        except Exception as e:
            print(f"❌ API error: {e}")
            time.sleep(2)
            continue

        thought = action.get("thought", "")
        if verbose and thought:
            print(f"💭 {thought}")

        # 3. 执行
        result = execute_action(action)
        print(f"▶️  {result}")

        # 4. 检查是否完成
        if action.get("action") == "done":
            print(f"\n✅ {result}")
            return result

        # 5. 记录历史（只保留最近 3 轮避免 token 爆炸）
        history.append({
            "role": "assistant",
            "content": json.dumps(action, ensure_ascii=False),
        })
        history.append({
            "role": "user",
            "content": f"Action executed: {result}",
        })
        if len(history) > 6:
            history = history[-6:]

        # 等一下让 UI 响应
        time.sleep(1)

    print("\n⏰ Reached max steps")
    return "Max steps reached"

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Computer Use Lite — 用多模态 API 控制电脑")
    parser.add_argument("--api-base", required=True, help="API base URL (OpenAI 兼容)")
    parser.add_argument("--api-key", required=True, help="API key")
    parser.add_argument("--model", required=True, help="模型名称")
    parser.add_argument("--task", required=True, help="要执行的任务描述")
    parser.add_argument("--max-steps", type=int, default=20, help="最大步数 (default: 20)")
    parser.add_argument("--screenshot-quality", type=int, default=80, help="截图质量 1-100 (default: 80)")
    parser.add_argument("--quiet", action="store_true", help="减少输出")
    args = parser.parse_args()

    run_agent(
        api_base=args.api_base,
        api_key=args.api_key,
        model=args.model,
        task=args.task,
        max_steps=args.max_steps,
        screenshot_quality=args.screenshot_quality,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
