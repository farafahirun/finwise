import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. f"{level_info['level']} ({level_info['group']}, tooltip="")"
    content = content.replace(
        'f"{level_info[\'level\']} ({level_info[\'group\']}, tooltip=\"\")"',
        'f"{level_info[\'level\']} ({level_info[\'group\']})", tooltip=""'
    )
    
    # 2. habit_sum['level'].split(" - ", tooltip="")[0], help=habit_sum['level'].split(" - ")[1]
    # Wait, the original code had `help=...`. If render_metric_card doesn't support help=..., it should be tooltip=...
    content = content.replace(
        'habit_sum[\'level\'].split(" - ", tooltip="")[0], help=habit_sum[\'level\'].split(" - ")[1]',
        'habit_sum[\'level\'].split(" - ")[0], tooltip=habit_sum[\'level\'].split(" - ")[1]'
    )
    
    # 3. f"{habit_sum['longest_streak_val']} ({habit_sum['longest_streak_name']}, tooltip="")"
    content = content.replace(
        'f"{habit_sum[\'longest_streak_val\']} ({habit_sum[\'longest_streak_name\']}, tooltip=\"\")"',
        'f"{habit_sum[\'longest_streak_val\']} ({habit_sum[\'longest_streak_name\']})", tooltip=""'
    )

    # 4. len(chal_dash['active'], tooltip="")
    content = content.replace(
        'len(chal_dash[\'active\'], tooltip="")',
        'str(len(chal_dash[\'active\'])), tooltip=""'
    )

    # 5. len(learn_sum['materials_done'], tooltip="")
    content = content.replace(
        'len(learn_sum[\'materials_done\'], tooltip="")',
        'str(len(learn_sum[\'materials_done\'])), tooltip=""'
    )

    # 6. len(learn_sum['badges'], tooltip="")
    content = content.replace(
        'len(learn_sum[\'badges\'], tooltip="")',
        'str(len(learn_sum[\'badges\'])), tooltip=""'
    )

    # 7. len(summary['materials_done'], tooltip="")
    content = content.replace(
        'len(summary[\'materials_done\'], tooltip="")',
        'str(len(summary[\'materials_done\'])), tooltip=""'
    )

    # 8. len(summary['quizzes_done'], tooltip="")
    content = content.replace(
        'len(summary[\'quizzes_done\'], tooltip="")',
        'str(len(summary[\'quizzes_done\'])), tooltip=""'
    )

    # Convert remaining tooltip="" that might be wrongly placed
    # e.g., if there's any render_metric_card passing integer
    # Actually render_metric_card parameter 'value' can be any type because in f-string inside render_metric_card it converts to str natively.
    # We just need to make sure syntax is valid.

    with open(filepath, 'w') as f:
        f.write(content)

for root, dirs, files in os.walk("pages/"):
    for file in files:
        if file.endswith(".py"):
            fix_file(os.path.join(root, file))

print("Syntax fixed")
