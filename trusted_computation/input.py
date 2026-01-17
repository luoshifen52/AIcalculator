import ast
import re
from decimal import Decimal, getcontext

def preprocess_decimal_constants(expr):
    """
    将高精度浮点数（如 123.456...）转换为 Decimal('...') 字符串形式
    以防止被 Python 自动识别为 float 而损失精度
    """
    # 匹配独立的浮点常数（非函数名、变量名等）
    pattern = re.compile(r'(?<![\w.])(\d+\.\d+)(?![\w.])')
    return pattern.sub(r"Decimal('\1')", expr)

def parse_expression(expr):
    """
    解析用户输入的数学表达式，转换成数学操作树，部分表达式形式:log(a,b),ln(a),e^a,a^b
    """
    expr = preprocess_decimal_constants(expr.replace("^", "**"))
    tree = ast.parse(expr, mode='eval')

    def _parse(node):
        if isinstance(node, ast.BinOp):  # 处理二元运算 (如 +, -, *, /, **)
            left = _parse(node.left)
            right = _parse(node.right)

            if isinstance(node.op, ast.Pow):  # 幂运算 (**)
                if left == 'e':  # 处理 e^a
                    return ('exp1', right)
                else:  # 处理 a^b
                    return ('exp', left, right)
            elif isinstance(node.op, ast.Add):
                return ('+', left, right)
            elif isinstance(node.op, ast.Sub):
                return ('-', left, right)
            elif isinstance(node.op, ast.Mult):
                return ('*', left, right)
            elif isinstance(node.op, ast.Div):
                return ('/', left, right)
            else:
                raise ValueError(f"不支持的运算符: {node.op}")

        elif isinstance(node, ast.Call):  # 处理函数调用，如 sin(x)
            func_name = node.func.id
            args = [_parse(arg) for arg in node.args]

            if func_name == 'Decimal' and len(args) == 1:
                return Decimal(args[0])  # 处理 Decimal('...')

            if func_name in {"sin", "cos", "tan", "cot", "sec", "csc",
                             "sinh", "cosh", "arcsin", "arccos", "arctan", "arccot",
                             "ln"}:
                return (func_name, *args)
            elif func_name == "log":  # log(a, b) 转换成 ('log', a, b)
                if len(args) == 2:
                    return ('log', args[0], args[1])
                else:
                    raise ValueError("log 函数需要两个参数")
            else:
                raise ValueError(f"不支持的函数: {func_name}")

        elif isinstance(node, ast.Name):  # 处理变量，如 e, pi
            if node.id == "pi":
                return "pi"
            elif node.id == "e":
                return "e"
            else:
                raise ValueError(f"未知变量: {node.id}")

        # elif isinstance(node, ast.Num):  # 处理数字
        #     return Decimal(str(node.n))  # 解决 float 精度丢失问题

        elif isinstance(node, ast.Str):  # 字符串 → Decimal 参数中出现
            return node.s

        elif isinstance(node, ast.Constant):  # Python 3.8+
            return Decimal(str(node.value))

        elif isinstance(node, ast.Num):  # Python 3.7 兼容
            return Decimal(str(node.n))

        elif isinstance(node, ast.UnaryOp):  # 处理负号 -x
            operand = _parse(node.operand)
            if isinstance(node.op, ast.UAdd):  # +x
                return operand
            elif isinstance(node.op, ast.USub):  # -x
                return ('-', operand)
            else:
                raise ValueError(f"不支持的单目运算: {node.op}")

        else:
            raise ValueError(f"输入无法解析的表达式: {ast.dump(node)}")

    return _parse(tree.body)


# # === 测试代码 ===
# if __name__ == "__main__":
#     while True:
#         user_input = input("请输入数学表达式: ").replace("^", "**")  # 先替换 ^ 为 **
#
#         try:
#             d = input("请输入有效位数 (默认100位): ")
#             d = int(d) if d.strip() else 100  # 默认 d = 100
#             ε = Decimal(10) ** (-d)  # 计算 ε
#             # getcontext().prec = d + 5  # 设置 Decimal 计算精度，略高于 d
#             getcontext().prec = d
#
#             parsed_expr = parse_expression(user_input)
#             print("\n转换后的数学操作树:")
#             print(parsed_expr)
#             print(f"计算精度: ε = {ε}")
#         except ValueError as e:
#             print(f"错误: {e}")
