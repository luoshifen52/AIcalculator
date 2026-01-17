from decimal import Decimal, getcontext
from .factorial import factorial
from .pi import get_pi
from .log_util import add_log

def sin(x, epsilon):
    """
    sin(pi/2-pi/2-pi)不精确，测试用例：sin(pi/2+pi) sin(pi/2+pi/2)

    计算 sin(x) 函数，依据输入是常数还是表达式来进行不同的处理。

    参数:
    x -- 输入值，可能是一个数值或表达式
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ sin(x)，满足 |y - sin(x)| < epsilon
    """
    # 如果 x 是常数，直接使用 Sin1 函数
    # 在 Python 中，isinstance 函数用于检查一个对象是否是指定类的实例。isinstance 是一个内置函数，可以用来检查对象是否属于某个类型（包括基本类型和用户定义的类型）。使用 isinstance 来判断输入值是否是常数（如 int、float 或 Decimal 类型）。如果输入值是这几种类型之一，就认为它是常数；否则，是一个表达式。

    from .main import Main  # **在函数内部导入 Main，避免循环导入**

    if isinstance(x, (int, float, Decimal)):  # 判断是否为常数
        x = Decimal(x)  # 转为 Decimal 类型
        add_log(f"【sin】sin({x}) 是常数，直接展开计算")
        return sin1(x, epsilon)
    else:
        # 如果 x 是表达式，通过 Main 函数计算近似值
        x_tilde = Decimal(Main(x, Decimal(epsilon / 2)))  # 计算满足误差要求的 x_tilde
        add_log(f"【sin】sin({x}) 是表达式，粗略求得 x̃ ≈ {x_tilde}（ε′ = {Decimal(epsilon/2)}）")
        return sin1(x_tilde, epsilon / 2)  # 用 Sin1 计算 sin(x_tilde)

def sin1(x, epsilon):
    """
    计算正弦函数 sin(x)，使用泰勒展开，满足误差限 epsilon。

    参数:
    x -- 输入值，是一个数值
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ sin(x)，满足 |y - sin(x)| < epsilon
    """
    # from main import Main  # **在函数内部导入 Main，避免循环导入**
    from decimal import localcontext

    # epsilon_high = epsilon.scaleb(-1000)
    epsilon_high = Decimal('1E-1000')
    # 将输入值转换为 Decimal 类型，以便进行高精度计算
    x = Decimal(x)

    # **归一化 x 到 [-π, π]**
    # pi_value = Main('pi', Decimal(epsilon))  # 计算 π
    pi_value = get_pi(epsilon_high)
    two_pi = 2 * pi_value  # 2π
    with localcontext() as ctx:
        # ctx.prec += 20  # 增加上下文精度，避免精度不足
        x = x.remainder_near(two_pi)
        if x > pi_value:
            x -= two_pi  # 归一化到 [-π, π]
        add_log(f"【sin1】将 x 归一化到 [-π, π] 区间: x = {x}")

    # 初始化变量
    n = 1  # 当前项数
    term = x  # 初始项是 x
    result = term  # 初始化结果为第一项
    add_log(f"使用泰勒展开 sin({x})，初始项为 x = {x}")

    # 使用给定的公式计算每一项，直到满足误差条件
    while abs(x ** (2 * n + 1)/factorial(2 * n + 1)) >= epsilon / 2:
        # n += 1
        # term *= -x ** 2 / ((2 * n) * (2 * n + 1))  # 每一项通过前一项递推
        print(f"term, {term}")
        term = Decimal((-1) ** n * x ** (2 * n + 1) / factorial(2 * n + 1))  # 计算当前项：(-1)^n * x^(2n+1) / (2n+1)!
        result += term  # 累加当前项
        add_log(f"第 {n} 项: {term}，累计结果: {result}")
        n += 1

    # 最终结果通过 main 函数调用得到
    add_log(f"sin({x}) ≈ {result}，共展开 {n} 项")
    return Decimal(result)
