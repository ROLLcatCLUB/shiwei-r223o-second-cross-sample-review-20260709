# R223O 跨样本课堂事件展开验证报告

```text
stage_id=1013R_R223O_SECOND_CROSS_SAMPLE_VALIDATION
source_standard=R223M-P5 GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1
sample=第二单元 色彩的碰撞
decision=PASS_SECOND_CROSS_SAMPLE_VALIDATION_WITH_TEACHER_MANUSCRIPT_STANDARD
rubric_score=23/25
formal_ui=false
r97b_modified=false
runtime_connected=false
provider_model_connected=false
database_written=false
```

## 验证结论

R223O 使用《色彩的碰撞》验证课堂事件展开标准是否能迁移到视觉语言和色彩感知类课型。结果显示，同一 classroom_event_expansion schema 可以表达“校园色彩观察、三原色起点、两色调和、同色差异、复色进阶、色彩碰撞任务、展示收束”等课堂事件。

教师默认稿采用 R223N-P3-P1 确认后的文稿文法：课时定位、本课在单元中的位置、教学目标、重难点、教学准备、单课结构、教学过程、评价设计和板书 / 大屏结构。完整 review ledger 另行保留，不进入教师默认稿。

## 关键守住点

- 不迁移《我为文具代言》的文具、智造、代言、赠笔礼。
- 不迁移《有趣的纸印》的纸材、版画、印痕、试印结构。
- 组件、大屏、学习单和证据均从课堂事件触发。
- 教师默认稿不显示 event_id、component_trigger、screen_trigger 等后端字段。
- 本包只做静态验证，不改 R97B，不接 runtime / model / prompt / db。

## 浏览器 smoke

```text
url=http://127.0.0.1:8909/R223O_teacher_manuscript_draft_v1.html
design_intent_count=4
h4_count=7
table_count=3
has_unit_position=true
has_color_language=true
has_backend_terms=false
has_migrated_wenju=false
has_migrated_paper_print=false
page_overflow=false
```

## 建议

第三样本已证明标准可迁移到视觉语言 / 色彩感知类课型。下一步可以继续选择《会说话的手》验证身体符号 / 表演 / 图像转译类课型，或先由教师审核本稿的课堂可读性与色彩美术味。
