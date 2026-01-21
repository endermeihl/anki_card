
# anki卡片学习英语的功能

根据你的最新需求，我们需要引入**多卡片模式**（即一个单词在练习库中会生成 3 张不同的卡片：完形、拼写、场景）。


### 一、 系统流程设计 (Workflow)

我们放弃“单文件+日志”模式，采用 **“Inbox (收件箱)”** 处理模式。

#### 1. 文件夹结构

你需要建立一个工作目录，结构如下：

```text
/Anki_Auto_Builder
    /input          <-- 每天把今天的 txt 扔进去 (例如 day01.txt, words_20240121.txt)
    /processed      <-- 处理完的文件会被移动到这里 (自动加上时间戳重命名)
    /output         <-- 生成的 CSV 结果存放在这里

```

#### 2. 处理逻辑 (Controller)

1. **扫描:** 程序启动，扫描 `/input` 文件夹下所有 `.txt` 文件。
2. **读取:** 逐行读取单词。
* `strip()`: 去除首尾空格。
* `lower()`: 转为小写 (确保 DeepSeek 识别准确，但在生成卡片时，例句中的单词可以保留首字母大写等语态)。
* **去重:** 如果今天扔进去的两个文件有重复词，或者和本次运行已处理的词重复，跳过。


3. **请求:** 带着单词去请求 DeepSeek API。
4. **保存:** 分别追加写入到 `/output/learning_import.csv` 和 `/output/practice_import.csv`。
5. **归档:** 将处理完的 txt 文件移动到 `/processed`，建议重命名为 `原始文件名_processed_时间戳.txt`。

---

### 二、 DeepSeek API 交互设计 (JSON Schema)

为了满足你的 **Type A + Type B (3种模式)**，我们需要 AI 返回一个非常详细的 JSON 对象。

**System Prompt 设定：**

> 你是一个专业的 Anki 卡片生成助手。请针对用户提供的单词，生成用于语言学习的 JSON 数据。
> 如果单词没有明显的语音同化现象（Assimilation），该字段请填“无”。

**User Prompt 模板：**

> 单词：{target_word}
> 请返回如下 JSON 格式：
> ```json
> {
>   "word": "原词",
>   "phonetic": "音标 (英/美)",
>   "meaning": "中文简明释义",
>   "learning_data": {
>     "source_code": "词根词缀分析",
>     "assimilation": "语音同化规则 (若无则填'无')",
>     "logic": "记忆逻辑链",
>     "note": "扩展备注/词源",
>     "example": "例句 (英文)",
>     "example_cn": "例句 (中文翻译)"
>   },
>   "practice_data": {
>     "cloze": {
>       "sentence": "生成一个完形填空句子，将目标词替换为 {{c1::目标词}}，确保语境不同于学习卡例句",
>       "hint": "中文提示"
>     },
>     "spelling": {
>       "definition": "用于拼写检查的英文释义或中文释义",
>       "sentence_front": "用于提示的句子，目标词用 _____ 代替"
>     },
>     "scenario": {
>       "context": "描述一个微小的具体场景（中文），诱导用户用出这个词",
>       "question": "问题引导 (例如：你会用哪个动词来描述这个动作？)"
>     }
>   }
> }
> 
> ```
> 
> 

---

### 三、 CSV 与 Anki 卡片模型设计

这是最关键的部分。为了实现导入，我们需要定义两个 CSV 文件的表头。

#### 1. 学习用 CSV (`learning_import.csv`)

**对应 Anki 模板：** `English_Deep_Learning` (新建一个模板)
**字段 (Columns):**

1. **Word** (主键)
2. **Phonetic**
3. **Meaning**
4. **SourceCode**
5. **Assimilation**
6. **Logic**
7. **Note**
8. **Example_En**
9. **Example_Cn**

#### 2. 练习用 CSV (`practice_import.csv`)

**策略：** 这里我们创建一个 **“多合一”的笔记类型 (Note Type)**，命名为 `English_Practice_Master`。
**原理：** 你只需要导入一行数据，Anki 会根据这行数据，自动生成 3 张不同的卡片（完形卡、拼写卡、场景卡）。

**字段 (Columns):**

1. **Word** (答案)
2. **Meaning** (作为提示)
3. **Cloze_Text** (API返回的 `practice_data.cloze.sentence`)
4. **Cloze_Hint** (API返回的 `practice_data.cloze.hint`)
5. **Spell_Def** (API返回的 `practice_data.spelling.definition`)
6. **Scenario_Context** (API返回的 `practice_data.scenario.context`)
7. **Scenario_Question** (API返回的 `practice_data.scenario.question`)

---

### 四、 Anki 内部卡片呈现 (预览)

在导入 `practice_import.csv` 后，Anki 会基于一行数据生成以下三张卡片：

#### **卡片 1：完形填空 (Cloze)**

* **正面:**
* The plan was {{c1::combined}} with regular exercise.
* *提示按钮:* 联合


* **背面:**
* The plan was **combined** with regular exercise.
* (附加: Meaning)



#### **卡片 2：拼写检查 (Spelling)**

* **正面:**
* **Definition:** (使)联合
* **Context:** A good diet _____ with regular exercise is key.
* **Input Box:** [ 用户输入框 ] (使用 Anki 的 `{{type:Word}}` 功能)


* **背面:**
* **Word:** combine
* **Check:** (显示你输入的对错比对)



#### **卡片 3：微场景 (Micro-Scenario)**

* **正面:**
* **场景:** 汤姆手里有两种不同颜色的粘土，他把它们捏在了一起，变成了一个大的双色球。
* **提问:** 描述“捏在一起/结合”这个动作的动词原形是？
* **Input Box:** [ 用户输入框 ] (同样使用 `{{type:Word}}`)


* **背面:**
* **Answer:** combine
* **Check:** (比对结果)

---

### 五、 总结确认

这个设计满足了你的所有需求：

1. **输入自动化：** 只要把 txt 扔进文件夹，程序自动处理并移走，不修改原文件。
2. **内容深度：** 包含词源、逻辑，并处理了“无同化”的情况。
3. **练习多样性：** 实现了**完形、拼写、场景**三种训练模式。
4. **输出结构：** 两个独立的 CSV，分别用于“学习”和“练习”两个不同的 Deck 或用途。

