# IELTS Essay Assistant - 雅思写作助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill Type: Claude Code](https://img.shields.io/badge/Skill-Claude%20Code-blue.svg)](https://claude.ai/code)

> 一个全面的雅思写作模块助手，帮助考生通过专业评估、详细反馈和范文参考来提高写作成绩。

---

## 📖 项目简介

本项目是一个为 [Claude Code](https://claude.ai/code) 设计的 Skill，旨在帮助雅思考生提升写作能力。通过分析官方雅思评分标准（Band Descriptors），该助手能够提供精准的作文评分、详细的批改建议以及基于官方高分范文的学习资源。

### 主要功能

| 功能 | 描述 |
|------|------|
| 📝 **作文评分** | 基于官方雅思写作评分标准进行专业评估 |
| ✏️ **批改润色** | 识别错误、提供改进建议、给出修订版本 |
| 📚 **范文参考** | 生成基于官方高分范文模式的 AI 范文 |
| 🔍 **语料库管理** | 支持个人语料库，存储和学习官方范文 |
| 📊 **差距分析** | 对比不同分数段作文，找出提升空间 |

---

## 🎯 适用场景

- 需要为雅思作文评分的考生
- 希望改进写作语法和词汇的学习者
- 想要获取特定话题范文参考的用户
- 准备建立个人语料库进行系统学习的考生

---

## 📂 项目结构

```
ielts-essay-assistant/
├── SKILL.md                          # Skill 主文件（英文）
├── README.md                         # 项目说明文档（本文档）
├── references/                       # 参考资料目录
│   ├── sample-essays.md             # AI 生成范文示例
│   ├── official-samples-learning.md # 官方范文学习框架
│   ├── personal-corpus-guide.md     # 个人语料库使用指南
│   └── official-resources-index.md  # 官方资源索引
└── evals/                           # 评估测试目录
```

---

## 🚀 快速开始

### 安装要求

- [Claude Code](https://claude.ai/code) 已安装并配置
- 将本 Skill 文件放置在 Claude Code 的 skills 目录中

### 使用方法

1. **复制 Skill 到 Claude Code 目录**

   ```bash
   # Windows
   xcopy /E /I "ielts-essay-assistant" "%USERPROFILE%\.claude\skills\ielts-essay-assistant"
   
   # macOS/Linux
   cp -r ielts-essay-assistant ~/.claude/skills/
   ```

2. **在 Claude Code 中使用**

   启动 Claude Code 后，直接输入以下类型的请求即可触发 Skill：

   - `"请帮我评分这篇雅思作文"`
   - `"批改我的 Task 2 作文"`
   - `"生成一篇关于科技的范文"`
   - `"添加范文到语料库"`

---

## 📊 评分标准

本 Skill 严格遵循官方雅思写作评分标准（IELTS Writing Band Descriptors）：

### Task 1 评分维度

| 评分维度 | 权重 | 说明 |
|---------|------|------|
| **Task Achievement (TA)** | 25% | 是否完整回应题目要求，概述是否清晰 |
| **Coherence & Cohesion (CC)** | 25% | 逻辑组织、段落结构、衔接手段 |
| **Lexical Resource (LR)** | 25% | 词汇范围、准确性、拼写 |
| **Grammatical Range & Accuracy (GRA)** | 25% | 句式结构、语法错误、标点符号 |

### Task 2 评分维度

| 评分维度 | 权重 | 说明 |
|---------|------|------|
| **Task Response (TR)** | 25% | 是否完整回应题目，立场是否清晰 |
| **Coherence & Cohesion (CC)** | 25% | 逻辑流畅、段落划分、连接词使用 |
| **Lexical Resource (LR)** | 25% | 词汇范围、搭配、错误控制 |
| **Grammatical Range & Accuracy (GRA)** | 25% | 复杂句式、错误频率 |

### 分数等级说明

| 分数 | 描述 |
|------|------|
| 9 | Expert - 完全自然，精妙的语言控制 |
| 8 | Very Good - 偶尔失误，能处理复杂论证 |
| 7 | Good - 总体有效，存在一些不准确之处 |
| 6 | Competent - 尽管有错误，能有效沟通 |
| 5 | Modest - 部分掌握，频繁出错 |
| 4 | Limited - 基本能力，问题频发 |

---

## 📝 支持的作文类型

### Task 1 Academic（学术类）

- 线图 (Line Graph)
- 柱状图 (Bar Chart)
- 饼图 (Pie Chart)
- 表格 (Table)
- 流程图 (Process Diagram)
- 地图 (Map)

### Task 1 General（培训类）

- 正式信函 (Formal Letter)
- 半正式信函 (Semi-formal Letter)
- 非正式信函 (Informal Letter)

### Task 2（大作文）

- 观点类 (Opinion Essay)
- 讨论类 (Discussion Essay)
- 问题解决类 (Problem-Solution Essay)
- 优缺点类 (Advantages-Disadvantages Essay)
- 双问题类 (Double Question Essay)

---

## 💾 个人语料库功能

本 Skill 支持建立**个人语料库**，用于收集和学习官方范文：

### 功能特点

1. **添加官方范文** - 从 Cambridge IELTS 书籍、British Council PDF 等来源
2. **存储个人习作** - 保存自己的练习作文
3. **AI 分析学习** - 自动提取高分技巧
4. **生成新范文** - 应用学习到的技巧到新话题

### 常用命令

| 命令 | 功能 |
|------|------|
| `添加范文` / `Add essay` | 添加范文到语料库 |
| `查看语料库` / `View corpus` | 查看语料库统计和概览 |
| `分析语料库` / `Analyze corpus` | 分析已存储的作文 |
| `基于语料库生成` / `Generate from corpus` | 使用学习到的模式生成作文 |

详细使用方法请参考：`references/personal-corpus-guide.md`

---

## ⚠️ 重要声明

### 关于 AI 生成范文

> 本 Skill 提供的所有范文均为 **AI 生成**，基于雅思评分标准和官方高分范文（Cambridge IELTS 系列）中观察到的模式。这些范文仅供学习和练习使用。
>
> **如需获取真实官方范文，请参考：**
> - Cambridge IELTS Books 10-18（真题+考官认可范文）
> - 官方雅思练习资料（British Council/IDP）
> - ielts.org 官方样题

### 使用建议

1. AI 生成的范文用于学习结构、词汇和句式
2. 真实考试前务必参考官方 Cambridge IELTS 书籍
3. 不要背诵 AI 范文，考试中使用 memorize 的内容会被扣分

---

## 📚 官方资源索引

我们整理了免费的官方学习资源：

### 免费官方资源

| 资源名称 | 来源 | 内容 |
|---------|------|------|
| Academic Writing Sample Tasks | British Council | Task 1 & 2 样题 |
| Sample Candidate Responses | British Council | 考生范文+考官点评+分数 |
| IELTS Ready Free | British Council | 6套免费模拟测试+范文 |
| Practice Tests Portal | IELTS.org | 限时写作练习+范文 |

详细资源列表请参考：`references/official-resources-index.md`

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进本项目！

### 贡献方式

1. **报告问题** - 提交 Issue 描述你遇到的问题
2. **改进文档** - 完善 README 或其他文档
3. **添加功能** - 提交 PR 增加新功能
4. **分享范文** - 分享你收集的官方范文（确保不侵权）

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🙏 致谢

- 感谢 [Claude Code](https://claude.ai/code) 提供的强大平台
- 感谢 Cambridge Assessment English 提供的官方评分标准
- 感谢所有为雅思教学做出贡献的教育工作者

---

**祝大家雅思考试顺利，取得理想成绩！** 🎉
