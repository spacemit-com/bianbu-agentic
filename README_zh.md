# SpacemiT Bianbu AgentOS

[English](README.md) | 简体中文

Bianbu AgentOS 汇总了面向 SpacemiT K 系列处理器的端侧 Agent 操作系统的各个组件。
本仓库用 **Git submodule** 收拢组件：每个组件保留独立仓库、独立发布节奏和 Debian 打包，
本仓库为每个组件记录一个固定提交，因此一个 SHA 就能复现整套系统镜像。

## 1. 架构

![Bianbu AgentOS 架构](docs/images/architecture-zh.png)

桌面层承载 BiBit GUI 与签名插件、离线语音服务和 LXQt 日程模块；Agent 运行时负责会话、
生命周期、模型调用与 Tool 执行，记忆与安全是一等子系统；能力服务提供意图路由与本地语义
检索；资源与工具层镜像 Skill 并管理 Power。完整说明见
[docs/architecture.md](docs/architecture.md)。

## 2. 组件总览

组件目录位于本仓库根目录，仓库内不存放组件源码，只保留 submodule 指针、文档与工具。

### 运行时核心

| 路径 | 组件 | 作用 | 形态 | 分支 |
|---|---|---|---|---|
| [`bianbu-agent-runtime/`](https://github.com/spacemit-com/bianbu-agent-runtime) | Bianbu Agent Runtime | YAML 配置驱动的 Agent 服务与运行时核心：会话事件流、Agent 生命周期、模型调用、Tool 与插件执行、安全边界 | Python | `main` |
| [`bianbu-agent-security/`](https://github.com/spacemit-com/bianbu-agent-security) | Bianbu Agent Security | 安全边界：Tool 审批、per-Agent 能力同步、`securityd` 签名清单；含设计/H‑LD/LLD 文档与 Debian 打包 | 守护进程 + Debian | `main` |
| [`bianbu-agent-memory/`](https://github.com/spacemit-com/bianbu-agent-memory) | Bianbu Agent Memory | 记忆子系统：L1 会话、L2 工作记忆、L3 长期记忆，含 SDK、adapters 与 migrations | Rust | `main` |
| [`bibit-intent/`](https://github.com/spacemit-com/bibit-intent) | Bibit Intent | 意图路由与工具执行：确定性规则 → 本地推理 → 云端升级 | Python | `main` |

### 桌面与交互

| 路径 | 组件 | 作用 | 形态 | 分支 |
|---|---|---|---|---|
| [`bibit/`](https://github.com/spacemit-com/bibit) | BiBit GUI | Agent 桌面前端（以 Jan 为骨架）：对话、富消息、附件、会话历史、桌面外壳 | TypeScript / Rust (Tauri) | `main` |
| [`bibit-voice/`](https://github.com/spacemit-com/bibit-voice) | Bibit Voice | 离线语音服务：KWS 唤醒、VAD、ASR，经 `/run/bibit/audio.sock` 提供服务 | C++ / Python | `main` |
| [`bibit-filesearch/`](https://github.com/spacemit-com/bibit-filesearch) | Bibit File Search | 本地语义文件检索服务，对外是 HTTP 契约，数据不出本机 | Python | `main` |
| [`lxqt-schedule/`](https://github.com/spacemit-com/lxqt-schedule) | lxqt-schedule | LXQt 日程与提醒模块：D-Bus 守护进程 + CLI，对接 `lxqt-notificationd`、面板世界时钟与 `bibit-intent` | C++ | `main` |

### BiBit 插件（前端贡献）

| 路径 | 组件 | 作用 | 形态 | 分支 |
|---|---|---|---|---|
| [`bibit-runtime-plugin/`](https://github.com/spacemit-com/bibit-runtime-plugin) | Runtime Plugin | 专家、服务商、本地模型、工具、MCP、技能、Hook、插件、安全等设置页，以及 Agent Top / Runtime 状态 / 日志 | TypeScript | `main` |
| [`bibit-agenthub-plugin/`](https://github.com/spacemit-com/bibit-agenthub-plugin) | Agent Hub Plugin | Agent Hub 页面与设置子页；通过 `service:store`、`file:transfer`、`job:manage` 与 Provider Protocol v2 接入 | TypeScript | `bianbu-26.04` |
| [`bibit-filesearch-plugin/`](https://github.com/spacemit-com/bibit-filesearch-plugin) | File Search Plugin | 「设置 → Features → File Search」页面，用于配置与观测 `bibit-filesearch` | TypeScript | `main` |
| [`bibit-memory-plugin/`](https://github.com/spacemit-com/bibit-memory-plugin) | Memory Plugin | 「设置 → Memory」页面：开关记忆、保留时长、清空会话、全部清除、JSON 导入导出 | TypeScript | `main` |

### 资源与工具

| 路径 | 组件 | 作用 | 形态 | 分支 |
|---|---|---|---|---|
| [`bianbu-skill/`](https://github.com/spacemit-com/bianbu-skill) | Bianbu Skills | SpacemiT APC 上公开 Skill 的只读镜像，`skills/` 按发布包原样解包 | Markdown | `main` |
| [`agent-power-manager/`](https://github.com/spacemit-com/agent-power-manager) | Agent Power Manager | 管理 Skill、Plugin、MCP、Expert 的命令行工具 | Go | `bianbu-26.04` |

> 说明：`.gitmodules` 里的 `branch` 只影响带 `--remote` 的操作；真正被锁定的是父仓库索引中
> 记录的组件提交。

## 3. 获取源码

推荐递归克隆：

```bash
git clone --recurse-submodules https://github.com/spacemit-com/bianbu-agentic.git
# 或使用 SSH：
# git clone --recurse-submodules git@github.com:spacemit-com/bianbu-agentic.git
```

已经克隆但未拉子模块：

```bash
cd bianbu-agentic
make init          # 等价于 scripts/submodules.sh init
```

常用命令：

```bash
make status        # 查看每个组件的锁定提交、分支与脏状态
make sync          # 让所有子模块跟进各自跟踪分支的最新提交
make update        # 把子模块快进到本仓库记录的提交
```

`make sync` 只改工作区；确认要发布新版本时再提交 submodule 指针。

## 4. 目录结构

```text
bianbu-agentic/
├── bianbu-agent-runtime/        # submodule
├── bianbu-agent-security/       # submodule
├── bianbu-agent-memory/         # submodule
├── bibit-intent/                # submodule
├── bibit/                       # submodule
├── bibit-voice/                 # submodule
├── bibit-filesearch/            # submodule
├── lxqt-schedule/               # submodule
├── bibit-runtime-plugin/        # submodule
├── bibit-agenthub-plugin/       # submodule
├── bibit-filesearch-plugin/     # submodule
├── bibit-memory-plugin/         # submodule
├── bianbu-skill/                # submodule
├── agent-power-manager/         # submodule
├── docs/                        # 汇总仓库自身的架构说明
├── scripts/submodules.sh        # submodule 辅助脚本
├── Makefile
└── .github/workflows/           # submodule 指针同步
```

## 5. 版本策略

- 所有组件钉在具体提交上：只凭父仓库的 SHA 就能复现镜像，`git describe` 即发布标识。
- `.github/workflows/sync-submodules.yml` 在 `main` 上前移指针，并以 `chore(submodule): ...`
  提交，使指针变更与内容变更分开评审。
- 代码、issue、发布仍以组件仓库为准。不要在本仓库内改组件源码，改上游后让指针跟进。
- `bibit-agenthub-plugin` 与 `agent-power-manager` 跟踪 `bianbu-26.04`，其余跟踪 `main`。

## 6. 新增或移除组件

```bash
git submodule add -b main https://github.com/spacemit-com/<repo>.git <repo>
git commit -m "chore(submodule): add <repo>"
```

随后把该路径补进 `.github/workflows/sync-submodules.yml` 的 `submodule_paths` 列表和上面的
表格。

> 注意：子模块目录未初始化时，工作区里并不存在对应目录，此时 `git add -A` / `git add .`
> 会把 gitlink 当成「已删除」写进索引，提交后子模块就全丢了。请用 `git add <具体文件>`
> 暂存改动，或先 `make init` 把子模块拉下来。

移除时：

```bash
git submodule deinit -f -- <repo>
git rm -f <repo>
rm -rf .git/modules/<repo>
```

## 7. 文档

- [架构说明](docs/architecture.md)
- 架构图：`docs/images/architecture-{zh,en}.svg`，可用
  `python3 docs/images/architecture.py <zh|en> <out.svg>` 重新生成
- 各组件 README 见对应子目录
