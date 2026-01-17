from decimal import Decimal, getcontext
from .input import parse_expression  # 导入 input.py 解析函数
from .mul import mul
from .div import div
from .sin import sin
from .arctan import arctan
from .ln import ln
from .Exp import Exp
from .Exp2 import Exp2
from .pi import get_pi
from .log_util import add_log, set_log_level, get_log_level

import math

def format_sig_digits(val, sig_digits):
    """
    将 Decimal 或 float 格式化为保留指定有效数字的字符串（科学计数法或普通形式）
    """
    from decimal import Decimal
    if not isinstance(val, Decimal):
        val = Decimal(val)

    if val.is_zero():
        return f"{Decimal(0):.{sig_digits - 1}e}"
    else:
        # 转为科学计数法，保留 sig_digits 位有效数字
        return f"{val:.{sig_digits - 1}e}"

# === 论文算法1：Main 主计算函数 ===
def Main(a, ε, mode="compute"):
    # ε = standardize_epsilon(ε)  #  精度标准化处理
    """
     主可信计算函数

     参数:
     expr    : 解析后的表达式树
     epsilon : 误差上界
     mode    : "compute" | "explain"

    mode:
     - "compute": 高精度计算，关闭日志 (NONE)
     - "explain": 解释模式，记录摘要日志 (SUMMARY)
     """
    # 1. 保存当前的日志等级
    previous_level = get_log_level()

    try:
        # 2. 根据模式设置新的日志等级
        if mode == "compute":
            set_log_level("NONE")
        elif mode == "explain":
            set_log_level("SUMMARY")
        else:
            # 如果没有指定 mode（或为 None），保持当前等级不变（用于递归调用）
            pass

        return _Main(a, ε)

    finally:
        # 3. 函数执行完毕后，务必恢复之前的日志等级
        # 这样内部的 compute 调用不会永久关闭外部的 explain 日志
        set_log_level(previous_level)

def _Main(a, ε):
    # ε = standardize_epsilon(ε)  #  精度标准化处理

    """ 递归计算数学表达式树 """
    if isinstance(a, (int, float, Decimal)):  # 允许 float 转换
        # print(f"操作数，精度: {a}，{ε}")
        return Decimal(str(a))

    # **增加对 pi 和 e 的识别**
    if isinstance(a, str):
        if a.lower() == 'pi':
            add_log("读取常数 π", level="SUMMARY")
            return get_pi(Decimal('1E-1000'))
        elif a.lower() == 'e':
            add_log("读取常数 e", level="SUMMARY")
            return Decimal(str(math.e))  # 直接使用 math.e 计算 e

        raise ValueError(f"计算时无法解析的表达式: {a}")

    elif isinstance(a, tuple):
        op = a[0]

        if op == '+':  # 加法
            add_log("执行加法运算", level="SUMMARY")
            # print(f"操作符: +, 精度: {ε}")
            result = Decimal(Main(a[1], ε / 2) + Main(a[2], ε / 2))
            return Decimal(result)

        elif op == '-':  # 减法
            # print(f"操作符: -, 精度: {ε}")
            if len(a) == 2:
                add_log("执行取负运算", level="SUMMARY")
                return -Main(a[1], ε)  # 计算 a1 的值并取其相反数
            else:
                # 如果是减法 (a1 - a2)，处理两个操作数
                add_log("执行减法运算", level="SUMMARY")
                result = Decimal(Main(a[1], ε / 2) - Main(a[2], ε / 2))
                return Decimal(result)

        elif op == '*':  # 乘法
            # print(f"操作符: *, 精度: {ε}")
            add_log("执行乘法运算", level="SUMMARY")
            result = Decimal(mul(a[1], a[2], ε))  # 调用 mul 计算乘法
            return Decimal(result)

        elif op == '/':  # 除法
            # print(f"操作符: /, 精度: {ε}")
            add_log("执行除法运算", level="SUMMARY")
            result = Decimal(div(a[1], a[2], ε))  # 调用 div 计算除法
            return Decimal(result)

        elif op == 'exp1':  # e^a
            # print(f"操作符: e^ a1, 精度: {ε} {a[1]}")
            # add_log("执行指数运算 e^x", level="SUMMARY")
            # return Decimal(Exp(a[1], ε)).quantize(ε)
            result = Decimal(Exp(a[1], ε))
            return Decimal(result)

        elif op == 'exp':  # a^b
            # print(f"操作符: a1^a2 a1, a2, 精度: {ε} {a[1]} {a[2]}")
            # add_log("执行幂运算 x^y", level="SUMMARY")
            result = Decimal(Exp2(a[1], a[2], ε))
            return Decimal(result)

        elif op == 'ln':  # ln(a)
            # print(f"操作符: ln a1, 精度: {ε} {a[1]}")
            add_log(f"执行自然对数计算：ln({a[1]})")  # 日志记录
            result = Decimal(ln(Main(a[1], ε), ε))
            return Decimal(result)

        elif op == 'log':  # log(a, b)
            add_log("执行对数换底公式", level="SUMMARY")
            result = Main(('/', ('ln', a[2]), ('ln', a[1])), ε)
            return Decimal(result)

        elif op == 'sin':
            # print(f"操作符: sin, 精度: {ε}")
            # add_log("执行正弦函数 sin(x)", level="SUMMARY")
            result = Decimal(sin(a[1], ε))  # 调用 sin 计算sin函数
            return Decimal(result)

        elif op == 'cos':  # cos(a) = sin(π/2 - a)
            add_log("执行余弦函数 cos(x)", level="SUMMARY")
            result = Decimal(sin(('-', ('/', 'pi', 2), a[1]), ε))  # 调用 sin 计算cos函数
            return Decimal(result)

        elif op == 'tan':  # tan(a) = sin(a) / cos(a)
            # return Decimal(div(sin(a[1], ε), sin(('-', ('/', 'pi', 2), a[1]), ε), ε)).quantize(ε)
            x = a[1]
            x_val = Decimal(Main(x, ε))  # 获取 x 的近似值

            pi_val = get_pi(ε)
            half_pi = pi_val / 2
            mod_val = x_val % pi_val  # 计算 x mod π

            # 检查是否接近 π/2（tan(x) 的极点）
            if abs(mod_val - half_pi) < ε:
                raise ValueError(f"tan({x_val}) 未定义：x ≈ π/2 + nπ")

            # 正常计算 tan(x) = sin(x) / cos(x)
            add_log("执行正切函数 tan(x)", level="SUMMARY")
            sin_val = sin(x, ε)
            cos_val = sin(('-', ('/', 'pi', 2), x), ε)
            result = Decimal(div(sin_val, cos_val, ε))
            return Decimal(result)

        elif op == 'cot':  # cot(a) = cos(a) / sin(a)
            # return Decimal(div(sin(('-', ('/', 'pi', 2), a[1]), ε), sin(a[1], ε), ε)).quantize(ε)
            x = a[1]
            x_val = Decimal(Main(x, ε))  # 计算 x 的近似值

            pi_val = get_pi(ε)
            mod_val = x_val % pi_val  # 计算 x mod π

            # 检查是否接近 nπ，即 sin(x) ≈ 0，会导致 cot(x) 发散
            if abs(mod_val) < ε or abs(mod_val - pi_val) < ε:
                raise ValueError(f"cot({x_val}) 未定义：x ≈ nπ")

            # cot(x) = cos(x) / sin(x) = sin(π/2 - x) / sin(x)
            add_log("执行余切函数 cot(x)", level="SUMMARY")
            cos_val = sin(('-', ('/', 'pi', 2), x), ε)
            sin_val = sin(x, ε)
            result = Decimal(div(cos_val, sin_val, ε))
            return Decimal(result)

        elif op == 'sec':  # sec(a) = 1 / cos(a)
            x = a[1]
            x_val = Decimal(Main(x, ε))
            pi_val = get_pi(ε)
            half_pi = pi_val / 2
            mod_val = x_val % pi_val

            # 极点判断：x ≈ π/2 + nπ，即 cos(x) ≈ 0
            if abs(mod_val - half_pi) < ε:
                raise ValueError(f"sec({x_val}) 未定义：x ≈ π/2 + nπ")

            # 正常计算
            add_log("执行正割函数 sec(x)", level="SUMMARY")
            cos_val = sin(('-', ('/', 'pi', 2), x), ε)
            result = Decimal(div(1, cos_val, ε))
            return Decimal(result)

        elif op == 'csc':  # csc(a) = 1 / sin(a)
            x = a[1]
            x_val = Decimal(Main(x, ε))
            pi_val = get_pi(ε)
            mod_val = x_val % pi_val

            # 极点判断：x ≈ nπ，即 sin(x) ≈ 0
            if abs(mod_val) < ε or abs(mod_val - pi_val) < ε:
                raise ValueError(f"csc({x_val}) 未定义：x ≈ nπ")

            add_log("执行余割函数 tan(x)", level="SUMMARY")
            sin_val = sin(x, ε)
            result = Decimal(div(1, sin_val, ε))
            return Decimal(result)

        elif op == 'arcsin':  # arcsin(a)
            val = Main(a[1], ε)
            if val < -1 or val > 1:
                raise ValueError(f"arcsin 输入值超出定义域：{val}")

            add_log("执行反正弦函数 arcsin(x)", level="SUMMARY")
            result = Decimal(Main(('*', 2, ('arctan', ('/', a[1], ('+', 1, ('exp', ('-', 1, ('exp', a[1], 2)), ('/', 1, 2)))))), ε))
            return Decimal(result)

        elif op == 'arccos':  # arccos(a) = π/2 - arcsin(a)
            val = Main(a[1], ε)
            if val < -1 or val > 1:
                raise ValueError(f"arccos 输入值超出定义域：{val}")

            add_log("执行反余弦函数 arccos(x)", level="SUMMARY")
            result = Decimal(Main(('-', ('/', 'pi', 2), ('arcsin', a[1])), ε))
            return Decimal(result)

        elif op == 'arctan':  # arctan(a)
            # add_log("执行反正切函数 arctan(x)", level="SUMMARY")
            result = Decimal(arctan(a[1], ε))
            return Decimal(result)

        elif op == 'arccot':  # arccot(a) = π/2 - arctan(a)
            add_log("执行反余切函数 arcot(x)", level="SUMMARY")
            result = Decimal(Main(('-', ('/', 'pi', 2), ('arctan', a[1])), ε))
            return Decimal(result)

        elif op == 'sinh':  # sinh(a) = (e^a - e^(-a)) / 2
            add_log("执行双曲正弦 sinh(x)", level="SUMMARY")
            result = Decimal(Main(('/', ('-', ('exp1', a[1]), ('exp1', ('-', a[1]))), 2), ε))
            return Decimal(result)

        elif op == 'cosh':  # cosh(a) = (e^a + e^(-a)) / 2
            add_log("执行双曲余弦 cosh(x)", level="SUMMARY")
            result = Decimal(Main(('/', ('+', ('exp1', a[1]), ('exp1', ('-', a[1]))), 2), ε))
            return Decimal(result)

        else:
            raise ValueError(f"无法解析的操作: {op}")

    else:
        raise ValueError(f"计算时无法解析的表达式: {a}")

# === 测试代码 ===
if __name__ == "__main__":
    while True:
        user_input = input("请输入数学表达式: ").replace("^", "**")  # 先替换 ^ 为 **
        if not user_input:
            break

        try:
            sig_digits = input("请输入保留有效数字位数(默认100位): ")
            sig_digits = int(sig_digits.strip()) if sig_digits.strip() else 100
            # ε = Decimal(10) ** (-sig_digits)  # ε 仍用于误差控制
            ε = Decimal(10) ** (-1000)  # ε 仍用于误差控制
            print(f"计算精度: ε = {ε}")
            getcontext().prec = sig_digits + 1000  # Decimal 内部计算精度

            get_pi(ε)  # 缓存pi值，避免死循环

            parsed_expr = parse_expression(user_input)
            print(f"转换后的数学操作树: {parsed_expr}")
            result = Main(parsed_expr, ε)

            # print(f"转换后的数学操作树: {parsed_expr}")
            print(f"计算结果: {result}")
            print(f"计算结果（{sig_digits}位有效数字）: {format_sig_digits(result, sig_digits)}")

            print(f"计算精度: ε = {ε}")

        except ValueError as e:
            print(f"错误: {e}")
        pass
