# R223O 第二轮跨样本验证审核包

```text
stage_id=1013R_R223O_SECOND_CROSS_SAMPLE_VALIDATION
status=PASS_LOCAL_VALIDATOR
sample=第二单元 色彩的碰撞
rubric_score=23/25
formal_ui=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 建议 GPT 审核顺序

1. `R223O_teacher_manuscript_draft_v1.html`
2. `R223O_teacher_manuscript_draft_v1.md`
3. `R223O_teacher_manuscript_draft_v1_screenshot.png`
4. `R223O_rubric_score.md`
5. `R223O_classroom_event_expansion_chain.json`
6. `R223O_review_ledger_sample.json`
7. `R223O_cross_sample_validation_report.md`
8. `R223O_browser_smoke_result.json`

## 审核重点

- 是否像成熟教师教案文稿，而不是事件字段稿；
- 是否真正适配视觉语言 / 色彩感知课型；
- 是否没有迁移文具课或纸印课内容；
- 学生反应和教师追问是否符合三年级学情；
- 大屏、学习单、评价证据是否从课堂事件长出来；
- 是否仍然不改 R97B、不接 runtime、不做 formal apply。
