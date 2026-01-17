from decimal import Decimal, ROUND_HALF_EVEN, InvalidOperation, ROUND_CEILING
from .factorial import factorial
from .cons import cons
from .log_util import add_log, get_log_level, format_val

def Exp(a, epsilon):
    from .main import Main

    """
    计算 exp(a)，如果 a 是常数，则直接计算；如果是表达式则通过 main 进行处理。

    参数:
    a -- 输入值，可能是一个数值或表达式
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ exp(a)，满足 |y - exp(a)| < epsilon
    """
    # 如果 a 是常数，直接计算 exp(a)
    if isinstance(a, (int, float, Decimal)):  # 判断是否为常数
        a = Decimal(a)  # 转为 Decimal 类型
        # add_log(f"【Exp】计算 exp({a})，a 是常数，直接展开计算")
        return Exp1(a, epsilon)
    else:
        # 如果 a 是表达式，通过 Main 函数计算近似值
        epsilon_prime = Decimal('0.1')  # 初始化 ε′ 为 0.1
        a_tilde = Decimal(Main(a, epsilon_prime))  # 计算满足误差要求的 a_tilde
        # add_log(f"【Exp】a 是表达式，粗略计算得到 ã ≈ {a_tilde}（ε′ = 0.1）")

        epsilon_double_prime = Decimal('0.2')  # 初始化 ε′′ 为 0.2
        y1 = Exp1(a_tilde + epsilon_prime, epsilon_double_prime)  # 计算 Exp1
        # add_log(f"用 ã + ε′ = {a_tilde + epsilon_prime} 估算 y1 ≈ {y1}")

        # 更新 a_tilde，并调用 Exp1 计算最终结果
        refined_eps = Decimal(cons(epsilon / (2 * (y1 + epsilon_double_prime))))
        a_tilde = Decimal(Main(a, refined_eps))
        # add_log(f"重新计算 ã ≈ {a_tilde}（精度 refined ε = {refined_eps}）")

        return Exp1(a_tilde, epsilon / 2)

def Exp1(c, epsilon):
    from .main import Main
    """
    计算 e^c，使用泰勒展开，满足误差限 epsilon。

    参数:
    c -- 输入值
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ e^c，满足 |y - e^c| < epsilon
    """
    c = Decimal(c)  # 将输入值转换为 Decimal 类型，以便进行高精度计算
    log_level = get_log_level()

    if c < 0:
        add_log("【exp】指数为负，转化为 1 / exp(|c|)", level="SUMMARY")
        y = Exp1(-c, epsilon)
        result = Decimal(Main(('/', 1, y), epsilon))
        # add_log(f"最终结果：1 / {y} = {result}")
        return Decimal(result)

    # ========= 日志摘要 =========
    if log_level != "NONE":
        # 【修改这里】截断 c 的显示长度，避免打印几百位小数
        c_str = str(c)
        if len(c_str) > 20:
            c_str = c_str[:20] + "..."

        add_log(f"【exp】使用泰勒展开计算 e^{c_str}", level="SUMMARY")

    # 初始化 n 为 max(|c|向上取整, 1)
    n = max(int(abs(c).to_integral_exact(rounding=ROUND_CEILING)), 1)
    # add_log(f"根据 |c| 估计初始展开项数上限 n = {n}")
    i = Decimal(1)  # 初始化求和循环次数为 1
    term = Decimal(1)  # 初始化第一项为 1
    result = term  # 初始化结果为第一项

    # 计算满足误差条件的n
    while 2 * c ** n >= factorial(n - 1) * (n - c) * epsilon:
        # print(f"left right: {2 * c ** n} {factorial(n - 1) * (n - c) * epsilon}")
        # add_log(f"误差校验不通过：n = {n}，扩大 n")
        n += 1
    while i <= n:
        term = c ** i / factorial(i)  # 更新每一项的计算
        result += term  # 累加每一项
        # add_log(f"第 {int(i)} 项: {term}，累计结果: {result}")
        i += 1

    # ========= 日志：只记录项数 =========
    if log_level == "SUMMARY":
        add_log(
            f"【exp】泰勒展开 {n} 项，满足误差界 |R_n| < ε",
            level="SUMMARY"
        )
    return Decimal(result)