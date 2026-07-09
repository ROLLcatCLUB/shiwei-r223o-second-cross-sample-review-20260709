import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "R223O_cross_sample_selection_note.md",
    "R223O_color_collision_reasoning_chain_product.md",
    "R223O_classroom_event_expansion_chain.json",
    "R223O_teacher_manuscript_draft_v1.md",
    "R223O_teacher_manuscript_draft_v1.html",
    "R223O_review_ledger_sample.json",
    "R223O_component_screen_evidence_trigger_map.md",
    "R223O_rubric_score.md",
    "R223O_cross_sample_validation_report.md",
    "R223O_browser_smoke_result.json",
    "R223O_teacher_manuscript_draft_v1_screenshot.png",
    "PACKAGE_MANIFEST.json",
    "README_FOR_GPT_REVIEW.md",
]

checks = []
failures = []

def check(name, cond):
    checks.append(name)
    if not cond:
        failures.append(name)

for file in REQUIRED:
    check(f"exists:{file}", (ROOT / file).exists())

teacher = (ROOT / "R223O_teacher_manuscript_draft_v1.md").read_text(encoding="utf-8")
events = json.loads((ROOT / "R223O_classroom_event_expansion_chain.json").read_text(encoding="utf-8"))
ledger = json.loads((ROOT / "R223O_review_ledger_sample.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
rubric = (ROOT / "R223O_rubric_score.md").read_text(encoding="utf-8")
smoke = json.loads((ROOT / "R223O_browser_smoke_result.json").read_text(encoding="utf-8"))

required_event_fields = [
    "event_id", "event_name", "section", "source_anchor", "teaching_responsibility",
    "student_problem", "task_release", "expected_student_responses",
    "likely_misconceptions_or_failures", "teacher_follow_up_questions",
    "teacher_scaffolding_moves", "teacher_rescue_strategy", "screen_trigger",
    "component_trigger", "learning_sheet_trigger", "evidence_trigger",
    "assessment_alignment", "transition_chain", "teacher_visible_note", "control_points"
]
required_control = ["observe", "ask_when", "rescue_when", "screen_when", "component_when", "evidence_when", "proceed_when"]

check("event_count_at_least_7", len(events["events"]) >= 7)
for i, event in enumerate(events["events"]):
    for field in required_event_fields:
        check(f"event_{i}_has_{field}", field in event and event[field] not in ("", [], {}))
    for field in required_control:
        check(f"event_{i}_control_{field}", field in event.get("control_points", {}))

check("ledger_event_count_matches", len(ledger["events"]) == len(events["events"]))
check("teacher_has_manuscript_sections", all(s in teacher for s in ["课时定位", "本课在单元中的位置", "教学目标", "教学重难点", "教学过程", "评价设计", "板书 / 大屏结构"]))
check("teacher_has_design_intents", teacher.count("【设计意图】") >= 4)
check("teacher_has_color_language", all(s in teacher for s in ["偏红", "偏蓝", "冷", "暖", "色彩感受"]))
check("teacher_has_evidence", all(s in teacher for s in ["校园色彩观察", "调色记录", "色彩创想卡"]))
check("rubric_score_23", "score=23/25" in rubric or "23/25" in rubric)
check("manifest_boundary_formal_ui_false", manifest.get("formal_ui") is False)
check("manifest_boundary_r97b_false", manifest.get("r97b_modified") is False)
check("manifest_boundary_runtime_false", manifest.get("runtime_connected") is False)
check("browser_smoke_no_backend_terms", smoke.get("hasBackendTerms") is False)
check("browser_smoke_no_wenju_migration", smoke.get("hasMigratedWenju") is False)
check("browser_smoke_no_paper_print_migration", smoke.get("hasMigratedPaperPrint") is False)
check("browser_smoke_no_overflow", smoke.get("pageOverflow") is False)
check("browser_smoke_color_language", smoke.get("hasColorLanguage") is True)

banned_sample_terms = ["文具", "智造", "代言", "赠笔礼", "纸印", "版画车间坊", "印痕"]
for term in banned_sample_terms:
    check(f"teacher_not_migrate_{term}", term not in teacher)

backend_terms = ["event_id", "component_trigger", "screen_trigger", "learning_sheet_trigger", "evidence_trigger"]
for term in backend_terms:
    check(f"teacher_no_backend_{term}", term not in teacher)

result = {
    "passed": not failures,
    "check_count": len(checks),
    "failed": len(failures),
    "failures": failures,
    "event_count": len(events["events"]),
    "rubric_score": "23/25"
}
(ROOT / "validate_1013R_R223O_second_cross_sample_validation_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
if failures:
    raise SystemExit(1)
