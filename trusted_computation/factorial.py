from decimal import Decimal
from .log_util import add_log

def factorial(n):
    """计算 n! 的阶乘"""
    n = int(n)
    if n == 0 or n == 1:
        add_log(f"【factorial】{n}! = 1")
        return Decimal(1)  # 返回 Decimal 类型的 1
    else:
        result = Decimal(1)
        for i in range(2, n + 1):
            result *= i
        add_log(f"【factorial】{n}! = {result}")
        return Decimal(result)