#没什么用，突然想起来直接x//10//2就可以速算估价105%
from z3 import *
from itertools import chain, product
import math

items = ["ribwich","fuel","hand"]
item = items[2]
solve_check,strict_check = False,True
view_prices = False
simp = True
item_dict = {"ribwich":{"base":150,"min_value":40,"ranges":[
    [(0,None),(80,'x1')],[(0,None),(50,'x2')],[(50,'x3'),(-50,'x4')],[(0,None),(300,'x5')],[(0,None),(800,'x6')],
]},"fuel":{"base":100,"min_value":30,"filt_prove":2,"relax":4,"ranges":[
    [(0,None),(-15,'x1'),(-30,'x2')],[(0,None),(-50,'x3')],[(0,None),(-10,'x4')],[(0,None),(20,'x5')],\
    [(0,None),(-50,'x6'),(50,'x7')],[(0,None),(20,'x8',{4:[0,-50]}),(40,'x9',{0:[0],1:[0],2:[0],4:[0]}),\
    (40,'x10',{1:[0],4:[0]}),(80,'x11',{0:[0],1:[0],2:[0],3:[0],4:[50]})]
]},"hand":{"base":100,"min_value":50,"filt_prove":4,"relax":3,"ranges":[
    [(0,None),(50,'x1'),(200,'x2')],[(0,None),(-35,'x3'),(-85,'x4')],[(0,None),(45,'x5'),(120,'x6'),(-60,'x7')],\
    [(0,None),(50,'x8')],[(0,None),(80,'x9')],[(0,None),(100,'x10',{0:[50],1:[0],2:[45,120],3:[50],4:[80]}),\
    (200,'x11',{0:[200],1:[0],2:[120]})]
]}}
if simp: item_dict = {"ribwich":{"base":150,"min_value":40,"relax":5,"rules":['x2==x3','x1==4','x4==0'],"ranges":[
    [(0,None),(80,'x1')],[(0,None),(50,'x2')],[(50,'x3'),(-50,'x4')],[(0,None),(300,'x5')],[(0,None),(800,'x6')],
]},"fuel":{"base":100,"min_value":30,"relax":4,"rules":['x11==4','x10==x9','x5==x8','x3==x6'],"ranges":[
    [(0,None),(-15,'x1'),(-30,'x2')],[(0,None),(-50,'x3')],[(0,None),(-10,'x4')],[(0,None),(20,'x5')],\
    [(0,None),(-50,'x6'),(50,'x7')],[(0,None),(20,'x8',{4:[0,-50]}),(40,'x9',{0:[0],1:[0],2:[0],4:[0]}),\
    (40,'x10',{1:[0],4:[0]}),(80,'x11',{0:[0],1:[0],2:[0],3:[0],4:[50]})]
]},"hand":{"base":100,"min_value":50,"relax":4,"rules":['x1==x8','4==x9','x2==x11'],"ranges":[
    [(0,None),(50,'x1'),(200,'x2')],[(0,None),(-35,'x3'),(-85,'x4')],[(0,None),(45,'x5'),(120,'x6'),(-60,'x7')],\
    [(0,None),(50,'x8')],[(0,None),(80,'x9')],[(0,None),(100,'x10',{0:[50],1:[0],2:[45,120],3:[50],4:[80]}),\
    (200,'x11',{0:[200],1:[0],2:[120]})]
]}}

def solve_p(it):
    base,min_v,ranges,filt_p,relax,rules = it["base"],it["min_value"],it["ranges"],it.get("filt_prove",20),it.get("relax",0),it.get("rules",[])
    names,price = [],[]
    for t in chain.from_iterable(ranges):
        if t[1] and t[1] not in names:
            names.append(t[1])
    idx = {n: i for i, n in enumerate(names)}
    x = [Int(n) for n in names]
    ns = {n: x[idx[n]] for n in names}

    s = Solver()
    MINp = -200
    for r in rules: 
        if r: s.add(eval(r, {"__builtins__": {}}, ns))
    for cond in product(*ranges):
        if any(cond[idx][0] not in allowed for t in cond if len(t) > 2 for idx, allowed in t[2].items()): continue
        p_pre = base + sum(_[0] for _ in cond)
        price.append((p_pre, [_[0] for _ in cond]))
        p_ext = int(max(p_pre,min_v) * 1.05)
        p_min = MINp if p_pre<min_v else math.ceil(int(p_ext*0.15)/0.15) if int(p_ext*0.15)-int(p_pre*0.15)>=filt_p else max(int(p_pre*0.95),math.ceil(int(p_ext*0.15)/0.15)-relax)

        active = [x[idx[t[1]]] for t in cond if t[1]]
        s.add(Sum(active) <= p_ext - p_pre)
        s.add(Sum(active) >= p_min - p_pre)
    if view_prices: 
        for p in sorted(price):
            print(p)
    solutions,solution = [],()
    MAX = 10000   # 防止无限循环

    while s.check() == sat and len(solutions) < MAX:
        m = s.model()
        sol = tuple(m[v].as_long() for v in x)
        solutions.append(sol)
        # 排除刚找到的解
        s.add(Or([v != m[v] for v in x]))

    if solutions: solution = max(solutions, key=lambda s: s.count(0))
    print(f"{solution}; 共找到 {len(solutions)} 组解")

    if solutions and solve_check:
        print("=" * 90)
        print(f"变量顺序 : {names}")
        print(f"计算参数 : {dict(zip(names, solution))}")
        print("=" * 90)

        all_ok = True
        fail_count = 0

        for cond in product(*ranges):
            #是否满足组合条件
            if any(cond[idx][0] not in allowed for t in cond if len(t) > 2 for idx, allowed in t[2].items()): continue

            # 标准价值 p_pre
            p_pre = base + sum(_[0] for _ in cond)

            # 理论最高估价 p_ext = int(p_pre * 1.05)
            p_ext = int(max(p_pre,min_v) * 1.05)

            # p_min：为了让奖金 +1，估价至少要达到的值
            p_min = MINp if p_pre<min_v else math.ceil(int(p_ext*0.15)/0.15) if int(p_ext*0.15)-int(p_pre*0.15)>=filt_p else max(int(p_pre*0.95),math.ceil(int(p_ext*0.15)/0.15)-relax)
            if strict_check: p_min = MINp if p_pre<min_v else math.ceil(int(p_ext*0.15)/0.15)
            # 当前组合里活跃的变量，以及用计算参数叠加后的估价
            active = [t[1] for t in cond if t[1]]
            adj = sum(solution[idx[n]] for n in active)
            p_adj = p_pre + adj

            # 三种估价对应的奖金收入
            inc_pre = int(p_pre * 0.15)
            inc_ext = int(p_ext * 0.15)
            inc_adj = int(p_adj * 0.15)

            # 约束检查：p_min <= p_adj <= p_ext
            ok = (p_min <= p_adj <= p_ext)
            if not ok:
                all_ok = False
                fail_count += 1

            # ---------- 打印 ----------
            print(f"组合: {cond}")
            print(f"  活跃变量: {active}   调整量: {adj}")
            print(f"  标准价值   p_pre = {p_pre:5d}   收入 int(p_pre*0.15) = {inc_pre}")
            print(f"  理论最高   p_ext = {p_ext:5d}   收入 int(p_ext*0.15) = {inc_ext}")
            print(f"  调整后     p_adj = {p_adj:5d}   收入 int(p_adj*0.15) = {inc_adj}")
            print(f"  约束: p_min = {p_min}, 需满足 {p_min - p_pre} <= adj <= {p_ext - p_pre}"
                f"   ->  {'OK' if ok else 'FAIL'}")
            print()

        print("=" * 90)
        if all_ok:
            print("所有组合全部通过约束检查 ✔")
        else:
            print(f"存在 {fail_count} 个组合不满足约束 ✘")        

solve_p(item_dict[item])
