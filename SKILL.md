---
name: ielts-essay-assistant
description: IELTS 写作助手 — 批改作文、评分、改写提升、话题整理、出题生成。当用户提到雅思、IELTS、写作、作文、Task 1、Task 2、上传作文图片、要求批改/评分/改写/出题/整理话题时触发。即使用户只是说"帮我看看这篇作文"或"这个话题怎么写"，也应使用此 skill。
---

# IELTS Essay Assistant

基于 RAG 的雅思写作助手，内置 Cambridge IELTS 8-20 范文库，开箱即用。

## Skill 目录定位

本 skill 是自包含的，所有代码和数据都在 skill 目录内。执行命令前，先定位 skill 目录：

本 skill 是自包含的，所有代码和数据都在 skill 目录内。安装后所有命令自动在 skill 目录下执行。

## 核心能力

1. **作文批改** — 模仿雅思考官，按 TR/CC/LR/GRA 四项评分
2. **范文完善** — 将低分范文改写为高分范文，给出修改对照
3. **话题整理** — 按话题检索资料库，汇总题目+范文+词汇+论点
4. **出题生成** — 根据话题方向生成 Task 2 新题 + Band 8.5 参考范文
5. **重建索引** — data 目录有新数据后，运行重建索引

## 工作流程

### Step 1: 意图检测

| 模式 | 触发词 |
|------|--------|
| grading (批改) | 批改、评分、打分、批阅、改作文 |
| refinement (完善) | 完善、改写、提升、润色、改写成、优化 |
| topic-summary (话题) | 总结、整理、话题、相关题目、资料、汇总 |
| question-gen (出题) | 出题、生成题目、新题、模拟题、练习题 |
| rebuild-index (重建索引) | 重建索引、更新索引、rebuild index、/yasi-init |
| 自定义模式 | 读取 `src/prompts/*.md` 中的 triggers 字段动态匹配 |

### Step 2: RAG 检索

```bash
cd src && python -c "
from ielts_assistant import IELTSAssistant
assistant = IELTSAssistant('../index')
result = assistant.run_mode('{mode}', '{用户内容}', '{题目}', '{task_type}')
print(result)
"
```

检索策略：
- **grading**: `mixed_scores` — 混合高/中/低分范文
- **refinement**: `high_only` — 仅高分范文(7.5+)
- **topic-summary**: `all` — 该话题下所有材料
- **question-gen**: `all` — 现有题目避免重复

### Step 3: 生成回答

结合 prompt 模板 + RAG 检索结果 + 用户输入，生成结构化回答。

### 重建索引

用户输入 `/yasi-init` 或说"重建索引"时，执行：

```bash
cd src && python indexer.py
```

### 图片处理

用户上传 IELTS 图片时：
1. 识别图片内容
2. 确认：题目还是范文？哪个 test？分数？
3. 保存到 `data/cambridge-{N}/test-{XX}/`
4. 提示用户重建索引

## 重要原则

### 避免"过拟合"
- 参考范文仅作为"评分坐标系"，不是"模仿模板"
- 对比高/中/低分范文，说明分数差异原因
- 提炼通用技巧，不要模仿特定表达

### 输出语言
- 评语和解释用 **中文**
- 引用原文和修改建议用 **英文**
- 专业术语保留英文（TR, CC, LR, GRA, Band score）

### 批改深度
- 必须引用具体句子
- 每个维度给出明确分数（1-9）和理由
- 提供可操作的改进建议

## 目录结构

```
ielts-essay-assistant/          ← skill 目录
├── SKILL.md                    ← 本文件
├── src/
│   ├── prompts/                ← Prompt 模板（可自定义）
│   ├── ielts_assistant.py      ← 主控脚本
│   ├── indexer.py              ← 索引构建
│   └── retriever.py            ← 检索引擎
├── data/                       ← Cambridge IELTS 8-20
└── index/                      ← FAISS 索引
```

## 环境要求

- Python 3.10+
- sentence-transformers — 文本向量化
- faiss-cpu — 向量检索
- pyyaml — 解析 frontmatter
- numpy — 数值计算
