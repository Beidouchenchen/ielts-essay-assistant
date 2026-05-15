# IELTS Essay Assistant - 雅思写作助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill Type: Claude Code](https://img.shields.io/badge/Skill-Claude%20Code-blue.svg)](https://claude.ai/code)

> 基于 RAG 的雅思写作 Claude Code Skill，内置 Cambridge IELTS 8-20 范文库，开箱即用。

---

## 这是什么？

这是一个 **Claude Code Skill**（插件），安装后可以在 [Claude Code](https://claude.ai/code) 中通过自然语言交互使用雅思写作辅助功能。

**核心特性：**
- 内置 Cambridge IELTS 8-20 官方范文（已向量化，开箱即用）
- 按 Band 分数段检索（高/中/低分范文对比），避免"过拟合"单一风格
- 支持作文批改、范文完善、话题整理、出题生成
- 支持上传图片自动识别转 Markdown
- RAG 结果缓存，重复查询秒级响应
- 可扩展：在 `src/prompts/` 添加 `.md` 文件即可自定义新模式

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Beidouchenchen/ielts-essay-assistant.git
cd ielts-essay-assistant
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

依赖说明：
- `sentence-transformers` — 文本向量化
- `faiss-cpu` — 向量检索
- `pyyaml` — 解析 frontmatter
- `numpy` — 数值计算

### 3. 构建索引

```bash
cd src && python indexer.py
```

这会读取 `data/` 目录下的所有 `.md` 文件，生成 FAISS 索引到 `index/` 目录。

> 项目已内置 Cambridge 8-20 的范文数据，克隆后即可使用。

### 4. 安装为 Claude Code Skill

将整个项目复制到 Claude Code 的 skills 目录：

```bash
# Windows
xcopy /E /I "ielts-essay-assistant" "%USERPROFILE%\.claude\skills\ielts-essay-assistant"

# macOS/Linux
cp -r ielts-essay-assistant ~/.claude/skills/
```

### 5. 使用

在 Claude Code 中直接输入自然语言即可触发：

```
请帮我批改这篇雅思作文
生成一篇关于科技话题的范文
总结一下教育类的题目和范文
```

---

## 功能说明

| 功能 | 触发词示例 | 说明 |
|------|-----------|------|
| **作文批改** | 批改、评分、打分 | 按 TR/CC/LR/GRA 四项评分，引用具体句子 |
| **范文完善** | 完善、改写、润色 | 低分改高分，附 Band 分数对比 + 修改对照表 |
| **话题整理** | 总结、整理、话题 | 汇总题目+范文+词汇+论点 |
| **出题生成** | 出题、生成题目 | 生成 Task 2 新题 + Band 8.5 参考范文 |
| **重建索引** | `/yasi-init`、重建索引 | data 有新数据后重新向量化 |

---

## 添加数据

### 方式一：直接写 Markdown

在 `data/` 对应目录下创建 `.md` 文件：

```
data/
├── cambridge-18/
│   └── test-01/
│       ├── metadata.yaml
│       ├── task1-question.md
│       ├── task1-sample-6.0.md
│       ├── task2-question.md
│       └── task2-sample-8.0.md
└── ...
```

文件名格式：
- 题目：`task{1|2}-question.md`
- 范文：`task{1|2}-sample-{分数}.md`

### 方式二：上传图片，AI 自动识别

拍照或截图上传给 Claude，它会：
1. 识别图片中的题目/作文内容
2. 转换成结构化 Markdown
3. 保存到对应目录

提示：上传范文时告知分数（如"这是 Band 7.5 的范文"），以便正确命名。

### 方式三：批量导入

一次性上传多张图片，Claude 会按顺序识别并批量生成文件。

添加新数据后，输入 `/yasi-init` 重建索引。

---

## 评分标准

严格遵循官方雅思写作评分标准：

| 评分维度 | Task 1 | Task 2 |
|---------|--------|--------|
| Task Achievement / Response | 25% | 25% |
| Coherence & Cohesion | 25% | 25% |
| Lexical Resource | 25% | 25% |
| Grammatical Range & Accuracy | 25% | 25% |

---

## 项目结构

```
ielts-essay-assistant/
├── SKILL.md                  # Skill 定义
├── README.md                 # 本文档
├── requirements.txt          # Python 依赖
├── .gitignore                # Git 忽略规则
├── src/
│   ├── prompts/              # Prompt 模板（可自定义）
│   │   ├── grading.md        # 批改标准
│   │   ├── refinement.md     # 改写策略（含 Band 评分对比）
│   │   ├── topic-summary.md  # 总结模板
│   │   └── question-gen.md   # 出题风格
│   ├── ielts_assistant.py    # 主控脚本（含 RAG 缓存）
│   ├── indexer.py            # 索引构建
│   └── retriever.py          # 检索引擎
├── data/                     # Cambridge IELTS 8-20 范文库
├── index/                    # FAISS 索引
└── evals/                    # 测试用例
```

---

## 自定义扩展

在 `src/prompts/` 下创建新的 `.md` 文件即可添加新模式：

```markdown
---
mode: my-mode
description: 功能描述
triggers:
  - 触发词1
  - 触发词2
rag_strategy: all
---

# Prompt 内容...
```

新模式立即生效，无需重启。

---

## 许可证

[MIT License](LICENSE)
