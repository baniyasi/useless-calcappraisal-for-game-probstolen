import re, copy, random
from collections import defaultdict
wikistring = '''
| [一次性钥匙卡（医疗）](/items/med_keycard)       | 75      | m * 50% |
| [一次性钥匙卡（医疗）](/items/med_keycard)       | 75      | m * 50% |
| [赛纳普斯注射器](/items/black_injector)       | 350     | m * 33% |
'''
frida_func = '''
function dumpShape(id) {
    var shape = Il2Cpp.domain.assembly("Assembly-CSharp").image.class("DirectoryMaster").method("Item").invoke(Il2Cpp.string(id), true).field("<shape>k__BackingField").value
    var w = shape.field("<width>k__BackingField").value
    var h = shape.field("<height>k__BackingField").value
    var data = shape.field("data").value
    console.log("----")
    for (var y = 0; y < h; y++) {
        var row = ""
        for (var x = 0; x < w; x++) { row += data.get(y * w + x) ? "+" : "·" }
        console.log(row)
    }
}
'''
frida_shape = '''
----
+
+
----
+
'''
shapedict = {'bandage_item': [[1], [1]], 'birth_control_pill': [[1]], 'black_injector': [[1, 1, 1, 1]], 'blood_bag': [[1, 1], [1, 1], [1, 1]], 'blue_blood_bag': [[1, 1], [1, 1], [1, 1]], 'caffeine_pill': [[1]], 'common_chemical': [[1, 1, 1], [1, 1, 1]], 'energy_credit': [[1], [1]], 'fanta_pill': [[1]], 'galaxy_blend': [[1, 1], [1, 1]], 'hemostatic_bandage_item': [[1], [1]], 'large_purple_injector': [[1, 1, 1, 1]], 'med_keycard': [[1, 1], [1, 1]], 'phagimycin_pill': [[1]], 'pink_injector': [[1, 1, 1, 1]], 'restricted_chemical': [[1, 1, 1], [1, 1, 1]], 'rubbing_alcohol': [[1], [1]], 'salve': [[1, 1], [1, 1]], 'smelling_salt': [[1]], 'surgery_tool': [[1, 1, 1, 1], [1, 1, 1, 1]]}


box_prob = {"med": [({'med_keycard': 1}, 50.0), ({'med_keycard': 1}, 50.0), ({'black_injector': 1}, 33.0), ({'black_injector': 1}, 33.0), ({'large_purple_injector': 1}, 100.0), ({'surgery_tool': 1}, 25.0), ({'common_chemical': 1}, 75.0), ({'restricted_chemical': 1}, 50.0), ({'common_chemical': 1}, 50.0), ({'salve': 1}, 75.0), ({'rubbing_alcohol': 1}, 75.0), ({'energy_credit': 1}, 100.0), ({'bandage_item': 1}, 75.0), ({'bandage_item': 1}, 75.0), ({'bandage_item': 1}, 50.0), ({'bandage_item': 1}, 50.0), ({'blood_bag': 1}, 50.0), ({'blue_blood_bag': 1}, 25.0), ({'galaxy_blend': 1}, 33.0), ({'galaxy_blend': 1}, 33.0), ({'hemostatic_bandage_item': 1}, 75.0), ({'hemostatic_bandage_item': 1}, 75.0), ({'pink_injector': 1}, 50.0), ({'pink_injector': 1}, 33.0), ({'pink_injector': 1}, 33.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'caffeine_pill': 1}, 50.0)],
            }
def getnamesfromwiki(text):
    pattern = re.compile(r'/items/([A-Za-z0-9_]+)')
    items = sorted(set(pattern.findall(text)))
    frida_getshape = f'''["{'","'.join(items)}"].forEach(dumpShape)'''
    print("please run following code in frida before getshape")
    print(frida_func)
    print(frida_getshape)
    return items
def getshapefromfrida(items,text):
    shapes = [block.strip() for block in re.split(r'-{4,}', text) if block.strip()]
    if len(items)!=len(shapes): print("string frida_shape not match with wikistring items")
    else:
        shapedict = {}
        for i,block in enumerate(shapes): shapedict[items[i]] = [[1 if ch=='+' else 0 for ch in line] for line in block.splitlines()]
        print(shapedict)
def getprobfromwiki(text):
    pattern = re.compile(r'/items/([A-Za-z0-9_]+)[^\n%]*?(\d+(?:\.\d+)?)%')
    matches = pattern.findall(text)
    prob = [({item:1},float(pct)) for item, pct in matches]
    print(prob)

# getshapefromfrida(getnamesfromwiki(wikistring),frida_shape)
# getprobfromwiki(wikistring)

def _rotate90(m): return [list(row) for row in zip(*m[::-1])]
def _mirror_lr(m): return [row[::-1] for row in m]
def _candidates(item):
    shapes, cur = [], [list(row) for row in item]
    for _ in range(4):
        shapes.append(cur)
        cur = _rotate90(cur)
    cur = _mirror_lr(item)
    for _ in range(4):
        shapes.append(cur)
        cur = _rotate90(cur)
    return shapes
def unique_candidates(item):
    seen, result = set(), []
    for shape in _candidates(item):
        key = tuple(tuple(row) for row in shape)
        if key not in seen:
            seen.add(key)
            result.append(shape)
    return result
def _can_place(box, shape, r, c):
    bh, sh, bw, sw = len(box), len(shape), len(box[0]), len(shape[0])
    if r + sh > bh or c + sw > bw: return False
    for i in range(sh):
        for j in range(sw):
            if shape[i][j] and box[r + i][c + j]: return False
    return True
def tryadd(box, shapes, tag):
    if not shapes:
        return False
    for shape in shapes:
        sh, sw = len(shape), len(shape[0])
        if sh == 0 or sw == 0:
            continue
        for r in range(len(box) - sh + 1):
            for c in range(len(box[0]) - sw + 1):
                if _can_place(box, shape, r, c):
                    for i in range(sh):
                        for j in range(sw):
                            if shape[i][j]:
                                box[r + i][c + j] = tag
                    return True
    return False
def format_box(box): 
    print('\n'.join(['\t'.join('.' if v == 0 else str(v >> 8) for v in row) for row in box]))
    print('-' * 20)

def openbox_one_forMC(boxname, mul):
    box = [[0] * 7 for _ in range(5)]
    prob_arr = box_prob.get(boxname, [])
    shapedict_candi = {k: unique_candidates(v) for k, v in shapedict.items()}
    for i, (items_dict, p_pct) in enumerate(prob_arr):
        p_pct = min(100, mul * p_pct)
        if random.random() * 100 < p_pct:
            keys = list(items_dict.keys())
            weights = list(items_dict.values())
            if not keys or sum(weights) == 0:
                continue
            idx = random.choices(range(len(keys)), weights=weights, k=1)[0]
            k = keys[idx]
            tag = ((i + 1) << 8) | (idx & 0xFF)
            tryadd(box, shapedict_candi.get(k, []), tag)
    return box
def estimate_prob(boxname, mul, N=100_000):
    prob_arr = box_prob.get(boxname, [])
    seen = defaultdict(int)

    for _ in range(N):
        box = openbox_one_forMC(boxname, mul)
        present = set()
        for row in box:
            for v in row:
                if v:
                    present.add(v)
        for v in present:
            seen[v] += 1

    result = defaultdict(int)
    for tag, c in seen.items():
        layer = (tag >> 8) - 1
        idx = tag & 0xFF
        keys = list(prob_arr[layer][0].keys())
        if idx >= len(keys):
            print(f"bad tag {tag}: layer={layer}, idx={idx}, keys={keys}")
            continue
        result[(layer, keys[idx])] += c

    for (layer, item_id), c in sorted(result.items()):
        print(f"layer {layer:2d} | {item_id:30s} | {c / N:.4%}")
    return result
def openbox_one(boxname, mul):
    box = [[0] * 7 for _ in range(5)]
    prob_arr = box_prob.get(boxname, [])
    shapedict_candi = {k: unique_candidates(v) for k, v in shapedict.items()}
    for i, (items_dict, p_pct) in enumerate(prob_arr):
        p_pct = min(100, mul * p_pct)
        if random.random() * 100 < p_pct:
            keys = list(items_dict.keys())
            weights = list(items_dict.values())
            if not keys or sum(weights) == 0:
                continue
            idx = random.choices(range(len(keys)), weights=weights, k=1)[0]
            k = keys[idx]
            tag = ((i + 1) << 8) | (idx & 0xFF)
            tryadd(box, shapedict_candi.get(k, []), tag)
    format_box(box)

openbox_one("med", 1)
# estimate_prob("med", 1, N=100_000)



