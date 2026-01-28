from decimal import Decimal, getcontext
from .cons import cons  # 导入 cons.py 选取不大于 value 的最大 10 的负整数次幂
from .log_util import add_log

def div(a1, a2, epsilon):
    """
    算法 3: 除法算法 (Div)
    计算 a1 / a2 的值，满足误差限 epsilon。

    参数:
    a1, a2 -- 表达式或数值
    epsilon -- 误差限

    返回:
    近似值 y ≈ a1 / a2，满足 |y - a1 / a2| < epsilon
    """
    from .main import Main  # **在函数内部导入 Main，避免循环导入**

    # 【修改】截断操作数
    a1_str = str(a1)
    if len(a1_str) > 20: a1_str = a1_str[:20] + "..."

    a2_str = str(a2)
    if len(a2_str) > 20: a2_str = a2_str[:20] + "..."

    add_log(f"【Div】执行除法 {a1_str} ÷ {a2_str}", level="SUMMARY")

    # Step 1: 初步估算分子 a1
    a1_tilde = Decimal(Main(a1, Decimal('0.1')))  # 将结果转换为 Decimal 类型
    abs_a1 = abs(a1_tilde) + Decimal('0.1')  # 计算 |a1| 的上界
    # add_log(f"Step 1: 粗略计算 a1 ≈ {a1_tilde}，|a1| + 0.1 = {abs_a1}")

    # Step 2: 初始化分母的误差限 epsilon2
    epsilon2 = Decimal('0.1')
    a2_tilde = Decimal(Main(a2, Decimal(epsilon2)))  # 将结果转换为 Decimal 类型
    # add_log(f"Step 2: 初步计算 a2 ≈ {a2_tilde}（误差限 {epsilon2}）")

    # Step 3: 确保分母的绝对值足够大
    while abs(a2_tilde) <= 2 * epsilon2:
        epsilon2 *= Decimal('0.1')
        a2_tilde = Decimal(Main(a2, Decimal(epsilon2)))
        # add_log(f"Step 3: 重新计算 a2 ≈ {a2_tilde}，因为 |a2| ≤ 2 × {epsilon2}")

    abs_a2_lower_bound = abs(a2_tilde) - epsilon2  # 计算分母的下界
    # add_log(f"a2 的下界估计为 {abs_a2_lower_bound}")

    # Step 4: 确保误差满足总要求
    while abs(4 * abs_a1 * epsilon2) >= abs(a2_tilde * abs_a2_lower_bound * Decimal(epsilon)):
        epsilon2 *= Decimal('0.1')
        a2_tilde = Decimal(Main(a2, Decimal(epsilon2)))
        # add_log(f"Step 4: 再次调整 epsilon2 = {epsilon2}，更新 a2 ≈ {a2_tilde}")

    # Step 5: 计算分子的更精确值
    epsilon1 = cons(abs(a2_tilde) / 4 * Decimal(epsilon))  # 分配分子的误差限
    a1_tilde = Decimal(Main(a1, Decimal(epsilon1)))  # 转换 epsilon1 为 float 传给 main
    # add_log(f"Step 5: 更精确计算 a1 ≈ {a1_tilde}（误差限 {epsilon1}）")

    # Step 6: 计算最终结果
    y = Decimal(Main(a1_tilde / a2_tilde, Decimal(epsilon / 2)))  # 转换 epsilon 为 float 传给 main
    # add_log(f"Step 6: 结果 = {a1_tilde} ÷ {a2_tilde} = {y}")
    return y
