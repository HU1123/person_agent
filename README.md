# Personal Agent

个人 AI Agent 学习项目。通过实践 Cursor、OpenSpec 等工具，探索规范驱动开发（Spec-Driven Development）与 AI 辅助编程的工作流。

文档总结：
https://hcnzzf4m2k4n.feishu.cn/wiki/J4njwu6VKigonBkJHfocogWKnFb

## 项目目标

- 学习如何在 Cursor 中与 AI Agent 协作开发
- 使用 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 管理需求与变更，避免「需求只活在聊天里」
- 记录实验、沉淀可复用的开发模式

## 技术栈

| 工具 | 用途 |
|------|------|
| [Cursor](https://cursor.com) | AI 编程 IDE |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 规范驱动开发框架 |
| Node.js ≥ 20.19 | OpenSpec CLI 运行环境 |

## 项目结构

```
.
├── README.md
├── openspec/                  # OpenSpec 规范目录
│   ├── specs/                 # 系统现状 spec（按领域划分）
│   └── changes/               # 进行中的变更
│       └── archive/           # 已归档变更
└── .cursor/
    ├── commands/              # Cursor 斜杠命令
    └── skills/                # Agent Skills
```

## 快速开始

### 1. 安装 OpenSpec CLI

```bash
npm install -g @fission-ai/openspec@latest
```

### 2. 克隆项目

```bash
git clone <repo-url>
cd agent
```

### 3. 在 Cursor 中打开项目

用 Cursor 打开本目录即可使用已配置的 OpenSpec 工作流。

## 开发工作流

OpenSpec 默认 **core** 流程：

```
/opsx:propose → /opsx:apply → /opsx:sync → /opsx:archive
```

| 命令 | 说明 |
|------|------|
| `/opsx:propose [描述]` | 创建变更，生成 proposal、specs、design、tasks |
| `/opsx:explore [话题]` | 需求不清时先探索，再决定是否 propose |
| `/opsx:apply` | 按 tasks.md 逐项实现 |
| `/opsx:sync` | 将 delta spec 合并到主 spec |
| `/opsx:archive` | 归档已完成变更 |

### 示例

```text
/opsx:propose add-hello-world
/opsx:apply
/opsx:archive
```

## CLI 常用命令

```bash
openspec list              # 列出进行中的变更
openspec show <change>     # 查看变更详情
openspec validate <change> # 校验 spec 格式
openspec view              # 交互式仪表盘
openspec update            # 刷新 Cursor 命令与 Skills
```

## 学习计划

转行 Agent 应用开发的一个月学习计划（含进度跟踪）见 [docs/learning-plan.md](docs/learning-plan.md)。

## 学习笔记

> 在此记录实验心得、踩坑与最佳实践。

- （待补充）

## 参考

- [OpenSpec 文档](https://github.com/Fission-AI/OpenSpec/tree/main/docs)
- [Cursor 文档](https://docs.cursor.com)
- [OpenSpec + Cursor 指南](https://openspec.pro/cursor-openspec/)

## License

MIT
