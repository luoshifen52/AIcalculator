from decimal import Decimal, getcontext
from .cons import cons  # 导入 cons.py 选取不大于 value 的最大 10 的负整数次幂
from .log_util import add_log

# 设置精度
#getcontext().prec = 50  # 设置精度为50位数字（可以根据需要调整）

def mul(a1, a2, epsilon):
    """
    乘法算法 (Mul)
    计算 a1 * a2 的值，满足误差限 epsilon。

    参数:
    a1, a2 -- 表达式或数值
    epsilon -- 误差限

    返回:
    近似值 y ≈ a1 * a2，满足 |y - a1 * a2| < epsilon
    """

    from .main import Main  # **在函数内部导入 Main，避免循环导入**

    # 【修改】截断操作数
    a1_str = str(a1)
    if len(a1_str) > 20: a1_str = a1_str[:20] + "..."

    a2_str = str(a2)
    if len(a2_str) > 20: a2_str = a2_str[:20] + "..."

    add_log(f"【Mul】执行乘法 {a1_str} × {a2_str}", level="SUMMARY")
    add_log(f"【Mul Detail】目标误差限 ε = {epsilon}", level="DETAIL")

    # Step 1: 获取 a2 的粗略值，误差限为 0.1
    a2_tilde = Decimal(Main(a2, Decimal('0.1')))  # 使用 Decimal 类型
    add_log(f"Step 1: 粗略计算 a2 ≈ {a2_tilde}", level="DETAIL")

    # Step 2: 计算 a1 的误差限 epsilon1，选择不大于公式右侧的一个正数
    epsilon1 = cons(Decimal(epsilon) / (2 * (abs(a2_tilde) + Decimal('0.1'))))
    add_log(f"Step 2: 分配给 a1 的误差限 ε1 = {epsilon1}", level="DETAIL")

    # Step 3: 获取 a1 的近似值，误差限为 epsilon1
    a1_tilde = Decimal(Main(a1, Decimal(epsilon1)))  # 将 epsilon1 转为 float 传递给 main
    add_log(f"Step 3: 精确计算 a1 ≈ {a1_tilde}", level="DETAIL")

    # Step 4: 计算 a2 的误差限 epsilon2，选择不大于公式右侧的一个正数
    epsilon2 = cons(Decimal(epsilon) / (2 * abs(a1_tilde)))
    add_log(f"Step 4: 分配给 a2 的误差限 ε2 = {epsilon2}", level="DETAIL")

    # Step 5: 获取 a2 的更精确值，误差限为 epsilon2
    a2_tilde = Decimal(Main(a2, Decimal(epsilon2)))  # 将 epsilon2 转为 float 传递给 main
    add_log(f"Step 5: 精确计算 a2 ≈ {a2_tilde}", level="DETAIL")

    # Step 6: 返回最终结果
    # print(f"mul: {a1_tilde * a2_tilde}")
    result = a1_tilde * a2_tilde
    add_log(f"Step 6: 最终结果 = {result}", level="DETAIL")
    return result