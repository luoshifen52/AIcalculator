from decimal import Decimal, getcontext
from .pi import get_pi
from .log_util import add_log, get_log_level
import math

def arctan(a, epsilon):
    """
    计算 arctan(a)，如果 a 是常数，则直接计算，如果是表达式则通过 main 进行处理。

    参数:
    a -- 输入值，可能是一个数值或表达式
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ arctan(a)，满足 |y - arctan(a)| < epsilon
    """

    from .main import Main  # **在函数内部导入 Main，避免循环导入**

    # 如果 a 是常数，直接计算 arctan(a)
    if isinstance(a, (int, float, Decimal)):  # 判断是否为常数
        # add_log(f"【arctan】arctan({a}) 是常数，调用 arctan1 展开")
        return arctan1(a, epsilon)
    else:
        # 如果 a 是表达式，通过 Main 函数计算近似值
        # add_log(f"【arctan】arctan({a}) 是表达式，先估算 ã")
        a_tilde = Decimal(Main(a, epsilon / 2))  # 计算满足误差要求的 a_tilde
        # add_log(f"表达式估算结果 ã ≈ {a_tilde}，递归调用 arctan(ã)")
        return Main(('arctan', a_tilde), epsilon / 2)  # 返回 arctan(a_tilde) 的结果
        # return Main(Decimal(math.atan(a_tilde)), epsilon / 2)

def arctan1(c, epsilon):
    """
    计算反正切 arctan(c)，使用泰勒展开，满足误差限 epsilon。

    参数:
    c -- 输入值，是一个数值
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ arctan(c)，满足 |y - arctan(c)| < epsilon
    """

    from .main import Main  # **在函数内部导入 Main，避免循环导入**

    c = Decimal(c)  # 将输入值转换为 Decimal 类型，以便进行高精度计算
    epsilon_high = Decimal('1E-1000')
    log_level = get_log_level()  # 获取当前日志等级

    if c == Decimal('1'):
        # 快速路径：arctan(1) = π/4
        pi_val = get_pi(epsilon_high)
        add_log(f"【arctan】特例 arctan(1) = π/4", level="SUMMARY")
        return Main(('/', pi_val, 4), epsilon)

    # 如果 c 不在区间 [-1, 1]，使用变换公式
    if abs(c) > 1:
        # 使用公式：arctan(c) = 2 * arctan(c / (1 + sqrt(1 + c^2)))
        add_log(f"【arctan】|x| > 1，使用变换公式 arctan(x) = 2*arctan(x/(1+sqrt(1+x^2)))", level="SUMMARY")
        transformed_c = c / (1 + (1 + c ** 2).sqrt())  # 计算 c / (1 + sqrt(1 + c^2))
        # add_log(f"变换后 c̃ ≈ {transformed_c}，递归调用 arctan")
        return Main(('*', 2, ('arctan', ('/', c, ('+', 1, ('exp', ('+', 1, ('exp', c, 2)), ('/', 1, 2)))))), epsilon)  # 递归调用计算反正切(错误版)

    # 泰勒展开路径
    if log_level != "NONE":
        add_log(f"【arctan】使用泰勒展开计算 arctan({c})", level="SUMMARY")

    # 如果 c 在区间 [-1, 1] 内，使用泰勒级数展开计算反正切
    n = 1
    term = c  # 第一项是 c
    result = term  # 初始化结果为第一项
    # add_log(f"【arctan1】使用泰勒展开计算 arctan({c})，初始项: {term}")

    # 循环计算每一项，直到满足误差条件
    while abs(c ** (2 * n + 1) / (2 * n + 1)) >= epsilon / 2:  # 判断当前项是否满足精度要求
        # print(f"term, {term}")
        term = Decimal((-1) ** n * c ** (2 * n + 1) / (2 * n + 1))  # 更新项：(-1)^n * x^(2n+1) / (2n+1)!
        result += term  # 累加当前项
        # add_log(f"第 {n} 项: {term}，累计结果: {result}")
        n += 1

    # === 关键修改：循环结束后只记录一条总结 ===
    if log_level == "SUMMARY":
        add_log(f"【arctan】展开 {n} 项，满足误差限，结果收敛", level="SUMMARY")

    return Main(Decimal(result), epsilon / 2)  # 通过 main 函数计算前 n 项的和，精度为 epsilon/2