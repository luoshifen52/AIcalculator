from decimal import Decimal
from .log_util import add_log

def cons(value):
    """
    实现论文中的 Cons 函数，选取不大于 value 的最大 10 的负整数次幂。

    参数:
    value -- Decimal 类型的数值

    返回:
    不大于 value 的一个正数
    """
    if value <= 0:
        raise ValueError("Cons 函数输入值必须为正数")

    # 使用 math.log10(value) 计算 value 的以 10 为底的对数，这表示 value 的数量级。
    # 使用 math.floor 将对数值向下取整，获取 value 所在的数量级
    power = -int(value.log10())  # 使用 Decimal 类型的 log10 方法

    # 计算候选值 10 的 −power 次方，即 10 的负整数次幂
    candidate = Decimal(10) ** (-power)

    # 如果候选值不大于 value，直接返回它。如果候选值大于 value，选择下一个更小的次幂 10^−(power+1)
    if candidate <= value:
        chosen = candidate
    else:
        chosen = Decimal(10) ** (-(power + 1))

    # add_log(f"【cons】cons({value}) = {chosen}，选取的不大于该值的最大 10 的负整数次幂")
    return chosen
