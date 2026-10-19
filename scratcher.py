# p = [20,20,20,20]
# acc = 1
# out = []
# for x in p:
#     out.append(acc * x)
#     acc *= (100 - x) / 100
# out.append(acc * 100)
# print(out)

import sympy as sp

m = sp.symbols('m', real=True)

# ---------- 你自己填这几行 ----------
# 每个结果：概率表达式（关于 m 的多项式）、奖金
# 注意：p = 0.2m 已经代入，直接写 m
p = sp.Rational(1, 5) * m
q = 1 - p

P_three_1   = p**3                      # 三个 1
P_three_x   = q * p**2                  # 三个相同非 1
P_two_1     = 2*p**2*q + p*q**2/3       # 恰好两个 1
P_two_x     = 2*p*q**2 + q**3/3         # 恰好两个相同非 1
P_other     = 1 - (P_three_1 + P_three_x + P_two_1 + P_two_x)

prize_three_1 = 350
prize_three_x = 75
prize_two_1   = 30
prize_two_x   = 10
prize_other   = 0

# ---------- 期望 ----------
E = (P_three_1 * prize_three_1
   + P_three_x * prize_three_x
   + P_two_1   * prize_two_1
   + P_two_x   * prize_two_x
   + P_other   * prize_other)


E = sp.expand(E)
print("E(m) =", sp.simplify(E))

print(E.subs(m, 1.23).evalf()) 
# ---------- 解 E = 17 ----------
# eq = sp.Eq(E, 17)
# sols = sp.solve(eq, m)
# print("符号解:", sols)

# # 只保留实数、且在 [0, 5] 范围内的解（m=5 时 p=1 封顶）
# real_sols = [s.evalf() for s in sols if s.is_real]
# print("实数解:", real_sols)
# print("在 [0,5] 内的解:", [s for s in real_sols if 0 <= s <= 5])