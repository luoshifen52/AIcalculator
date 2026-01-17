log_steps = []

# 日志等级：
# NONE     - 不记录任何日志（用于高精度计算）
# SUMMARY  - 仅记录关键步骤（用于解释）
# DETAIL   - 记录详细步骤（调试用）
LOG_LEVEL = "DETAIL"


def set_log_level(level: str):
    """
    设置日志等级: NONE / SUMMARY / DETAIL
    """
    global LOG_LEVEL
    if level not in ("NONE", "SUMMARY", "DETAIL"):
        raise ValueError("Invalid log level")
    LOG_LEVEL = level

def get_log_level():
    """
    获取当前日志等级
    """
    return LOG_LEVEL

# === 新增：数值格式化函数 ===
def format_val(val):
    """截断过长的数值字符串，用于日志显示"""
    s = str(val)
    if len(s) > 20:
        return s[:15] + "..." + s[-3:]
    return s

def add_log(message: str, level: str = "DETAIL"):
    """
    添加一步计算日志
    """
    if LOG_LEVEL == "NONE":
        return
    if LOG_LEVEL == "SUMMARY" and level == "DETAIL":
        return
    log_steps.append(message)


def clear_log():
    """
    清空日志（每次计算前调用）
    """
    log_steps.clear()


def get_log():
    """
    获取所有日志（最终用于 LLM）
    """
    return log_steps[:]
