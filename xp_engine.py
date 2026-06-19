from db import (
    get_user_xp,
    update_user_xp,
    add_xp_history,
    get_xp_history
)
from langchain_service import ask_langchain

def calculate_level_from_xp(total_xp):
    # Asumsikan 100 XP per level
    level = (total_xp // 100) + 1
    return level

def get_xp_for_next_level(level):
    return level * 100

def get_level_group(level):
    if level >= 31: return "Financial Master"
    elif level >= 21: return "Financial Optimizer"
    elif level >= 11: return "Financial Planner"
    elif level >= 6: return "Developing Saver"
    else: return "Financial Beginner"

def determine_title(level, streaks):
    if level >= 31:
        return "Financial Master"
    
    # Cari streak tertinggi
    if not streaks:
        return "Starter"
        
    best_habit = max(streaks, key=streaks.get)
    if streaks[best_habit] == 0:
        return "Starter"
        
    if "Budget" in best_habit:
        return "Budget Guardian"
    elif "Goal" in best_habit:
        return "Goal Hunter"
    elif "Saving" in best_habit:
        return "Savings Champion"
    else:
        return "Debt Destroyer" # Default alternative

def award_xp(user_id, activity, xp_amount, streaks=None):
    user_xp_data = get_user_xp(user_id)
    if user_xp_data:
        total_xp = user_xp_data['total_xp'] + xp_amount
        old_level = user_xp_data['level']
    else:
        total_xp = xp_amount
        old_level = 1
        
    new_level = calculate_level_from_xp(total_xp)
    
    # Calculate title
    title = "Starter"
    if streaks is not None:
        title = determine_title(new_level, streaks)
    elif user_xp_data:
        title = user_xp_data['title']
        
    update_user_xp(user_id, total_xp, new_level, title)
    add_xp_history(user_id, activity, xp_amount)
    
    return {
        "leveled_up": new_level > old_level,
        "new_level": new_level,
        "total_xp": total_xp,
        "xp_added": xp_amount,
        "title": title
    }

def get_user_level_info(user_id, streaks=None):
    data = get_user_xp(user_id)
    if not data:
        # User baru
        title = determine_title(1, streaks) if streaks else "Starter"
        update_user_xp(user_id, 0, 1, title)
        data = {"total_xp": 0, "level": 1, "title": title}
        
    level = data['level']
    total_xp = data['total_xp']
    
    # Perbaiki title jika streaks tersedia
    if streaks:
        new_title = determine_title(level, streaks)
        if new_title != data['title']:
            update_user_xp(user_id, total_xp, level, new_title)
            data['title'] = new_title
            
    next_level_xp = get_xp_for_next_level(level)
    current_level_base_xp = (level - 1) * 100
    
    progress = total_xp - current_level_base_xp
    target = 100 # 100 xp per level
    
    return {
        "total_xp": total_xp,
        "level": level,
        "group": get_level_group(level),
        "title": data['title'],
        "next_level_xp": next_level_xp,
        "progress_percent": min(progress / target, 1.0),
        "progress_val": progress,
        "target_val": target
    }

def get_ai_motivation_insight(level_info, knowledge_context):
    ctx = f"""
    Level: {level_info['level']} ({level_info['group']})
    Title: {level_info['title']}
    Total XP: {level_info['total_xp']}
    Progress to Next Level: {level_info['progress_percent']*100:.1f}%
    """
    prompt = f"""
    Berdasarkan Financial Level pengguna berikut:
    {ctx}
    
    Berikan Motivation Insight yang menjelaskan:
    1. Pujian atas pencapaian dan gelar (Title) pengguna saat ini.
    2. Makna dari perkembangan level mereka.
    3. Target level berikutnya dan mengapa itu penting.
    4. Tindakan taktis apa yang memberi banyak XP (Assessment, Challenge, Budget) yang harus difokuskan selanjutnya.
    
    Gunakan gaya bahasa seorang pelatih (coach) yang inspiratif layaknya di dalam game.
    """
    return ask_langchain(ctx, knowledge_context, prompt)

def format_xp_context(level_info):
    return f"""
    === FINANCIAL XP & LEVEL SUMMARY ===
    Level Saat Ini: {level_info['level']} ({level_info['group']})
    Title: {level_info['title']}
    Total XP: {level_info['total_xp']}
    Menuju Level {level_info['level']+1}: {level_info['progress_val']} / {level_info['target_val']} XP
    """
