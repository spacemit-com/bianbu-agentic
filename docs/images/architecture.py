#!/usr/bin/env python3
"""Generate docs/images/architecture-{zh,en}.svg for bianbu-agentic.

Usage:
    python3 docs/images/architecture.py zh docs/images/architecture-zh.svg
    python3 docs/images/architecture.py en docs/images/architecture-en.svg

The SVGs are the source of truth; render the PNG used by the README with any
SVG-to-PNG renderer (rsvg-convert, Inkscape, or a short node script built on
@resvg/resvg-js).
"""

import sys

W, H = 1240, 852

INK = "#2C2C2A"
MUT = "#5F5E5A"
HINT = "#888780"
RAIL = "#D3D1C7"
FLOW = "#5F5E5A"

BLUE = ("#F2F8FE", "#185FA5", "#0C447C")
TEAL = ("#E8F6F1", "#0F6E56", "#085041")
TEAL_GROUP = ("#F6FBF9", "#9FE1CB", "#0F6E56")
AMBER = ("#FDF4E4", "#854F0B", "#633806")
GRAY = ("#F6F5F1", "#B4B2A9", "#444441")

L = {
    "zh": {
        "font": "'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Helvetica,Arial,sans-serif",
        "layers": [("桌面层", "desktop", 156), ("运行时", "runtime", 413), ("能力服务", "services", 640), ("资源与工具", "install-time", 764)],
        "bibit_sub": "BiBit GUI · Tauri 桌面外壳 · 签名插件宿主",
        "bibit_note": "启动时校验插件签名并解包；插件贡献 Tool / Skill / Hook / MCP 与设置页",
        "voice": ["KWS 唤醒 · VAD · ASR", "PipeWire 采集", "监听 /run/bibit/audio.sock", "bibit-voice-tool 服务", "完全离线"],
        "sched": ["D-Bus 守护进程 + CLI", "一次性 / 每日 / 每周 …", "lxqt-notificationd 提醒", "面板世界时钟 · 自启动"],
        "group_header": "运行期协同的三个组件：memory 经 SDK 对接，security 经审批与能力同步接口",
        "rt_sub": "YAML 配置驱动的 Agent 服务 · Python",
        "rt_cells": ["会话事件流", "Agent 生命周期", "模型调用", "Tool · Plugin 执行"],
        "rt_note": ["Provider 存连接信息，模型名写在 agent.yaml", "安全边界 fail-closed · 目标平台 K3（riscv64）"],
        "mem_title": "bianbu-agent-memory",
        "mem_lines": ["L1 会话 · L2 工作 · L3 长期", "SDK · adapters · migrations", "Rust · 会话与用户隔离", "自带 debian 包装"],
        "sec_title": "bianbu-agent-security",
        "sec_lines": ["Tool 审批 · per-Agent 能力同步", "securityd 签名清单 · fail-closed", "设计 / H-LD / LLD / API 文档", "安全 WebUI demo"],
        "int_title": "bibit-intent",
        "int_line": "意图路由 + 工具执行",
        "int_sub": "确定性规则 → 本地推理 → 云端升级",
        "fs_title": "bibit-filesearch",
        "fs_line": "本地语义检索服务 · HTTP 契约",
        "fs_sub": "默认索引 ~/Documents，数据不出本机",
        "lg_title": "集成面",
        "lg_items": [
            "HTTP　检索服务，每用户独立实例",
            "Unix socket　/run/bibit/audio.sock",
            "D-Bus　日程、提醒与桌面集成",
            "事件流　会话 seq 日志，可多端同看",
            "插件包　签名 .bibit-plugin.tgz",
            "打包　各组件自带 debian/",
        ],
        "sk_title": "bianbu-skill",
        "sk_line": "APC 公开 Skill 的只读镜像",
        "sk_sub": "skills/ 按发布包原样解包",
        "ap_title": "agent-power-manager",
        "ap_line": "管理 Skill / Plugin / MCP / Expert 的 CLI",
        "ap_sub": "Go · 面向 Agent Power Cloud（APC）",
        "a1": "会话事件流 · 插件页面",
        "a2": "意图路由 / 工具调用",
        "a3": "HTTP 检索",
        "footer": "14 个组件以 git submodule 平铺在仓库根目录；箭头表示文档层面记录的调用方向。",
    },
    "en": {
        "font": "'Helvetica Neue',Helvetica,Arial,sans-serif",
        "layers": [("Desktop", "", 156), ("Runtime", "", 413), ("Services", "", 640), ("Tooling", "", 764)],
        "bibit_sub": "BiBit GUI · Tauri desktop shell · signed plugin host",
        "bibit_note": "Verifies plugin signatures at startup; plugins contribute Tool / Skill / Hook / MCP and settings pages",
        "voice": ["KWS wake word · VAD · ASR", "PipeWire capture", "Listens on /run/bibit/audio.sock", "bibit-voice-tool service", "Fully offline"],
        "sched": ["D-Bus daemon + CLI", "One-off / daily / weekly …", "Reminders via lxqt-notificationd", "Panel world clock · autostart"],
        "group_header": "Three components that cooperate at runtime: memory over its SDK, security over approval and capability sync",
        "rt_sub": "YAML-driven agent service · Python",
        "rt_cells": ["Session event stream", "Agent lifecycle", "Model calls", "Tool · plugin execution"],
        "rt_note": ["Providers keep connection info; model names live in agent.yaml", "Security boundary fails closed · target K3 (riscv64)"],
        "mem_title": "bianbu-agent-memory",
        "mem_lines": ["L1 session · L2 working · L3 long-term", "SDK · adapters · migrations", "Rust · per-session/user isolation", "ships debian/"],
        "sec_title": "bianbu-agent-security",
        "sec_lines": ["Tool approval · per-agent capability sync", "securityd signed manifests · fails closed", "SRS / H-LD / LLD / API docs", "security WebUI demo"],
        "int_title": "bibit-intent",
        "int_line": "Intent routing + tool execution",
        "int_sub": "Rules → local inference → cloud escalation",
        "fs_title": "bibit-filesearch",
        "fs_line": "Local semantic search · HTTP contract",
        "fs_sub": "Indexes ~/Documents; data stays on device",
        "lg_title": "Integration surfaces",
        "lg_items": [
            "HTTP · search service, one per user",
            "Unix socket · /run/bibit/audio.sock",
            "D-Bus · schedules and desktop",
            "Event stream · session seq log",
            "Plugin bundle · signed .tgz",
            "Packaging · debian/ per component",
        ],
        "sk_title": "bianbu-skill",
        "sk_line": "Read-only mirror of Skills on APC",
        "sk_sub": "skills/ unpacked verbatim",
        "ap_title": "agent-power-manager",
        "ap_line": "CLI for Skill / Plugin / MCP / Expert",
        "ap_sub": "Go · targets Agent Power Cloud (APC)",
        "a1": "session event stream · plugin pages",
        "a2": "intent routing / tool calls",
        "a3": "HTTP search",
        "footer": "Fourteen components as git submodules at the repository root; arrows show the documented call direction.",
    },
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def vwidth(s):
    return sum(12.2 if ord(c) > 0x2E7F else 6.4 for c in s)


class Svg:
    def __init__(self, font):
        self.font = font
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=13, fill=INK, weight=400, anchor="start", mono=False):
        fam = "'JetBrains Mono','SF Mono',Menlo,Consolas,monospace" if mono else self.font
        self.add(
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'dominant-baseline="central">{esc(s)}</text>'
        )

    def rect(self, x, y, w, h, fill, stroke, rx=10, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def flow(self, x1, y1, x2, y2, label=None):
        self.add(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{FLOW}" '
            f'stroke-width="1.4" stroke-linecap="round" marker-end="url(#arrow)"/>'
        )
        if label:
            w = vwidth(label) + 20
            cy = (y1 + y2) / 2
            self.add(f'<rect x="{x1 - w / 2:.1f}" y="{cy - 12}" width="{w:.1f}" height="24" rx="6" fill="#FFFFFF"/>')
            self.text(x1, cy, label, 12, MUT, 400, "middle")

    def render(self):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img">\n'
            f"<defs>\n"
            f'<marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" '
            f'markerHeight="8" orient="auto">'
            f'<path d="M2.5 1.5L8 5L2.5 8.5" fill="none" stroke="{FLOW}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/></marker>\n'
            f"</defs>\n"
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>\n'
            + "\n".join(self.parts)
            + "\n</svg>\n"
        )


def build(lang):
    t = L[lang]
    g = Svg(t["font"])

    # left rail
    g.add(f'<line x1="134" y1="64" x2="134" y2="812" stroke="{RAIL}" stroke-width="1"/>')
    for name, sub, y in t["layers"]:
        g.add(f'<line x1="128" y1="{y}" x2="134" y2="{y}" stroke="{RAIL}" stroke-width="1"/>')
        g.text(122, y - (7 if sub else 0), name, 15, INK, 500, "end")
        if sub:
            g.text(122, y + 12, sub, 11, HINT, 400, "end")

    # ---- desktop
    g.rect(150, 64, 610, 176, BLUE[0], BLUE[1], rx=14)
    g.text(168, 96, "bibit", 17, BLUE[2], 500, mono=True)
    g.text(168, 118, t["bibit_sub"], 12.5, MUT)
    for i, c in enumerate(["bibit-runtime-plugin", "bibit-agenthub-plugin", "bibit-filesearch-plugin", "bibit-memory-plugin"]):
        x = 168 + (i % 2) * 292
        y = 136 + (i // 2) * 40
        g.rect(x, y, 282, 32, "#FFFFFF", "#B5D4F4", rx=8, sw=0.9)
        g.text(x + 14, y + 16, c, 12, BLUE[2], 400, mono=True)
    g.text(168, 226, t["bibit_note"], 12, HINT)

    g.rect(778, 64, 192, 176, BLUE[0], BLUE[1], rx=14)
    g.text(796, 96, "bibit-voice", 15, BLUE[2], 500, mono=True)
    for i, s in enumerate(t["voice"]):
        g.text(796, 126 + i * 23, s, 11.5, MUT)

    g.rect(986, 64, 190, 176, BLUE[0], BLUE[1], rx=14)
    g.text(1004, 96, "lxqt-schedule", 15, BLUE[2], 500, mono=True)
    for i, s in enumerate(t["sched"]):
        g.text(1004, 126 + i * 23, s, 11.5, MUT)

    # ---- runtime group
    g.rect(150, 306, 1026, 214, TEAL_GROUP[0], TEAL_GROUP[1], rx=16, sw=1, dash="6 5")
    g.text(168, 328, t["group_header"], 12, TEAL[1])

    g.rect(166, 346, 400, 158, TEAL[0], TEAL[1], rx=12)
    g.text(184, 370, "bianbu-agent-runtime", 15.5, TEAL[2], 500, mono=True)
    g.text(184, 389, t["rt_sub"], 11.5, MUT)
    for i, c in enumerate(t["rt_cells"]):
        x = 184 + (i % 2) * 194
        y = 402 + (i // 2) * 34
        g.rect(x, y, 182, 28, "#FFFFFF", TEAL_GROUP[1], rx=7, sw=0.9)
        g.text(x + 91, y + 14, c, 12, TEAL[2], 400, "middle")
    for i, s in enumerate(t["rt_note"]):
        g.text(184, 476 + i * 18, s, 11, HINT)

    g.rect(586, 346, 280, 158, "#FFFFFF", TEAL[1], rx=12)
    g.text(602, 370, t["mem_title"], 15, TEAL[2], 500, mono=True)
    for i, s in enumerate(t["mem_lines"]):
        g.text(602, 400 + i * 24, s, 12 if i == 0 else 11.5, MUT if i else TEAL[2])

    g.rect(886, 346, 274, 158, "#FFFFFF", TEAL[1], rx=12)
    g.text(902, 370, t["sec_title"], 15, TEAL[2], 500, mono=True)
    for i, s in enumerate(t["sec_lines"]):
        g.text(902, 400 + i * 24, s, 12 if i == 0 else 11.5, MUT if i else TEAL[2])

    # ---- services
    g.rect(150, 596, 320, 96, AMBER[0], AMBER[1], rx=12)
    g.text(168, 622, t["int_title"], 15, AMBER[2], 500, mono=True)
    g.text(168, 648, t["int_line"], 12, MUT)
    g.text(168, 670, t["int_sub"], 11.5, HINT)

    g.rect(490, 596, 320, 96, AMBER[0], AMBER[1], rx=12)
    g.text(508, 622, t["fs_title"], 15, AMBER[2], 500, mono=True)
    g.text(508, 648, t["fs_line"], 12, MUT)
    g.text(508, 670, t["fs_sub"], 11.5, HINT)

    # ---- tooling
    g.rect(150, 716, 320, 96, AMBER[0], AMBER[1], rx=12)
    g.text(168, 742, t["sk_title"], 15, AMBER[2], 500, mono=True)
    g.text(168, 768, t["sk_line"], 12, MUT)
    g.text(168, 790, t["sk_sub"], 11.5, HINT)

    g.rect(490, 716, 320, 96, AMBER[0], AMBER[1], rx=12)
    g.text(508, 742, t["ap_title"], 15, AMBER[2], 500, mono=True)
    g.text(508, 768, t["ap_line"], 12, MUT)
    g.text(508, 790, t["ap_sub"], 11.5, HINT)

    # ---- integration surfaces
    g.rect(830, 596, 346, 216, GRAY[0], GRAY[1], rx=14, dash="6 5")
    g.text(850, 622, t["lg_title"], 14, GRAY[2], 500)
    for i, s in enumerate(t["lg_items"]):
        g.text(850, 652 + i * 25, s, 11.5, MUT)

    # ---- flows
    g.flow(330, 240, 330, 302, t["a1"])
    g.flow(310, 520, 310, 592, t["a2"])
    g.flow(650, 520, 650, 592, t["a3"])

    g.text(150, 832, t["footer"], 11.5, HINT)
    return g.render()


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else "zh"
    out = sys.argv[2] if len(sys.argv) > 2 else f"architecture-{lang}.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(build(lang))
    print(f"wrote {out}")
