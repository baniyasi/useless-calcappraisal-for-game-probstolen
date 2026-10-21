import random, time
from collections import defaultdict

shapedict = {'bandage_item': [[1], [1]], 'birth_control_pill': [[1]], 'black_injector': [[1, 1, 1, 1]], 'blood_bag': [[1, 1], [1, 1], [1, 1]], 'blue_blood_bag': [[1, 1], [1, 1], [1, 1]], 'caffeine_pill': [[1]], 'common_chemical': [[1, 1, 1], [1, 1, 1]], 'energy_credit_med': [[1], [1]], 'fanta_pill': [[1]], 'galaxy_blend': [[1, 1], [1, 1]], 'hemostatic_bandage_item': [[1], [1]], 'large_purple_injector': [[1, 1, 1, 1]], 'med_keycard': [[1, 1], [1, 1]], 'phagimycin_pill': [[1]], 'pink_injector': [[1, 1, 1, 1]], 'restricted_chemical': [[1, 1, 1], [1, 1, 1]], 'rubbing_alcohol': [[1], [1]], 'salve': [[1, 1], [1, 1]], 'smelling_salt': [[1]], 'surgery_tool': [[1, 1, 1, 1], [1, 1, 1, 1]], 'advanced_flux_agent': [[1, 1], [1, 1]], 'common_electronic': [[1, 1, 1], [1, 1, 1]], 'energy_credit_breeder': [[1], [1]], 'energy_credit_eng1': [[1], [1]], 'energy_credit_eng2': [[1], [1]], 'energy_credit_ext_eng': [[1], [1]], 'eng_keycard': [[1, 1], [1, 1]], 'flux_agent': [[1]], 'furnace_module_blast': [[1], [1], [1], [1]], 'module_bay_expansion_kit': [[1, 1], [1, 1]], 'module_extractor': [[1, 1], [1, 1], [1, 1]], 'module_extractor_advanced': [[1, 1], [1, 1], [1, 1]], 'node_medium': [[1], [1]], 'nuts_metal': [[1, 1], [1, 1]], 'screwdriver': [[1], [1], [1]], 'system_capped_neural_core': [[1, 1], [1, 1]], 'turbo_booster': [[1, 1, 1], [1, 1, 1]], 'turbo_booster_adv': [[1, 1, 1], [1, 1, 1]], 'wire_cutter': [[1], [1], [1]], 'system_module': [[1, 1], [1, 1]], 'system_module_2': [[1, 1], [1, 1]], 'system_module_l': [[1, 1, 1], [0, 0, 1]], 'system_module_t': [[0, 1], [1, 1], [0, 1]], 'system_module_c': [[1, 1], [0, 1]], 'system_module_2_s': [[1, 1], [0, 1], [1, 1]], 'system_module_2_h': [[1, 1], [1, 1], [0, 1]], 'combat_knife': [[1, 1, 1, 1, 1]], 'energy_credit_sec': [[1], [1]], 'flashbang_grenade': [[1], [1]], 'flashlight': [[1, 1, 1]], 'glock_receiver': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'heavy_pistol_ammo': [[1]], 'heavy_pistol_ammo_nl': [[1]], 'heavy_pistol_ammo_p': [[1]], 'sec_keycard': [[1, 1], [1, 1]], 'smoke_grenade': [[1], [1]], 'stun_baton': [[1, 1, 1, 1, 1, 1]], 'stun_gun': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'tazer': [[1, 1], [1, 1], [1, 1]], 'topical_bandage_item': [[1], [1]], 'aquascan': [[1, 1], [1, 1], [1, 1]], 'beis_icecream': [[1, 1, 1], [1, 1, 1]], 'box_cutter': [[1, 1, 1, 1]], 'cassette1d': [[1, 1], [1, 1]], 'cat_bar': [[1, 1], [1, 1]], 'cup_noodle': [[1, 1, 1], [1, 1, 1]], 'energy_credit': [[1], [1]], 'energy_drink': [[1], [1]], 'hatchet': [[1, 1, 1, 1], [0, 0, 1, 1]], 'hydroreed_seed': [[1]], 'kitchen_knife': [[1, 1, 1, 1, 1]], 'kotton_seed': [[1]], 'li_eat_snackbar': [[1, 1, 1]], 'neuroactive_perfume': [[1, 1], [1, 1]], 'nudka': [[1, 1], [1, 1], [1, 1], [1, 1]], 'nutrient_tablet': [[1]], 'nutrifruit_seed_packet': [[1, 1], [1, 1]], 'paper_towel': [[1, 1], [1, 1], [1, 1]], 'portable_water_purifier': [[1, 1], [1, 1]], 'processed_cheese': [[1, 1], [1, 1]], 'processed_juice': [[1, 1], [1, 1], [1, 1]], 'processed_meat': [[1, 1], [1, 1]], 'processed_milk': [[1, 1], [1, 1], [1, 1]], 'red_beer': [[1], [1], [1], [1]], 'ser_keycard': [[1, 1], [1, 1]], 'shampoo': [[1, 1], [1, 1], [1, 1]], 'soda_red': [[1], [1]], 'toilet_paper': [[1, 1], [1, 1]], 'toothpaste': [[1, 1, 1]], 'uv_filter': [[1, 1, 1, 1, 1]], 'water_filter': [[1], [1]], 'water_filter_adv': [[1], [1], [1]], 'water_tablet_container': [[1], [1], [1]], 'water_test_container': [[1], [1]], 'zerochew': [[1]], 'bottled_water_premium': [[1], [1], [1], [1]], 'cmd_keycard': [[1, 1], [1, 1]], 'dream_dust': [[1]], 'glass_shard_shiv': [[1, 1, 1]], 'handmade_pistol': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'heavy_handmade_pistol': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'kitchen_cleaver': [[1, 1, 1, 1, 1], [0, 0, 1, 1, 1]], 'large_purple_injector_fake': [[1, 1, 1, 1]], 'pheromone_perfume': [[1, 1], [1, 1]], 'pipe_weapon': [[1, 1, 1, 1, 1], [0, 0, 0, 0, 1]], 'raw_meat': [[1, 1, 1], [1, 1, 1]], 'scav_token': [[1], [1]], 'scratcher': [[1, 1], [1, 1]], 'skincare_cream': [[1, 1], [1, 1]], 'small_pistol_ammo': [[1]], 'small_pistol_ammo_nl': [[1]], 'small_pistol_ammo_p': [[1]], 'unlicensed_phagimycin_pill': [[1]], 'wine_yeast_red': [[1], [1]], 'zyanide_pill': [[1]]}

valuedict = {'med_keycard': 75.0, 'black_injector': 350, 'large_purple_injector': 160, 'surgery_tool': 200, 'common_chemical': 50.0, 'restricted_chemical': 100.0, 'salve': 80, 'rubbing_alcohol': 35, 'bandage_item': 8, 'blood_bag': 33, 'blue_blood_bag': 250.0, 'galaxy_blend': 25.0, 'hemostatic_bandage_item': 16, 'pink_injector': 50.0, 'phagimycin_pill': 25, 'fanta_pill': 12.0, 'smelling_salt': 15, 'birth_control_pill': 15, 'caffeine_pill': 10.0, 'energy_credit_med': 47.5, 'energy_credit_eng1': 110.0, 'energy_credit_eng2': 60.0, 'energy_credit_ext_eng': 92.5, 'screwdriver': 25.0, 'wire_cutter': 40.0, 'module_bay_expansion_kit': 150.0, 'module_extractor': 100.0, 'module_extractor_advanced': 350.0, 'turbo_booster': 35.0, 'turbo_booster_adv': 300.0, 'energy_credit_breeder': 500.0, 'system_capped_neural_core': 250.0, 'advanced_flux_agent': 300.0, 'furnace_module_blast': 150.0, 'eng_keycard': 75.0, 'system_module': 75, 'system_module_c': 64, 'system_module_l': 69, 'system_module_t': 69, 'system_module_2': 105, 'system_module_2_s': 120, 'system_module_2_h': 120, 'node_medium': 50.0, 'common_electronic': 33.0, 'nuts_metal': 14.0, 'flux_agent': 4.0, 'glock_receiver': 200.0, 'stun_gun': 250.0, 'tazer': 100.0, 'energy_credit_sec': 85.0, 'stun_baton': 165.0, 'combat_knife': 75.0, 'sec_keycard': 100.0, 'flashbang_grenade': 75.0, 'flashlight': 40.0, 'smoke_grenade': 60.0, 'heavy_pistol_ammo': 30.0, 'heavy_pistol_ammo_p': 36.0, 'heavy_pistol_ammo_nl': 24.0, 'topical_bandage_item': 16.0, 'cassette1d': 35.0, 'neuroactive_perfume': 150.0, 'ser_keycard': 40.0, 'aquascan': 200.0, 'uv_filter': 150.0, 'water_filter_adv': 250.0, 'portable_water_purifier': 225.0, 'toilet_paper': 25.0, 'processed_cheese': 20.0, 'toothpaste': 15.0, 'water_filter': 25.0, 'nutrifruit_seed_packet': 91.0, 'water_test_container': 31.0, 'water_tablet_container': 55.0, 'energy_credit': 43.0, 'box_cutter': 28.0, 'kitchen_knife': 35.0, 'hatchet': 45.0, 'paper_towel': 35.0, 'shampoo': 30.0, 'kotton_seed': 20.0, 'hydroreed_seed': 20.0, 'nutrient_tablet': 5.0, 'energy_drink': 18.0, 'soda_red': 15.0, 'cat_bar': 15.0, 'li_eat_snackbar': 17.0, 'red_beer': 18.0, 'processed_milk': 16.0, 'processed_juice': 14.0, 'processed_meat': 25.0, 'zerochew': 8.0, 'cup_noodle': 20.0, 'nudka': 85.0, 'beis_icecream': 40.0, 'skincare_cream': 500.0, 'bottled_water_premium': 325.0, 'pheromone_perfume': 200.0, 'scav_token': 100.0, 'large_purple_injector_fake': 40.0, 'heavy_handmade_pistol': 160.0, 'handmade_pistol': 120.0, 'glass_shard_shiv': 8.0, 'kitchen_cleaver': 50.0, 'pipe_weapon': 15.0, 'raw_meat': 120.0, 'cmd_keycard': 125.0, 'scratcher': 20.0, 'unlicensed_phagimycin_pill': 5.0, 'dream_dust': 18.0, 'zyanide_pill': 33.0, 'small_pistol_ammo': 20.0, 'small_pistol_ammo_p': 26.0, 'small_pistol_ammo_nl': 14.0, 'wine_yeast_red': 8.0}

box_prob = {"med": [({'med_keycard': 1}, 50.0), ({'med_keycard': 1}, 50.0), ({'black_injector': 1}, 33.0), ({'black_injector': 1}, 33.0), ({'large_purple_injector': 1}, 100.0), ({'surgery_tool': 1}, 25.0), ({'common_chemical': 1}, 75.0), ({'restricted_chemical': 1}, 50.0), ({'common_chemical': 1}, 50.0), ({'salve': 1}, 75.0), ({'rubbing_alcohol': 1}, 75.0), ({'energy_credit_med': 1}, 100.0), ({'bandage_item': 1}, 75.0), ({'bandage_item': 1}, 75.0), ({'bandage_item': 1}, 50.0), ({'bandage_item': 1}, 50.0), ({'blood_bag': 1}, 50.0), ({'blue_blood_bag': 1}, 25.0), ({'galaxy_blend': 1}, 33.0), ({'galaxy_blend': 1}, 33.0), ({'hemostatic_bandage_item': 1}, 75.0), ({'hemostatic_bandage_item': 1}, 75.0), ({'pink_injector': 1}, 50.0), ({'pink_injector': 1}, 33.0), ({'pink_injector': 1}, 33.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'caffeine_pill': 1}, 50.0), ({'caffeine_pill': 1}, 50.0), ({'caffeine_pill': 1}, 50.0)],
            "eng": [({'energy_credit_eng1': 1}, 100.0), ({'energy_credit_eng2': 1}, 50.0), ({'energy_credit_ext_eng': 1}, 100.0), ({'screwdriver': 1}, 66.0), ({'wire_cutter': 1}, 66.0), ({'module_bay_expansion_kit': 1}, 25.0), ({'module_bay_expansion_kit': 1}, 25.0), ({'module_extractor': 1}, 25.0), ({'module_extractor': 1}, 25.0), ({'module_extractor_advanced': 1}, 12.0), ({'turbo_booster': 1}, 25.0), ({'turbo_booster': 1}, 25.0), ({'turbo_booster_adv': 1}, 8.0), ({'energy_credit_breeder': 1}, 12.0), ({'system_capped_neural_core': 1}, 4.0), ({'advanced_flux_agent': 1}, 12.0), ({'furnace_module_blast': 1}, 15.0), ({'eng_keycard': 1}, 50.0), ({'eng_keycard': 1}, 50.0), ({'system_module':25,'system_module_c':25,'system_module_t':25,'system_module_l':26}, 50.0), ({'system_module':25,'system_module_c':25,'system_module_t':25,'system_module_l':26}, 50.0), ({'system_module':25,'system_module_c':25,'system_module_t':25,'system_module_l':26}, 50.0), ({'node_medium': 1}, 50.0), ({'node_medium': 1}, 50.0), ({'system_module_2':33,'system_module_2_h':34,'system_module_2_s':34}, 33.0), ({'system_module_2':33,'system_module_2_h':34,'system_module_2_s':34}, 33.0), ({'system_module_2':33,'system_module_2_h':34,'system_module_2_s':34}, 33.0), ({'common_electronic': 1}, 33.0), ({'common_electronic': 1}, 33.0), ({'common_electronic': 1}, 33.0), ({'nuts_metal': 1}, 33.0), ({'nuts_metal': 1}, 33.0), ({'flux_agent': 1}, 50.0), ({'flux_agent': 1}, 50.0), ({'flux_agent': 1}, 50.0)],
            "sec": [({'glock_receiver': 1}, 20.0), ({'stun_gun': 1}, 20.0), ({'tazer': 1}, 33.0), ({'energy_credit_sec': 1}, 100.0), ({'stun_baton': 1}, 35.0), ({'stun_baton': 1}, 35.0), ({'combat_knife': 1}, 35.0), ({'combat_knife': 1}, 35.0), ({'pink_injector': 1}, 50.0), ({'pink_injector': 1}, 50.0), ({'pink_injector': 1}, 50.0), ({'sec_keycard': 1}, 50.0), ({'sec_keycard': 1}, 50.0), ({'flashbang_grenade': 1}, 50.0), ({'flashbang_grenade': 1}, 50.0), ({'flashlight': 1}, 33.0), ({'smoke_grenade': 1}, 50.0), ({'smoke_grenade': 1}, 50.0), ({'heavy_pistol_ammo': 1}, 55.0), ({'heavy_pistol_ammo_p': 1}, 55.0), ({'heavy_pistol_ammo_nl': 1}, 55.0), ({'heavy_pistol_ammo': 1}, 55.0), ({'heavy_pistol_ammo_p': 1}, 55.0), ({'heavy_pistol_ammo_nl': 1}, 55.0), ({'topical_bandage_item': 1}, 55.0), ({'topical_bandage_item': 1}, 55.0)],
            "ser": [({'cassette1d': 1}, 20.0), ({'neuroactive_perfume': 1}, 8.0), ({'ser_keycard': 1}, 66.0), ({'ser_keycard': 1}, 33.0), ({'aquascan': 1}, 15.0), ({'uv_filter': 1}, 15.0), ({'water_filter_adv': 1}, 12.0), ({'portable_water_purifier': 1}, 8.0), ({'toilet_paper': 1}, 50.0), ({'toilet_paper': 1}, 33.0), ({'toilet_paper': 1}, 15.0), ({'processed_cheese': 1}, 33.0), ({'toothpaste': 1}, 75.0), ({'water_filter': 1}, 75.0), ({'water_filter': 1}, 50.0), ({'water_filter': 1}, 33.0), ({'nutrifruit_seed_packet': 1}, 33.0), ({'water_test_container': 1}, 50.0), ({'water_tablet_container': 1}, 50.0), ({'energy_credit': 1}, 75.0), ({'energy_credit': 1}, 25.0), ({'box_cutter': 1}, 33.0), ({'kitchen_knife': 1}, 33.0), ({'hatchet': 1}, 25.0), ({'paper_towel': 1}, 33.0), ({'paper_towel': 1}, 33.0), ({'shampoo': 1}, 33.0), ({'shampoo': 1}, 33.0), ({'caffeine_pill': 1}, 33.0), ({'caffeine_pill': 1}, 33.0), ({'caffeine_pill': 1}, 33.0), ({'kotton_seed': 1}, 75.0), ({'kotton_seed': 1}, 50.0), ({'kotton_seed': 1}, 33.0), ({'hydroreed_seed': 1}, 75.0), ({'hydroreed_seed': 1}, 50.0), ({'module_bay_expansion_kit': 1}, 25.0), ({'nutrient_tablet': 1}, 50.0), ({'nutrient_tablet': 1}, 50.0), ({'nutrient_tablet': 1}, 50.0),
                    ({'galaxy_blend':90,'energy_drink':90,'soda_red':90,'cat_bar':90,'li_eat_snackbar':90,'red_beer':90,'processed_milk':90,'processed_juice':90,'processed_meat':90,'zerochew':90,'cup_noodle':90,'nudka':55,'beis_icecream':55}, 100),({'galaxy_blend':90,'energy_drink':90,'soda_red':90,'cat_bar':90,'li_eat_snackbar':90,'red_beer':90,'processed_milk':90,'processed_juice':90,'processed_meat':90,'zerochew':90,'cup_noodle':90,'nudka':55,'beis_icecream':55}, 100)],
            "evi": [({'skincare_cream': 1}, 4.0), ({'bottled_water_premium': 1}, 6.0), ({'neuroactive_perfume': 1}, 4.0), ({'pheromone_perfume': 1}, 6.0), ({'turbo_booster_adv': 1}, 6.0), ({'blue_blood_bag': 1}, 6.0), ({'scav_token': 1}, 15.0), ({'water_filter_adv': 1}, 6.0), ({'portable_water_purifier': 1}, 3.0), ({'large_purple_injector_fake': 1}, 25.0), ({'bottled_water_premium': 1}, 5.0), ({'heavy_handmade_pistol': 1}, 12.0), ({'handmade_pistol': 1}, 12.0), ({'cassette1d': 1}, 15.0), ({'kitchen_knife': 1}, 15.0), ({'combat_knife': 1}, 12.0), ({'glass_shard_shiv': 1}, 15.0), ({'kitchen_cleaver': 1}, 15.0), ({'hatchet': 1}, 12.0), ({'pipe_weapon': 1}, 15.0), ({'pink_injector': 1}, 25.0), ({'raw_meat': 1}, 25.0), ({'sec_keycard': 1}, 15.0), ({'med_keycard': 1}, 20.0), ({'eng_keycard': 1}, 20.0), ({'cmd_keycard': 1}, 10.0), ({'common_chemical': 1}, 75.0), ({'restricted_chemical': 1}, 50.0), ({'common_electronic': 1}, 33.0), ({'scratcher': 1}, 33.0), ({'processed_cheese': 1}, 25.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'dream_dust': 1}, 50.0), ({'dream_dust': 1}, 50.0), ({'dream_dust': 1}, 50.0), ({'dream_dust': 1}, 50.0), ({'zyanide_pill': 1}, 33.0), ({'zyanide_pill': 1}, 33.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'small_pistol_ammo': 1}, 33.0), ({'small_pistol_ammo_p': 1}, 33.0), ({'small_pistol_ammo_nl': 1}, 33.0), ({'heavy_pistol_ammo': 1}, 33.0), ({'heavy_pistol_ammo_p': 1}, 33.0), ({'heavy_pistol_ammo_nl': 1}, 33.0), ({'nudka': 1}, 25.0), ({'wine_yeast_red': 1}, 50.0), ({'wine_yeast_red': 1}, 50.0)]}

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
def getshapeidmap():
    next_sid, shape_key_to_id, shape_id_map, place_cache = 0, {}, {}, {}
    for k, raw in shapedict.items():
        key = tuple(tuple(row) for row in raw)
        if key not in shape_key_to_id: place_cache[next_sid], shape_key_to_id[key], next_sid = {}, next_sid, next_sid+1
        shape_id_map[k] = shape_key_to_id[key]
    item_cache = {k: place_cache[shape_id_map[k]] for k in shapedict}
    shapedict_candi = {k: unique_candidates(v) for k, v in shapedict.items()}
    shape_offsets = {}
    for k, shapes in shapedict_candi.items():
        sid = shape_id_map[k]
        if sid not in shape_offsets: shape_offsets[sid] = [(len(s), len(s[0]), [(i, j) for i in range(len(s)) for j in range(len(s[0])) if s[i][j]]) for s in shapes]
    shapes_candi = {k: shape_offsets[shape_id_map[k]] for k in shapedict}
    return (shape_id_map, item_cache, place_cache, shapes_candi)

start = time.time()
shape_id_map, item_cache, place_cache, shapes_candi = getshapeidmap()

def _can_place(box, shapes):
    for sh, sw, shape in shapes:
        for r in range(6 - sh): #len(box) - sh + 1
            for c in range(8 - sw): #len(box[0]) - sw + 1
                if not any(box[r + i][c + j] for i,j in shape):
                    return [(r+i,c+j) for i,j in shape]
    return []
def getrandomkindict(items_dict):
    if len(items_dict)==1: return (next(iter(items_dict)),0)
    keys, weights = list(items_dict.keys()), list(items_dict.values())
    idx = random.choices(range(len(keys)), weights=weights, k=1)[0]
    return (keys[idx], idx)

def openbox_one_forMC(prob_arr):
    mask, box, tags = 0, [[0] * 7 for _ in range(5)], []
    for i, (items_dict, p_pct) in enumerate(prob_arr,1):
        if random.random() < p_pct:
            k, idx = getrandomkindict(items_dict)
            cache = item_cache[k]
            if mask not in cache: cache[mask] = _can_place(box, shapes_candi[k])
            coords = cache[mask]
            if coords:
                tag = (idx << 8) | (i & 0xFF)
                tags.append(tag)
                for r, c in coords:
                    box[r][c] = tag
                    mask |= 1 << (r * 7 + c)
    return tags
def openbox_one(boxname):
    prob_arr, box, id_dict = box_prob.get(boxname, []), [[0] * 7 for _ in range(5)], []
    for i, (items_dict, p_pct) in enumerate(prob_arr,1):
        if random.random() < p_pct:
            k, idx = getrandomkindict(items_dict)
            coords = _can_place(box, shapes_candi[k])
            for r, c in coords: box[r][c] = (idx << 8) | (i & 0xFF)
            id_dict.append((i,idx,k))
    for id in id_dict: print(f"id {(id[1] << 8) | (id[0] & 0xFF):8d} | layer {id[0]:2d} | choice {id[1]:2d} | {id[2]:30s}")
    print(f"-----open one {boxname} box-----")
    print('\n'.join(['\t'.join('.' if v == 0 else str(v) for v in row) for row in box]))
    print('-' * 26)
def estimate_prob(boxname, N=100_000, maxlayer=1000):
    prob_arr = box_prob.get(boxname, [])[:maxlayer]
    seen = defaultdict(int)
    for _ in range(N): 
        for tag in openbox_one_forMC(prob_arr): seen[tag] += 1
    result = defaultdict(int)
    all_keys = [list(p[0].keys()) for p in prob_arr]
    for tag, c in seen.items():
        idx, layer = tag >> 8, tag & 0xFF
        result[(layer, all_keys[layer-1][idx])] += c
    print(f"cache len {sum([len(ca) for ca in place_cache.values()])}")
    v_count,result,layercount,lastlayer = 0,sorted(result.items()),[],0
    for (layer, item_id), c in result:
        pp = c / N
        if layer!=lastlayer:
            if len(layercount)>1: print(f"layer {lastlayer:2d} | ↑↑_this_layer_TOTAL{'='*11} | {sum(layercount):.4%}")
            layercount = [pp]
        else: layercount.append(pp)
        print(f"layer {layer:2d} | {item_id:30s} | {pp:.4%}")
        v_count, lastlayer = v_count + pp * valuedict[item_id], layer
    if len(layercount)>1: print(f"layer {lastlayer:2d} | ↑↑_this_layer_TOTAL{'='*11} | {sum(layercount):.4%}")
    print(f"total expect value = {v_count}")
    return result
def scanprop(boxname,Luck, N=100_000, maxlayer=1000):
    boxname_backup, state = box_prob[boxname][:maxlayer], []
    for i in range(Luck[0], Luck[1]):
        box_prob[boxname] = [(d, i/100*p/100) for d, p in boxname_backup]
        state.append((i-100,estimate_prob(boxname,N,maxlayer)[-1]))
    box_prob[boxname] = boxname_backup
    print(f"统计结果：物品次序 {state[0][1][0][0]} 物品名称 {state[0][1][0][1]} ")
    for s in state: print(f"幸运值 {s[0]} 概率值 {s[1][1] / N:.4%}")

# scanprop("eng",(144,147), N=4000_000_0, maxlayer=15)
mul = 1
box_prob = {k: [(d, mul*p/100) for d, p in v] for k, v in box_prob.items()}

# openbox_one("med")
# estimate_prob("med", N=10_000_0)
# openbox_one("eng")
# estimate_prob("eng", N=10_000_0) #, maxlayer=15
# openbox_one("sec")
# estimate_prob("sec", N=10_000_0)
# openbox_one("ser")
# estimate_prob("ser", N=10_000_0)
openbox_one("evi")
# estimate_prob("evi", N=10_000_000)

end = time.time()
print(f"运行时间：{(end - start)/60:.1f} 分钟")