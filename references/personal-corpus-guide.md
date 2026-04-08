# Personal Corpus Guide

## 个人语料库功能说明

个人语料库允许你：
1. **添加官方范文** - 从 Cambridge IELTS 书籍、British Council PDF 等来源
2. **存储个人习作** - 保存自己的练习作文
3. **AI 分析学习** - 自动提取高分技巧
4. **生成新范文** - 应用学习到的技巧到新话题

---

## 如何添加范文到语料库

### 方式1: 直接添加官方范文

```
你: 我要添加一篇官方范文

系统: 请提供以下信息：
- 来源 (如: Cambridge IELTS 16, Test 1)
- 官方评分 (如: Band 9)
- 题目 (Task prompt)
- 范文内容 (Essay text)

你: [提供信息]

系统: ✓ 已添加到语料库
    - 分析完成：提取了 5 个结构技巧，12 个高分词汇
    - 已应用学习：可在新话题中使用这些技巧
```

### 方式2: 批量添加

```
你: 我想批量添加多篇范文

系统: 请按照以下格式提供：

--- ESSAY 1 ---
Source: [来源]
Band: [分数]
Prompt: [题目]
Essay: [内容]

--- ESSAY 2 ---
Source: [来源]
...

你: [提供内容]

系统: ✓ 已添加 X 篇范文到语料库
```

### 方式3: 添加个人习作

```
你: 添加我的练习作文

系统: 请提供：
- 题目
- 你的作文
- 目标分数 (可选)
- 特定想改进的方面 (可选)

你: [提供内容]

系统: ✓ 已存储你的习作
    - 当前水平预估: Band X
    - 建议改进点: [具体分析]
    - 推荐对比的官方范文: [语料库中的相关范文]
```

---

## 语料库分析功能

### 1. 单篇分析

```
你: 分析语料库中 Cambridge IELTS 17 的那篇 Band 9 范文

系统: 
## 官方样本分析报告
**来源**: Cambridge IELTS 17, Test 2, Writing Task 2
**官方评分**: Band 9

### 结构技巧 (Structure)
1. **Introduction**: General → Specific → Thesis
   - Pattern: "The question of whether... is a contentious issue"
   - Clear position statement

2. **Body Paragraphs**: TEEL Structure
   - Topic sentence with clear main idea
   - Explanation with development
   - Example (specific or hypothetical)
   - Link to next paragraph

3. **Conclusion**: Restate + Summary + Final thought
   - No new ideas
   - Strong closing statement

### 高分词汇 (Lexical Resource)
| 基础词 | 高级替换 | 语境 |
|--------|----------|------|
| big problem | contentious issue | 争议话题 |
| think | argue / contend | 表达观点 |
| bad | detrimental / adverse | 负面影响 |
| good | beneficial / advantageous | 正面影响 |
| very | considerably / significantly | 程度修饰 |

### 句式变化 (Grammatical Range)
- **复合句**: While some argue that..., I believe that...
- **条件句**: Were governments to..., they would...
- **倒装句**: Not only does..., but it also...
- **分词结构**: Having considered..., ...
- **被动语态**: It is widely acknowledged that...

### 衔接技巧 (Cohesion)
- **观点对比**: On the one hand... On the other hand...
- **递进**: Furthermore, Moreover, In addition
- **转折**: Nevertheless, Conversely, However
- **因果**: Consequently, As a result, Therefore
- **举例**: For instance, A case in point is

### 可学习点 (Key Takeaways)
1. [技巧1]
2. [技巧2]
3. [技巧3]
```

### 2. 对比分析

```
你: 对比语料库中 Band 6 和 Band 9 的两篇范文

系统:
## 对比分析报告

### 主要差距

| 维度 | Band 6 | Band 9 | 改进方法 |
|------|--------|--------|----------|
| 词汇 | 基础词汇重复 | 精准多样 | 学习同义词替换 |
| 句式 | 简单句为主 | 复杂句多变 | 练习从句结构 |
| 衔接 | 基础连接词 | 自然过渡 | 学习高级连接词 |
| 论证 | 观点简单 | 深入展开 | TEEL结构训练 |

### 具体对比示例

**Introduction 对比:**
- Band 6: "Nowadays, crime is a big problem..."
- Band 9: "The question of how to effectively reduce crime rates is a contentious issue that has generated considerable debate..."

**Body Paragraph 对比:**
- Band 6: [简单陈述]
- Band 9: [详细展开，有例子，有深度]
```

### 3. 话题归类

```
你: 查看语料库中教育话题的所有范文

系统:
## 教育话题范文库 (X 篇)

### Band 9 范文
1. [来源] - [题目简述]
   - 关键技巧: [总结]
   
### Band 8 范文
1. [来源] - [题目简述]
   - 关键技巧: [总结]

### 该话题常用高分表达
| 中文意思 | 高级表达 |
|----------|----------|
| 获得知识 | acquire knowledge / gain insights |
| 培养技能 | cultivate skills / foster abilities |
| 批判思维 | critical thinking / analytical skills |
| 终身学习 | lifelong learning / continuous education |
```

---

## 基于语料库生成新范文

### 生成方式

```
你: 基于我语料库中的范文，生成一篇关于[新话题]的 Band 8 范文

系统:
## 新范文生成

**题目**: [新话题]

**应用的学习点**:
- 结构: 采用 Cambridge IELTS 17 Band 9 的 TEEL 结构
- 词汇: 使用语料库中提取的教育话题高分词汇
- 句式: 应用官方范文中的复合句和倒装结构
- 衔接: 使用学到的自然过渡技巧

**生成的范文**:
[完整范文]

**为什么这是 Band 8 水平**:
- [逐点解释]

**与官方范文的对比**:
- [展示如何应用了学到的技巧]
```

---

## 语料库管理

### 查看语料库

```
你: 查看我的语料库

系统:
## 个人语料库概览

**总计**: X 篇范文

**按来源分类**:
- Cambridge IELTS: X 篇
  - Book 16: X 篇
  - Book 17: X 篇
  - ...
- British Council PDF: X 篇
- 个人习作: X 篇

**按分数分类**:
- Band 9: X 篇
- Band 8: X 篇
- Band 7: X 篇
- Band 6: X 篇
- 未评分(个人习作): X 篇

**按话题分类**:
- 教育: X 篇
- 科技: X 篇
- 环境: X 篇
- 健康: X 篇
- 工作: X 篇
- ...
```

### 搜索语料库

```
你: 搜索语料库中包含 "critical thinking" 的范文

系统:
找到 X 篇包含 "critical thinking" 的范文:

1. [来源] - [上下文句子]
2. [来源] - [上下文句子]
...
```

### 删除/更新

```
你: 删除语料库中 [来源] 的范文
你: 更新 [来源] 范文的分析
```

---

## 使用建议

### 建立语料库的步骤

1. **Step 1**: 下载 British Council 免费 PDF (包含真实考生范文)
2. **Step 2**: 将 Band 7-9 的范文添加到语料库
3. **Step 3**: 让系统分析每篇范文，提取技巧
4. **Step 4**: 添加自己的习作作为对比
5. **Step 5**: 基于学习生成新范文练习

### 高效学习方法

- **每周添加 2-3 篇官方范文**
- **分析后模仿写同一话题**
- **对比自己的版本和官方版本**
- **积累话题-specific 词汇库**

### 推荐优先级

**高优先级** (先添加):
- Cambridge IELTS 16-18 (最新真题)
- Band 8-9 考生范文 (British Council PDF)

**中优先级**:
- Band 7 范文 (了解不同水平)
- 自己的习作 (跟踪进步)

**低优先级**:
- Band 6 及以下 (了解问题所在)
