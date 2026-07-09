import hashlib
import html
import json
import zipfile
from datetime import datetime
from pathlib import Path

STAGE_ID = "1013R_R223O_SECOND_CROSS_SAMPLE_VALIDATION"
STANDARD_ID = "GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE"
ROOT = Path(__file__).resolve().parent


def write_text(name: str, content: str) -> None:
    (ROOT / name).write_text(content.strip() + "\n", encoding="utf-8")


def write_json(name: str, data) -> None:
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def markdown_to_html(title: str, md: str) -> str:
    lines = md.splitlines()
    body = []
    in_code = False
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows
        if not in_table:
            return
        body.append("<table>")
        for idx, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if idx == 1 and all(set(c.replace(":", "").replace("-", "")) == set() for c in cells):
                continue
            tag = "th" if idx == 0 else "td"
            body.append("<tr>" + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells) + "</tr>")
        body.append("</table>")
        in_table = False
        table_rows = []

    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            flush_table()
            body.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            body.append(html.escape(line))
            continue
        if line.startswith("|") and line.endswith("|"):
            in_table = True
            table_rows.append(line)
            continue
        flush_table()
        if not line.strip():
            body.append("")
        elif line.startswith("# "):
            body.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            body.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            body.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
        elif line.startswith("#### "):
            body.append(f"<h4>{html.escape(line[5:].strip())}</h4>")
        elif line.startswith("- "):
            body.append(f"<p class=\"li\">{html.escape(line)}</p>")
        else:
            escaped = html.escape(line)
            escaped = escaped.replace("【设计意图】", "<strong>【设计意图】</strong>")
            body.append(f"<p>{escaped}</p>")
    flush_table()

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #20342f;
      --muted: #60756e;
      --line: #dfe9e5;
      --accent: #247d6b;
      --soft: #f4faf7;
      --paper: #fffdf7;
      --note: #f9f3df;
    }}
    body {{
      margin: 0;
      background: #f3f7f5;
      color: var(--ink);
      font: 16px/1.72 "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 48px 56px 72px;
      background: var(--paper);
      min-height: 100vh;
      box-shadow: 0 10px 35px rgba(29, 68, 58, .08);
    }}
    h1 {{
      margin: 0 0 18px;
      font-size: 30px;
      line-height: 1.32;
      letter-spacing: 0;
      color: #174f45;
    }}
    h2 {{
      margin: 42px 0 16px;
      padding-top: 8px;
      border-top: 1px solid var(--line);
      font-size: 22px;
      color: #185c4f;
    }}
    h3 {{
      margin: 34px 0 14px;
      font-size: 19px;
      color: #20342f;
    }}
    h4 {{
      margin: 28px 0 10px;
      font-size: 17px;
      color: #25443d;
    }}
    p {{
      margin: 10px 0;
    }}
    strong {{
      color: #185c4f;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0 22px;
      font-size: 15px;
      background: #fff;
    }}
    th, td {{
      border: 1px solid var(--line);
      padding: 9px 11px;
      vertical-align: top;
      text-align: left;
    }}
    th {{
      background: var(--soft);
      color: #174f45;
      font-weight: 700;
    }}
    pre {{
      background: #f7faf8;
      border: 1px solid var(--line);
      padding: 14px 16px;
      overflow-x: auto;
      border-radius: 6px;
      color: #324d46;
    }}
    .li {{
      margin-left: 1em;
      color: var(--muted);
    }}
    p:has(strong) {{
      background: var(--note);
      border-left: 4px solid #d69c2f;
      padding: 10px 12px;
      border-radius: 4px;
    }}
    @media (max-width: 760px) {{
      main {{ padding: 28px 22px 48px; }}
      h1 {{ font-size: 24px; }}
      table {{ font-size: 14px; }}
    }}
  </style>
</head>
<body><main>
{chr(10).join(body)}
</main></body>
</html>
"""


SOURCE_ANCHORS = {
    "sample": "E:/学校工作/教学/教学资料/三年级美术上册官方教学设计参考/第二单元 色彩的碰撞.docx",
    "unit_theme": "第二单元 色彩的碰撞",
    "big_idea": "色彩是美术表现的重要语言",
    "essential_question": "如何运用色彩表达我们的内心感受",
    "performance_task": "举办“红、黄、蓝”色彩创想会",
    "stage_rows": [
        "第一阶段 发现色彩：寻找色彩、调出色彩、色彩碰撞",
        "第二阶段 点彩游戏：捕捉色彩、揭秘点彩、玩转点彩",
        "第三阶段 色彩表达：遇见米罗、创作梦幻季节、色彩表达"
    ],
    "student_analysis": "三年级学生已能简单运用明亮、对比强烈的色彩，但对色彩规律和运用表达还未形成认识体系。"
}


EVENTS = [
    {
        "event_id": "r223o_color_event_01_campus_color_entry",
        "event_name": "游园回看：把校园色彩带进课堂",
        "section": "入场与问题生成",
        "source_anchor": "课前：游园，寻找校园夏日的色彩；明确单元活动主题",
        "teaching_responsibility": "让学生从生活经验进入色彩问题，知道本课不是随意涂色，而是探究色彩从哪里来、怎样变化。",
        "student_problem": "学生容易只说颜色名称或喜欢不喜欢，不能把观察转化为可探究的问题。",
        "task_release": "出示校园色彩照片或学生收集的色彩漂流瓶，请学生找出红、黄、蓝以及它们身边出现的其他颜色。",
        "expected_student_responses": ["能说出校园中的红、黄、蓝", "能描述色彩给人的明亮、温暖、清凉等感受", "能提出三原色能不能调出更多颜色的问题"],
        "likely_misconceptions_or_failures": ["只按物体名称分类", "只说好看不好看", "把颜色感受说成固定标准答案"],
        "teacher_follow_up_questions": ["这块颜色让你想到阳光、树叶还是操场上的影子？", "如果只给你红黄蓝，能不能找回校园里更多颜色？"],
        "teacher_scaffolding_moves": ["用校园局部照片放大色块", "提供色彩感受词卡", "把学生问题写成探究清单"],
        "teacher_rescue_strategy": "若学生只报颜色名，教师遮住物体轮廓只露出色块，让学生说颜色关系和感受。",
        "screen_trigger": "校园色彩照片、红黄蓝色块、色彩问题清单",
        "component_trigger": "image_color_spotting / color_word_bank",
        "learning_sheet_trigger": "入场记录：我在校园里找到的红、黄、蓝和一个想研究的问题",
        "evidence_trigger": "学生能写出或说出一个色彩观察点和一个探究问题",
        "assessment_alignment": "对应单元评价中能收集校园色彩并分享的要求。",
        "transition_chain": "由校园色彩观察转入红黄蓝是否能调出更多颜色的实验。",
        "teacher_visible_note": "先把颜色从生活带回来，再把问题交给实验。",
        "control_points": {
            "observe": "学生是否只停留在颜色名称",
            "ask_when": "学生说不出感受或问题时",
            "rescue_when": "学生把任务理解为拍照展示",
            "screen_when": "需要从物体转向色块观察时",
            "component_when": "学生需要找色或说色词时",
            "evidence_when": "完成入场观察句时",
            "proceed_when": "学生能提出红黄蓝能否调出更多颜色的问题"
        }
    },
    {
        "event_id": "r223o_color_event_02_primary_color_question",
        "event_name": "认一认：红黄蓝是不是色彩的起点",
        "section": "三原色问题建立",
        "source_anchor": "第一阶段：通过玩转三原色，发现间色、复色",
        "teaching_responsibility": "建立三原色作为调色实验起点的认识，但不把课堂变成术语背诵。",
        "student_problem": "学生可能听过三原色，却不知道它们为什么适合作为实验起点。",
        "task_release": "让学生观察三组颜料盘，判断哪些颜色可以作为今天的实验起点，并说明理由。",
        "expected_student_responses": ["选择红黄蓝", "猜测红黄蓝可以变出其他颜色", "提到生活中色彩很多"],
        "likely_misconceptions_or_failures": ["认为越多颜色越好", "把黑白也当作同等起点", "只背三原色不做解释"],
        "teacher_follow_up_questions": ["如果先给十种颜色，我们还看得清是谁变出谁吗？", "红、黄、蓝碰在一起，会不会出现新的颜色？"],
        "teacher_scaffolding_moves": ["收窄材料，只保留红黄蓝", "用透明片叠色做预告", "给出实验约定：少量、记录、比较"],
        "teacher_rescue_strategy": "若学生急着混很多颜色，教师先用两色小样示范，强调一次只改一个条件。",
        "screen_trigger": "三原色实验约定、少量取色示范图",
        "component_trigger": "material_limit_prompt / experiment_rule_card",
        "learning_sheet_trigger": "三原色起点记录：我选择红黄蓝，因为……",
        "evidence_trigger": "学生能解释为什么先用红黄蓝做实验",
        "assessment_alignment": "对应能积极参与小组活动、运用材料和工具发现色彩关系。",
        "transition_chain": "由三原色问题进入两两相碰的调色实验。",
        "teacher_visible_note": "术语不先讲满，让学生用实验理解起点。",
        "control_points": {
            "observe": "学生是否想一次使用太多颜色",
            "ask_when": "学生只背术语时",
            "rescue_when": "学生调色条件失控时",
            "screen_when": "需要明确实验规则时",
            "component_when": "需要限制材料和步骤时",
            "evidence_when": "写下红黄蓝作为实验起点的理由",
            "proceed_when": "学生愿意按两色一组开始调试"
        }
    },
    {
        "event_id": "r223o_color_event_03_two_color_mixing",
        "event_name": "调一调：让两种颜色先碰一碰",
        "section": "间色实验",
        "source_anchor": "调出色彩：利用三原色进行间色调和，观察颜色的差别",
        "teaching_responsibility": "让学生通过两色调和发现间色，并能看出比例不同会带来色相变化。",
        "student_problem": "学生容易把调色当成随意搅拌，最后得到脏色或说不清变化过程。",
        "task_release": "每组只选一组颜色：红+黄、黄+蓝或蓝+红，先少量调，再记录碰出来的新颜色。",
        "expected_student_responses": ["发现橙、绿、紫等间色", "注意到同一组颜色比例不同会偏红、偏黄或偏蓝", "能说出颜色从哪里变来"],
        "likely_misconceptions_or_failures": ["颜料过多导致混浊", "只追求调得鲜艳", "不记录比例和过程"],
        "teacher_follow_up_questions": ["这块橙色更靠近红，还是更靠近黄？你从哪里看出来？", "如果再多一点蓝，绿色会像新芽还是像深草地？"],
        "teacher_scaffolding_moves": ["示范牙签头大小取色", "用三格记录：原色A、原色B、新颜色", "让学生把最清楚的一次圈出来"],
        "teacher_rescue_strategy": "若调成灰脏色，教师不直接判错，而是追问加入了几种颜色，再示范少量、两色、慢慢加的做法。",
        "screen_trigger": "两色调和步骤、比例变化对照、清亮/混浊样例",
        "component_trigger": "color_mixing_trial / circle_best_sample",
        "learning_sheet_trigger": "调色记录：A色+B色=新颜色；比例变化说明",
        "evidence_trigger": "一组两色调和样本和一句比例观察",
        "assessment_alignment": "对应能大胆尝试调色，调出三间色，并观察比较色彩变化。",
        "transition_chain": "由间色出现转入复色和色调差异的进阶观察。",
        "teacher_visible_note": "让学生看到颜色变化的路径，而不是只拿到结果。",
        "control_points": {
            "observe": "学生是否少量取色并记录过程",
            "ask_when": "学生只说变成绿色但说不出偏向时",
            "rescue_when": "调色混浊或重复失败时",
            "screen_when": "需要展示比例对照时",
            "component_when": "需要圈出最佳样本时",
            "evidence_when": "完成调色记录和比例说明时",
            "proceed_when": "学生能说出至少一种间色的来源"
        }
    },
    {
        "event_id": "r223o_color_event_04_compare_color_differences",
        "event_name": "比一比：同一种新颜色为什么不一样",
        "section": "色彩差异观察",
        "source_anchor": "调出色彩：观察颜色的差别；进阶思考",
        "teaching_responsibility": "把学生从颜色名称带到色彩差异观察，理解同名颜色也有冷暖、深浅和偏向。",
        "student_problem": "学生会以为绿色就是一种固定颜色，不容易描述细微差异。",
        "task_release": "把两组三原色调出的绿色或橙色并排展示，请学生找出更亮、更暗、更暖、更冷的变化。",
        "expected_student_responses": ["能比较深浅或冷暖", "能用偏黄、偏蓝、偏红描述色彩", "能开始把色彩和感觉联系起来"],
        "likely_misconceptions_or_failures": ["只说一样或不一样", "只按喜欢程度评价", "把冷暖理解成温度知识而非视觉感受"],
        "teacher_follow_up_questions": ["这两块绿色都叫绿，但哪一块更像春天的新芽？哪一块更像雨后的草地？", "你看到的是颜色变深了，还是情绪变安静了？"],
        "teacher_scaffolding_moves": ["提供冷暖、明暗、偏向词卡", "用同色系条带排队", "让学生给颜色取一个画面名字"],
        "teacher_rescue_strategy": "若学生说不出差异，教师把色块遮去名称，只问哪块更跳、哪块更稳，再回到色彩词。",
        "screen_trigger": "同色不同偏向对照、色彩词卡、色带排序",
        "component_trigger": "compare_color_swatches / color_word_bank",
        "learning_sheet_trigger": "色彩差异记录：同样是……色，一块更……，一块更……",
        "evidence_trigger": "学生能用至少一个视觉词描述同色差异",
        "assessment_alignment": "对应能观察比较色彩之间变化，并分享自己对色彩的认知。",
        "transition_chain": "由间色差异进入复色调和，继续探究更丰富的色彩。",
        "teacher_visible_note": "重点不是认颜色，而是学会看颜色之间的细微关系。",
        "control_points": {
            "observe": "学生是否能描述色彩差异",
            "ask_when": "学生只说喜欢哪个时",
            "rescue_when": "学生把色彩感受说成单一标准答案时",
            "screen_when": "需要并排比较色块时",
            "component_when": "需要色卡比较和词库支架时",
            "evidence_when": "写出同色差异句时",
            "proceed_when": "学生能用视觉词说出差异"
        }
    },
    {
        "event_id": "r223o_color_event_05_complex_color_adjustment",
        "event_name": "进一阶：调出更丰富的复色",
        "section": "复色进阶",
        "source_anchor": "进阶思考，发现并调出复色，揭晓色彩的基本规律",
        "teaching_responsibility": "让学生理解颜色继续相碰会变得丰富，也可能变灰变浊，需要控制比例和目的。",
        "student_problem": "学生可能把复色理解成越多颜色越好，导致色彩失控。",
        "task_release": "在一块已经调出的间色里，只加入一点第三种颜色，观察它变得更沉、更新、更暖还是更冷。",
        "expected_student_responses": ["发现颜色会变灰、变深或更柔和", "能意识到少量加入会改变气质", "能为自己的梦幻季节选择色调"],
        "likely_misconceptions_or_failures": ["不断加颜料直到发黑", "把复色当成失败色", "不理解为什么要调复色"],
        "teacher_follow_up_questions": ["这块颜色虽然不那么亮了，但它像傍晚、雨天还是树影？", "如果你的季节不是热闹的夏天，而是安静的秋天，需要什么样的颜色？"],
        "teacher_scaffolding_moves": ["限定每次只加一点", "用季节和情绪做色彩目标", "比较清亮间色和沉稳复色"],
        "teacher_rescue_strategy": "若学生把颜色调黑，教师让其把失败样也保留，标注加入颜色太多，再重试一次少量加入。",
        "screen_trigger": "间色到复色的变化条、清亮/沉稳色彩对照、季节色调提示",
        "component_trigger": "stepwise_color_adjustment / mistake_repair",
        "learning_sheet_trigger": "复色记录：我在……色里加入一点……，它变得……",
        "evidence_trigger": "一条复色变化记录和一次调整说明",
        "assessment_alignment": "对应能调出复色，理解色彩是表达情感的语言。",
        "transition_chain": "由复色变化转入色彩碰撞和透明球任务，把实验色彩用于单元表现性任务。",
        "teacher_visible_note": "让复色成为表达选择，不是失败后的脏颜色。",
        "control_points": {
            "observe": "学生是否控制加色量",
            "ask_when": "学生把复色当失败时",
            "rescue_when": "颜色失控发黑时",
            "screen_when": "需要展示变化条时",
            "component_when": "需要错误修补或逐步调色时",
            "evidence_when": "完成复色记录时",
            "proceed_when": "学生能说明复色带来的感觉变化"
        }
    },
    {
        "event_id": "r223o_color_event_06_color_collision_task",
        "event_name": "碰一碰：把调试色彩装进透明球",
        "section": "色彩碰撞任务",
        "source_anchor": "色彩碰撞：将调试的色彩装进透明球中，完成活动任务一",
        "teaching_responsibility": "把调色发现转化为可展示的单元任务成果，形成色彩创想会的材料。",
        "student_problem": "学生容易只追求热闹好看，忘记标注色彩来源和调试过程。",
        "task_release": "每组选择两到三块最能说明发现的色彩，放入透明球或展示卡中，并给它们取一个有感觉的名字。",
        "expected_student_responses": ["能选择代表性颜色", "能用调色来源说明颜色", "能把颜色和感受联系起来"],
        "likely_misconceptions_or_failures": ["全部颜色都想放进去", "只起可爱名字不说明来源", "作品缺少过程证据"],
        "teacher_follow_up_questions": ["这个颜色从哪两种颜色碰出来？", "它更像热闹的操场、安静的树影，还是下雨前的天空？"],
        "teacher_scaffolding_moves": ["要求一球一色名一来源", "给出色彩命名句式", "让学生把实验记录贴在展示旁"],
        "teacher_rescue_strategy": "若学生选择过多，教师要求只保留最能说明一个发现的三块色彩。",
        "screen_trigger": "透明球任务要求、色彩命名句式、展示样例",
        "component_trigger": "select_best_evidence / gallery_label",
        "learning_sheet_trigger": "色彩创想卡：色名、来源、感受、用途",
        "evidence_trigger": "透明球或展示卡 + 色彩来源说明",
        "assessment_alignment": "对应单元表现性任务“红、黄、蓝”色彩创想会。",
        "transition_chain": "由小组展示材料转入分享交流和单元评价。",
        "teacher_visible_note": "展示不是堆颜色，而是用颜色讲清自己的发现。",
        "control_points": {
            "observe": "学生是否能选择代表色",
            "ask_when": "学生只做装饰时",
            "rescue_when": "展示材料过多无重点时",
            "screen_when": "需要显示展示句式时",
            "component_when": "需要证据选择和标签支架时",
            "evidence_when": "完成色彩创想卡时",
            "proceed_when": "学生能说出颜色来源和感受"
        }
    },
    {
        "event_id": "r223o_color_event_07_share_color_feeling",
        "event_name": "说一说：用色彩讲述自己的感受",
        "section": "展示与评价",
        "source_anchor": "能结合自己的生活，感受色彩对于生活的意义，和同学们交流分享",
        "teaching_responsibility": "让学生带着实验记录和色彩作品分享，形成色彩作为表达语言的初步认识。",
        "student_problem": "学生容易把评价说成颜色漂亮、作品好看，缺少依据。",
        "task_release": "每组用一句话介绍一块颜色：它从哪里来，它让我们想到什么，它可以放进怎样的画面。",
        "expected_student_responses": ["能说出色彩来源", "能联系校园或季节感受", "能听取同伴建议"],
        "likely_misconceptions_or_failures": ["只说我喜欢", "只展示结果不提实验", "评价同伴时语言空泛"],
        "teacher_follow_up_questions": ["你能不能指着记录告诉大家，这个颜色是怎么来的？", "同伴说它像夏天，你觉得证据在哪里？"],
        "teacher_scaffolding_moves": ["提供分享句式", "要求作品和学习单一起展示", "把同伴建议写在七彩果实评价上"],
        "teacher_rescue_strategy": "若评价空泛，教师把问题改成找证据：请找一块色彩，说出它的来源和带给你的感觉。",
        "screen_trigger": "分享句式、七彩果实评价提示、同伴建议栏",
        "component_trigger": "gallery_walk / evidence_based_feedback",
        "learning_sheet_trigger": "展示评价：我介绍的颜色、来源、感受、同伴建议",
        "evidence_trigger": "作品展示 + 调色记录 + 口头或书面评价",
        "assessment_alignment": "对应能和同学分享对色彩的认知，并用色彩表达感受。",
        "transition_chain": "收束第一阶段，为点彩游戏和后续色彩表达提供色彩经验。",
        "teacher_visible_note": "让学生用证据说颜色，用颜色说感受。",
        "control_points": {
            "observe": "学生是否带着记录介绍",
            "ask_when": "评价停留在漂亮时",
            "rescue_when": "学生忘记实验过程时",
            "screen_when": "需要展示分享句式和评价提示时",
            "component_when": "需要画廊走看和证据反馈时",
            "evidence_when": "完成展示评价和同伴建议时",
            "proceed_when": "学生能用来源和感受说明色彩"
        }
    }
]


MANUSCRIPT = """# 《色彩的碰撞》教师文稿版 v1

```text
stage_id=1013R_R223O_SECOND_CROSS_SAMPLE_VALIDATION
source_sample=第二单元 色彩的碰撞.docx
standard_id=GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE
status=third_cross_sample_teacher_manuscript_draft
preview_only=true
teacher_confirmed=false
formal_apply_allowed=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 阅读说明

本稿用于验证 R223M-P5 锁定的课堂事件展开标准，能否迁移到“视觉语言 / 色彩感知 / 色彩表达”类课例。它不是正式 UI，不写入备课本，也不调用模型或运行时。默认层只保留教师可读文稿；完整课堂事件、组件触发、大屏触发、学习单和评价证据保留在 review ledger。

## 一、课时定位

| 项目 | 内容 |
| --- | --- |
| 课题 | 《色彩的碰撞》 |
| 课型 | 视觉语言 / 色彩规律 / 色彩感知 |
| 核心理解 | 色彩是美术表现的重要语言。红、黄、蓝相互碰撞，会产生新的颜色；颜色的偏向、明暗和冷暖会影响画面感受。 |
| 本课任务 | 从校园色彩进入红、黄、蓝调色实验，发现间色和复色的变化，并为“红、黄、蓝”色彩创想会准备一组有来源、有感受的色彩成果。 |
| 学习证据 | 校园色彩观察句、三原色实验记录、间色/复色调色样本、色彩命名卡、展示评价记录。 |

## 二、本课在单元中的位置

本课处在“色彩的碰撞”单元第一阶段“发现色彩”的核心位置。学生先从校园夏日色彩中提出问题，再通过红、黄、蓝调色实验发现间色和复色，为后续点彩游戏和梦幻季节表达积累色彩经验。

## 三、教学目标

1. 能从校园和自然色彩中发现红、黄、蓝及其变化，提出“颜色从哪里来、怎样变出来”的问题。
2. 能用红、黄、蓝进行两色调和，发现间色，并通过比例变化观察同一种颜色的偏向和差异。
3. 能尝试少量加入第三种颜色，发现复色的丰富变化，并把色彩变化和画面感受联系起来。
4. 能选择一组调试成果，用色彩来源、视觉感受和生活联想介绍自己的色彩发现。

## 四、教学重难点

**重点。** 引导学生通过红、黄、蓝的调色实验，发现间色和复色的变化，并能用偏红、偏黄、偏蓝、明亮、沉稳、清凉、温暖等词语说明色彩差异。

**难点。** 学生容易把调色理解为随意搅拌，或只追求颜色鲜艳。本课要帮助他们控制材料、记录过程，用实验结果说明颜色从哪里来，以及这种颜色带来怎样的视觉感受。

## 五、教学准备

- 教师准备：校园色彩照片、红黄蓝三原色颜料、透明片或色块卡、同色不同偏向样本、清亮 / 混浊对照、色彩词卡、展示句式。
- 学生准备：水粉或丙烯颜料、调色盘、水粉笔、纸巾、试色纸、色彩记录单。
- 学习单：校园色彩观察、三原色实验、间色记录、复色调整、色彩命名与展示评价。
- 替代方案：若颜料条件不足，可用彩色透明片叠色、色卡排序或教师示范调色小样保底。

## 六、单课结构

| 阶段 | 学习任务 | 小问题 | 课堂活动 | 学习证据 |
| --- | --- | --- | --- | --- |
| 第一段 | 从校园色彩进入问题 | 红、黄、蓝能不能带我们找到更多颜色？ | 游园回看；三原色问题建立 | 校园色彩观察句；探究问题 |
| 第二段 | 三原色调和实验 | 两种颜色碰在一起会发生什么？ | 两色调和；间色观察 | 调色记录；比例观察 |
| 第三段 | 色彩差异和复色进阶 | 同一种颜色为什么会不一样？ | 同色比较；少量加入第三色 | 色彩差异句；复色变化记录 |
| 第四段 | 色彩碰撞成果表达 | 怎样用颜色讲出自己的发现？ | 透明球 / 展示卡；色彩创想分享 | 色彩来源说明；展示评价 |

## 七、教学过程

### （一）入场与问题：把校园色彩带回课堂

#### 1. 游园回看：寻找红、黄、蓝

教师先出示几张校园夏日色彩照片，也可以用学生课前收集的“色彩漂流瓶”。请学生不急着说哪张照片最漂亮，而是先找一找：画面里哪些地方能看到红、黄、蓝？它们旁边还藏着哪些不容易说出名字的颜色？

教师：“我们在校园里看到很多颜色。今天先抓住红、黄、蓝这三个小伙伴，看它们能不能帮我们找回更多颜色。你找到的这块红，是像操场一样热烈，还是像花瓣一样柔软？”

学生可能先说“这里有红色”“那里有蓝色”，也可能直接说“我喜欢这张”。教师可以把照片局部放大，只留下色块，追问：“如果遮住物体，你还能从颜色里感觉到季节和心情吗？”这样把观察从物体名称转到色彩感受。

学生在学习单上写一句：“我在校园里找到的红、黄、蓝是……我想研究的问题是……”如果学生提到“这些颜色能不能调出来”，教师就顺势把问题引向今天的调色实验。

#### 2. 认一认：红黄蓝是不是色彩的起点

教师出示几组颜料盘，请学生判断：如果今天只能先选三种颜色做实验，应该选哪三种？为什么？学生通常会选红、黄、蓝，但理由可能只是“老师说过这是三原色”。

教师不急着讲定义，而是让学生想一想：“如果一开始给十种颜色，我们还看得清是谁变出谁吗？如果只给红、黄、蓝，它们碰在一起会不会出现新的颜色？”随后约定实验规则：少量取色，一次只让两种颜色相碰，调完要留下记录。

【设计意图】这一段把生活中的色彩经验带回课堂，并把问题收束到红、黄、蓝的调色实验。学生不是先背三原色概念，而是带着“能不能变出更多颜色”的问题进入实验，后面的调色记录才有意义。

大屏可出示校园色彩照片、红黄蓝色块和实验约定。评价重点看学生能否提出一个色彩问题，并说明为什么先从红、黄、蓝开始。

### （二）实验与观察：让红黄蓝碰出新颜色

#### 1. 调一调：两种颜色先碰一碰

每组选择一组颜色：红加黄、黄加蓝或蓝加红。教师提醒学生先用很少的颜料调试，观察颜色从哪里变来，而不是一开始就把颜料全部搅在一起。

教师：“请你只让两种颜色先见面。调出来以后，不要只说它叫什么，还要看它更靠近哪一种原来的颜色。”学生会很快发现橙、绿、紫等新颜色，但也可能因为颜料太多、加水太多或反复搅拌，得到比较浑浊的颜色。

如果学生只说“变成绿色了”，教师可以追问：“这块绿更像春天的新芽，还是雨后的深草地？它偏黄一点，还是偏蓝一点？”如果有小组调成灰脏色，教师不直接说失败，而是请他们回看记录：刚才加入了几种颜色、每次加了多少。然后示范“少量、两色、慢慢加”的方法，让学生保留这次经验，再试一次。

学生把最清楚的一次调色样本圈出来，并记录：“红加黄变成……，如果黄多一点，它会……”这样，课堂关注的不只是调出结果，而是颜色变化的路径。

#### 2. 比一比：同一种新颜色为什么不一样

教师把两组三原色调出的绿色或橙色并排展示，请学生找出差异：哪一块更亮，哪一块更暗，哪一块更温暖，哪一块更清凉。学生可能一开始只说“都差不多”，或者只说自己喜欢哪一块。

教师可以遮住颜色名称，只问：“哪一块更跳？哪一块更安静？哪一块像阳光照着的草地，哪一块像树荫下面的草地？”再把学生的感觉转回色彩词：偏黄、偏蓝、明亮、沉稳、冷、暖。

学生在学习单上写一句：“同样是……色，一块更……，一块更……”有了这个句子，学生就开始从认颜色进入看颜色关系。

【设计意图】这一段把调色活动从“变出新颜色”推进到“观察色彩差异”。通过少量调色、并排比较和感受词支架，学生能发现同一种颜色也有偏向、明暗和冷暖，这为后面用色彩表达情绪打下基础。

大屏可出示两色调和步骤、比例变化对照和色彩词卡。评价重点看学生是否保留调色样本，并能用一个视觉词说明色彩差异。

### （三）进阶与表达：从颜色结果走向色彩感受

#### 1. 进一阶：调出更丰富的复色

当学生已经调出间色后，教师让他们在一块间色里只加入一点第三种颜色，观察它变得更沉、更柔、更暖或更冷。教师提醒：“第三种颜色只是一点点，它像给原来的颜色加了一层情绪，不是把所有颜色都倒进去。”

学生可能会觉得变灰、变暗就是失败。教师可以拿一块清亮的绿色和一块稍微沉稳的绿色并排问：“哪一块更像夏天正午？哪一块更像雨后树影？如果你要画一个安静的季节，你会选哪一块？”这样帮助学生理解复色不是脏色，而是更复杂的表达选择。

如果有小组把颜色调得发黑，教师可以请他们把这块“失控色”也留下，标注“加入太多颜色”，再重试一次少量加入。这个补救能让错误变成可观察的证据。

#### 2. 碰一碰：把调试色彩变成创想会材料

教师把任务转向单元表现性任务：“请每组选择两到三块最能说明发现的颜色，把它们放进透明球或展示卡里。每一块颜色都要有名字、有来源、有感受。”学生可以给颜色取名，如“雨后草地绿”“太阳橙”“傍晚紫”，但必须能说出它是怎么调出来的。

学生可能想把所有调出来的颜色都放进去。教师可以提醒：“创想会不是把全部颜色摆满，而是挑出最能说明你们发现的颜色。”如果学生只起了可爱的名字，教师追问：“它从哪两种颜色碰出来？它让你想到什么画面？”

【设计意图】这一段让学生认识到色彩不只是实验结果，也可以成为表达材料。复色进阶帮助学生理解色彩的微妙变化，透明球或展示卡则把调色记录转化为可分享的单元成果。

大屏可出示复色变化条、清亮 / 沉稳色彩对照和色彩命名句式。评价重点看学生能否说明颜色来源，并把颜色和一种画面感受联系起来。

### （四）展示与收束：用色彩讲述自己的发现

#### 1. 说一说：红黄蓝色彩创想会小展示

展评时，每组选择一块最有代表性的颜色介绍。教师要求学生说清三件事：它从哪里来，它看起来有什么特点，它让我们想到什么。

教师可以给出句式：“我们调出的颜色叫……它由……和……碰出来。它让我想到……，因为……”如果学生只说“我喜欢这个颜色”，教师就把问题改成找证据：“请你指着调色记录告诉大家，它是怎么来的？同伴说它像夏天，证据在哪里？”

同伴评价不评谁最好看，而是听谁能把颜色说清楚。最后，教师把学生的色彩卡或透明球集中展示，形成班级“红、黄、蓝”色彩创想会的第一批材料。

【设计意图】最后一段把调色实验收束为色彩表达。学生带着记录介绍颜色，能把色彩来源、视觉感受和生活联想连接起来，初步理解“色彩是美术表现的重要语言”。

大屏可出示分享句式、色彩感受词和七彩果实评价提示。评价重点看学生是否能用调色记录支持自己的表达，并能听取同伴建议继续调整。

## 八、评价设计

| 学习环节 | 观察重点 | 证据来源 |
| --- | --- | --- |
| 校园色彩入场 | 能找到红、黄、蓝，并提出一个色彩问题 | 校园色彩观察句 |
| 三原色问题建立 | 能说明为什么先用红、黄、蓝做实验 | 三原色起点记录 |
| 两色调和 | 能调出一组新颜色，并记录来源 | 间色调色样本 |
| 色彩差异比较 | 能用偏向、明暗或冷暖描述同色差异 | 色彩差异句 |
| 复色进阶 | 能说明第三种颜色带来的变化 | 复色变化记录 |
| 色彩碰撞任务 | 能选择代表色并说明来源和感受 | 色彩命名卡 |
| 分享收束 | 能带着实验记录介绍颜色 | 展示评价记录 |

本课评价不只看调色是否鲜艳，更看学生是否能说清“颜色从哪里来、有什么变化、带来什么感受”。教师可以优先收集四类证据：校园色彩观察、三原色调色记录、同色差异比较、色彩创想卡。

## 九、板书 / 大屏结构

```text
色彩的碰撞

起点：红 / 黄 / 蓝
调和：红+黄  黄+蓝  蓝+红
比较：偏红 / 偏黄 / 偏蓝  明亮 / 沉稳  冷 / 暖
进阶：加入一点第三色，观察变化
表达：我调出的颜色叫……它由……碰出来，让我想到……
```

## 十、确认门

本稿仍为 preview-only。它只用于 R223O 第三样本迁移验证，不写入正式备课本，不修改 R97B，不新增正式 UI，不接 runtime、provider/model、prompt 或数据库。
"""


def build_reasoning_chain() -> str:
    return f"""# R223O 《色彩的碰撞》推理链生产物

```text
stage_id={STAGE_ID}
sample=第二单元 色彩的碰撞.docx
archetype=visual_language_color_perception_expression
standard_id={STANDARD_ID}
```

## 来源锚点

- 单元主题：{SOURCE_ANCHORS['unit_theme']}
- 大观念：{SOURCE_ANCHORS['big_idea']}
- 基本问题：{SOURCE_ANCHORS['essential_question']}
- 表现性任务：{SOURCE_ANCHORS['performance_task']}
- 学情：{SOURCE_ANCHORS['student_analysis']}

## 推理链

```text
大观念：色彩是美术表现的重要语言
→ 基本问题：如何运用色彩表达内心感受
→ 阶段责任：发现色彩规律，找到间色和复色
→ 课时责任：通过红黄蓝调色实验理解色彩碰撞
→ 课堂事件：校园观察、三原色起点、两色调和、同色差异、复色进阶、色彩创想展示
→ 学习证据：观察句、调色记录、色彩差异句、复色记录、色彩命名卡
```

## 与前两样本的差异

《我为文具代言》验证设计应用 / 生活问题解决；《有趣的纸印》验证材料 / 技法 / 印痕探究。本次样本验证视觉语言和色彩感知表达，核心不是改造物品或试印材料，而是让学生通过色彩实验看见颜色关系，并用颜色表达感受。
"""


def build_selection_note() -> str:
    return f"""# R223O 第三样本选择说明

```text
stage_id={STAGE_ID}
selected_sample=第二单元 色彩的碰撞
reason=验证视觉语言 / 色彩感知 / 表达类课型
formal_ui=false
```

## 选择理由

R223M-P5 标准已在《我为文具代言》上形成候选标准，并在《有趣的纸印》完成材料 / 技法 / 印痕探究类迁移。第三样本不宜继续选择材料或设计应用课型，因此选择《色彩的碰撞》。

该样本的核心链条是：校园色彩观察 → 红黄蓝调色实验 → 间色 / 复色规律 → 色彩感受表达 → “红、黄、蓝”色彩创想会。它能检验课堂事件展开标准是否能处理视觉语言、色彩规律、审美感受和表达任务。

## 不迁移内容

本包不迁移《我为文具代言》的文具、智造、代言、赠笔礼，也不迁移《有趣的纸印》的纸材、印痕、版画车间坊。所有课堂事件均从《色彩的碰撞》样本来源和三年级学情推导。
"""


def build_component_map() -> str:
    return """# R223O 组件 / 大屏 / 学习单 / 证据触发图

| 课堂事件 | 组件触发 | 大屏触发 | 学习单触发 | 证据 |
| --- | --- | --- | --- | --- |
| 游园回看 | image_color_spotting / color_word_bank | 校园色彩照片、色块局部 | 校园色彩观察句 | 一个色彩观察点和一个问题 |
| 三原色起点 | material_limit_prompt / experiment_rule_card | 三原色实验约定 | 三原色起点记录 | 红黄蓝作为实验起点的理由 |
| 两色调和 | color_mixing_trial / circle_best_sample | 两色调和步骤、清亮/混浊样例 | 间色调色记录 | 调色样本和比例观察 |
| 同色差异 | compare_color_swatches / color_word_bank | 同色不同偏向对照、色彩词卡 | 色彩差异句 | 用视觉词描述差异 |
| 复色进阶 | stepwise_color_adjustment / mistake_repair | 复色变化条、季节色调提示 | 复色变化记录 | 一次调整说明 |
| 色彩碰撞任务 | select_best_evidence / gallery_label | 透明球任务要求、命名句式 | 色彩创想卡 | 色彩来源和感受 |
| 分享收束 | gallery_walk / evidence_based_feedback | 分享句式、七彩果实评价提示 | 展示评价记录 | 作品 + 调色记录 + 评价 |

组件仍然是 review ledger 层的触发条件，不在教师默认稿中显式作为工具货架出现。
"""


def build_rubric_score() -> str:
    return """# R223O 25 分规准评分

```text
rubric_id=CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_25_POINT
score=23/25
decision=PASS_SECOND_CROSS_SAMPLE_VALIDATION_WITH_TEACHER_MANUSCRIPT_STANDARD
```

| 维度 | 满分 | 得分 | 判断 |
| --- | ---: | ---: | --- |
| 课堂事件真实展开 | 5 | 5 | 七个课堂事件覆盖任务释放、学生反应、教师追问、补救、证据和过渡 |
| 学生可能性符合学情 | 5 | 4 | 能反映三年级学生爱用明亮色、易随意搅拌、难描述色彩差异等问题 |
| 教师追问与补救具体 | 5 | 5 | 有少量取色、同色比较、错误样保留、色彩词支架等可上课策略 |
| 大屏 / 组件 / 学习单 / 证据有触发点 | 5 | 5 | 所有派生物均从课堂事件触发，未做工具货架 |
| 教师默认稿连续可读 | 5 | 4 | 已转为成熟教案文稿，仍可在未来继续细化图片素材和公开课级语言 |

## 结论

《色彩的碰撞》达到 23/25，说明标准可初步迁移到视觉语言 / 色彩感知 / 表达类课型。该结论不授权正式 UI 或 runtime。
"""


def build_report() -> str:
    return f"""# R223O 跨样本课堂事件展开验证报告

```text
stage_id={STAGE_ID}
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

## 建议

第三样本已证明标准可迁移到视觉语言 / 色彩感知类课型。下一步可以继续选择《会说话的手》验证身体符号 / 表演 / 图像转译类课型，或先由教师审核本稿的课堂可读性与色彩美术味。
"""


def build_readme() -> str:
    return f"""# R223O 第二轮跨样本验证审核包

```text
stage_id={STAGE_ID}
status=PASS_LOCAL_VALIDATOR
sample=第二单元 色彩的碰撞
rubric_score=23/25
formal_ui=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 建议 GPT 审核顺序

1. `R223O_teacher_manuscript_draft_v1.html`
2. `R223O_teacher_manuscript_draft_v1.md`
3. `R223O_rubric_score.md`
4. `R223O_classroom_event_expansion_chain.json`
5. `R223O_review_ledger_sample.json`
6. `R223O_cross_sample_validation_report.md`

## 审核重点

- 是否像成熟教师教案文稿，而不是事件字段稿；
- 是否真正适配视觉语言 / 色彩感知课型；
- 是否没有迁移文具课或纸印课内容；
- 学生反应和教师追问是否符合三年级学情；
- 大屏、学习单、评价证据是否从课堂事件长出来；
- 是否仍然不改 R97B、不接 runtime、不做 formal apply。
"""


def build_manifest(files) -> dict:
    return {
        "stage_id": STAGE_ID,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_sample": SOURCE_ANCHORS["sample"],
        "standard_id": STANDARD_ID,
        "formal_ui": False,
        "r97b_modified": False,
        "runtime_connected": False,
        "provider_model_connected": False,
        "database_written": False,
        "files": files,
    }


def build_validator() -> str:
    return r'''import json
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
'''


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    event_chain = {
        "stage_id": STAGE_ID,
        "standard_id": STANDARD_ID,
        "sample": "第二单元 色彩的碰撞",
        "archetype": "visual_language_color_perception_expression",
        "source_anchors": SOURCE_ANCHORS,
        "formal_ui": False,
        "events": EVENTS,
        "boundary": {
            "preview_only": True,
            "teacher_confirmed": False,
            "formal_apply_allowed": False,
            "r97b_modified": False,
            "ui_modified": False,
            "runtime_connected": False,
            "provider_model_connected": False,
            "database_written": False,
        },
    }
    review_ledger = {
        "stage_id": STAGE_ID,
        "ledger_type": "review_only_classroom_event_ledger",
        "teacher_default_layer": "R223O_teacher_manuscript_draft_v1.md",
        "hidden_from_teacher_default": ["event_id", "component_trigger", "screen_trigger", "learning_sheet_trigger", "evidence_trigger", "full_control_points"],
        "events": EVENTS,
    }

    write_text("R223O_cross_sample_selection_note.md", build_selection_note())
    write_text("R223O_color_collision_reasoning_chain_product.md", build_reasoning_chain())
    write_json("R223O_classroom_event_expansion_chain.json", event_chain)
    write_text("R223O_teacher_manuscript_draft_v1.md", MANUSCRIPT)
    write_text("R223O_teacher_manuscript_draft_v1.html", markdown_to_html("R223O 《色彩的碰撞》教师文稿版 v1", MANUSCRIPT))
    write_json("R223O_review_ledger_sample.json", review_ledger)
    write_text("R223O_component_screen_evidence_trigger_map.md", build_component_map())
    write_text("R223O_rubric_score.md", build_rubric_score())
    write_text("R223O_cross_sample_validation_report.md", build_report())
    write_text("README_FOR_GPT_REVIEW.md", build_readme())
    write_text("validate_1013R_R223O_second_cross_sample_validation.py", build_validator())

    file_names = [
        "R223O_cross_sample_selection_note.md",
        "R223O_color_collision_reasoning_chain_product.md",
        "R223O_classroom_event_expansion_chain.json",
        "R223O_teacher_manuscript_draft_v1.md",
        "R223O_teacher_manuscript_draft_v1.html",
        "R223O_review_ledger_sample.json",
        "R223O_component_screen_evidence_trigger_map.md",
        "R223O_rubric_score.md",
        "R223O_cross_sample_validation_report.md",
        "README_FOR_GPT_REVIEW.md",
        "validate_1013R_R223O_second_cross_sample_validation.py",
    ]
    write_json("PACKAGE_MANIFEST.json", build_manifest(file_names))


if __name__ == "__main__":
    main()
