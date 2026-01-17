log_steps = []

# 日志等级：
# NONE     : 完全不记录（高精度计算）
# SUMMARY  : 只记录关键步骤（解释用）
# DETAIL   : 详细调试（开发用）
LOG_LEVEL = "SUMMARY"


def set_log_level(level: str):
    """
    设置日志等级：NONE / SUMMARY / DETAIL
    """
    global LOG_LEVEL
    LOG_LEVEL = level


def add_log(message: str, level: str = "DETAIL"):
    """
    添加日志，根据日志等级决定是否记录
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
    获取日志（用于 LLM 解释）
    """
    return log_steps[:]
