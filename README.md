# Anki 卡片生成器 - 使用文档

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- DeepSeek API 密钥

### 安装步骤

1. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

2. **配置 API 密钥**

   复制 `.env.example` 为 `.env`，并填入你的 DeepSeek API 密钥：

   ```bash
   cp .env.example .env
   ```

   编辑 `.env` 文件：

   ```
   DEEPSEEK_API_KEY=你的API密钥
   ```

3. **准备单词文件**

   将包含单词的 `.txt` 文件放入 `Anki_Auto_Builder/input/` 目录。

   文件格式要求：
   - 每行一个单词
   - UTF-8 编码
   - 支持多个文件同时处理

   示例文件内容：
   ```
   combine
   elaborate
   demonstrate
   implement
   ```

4. **运行程序**

   ```bash
   python main.py
   ```

## 输出说明

### 输出文件位置

程序运行后，会在 `Anki_Auto_Builder/output/` 目录生成两个 CSV 文件：

- `learning_import.csv` - 学习卡片数据
- `practice_import.csv` - 练习卡片数据

### 学习卡片字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| Word | 单词 | combine |
| Phonetic | 音标 | /kəmˈbaɪn/ |
| Meaning | 中文释义 | v. 结合，联合；n. 联合企业 |
| SourceCode | 词源分析 | com-(一起) + bine(绑) = 绑在一起 |
| Assimilation | 记忆联想 | 联想：com(来) + bine(拜) = 来拜访后结合 |
| Logic | 使用逻辑 | 强调将不同元素整合为一体 |
| Note | 注意事项 | 区分 combine with 和 combine...and... |
| Example_En | 英文例句 | We need to combine theory with practice. |
| Example_Cn | 例句翻译 | 我们需要将理论与实践相结合。 |

### 练习卡片字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| Word | 单词 | combine |
| Meaning | 中文释义 | v. 结合，联合 |
| Cloze_Text | 完形填空句 | We need to _____ our efforts to succeed. |
| Cloze_Hint | 填空提示 | 联合，结合 |
| Spell_Def | 拼写练习定义 | to join or merge together |
| Scenario_Context | 情景描述 | 你正在参加团队会议讨论项目合作 |
| Scenario_Question | 情景问题 | 如何表达"结合两个团队的资源"？ |

## 导入 Anki

### 准备工作

在导入之前，需要在 Anki 中创建对应的笔记类型：

#### 1. 创建学习卡片笔记类型

笔记类型名称：`English_Deep_Learning`

字段（按顺序）：
1. Word
2. Phonetic
3. Meaning
4. SourceCode
5. Assimilation
6. Logic
7. Note
8. Example_En
9. Example_Cn

#### 2. 创建练习卡片笔记类型

笔记类型名称：`English_Practice_Master`

字段（按顺序）：
1. Word
2. Meaning
3. Cloze_Text
4. Cloze_Hint
5. Spell_Def
6. Scenario_Context
7. Scenario_Question

建议创建 3 个卡片模板：
- **完形填空卡片**：正面显示 Cloze_Text，背面显示 Word
- **拼写练习卡片**：正面显示 Spell_Def，背面显示 Word
- **情景问答卡片**：正面显示 Scenario_Context + Scenario_Question，背面显示 Word

### 导入步骤

1. 打开 Anki
2. 点击 **文件** → **导入**
3. 选择 `learning_import.csv` 或 `practice_import.csv`
4. 设置导入选项：
   - **类型**：选择对应的笔记类型
   - **牌组**：选择目标牌组
   - **字段分隔符**：逗号
   - **允许在字段中使用HTML**：勾选（如果内容包含格式）
5. 确认字段映射正确
6. 点击 **导入**

## 常见问题

### Q: API 调用失败怎么办？

程序会自动重试 3 次。如果仍然失败，该单词会被跳过并记录在最终报告中。你可以：
1. 检查网络连接
2. 确认 API 密钥是否正确
3. 检查 API 账户余额
4. 将失败的单词单独保存，稍后重试

### Q: 如何处理大量单词？

- 程序会逐个处理单词，显示进度
- 建议每次处理不超过 100 个单词
- 可以分批处理，每批生成的 CSV 会覆盖之前的文件

### Q: 如何自定义 API 提示词？

编辑 `api/deepseek.py` 文件中的 `SYSTEM_PROMPT` 和 `USER_PROMPT_TEMPLATE` 变量。

### Q: 输出的 CSV 文件乱码？

确保：
1. 使用支持 UTF-8 的编辑器查看
2. 导入 Anki 时选择 UTF-8 编码

### Q: 如何添加新的卡片类型？

1. 在 `generators/` 目录创建新的生成器类
2. 在 `api/deepseek.py` 中扩展 API 响应格式
3. 在 `main.py` 中集成新的生成器

## 文件归档说明

处理完成后，原始输入文件会被移动到 `Anki_Auto_Builder/processed/` 目录，并添加时间戳后缀。

例如：
- 原文件：`words.txt`
- 归档后：`words_20240115_143022.txt`

这样可以：
- 避免重复处理同一文件
- 保留处理历史记录
- 方便追溯和排查问题

## 运行示例

```
==================================================
Anki Card Generator
==================================================

[1/5] Scanning input directory...
Found 1 file(s):
  - test.txt

[2/5] Collecting words...
Found 3 unique word(s)

[3/5] Generating card data via DeepSeek API...
  Processing [1/3]: combine... OK
  Processing [2/3]: elaborate... OK
  Processing [3/3]: demonstrate... OK

[4/5] Writing CSV files...
  Learning cards: Anki_Auto_Builder/output/learning_import.csv
  Practice cards: Anki_Auto_Builder/output/practice_import.csv

[5/5] Archiving processed files...
  Archived: test_20240115_143022.txt

==================================================
Summary
==================================================
Total words: 3
Successful: 3
Failed: 0

Done!
```