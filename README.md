<p align="center">
  <img src="assets/banner.svg" alt="Pony Wei — local-first tools and verifiable output" width="100%">
</p>

<h1 align="center">Pony Wei</h1>

<p align="center">
  <img alt="重庆大学" src="https://img.shields.io/badge/%E9%87%8D%E5%BA%86%E5%A4%A7%E5%AD%A6-%E7%A0%94%E7%A9%B6%E7%94%9F-1f6feb?style=flat-square">
  <img alt="地点" src="https://img.shields.io/badge/%E5%9C%B0%E7%82%B9-%E9%87%8D%E5%BA%86-555?style=flat-square">
  <img alt="偏好" src="https://img.shields.io/badge/%E5%81%8F%E5%A5%BD-%E6%A1%8C%E9%9D%A2%E7%AB%AF%20%C2%B7%20%E5%85%A8%E6%A0%88%20%C2%B7%20AI%20%E5%B7%A5%E5%85%B7-2f7d5d?style=flat-square">
</p>

<p align="center">
  <a href="https://blog.csdn.net/weixin_44141520/">CSDN 博客</a> ·
  <a href="https://github.com/qweijiaq?tab=repositories">全部仓库</a> ·
  <a href="mailto:2112025700@qq.com">邮箱</a>
</p>

写软件的时候，我关心的不是「跑起来了」，而是**它在什么条件下还能被信任**。
仓库里的项目大多围绕同一件事：本地优先、不把代码和数据交出去、结论要能被验证。

## 正在做

- **[x-code](https://github.com/qweijiaq/x-code)** — 本地优先、模型无关的 AI 编程助手。桌面端与命令行共享同一份会话，支持 Claude / GPT / Gemini / DeepSeek / Ollama 与任意 OpenAI 兼容模型，内置 MCP 与 Skills，代码不出本机。
- **[anatomy](https://github.com/qweijiaq/anatomy)** — 把一个仓库拆成带行号证据的设计笔记。模型写的每条主张都先拿去和磁盘上的字节比对，加不上的行号会被拒绝，验证不过的说法不会进入报告。
- **[folio](https://github.com/qweijiaq/folio)** — Go + Vue 3 自托管个人知识站，博客、文档库、评论、RSS/SEO 与自带 Key 的 AI 问答打成一个可以 `docker compose up` 的整体。

## 项目

| 项目 | 它解决什么 | 技术栈 |
| --- | --- | --- |
| [x-code](https://github.com/qweijiaq/x-code) | 本地优先、模型无关的 AI 编程助手，桌面端与 CLI 共享会话 | TypeScript · Electron · MCP |
| [anatomy](https://github.com/qweijiaq/anatomy) | 仓库 → 带行号证据的设计笔记，每条结论都可回查 | TypeScript · Electron · 取证内核 |
| [folio](https://github.com/qweijiaq/folio) | 自托管个人知识站：博客 / 文档 / 评论 / RSS / AI 问答 | Go · Vue 3 · SQLite · Docker |
| [ThinRead](https://github.com/qweijiaq/ThinRead) | 本地优先的 AI 读书笔记，把章节读薄成草稿与核心卡片 | TypeScript · Electron · React |
| [CloseRead](https://github.com/qweijiaq/CloseRead) | 本地优先的英语精读：逐段译文、精读笔记、词卡导出 Anki | TypeScript · CLI · Anki |
| [RepoRadar](https://github.com/qweijiaq/RepoRadar) | 按你的技术栈发现值得关注的开源项目，附 AI 摘要与沙箱验证 | TypeScript · Next.js · Docker |

## 技术栈

<p>
  <img src="https://skillicons.dev/icons?i=ts,js,go,react,vue,electron,nodejs,nextjs,tailwind,sqlite,mysql,docker,git,vscode" alt="stack" />
</p>

日常是 macOS + VS Code，桌面端用 Electron，服务端更愿意写 Go。
最近在补的东西：Rust、Flutter、以及怎么让模型输出变得可验证。

## 读过的书

读书笔记还能查到的几本，技术书之外也读一些别的：

- [你不知道的 JavaScript](https://weread.qq.com/web/bookDetail/8c632230715c01a18c683d8) — 作用域、闭包、this，第一本真正读透的语言书
- [JavaScript 高级程序设计](https://weread.qq.com/web/bookDetail/751326d0720befab7514782) — 当字典用，边写边翻
- [Vue.js 设计与实现](https://weread.qq.com/web/bookDetail/c5c32170813ab7177g0181ae) — 框架作者亲自讲取舍
- [JavaScript 语言精髓与编程实践](https://weread.qq.com/web/bookDetail/bd73243071e43421bd7c139)
- [JavaScript 重难点实例精讲](https://weread.qq.com/web/bookDetail/2ba32920720a57e92ba5389)

工作之外：摄影、主机游戏、以及把读过的书拆成能复用的笔记。

---

<p align="center">
  想聊桌面端、本地优先工具、或者「怎么证明模型没胡说」，欢迎开 issue 或来信。
</p>
