# Pony Wei

写桌面端和 AI 工具。做的项目大多围绕两个前提：**数据留在本机**，**结论要能被验证**。

## 在做的事

**[x-code](https://github.com/qweijiaq/x-code)** — 本地优先、模型无关的 AI 编程助手。桌面端与命令行共享同一份会话、记忆和技能，支持 Claude、GPT、Gemini、DeepSeek、Ollama 与任意 OpenAI 兼容模型，代码不出本机。

**[anatomy](https://github.com/qweijiaq/anatomy)** — 把一个仓库拆成带行号证据的设计笔记。模型写的每条主张先和磁盘上的字节比对，对不上的行号会被拒绝，验证不过的说法不会进入报告。

**[folio](https://github.com/qweijiaq/folio)** — Go + Vue 3 自托管个人知识站。博客、文档库、评论、RSS/SEO 与自带 Key 的 AI 问答是一个整体，`docker compose up` 就能跑。

## 仓库

| 项目 | 它解决什么 | 技术栈 |
| --- | --- | --- |
| [x-code](https://github.com/qweijiaq/x-code) | 本地优先的 AI 编程助手，桌面端与 CLI 共享会话 | TypeScript · Electron · MCP |
| [anatomy](https://github.com/qweijiaq/anatomy) | 仓库 → 带行号证据的设计笔记，每条结论都可回查 | TypeScript · Electron |
| [folio](https://github.com/qweijiaq/folio) | 自托管知识站：博客 / 文档 / 评论 / RSS / AI 问答 | Go · Vue 3 · SQLite · Docker |
| [ThinRead](https://github.com/qweijiaq/ThinRead) | 把一本书的章节读薄成可发布的草稿与核心卡片 | TypeScript · Electron · React |
| [CloseRead](https://github.com/qweijiaq/CloseRead) | 英语精读：逐段译文、笔记、词卡，导出 Anki | TypeScript · CLI |
| [RepoRadar](https://github.com/qweijiaq/RepoRadar) | 按项目上下文找值得接入的开源库，用沙箱验证再决定 | TypeScript · Next.js · Docker |

## 关注

- **桌面端**：Electron 里那些只有真机上才会出现的问题——权限、签名、更新、窗口生命周期。
- **本地优先**：默认不上传。需要联网的地方应该说得清楚为什么需要。
- **可验证的 AI 输出**：让模型的主张落到证据上，行号、原文、比对结果都要能被复查。

## 联系

[CSDN 博客](https://blog.csdn.net/weixin_44141520/) · [邮箱](mailto:2112025700@qq.com)

聊桌面端、本地优先工具，或者怎么证明模型没胡说，都欢迎开 issue。
