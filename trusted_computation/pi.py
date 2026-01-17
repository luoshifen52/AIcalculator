from decimal import Decimal, getcontext, localcontext
from .log_util import add_log

_PRECOMPUTED_PRECISION = Decimal('1E-1000')
_pi_cached = None  # 用于缓存高精度 π 的值

def reset_pi_cache():
    global _pi_cached
    _pi_cached = None

def _compute_high_precision_pi():
    from .main import Main
    """仅在首次调用时计算高精度 π 值并缓存"""
    global _pi_cached

    """
    使用公式计算 π：
    π = 16 * arctan(1/5) - 4 * arctan(1/239)
    支持任意精度计算
    """
    # add_log("【pi】首次调用，使用 Machin 公式计算 π")
    # getcontext().prec = abs(_PRECOMPUTED_PRECISION.as_tuple().exponent) + 100  # 多留10位避免误差
    pi_expr = ('-', ('*', 16, ('arctan', ('/', 1, 5))), ('*', 4, ('arctan', ('/', 1, 239))))
    # 只计算一次
    pi_val = Main(pi_expr, _PRECOMPUTED_PRECISION)
    _pi_cached = Decimal(pi_val)
    # add_log(f"计算完成，缓存 π ≈ {_pi_cached}")

def get_pi(ε):
    # from main import safe_decimal_quantize

    """返回指定精度的 π，但不重新计算，仅从缓存中截取"""
    if _pi_cached is None:
        _compute_high_precision_pi()
    # add_log(f"【pi】返回缓存的 π 值（精度要求 ε = {ε}）")

    return Decimal(_pi_cached)