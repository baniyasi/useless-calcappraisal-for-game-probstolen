# -*- coding: utf-8 -*-
import sys, random
from itertools import cycle
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QSpinBox, QPushButton,
    QGridLayout, QHBoxLayout, QVBoxLayout
)

# ---------------- 全局配置 ----------------
MAIN_COLOR = "#ADD8E6"      # 主色调：浅蓝色
DEFAULT_COLOR = "#000000"   # 九宫格默认色（符合主色调的黑色）
ROWS = 5                    # 7 行
COLS = 7                    # 5 列
BLOCK_SIZE = 64             # 每个色块的边长（正方形）


class Block(QWidget):
    def __init__(self, name="空", value=0, color=DEFAULT_COLOR, parent=None):
        super().__init__(parent)
        self.name = name
        self.value = value
        self.color = QColor(color)
        self.default_color = QColor(DEFAULT_COLOR)
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.setMouseTracking(True)
    def enterEvent(self, event):
        self.setToolTip(str(self.name))
        super().enterEvent(event)
    def leaveEvent(self, event):
        super().leaveEvent(event)
    def _cell(self, r, c):
        w, h = self.width(), self.height()
        xs = (0, int(w * 0.1), int(w * 0.9), w)   # 中间列占 80%
        ys = (0, int(h * 0.1), int(h * 0.9), h)   # 中间行占 80%
        return QRect(xs[c], ys[r], xs[c + 1] - xs[c], ys[r + 1] - ys[r])
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.default_color)
        painter.fillRect(self._cell(1, 1), self.color)
        if self.up is not None and self.up.value == self.value:
            painter.fillRect(self._cell(0, 1), self.color)
        if self.down is not None and self.down.value == self.value:
            painter.fillRect(self._cell(2, 1), self.color)
        if self.left is not None and self.left.value == self.value:
            painter.fillRect(self._cell(1, 0), self.color)
        if self.right is not None and self.right.value == self.value:
            painter.fillRect(self._cell(1, 2), self.color)
class MainWindow(QWidget):
    namedict = {'energy_credit_eng1': '能量电池', 'energy_credit_eng2': '能量电池', 'energy_credit_ext_eng': '能量电池（2型）', 'screwdriver': '螺丝刀', 'wire_cutter': '剪线钳', 'module_bay_expansion_kit': '模组舱扩建套件', 'module_extractor': '模组提取器（基础）', 'module_extractor_advanced': '模组提取器（高级）', 'turbo_booster': '一次性涡轮增压器', 'turbo_booster_adv': '高级涡轮增压器', 'energy_credit_breeder': '自充电能量电池', 'system_capped_neural_core': '神经核心模组（受限）', 'advanced_flux_agent': '助熔剂（高级）', 'furnace_module_blast': '熔炉模组（高炉）', 'eng_keycard': '一次性钥匙卡（工程）', 'system_module.20': '性能模组', 'system_module.21': '效率模组', 'system_module.22': '质量模组', 'node_medium': '节点（中）', 'system_module_2.25': '超频模组', 'system_module_2.26': '环保模组', 'system_module_2.27': '精炼模组', 'common_electronic': '电子元件（普通）', 'nuts_metal': '金属螺丝', 'flux_agent': '助熔剂', 'med_keycard': '一次性钥匙卡（医疗）', 'black_injector': '赛纳普斯注射器', 'large_purple_injector': '免疫宁注射器', 'surgery_tool': '外科手术工具套装', 'common_chemical': '化学用品（普通）', 'restricted_chemical': '化学用品（管制）', 'salve': '南丁格尔软膏', 'rubbing_alcohol': '医用酒精', 'energy_credit_med': '能量电池', 'bandage_item': '基础绷带', 'blood_bag': '血袋', 'blue_blood_bag': '一袋“蓝血”', 'galaxy_blend': '繁星果糊', 'hemostatic_bandage_item': '止血绷带', 'pink_injector': '奥克西莫注射器', 'phagimycin_pill': '噬菌霉素药片', 'fanta_pill': '芬太片', 'smelling_salt': '嗅盐', 'birth_control_pill': '避孕药', 'caffeine_pill': '咖啡因药片', 'glock_receiver': '哨兵3型', 'stun_gun': '“脉冲卫士”电击枪', 'tazer': '电击枪', 'energy_credit_sec': '能量电池', 'stun_baton': '眩晕警棍', 'combat_knife': '战斗匕首', 'sec_keycard': '一次性钥匙卡（治安）', 'flashbang_grenade': '闪光弹', 'flashlight': '手电筒', 'smoke_grenade': '烟雾弹', 'heavy_pistol_ammo': '10毫米弹药', 'heavy_pistol_ammo_p': '10毫米弹药（穿甲弹）', 'heavy_pistol_ammo_nl': '10毫米弹药（非致命）', 'topical_bandage_item': '外用药膏绷带', 'cassette1d': '磁带（损坏）', 'neuroactive_perfume': '“同步”神经活性香水', 'ser_keycard': '一次性钥匙卡（服务）', 'aquascan': '水质扫描仪', 'uv_filter': '紫外线灯', 'water_filter_adv': '高级滤水器', 'portable_water_purifier': '海德拉科技微型净水器', 'toilet_paper': '一卷厕纸', 'processed_cheese': '合成奶酪', 'toothpaste': '一支牙膏', 'water_filter': '滤水器', 'nutrifruit_seed_packet': '一包营养果种子', 'water_test_container': '水质检测试剂盒', 'water_tablet_container': '一瓶净水药片', 'energy_credit_ser1': '能量电池', 'energy_credit_ser2': '能量电池', 'box_cutter': '美工刀', 'kitchen_knife': '厨刀', 'hatchet': '短柄斧', 'paper_towel': '一卷纸巾', 'shampoo': '一瓶四合一洗涤剂', 'kotton_seed': '韧棉种子', 'hydroreed_seed': '水芦种子', 'nutrient_tablet': '水培营养片', 'energy_drink': '能量饮料', 'soda_red': '汽水', 'cat_bar': '猫咪巧克力棒', 'li_eat_snackbar': '轻食能量棒', 'red_beer': '红魔鬼啤酒', 'processed_milk': '碳酸代乳', 'processed_juice': '代糖果汁', 'processed_meat': '“泥炭”合成肉', 'zerochew': '一板零嚼', 'cup_noodle': '速食拉面', 'nudka': '努特加', 'beis_icecream': '贝氏优质香草冰淇淋', 'skincare_cream': '“永恒”焕活精华', 'bottled_water_premium': '瓶装泉水', 'pheromone_perfume': '“本源”费洛蒙香水', 'scav_token': '拾荒者信物', 'large_purple_injector_fake': '免疫宁注射器', 'heavy_handmade_pistol': '“铁铸10”重型手枪', 'handmade_pistol': '“巢火”紧凑型手枪', 'glass_shard_shiv': '玻璃刀', 'kitchen_cleaver': '切肉刀', 'pipe_weapon': '铅管', 'raw_meat': '生肉（标准）', 'cmd_keycard': '一次性钥匙卡（指挥）', 'scratcher': '刮刮乐彩票', 'unlicensed_phagimycin_pill': '无证噬菌霉素药片', 'dream_dust': '一小瓶“梦尘”', 'zyanide_pill': '氰化物药片', 'small_pistol_ammo': '.22 SR弹药', 'small_pistol_ammo_p': '.22 SR弹药（穿甲）', 'small_pistol_ammo_nl': '.22 SR弹药（非致命）', 'wine_yeast_red': '合成酵母'}
    shapedict = {'bandage_item': [[1], [1]], 'birth_control_pill': [[1]], 'black_injector': [[1, 1, 1, 1]], 'blood_bag': [[1, 1], [1, 1], [1, 1]], 'blue_blood_bag': [[1, 1], [1, 1], [1, 1]], 'caffeine_pill': [[1]], 'common_chemical': [[1, 1, 1], [1, 1, 1]], 'energy_credit_med': [[1], [1]], 'energy_credit_ser1': [[1], [1]], 'energy_credit_ser2': [[1], [1]], 'fanta_pill': [[1]], 'galaxy_blend': [[1, 1], [1, 1]], 'hemostatic_bandage_item': [[1], [1]], 'large_purple_injector': [[1, 1, 1, 1]], 'med_keycard': [[1, 1], [1, 1]], 'phagimycin_pill': [[1]], 'pink_injector': [[1, 1, 1, 1]], 'restricted_chemical': [[1, 1, 1], [1, 1, 1]], 'rubbing_alcohol': [[1], [1]], 'salve': [[1, 1], [1, 1]], 'smelling_salt': [[1]], 'surgery_tool': [[1, 1, 1, 1], [1, 1, 1, 1]], 'advanced_flux_agent': [[1, 1], [1, 1]], 'common_electronic': [[1, 1, 1], [1, 1, 1]], 'energy_credit_breeder': [[1], [1]], 'energy_credit_eng1': [[1], [1]], 'energy_credit_eng2': [[1], [1]], 'energy_credit_ext_eng': [[1], [1]], 'eng_keycard': [[1, 1], [1, 1]], 'flux_agent': [[1]], 'furnace_module_blast': [[1], [1], [1], [1]], 'module_bay_expansion_kit': [[1, 1], [1, 1]], 'module_extractor': [[1, 1], [1, 1], [1, 1]], 'module_extractor_advanced': [[1, 1], [1, 1], [1, 1]], 'node_medium': [[1], [1]], 'nuts_metal': [[1, 1], [1, 1]], 'screwdriver': [[1], [1], [1]], 'system_capped_neural_core': [[1, 1], [1, 1]], 'turbo_booster': [[1, 1, 1], [1, 1, 1]], 'turbo_booster_adv': [[1, 1, 1], [1, 1, 1]], 'wire_cutter': [[1], [1], [1]], 'system_module': [[1, 1], [1, 1]], 'system_module_2': [[1, 1], [1, 1]], 'system_module_l': [[1, 1, 1], [0, 0, 1]], 'system_module_t': [[0, 1], [1, 1], [0, 1]], 'system_module_c': [[1, 1], [0, 1]], 'system_module_2_s': [[1, 1], [0, 1], [1, 1]], 'system_module_2_h': [[1, 1], [1, 1], [0, 1]], 'combat_knife': [[1, 1, 1, 1, 1]], 'energy_credit_sec': [[1], [1]], 'flashbang_grenade': [[1], [1]], 'flashlight': [[1, 1, 1]], 'glock_receiver': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'heavy_pistol_ammo': [[1]], 'heavy_pistol_ammo_nl': [[1]], 'heavy_pistol_ammo_p': [[1]], 'sec_keycard': [[1, 1], [1, 1]], 'smoke_grenade': [[1], [1]], 'stun_baton': [[1, 1, 1, 1, 1, 1]], 'stun_gun': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'tazer': [[1, 1], [1, 1], [1, 1]], 'topical_bandage_item': [[1], [1]], 'aquascan': [[1, 1], [1, 1], [1, 1]], 'beis_icecream': [[1, 1, 1], [1, 1, 1]], 'box_cutter': [[1, 1, 1, 1]], 'cassette1d': [[1, 1], [1, 1]], 'cat_bar': [[1, 1], [1, 1]], 'cup_noodle': [[1, 1, 1], [1, 1, 1]], 'energy_credit': [[1], [1]], 'energy_drink': [[1], [1]], 'hatchet': [[1, 1, 1, 1], [0, 0, 1, 1]], 'hydroreed_seed': [[1]], 'kitchen_knife': [[1, 1, 1, 1, 1]], 'kotton_seed': [[1]], 'li_eat_snackbar': [[1, 1, 1]], 'neuroactive_perfume': [[1, 1], [1, 1]], 'nudka': [[1, 1], [1, 1], [1, 1], [1, 1]], 'nutrient_tablet': [[1]], 'nutrifruit_seed_packet': [[1, 1], [1, 1]], 'paper_towel': [[1, 1], [1, 1], [1, 1]], 'portable_water_purifier': [[1, 1], [1, 1]], 'processed_cheese': [[1, 1], [1, 1]], 'processed_juice': [[1, 1], [1, 1], [1, 1]], 'processed_meat': [[1, 1], [1, 1]], 'processed_milk': [[1, 1], [1, 1], [1, 1]], 'red_beer': [[1], [1], [1], [1]], 'ser_keycard': [[1, 1], [1, 1]], 'shampoo': [[1, 1], [1, 1], [1, 1]], 'soda_red': [[1], [1]], 'toilet_paper': [[1, 1], [1, 1]], 'toothpaste': [[1, 1, 1]], 'uv_filter': [[1, 1, 1, 1, 1]], 'water_filter': [[1], [1]], 'water_filter_adv': [[1], [1], [1]], 'water_tablet_container': [[1], [1], [1]], 'water_test_container': [[1], [1]], 'zerochew': [[1]], 'bottled_water_premium': [[1], [1], [1], [1]], 'cmd_keycard': [[1, 1], [1, 1]], 'dream_dust': [[1]], 'glass_shard_shiv': [[1, 1, 1]], 'handmade_pistol': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'heavy_handmade_pistol': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0]], 'kitchen_cleaver': [[1, 1, 1, 1, 1], [0, 0, 1, 1, 1]], 'large_purple_injector_fake': [[1, 1, 1, 1]], 'pheromone_perfume': [[1, 1], [1, 1]], 'pipe_weapon': [[1, 1, 1, 1, 1], [0, 0, 0, 0, 1]], 'raw_meat': [[1, 1, 1], [1, 1, 1]], 'scav_token': [[1], [1]], 'scratcher': [[1, 1], [1, 1]], 'skincare_cream': [[1, 1], [1, 1]], 'small_pistol_ammo': [[1]], 'small_pistol_ammo_nl': [[1]], 'small_pistol_ammo_p': [[1]], 'unlicensed_phagimycin_pill': [[1]], 'wine_yeast_red': [[1], [1]], 'zyanide_pill': [[1]]}
    valuedict = {'med_keycard': 75.0, 'black_injector': 350, 'large_purple_injector': 160, 'surgery_tool': 200, 'common_chemical': 50.0, 'restricted_chemical': 100.0, 'salve': 80, 'rubbing_alcohol': 35, 'bandage_item': 8, 'blood_bag': 33, 'blue_blood_bag': 250.0, 'galaxy_blend': 25.0, 'hemostatic_bandage_item': 16, 'pink_injector': 50.0, 'phagimycin_pill': 25, 'fanta_pill': 12.0, 'smelling_salt': 15, 'birth_control_pill': 15, 'caffeine_pill': 10.0, 'energy_credit_med': 47.5, 'energy_credit_eng1': 110.0, 'energy_credit_eng2': 60.0, 'energy_credit_ext_eng': 92.5, 'screwdriver': 25.0, 'wire_cutter': 40.0, 'module_bay_expansion_kit': 150.0, 'module_extractor': 100.0, 'module_extractor_advanced': 350.0, 'turbo_booster': 35.0, 'turbo_booster_adv': 300.0, 'energy_credit_breeder': 500.0, 'system_capped_neural_core': 250.0, 'advanced_flux_agent': 300.0, 'furnace_module_blast': 150.0, 'eng_keycard': 75.0, 'system_module': 75, 'system_module_c': 64, 'system_module_l': 69, 'system_module_t': 69, 'system_module_2': 105, 'system_module_2_s': 120, 'system_module_2_h': 120, 'node_medium': 50.0, 'common_electronic': 33.0, 'nuts_metal': 14.0, 'flux_agent': 4.0, 'glock_receiver': 200.0, 'stun_gun': 250.0, 'tazer': 100.0, 'energy_credit_sec': 85.0, 'stun_baton': 165.0, 'combat_knife': 75.0, 'sec_keycard': 100.0, 'flashbang_grenade': 75.0, 'flashlight': 40.0, 'smoke_grenade': 60.0, 'heavy_pistol_ammo': 30.0, 'heavy_pistol_ammo_p': 36.0, 'heavy_pistol_ammo_nl': 24.0, 'topical_bandage_item': 16.0, 'cassette1d': 35.0, 'neuroactive_perfume': 150.0, 'ser_keycard': 40.0, 'aquascan': 200.0, 'uv_filter': 150.0, 'water_filter_adv': 250.0, 'portable_water_purifier': 225.0, 'toilet_paper': 25.0, 'processed_cheese': 20.0, 'toothpaste': 15.0, 'water_filter': 25.0, 'nutrifruit_seed_packet': 91.0, 'water_test_container': 31.0, 'water_tablet_container': 55.0, 'energy_credit_ser1': 110.0, 'energy_credit_ser2': 43.0, 'box_cutter': 28.0, 'kitchen_knife': 35.0, 'hatchet': 45.0, 'paper_towel': 35.0, 'shampoo': 30.0, 'kotton_seed': 20.0, 'hydroreed_seed': 20.0, 'nutrient_tablet': 5.0, 'energy_drink': 18.0, 'soda_red': 15.0, 'cat_bar': 15.0, 'li_eat_snackbar': 17.0, 'red_beer': 18.0, 'processed_milk': 16.0, 'processed_juice': 14.0, 'processed_meat': 25.0, 'zerochew': 8.0, 'cup_noodle': 20.0, 'nudka': 85.0, 'beis_icecream': 40.0, 'skincare_cream': 500.0, 'bottled_water_premium': 325.0, 'pheromone_perfume': 200.0, 'scav_token': 100.0, 'large_purple_injector_fake': 40.0, 'heavy_handmade_pistol': 160.0, 'handmade_pistol': 120.0, 'glass_shard_shiv': 8.0, 'kitchen_cleaver': 50.0, 'pipe_weapon': 15.0, 'raw_meat': 120.0, 'cmd_keycard': 125.0, 'scratcher': 20.0, 'unlicensed_phagimycin_pill': 5.0, 'dream_dust': 18.0, 'zyanide_pill': 33.0, 'small_pistol_ammo': 20.0, 'small_pistol_ammo_p': 26.0, 'small_pistol_ammo_nl': 14.0, 'wine_yeast_red': 8.0}
    box_prob = {"医疗箱": [({'med_keycard': 1}, 50.0), ({'med_keycard': 1}, 50.0), ({'black_injector': 1}, 33.0), ({'black_injector': 1}, 33.0), ({'large_purple_injector': 1}, 100.0), ({'surgery_tool': 1}, 25.0), ({'common_chemical': 1}, 75.0), ({'restricted_chemical': 1}, 50.0), ({'common_chemical': 1}, 50.0), ({'salve': 1}, 75.0), ({'rubbing_alcohol': 1}, 75.0), ({'energy_credit_med': 1}, 100.0), ({'bandage_item': 1}, 75.0), ({'bandage_item': 1}, 75.0), ({'bandage_item': 1}, 50.0), ({'bandage_item': 1}, 50.0), ({'blood_bag': 1}, 50.0), ({'blue_blood_bag': 1}, 25.0), ({'galaxy_blend': 1}, 33.0), ({'galaxy_blend': 1}, 33.0), ({'hemostatic_bandage_item': 1}, 75.0), ({'hemostatic_bandage_item': 1}, 75.0), ({'pink_injector': 1}, 50.0), ({'pink_injector': 1}, 33.0), ({'pink_injector': 1}, 33.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'phagimycin_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'smelling_salt': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'birth_control_pill': 1}, 50.0), ({'caffeine_pill': 1}, 50.0), ({'caffeine_pill': 1}, 50.0), ({'caffeine_pill': 1}, 50.0)],
                "工程箱": [({'energy_credit_eng1': 1}, 100.0), ({'energy_credit_eng2': 1}, 50.0), ({'energy_credit_ext_eng': 1}, 100.0), ({'screwdriver': 1}, 66.0), ({'wire_cutter': 1}, 66.0), ({'module_bay_expansion_kit': 1}, 25.0), ({'module_bay_expansion_kit': 1}, 25.0), ({'module_extractor': 1}, 25.0), ({'module_extractor': 1}, 25.0), ({'module_extractor_advanced': 1}, 12.0), ({'turbo_booster': 1}, 25.0), ({'turbo_booster': 1}, 25.0), ({'turbo_booster_adv': 1}, 8.0), ({'energy_credit_breeder': 1}, 12.0), ({'system_capped_neural_core': 1}, 4.0), ({'advanced_flux_agent': 1}, 12.0), ({'furnace_module_blast': 1}, 15.0), ({'eng_keycard': 1}, 50.0), ({'eng_keycard': 1}, 50.0), ({'system_module':25,'system_module_c':25,'system_module_t':25,'system_module_l':26}, 50.0), ({'system_module':25,'system_module_c':25,'system_module_t':25,'system_module_l':26}, 50.0), ({'system_module':25,'system_module_c':25,'system_module_t':25,'system_module_l':26}, 50.0), ({'node_medium': 1}, 50.0), ({'node_medium': 1}, 50.0), ({'system_module_2':33,'system_module_2_h':34,'system_module_2_s':34}, 33.0), ({'system_module_2':33,'system_module_2_h':34,'system_module_2_s':34}, 33.0), ({'system_module_2':33,'system_module_2_h':34,'system_module_2_s':34}, 33.0), ({'common_electronic': 1}, 33.0), ({'common_electronic': 1}, 33.0), ({'common_electronic': 1}, 33.0), ({'nuts_metal': 1}, 33.0), ({'nuts_metal': 1}, 33.0), ({'flux_agent': 1}, 50.0), ({'flux_agent': 1}, 50.0), ({'flux_agent': 1}, 50.0)],
                "治安箱": [({'glock_receiver': 1}, 20.0), ({'stun_gun': 1}, 20.0), ({'tazer': 1}, 33.0), ({'energy_credit_sec': 1}, 100.0), ({'stun_baton': 1}, 35.0), ({'stun_baton': 1}, 35.0), ({'combat_knife': 1}, 35.0), ({'combat_knife': 1}, 35.0), ({'pink_injector': 1}, 50.0), ({'pink_injector': 1}, 50.0), ({'pink_injector': 1}, 50.0), ({'sec_keycard': 1}, 50.0), ({'sec_keycard': 1}, 50.0), ({'flashbang_grenade': 1}, 50.0), ({'flashbang_grenade': 1}, 50.0), ({'flashlight': 1}, 33.0), ({'smoke_grenade': 1}, 50.0), ({'smoke_grenade': 1}, 50.0), ({'heavy_pistol_ammo': 1}, 55.0), ({'heavy_pistol_ammo_p': 1}, 55.0), ({'heavy_pistol_ammo_nl': 1}, 55.0), ({'heavy_pistol_ammo': 1}, 55.0), ({'heavy_pistol_ammo_p': 1}, 55.0), ({'heavy_pistol_ammo_nl': 1}, 55.0), ({'topical_bandage_item': 1}, 55.0), ({'topical_bandage_item': 1}, 55.0)],
                "服务箱": [({'cassette1d': 1}, 20.0), ({'neuroactive_perfume': 1}, 8.0), ({'ser_keycard': 1}, 66.0), ({'ser_keycard': 1}, 33.0), ({'aquascan': 1}, 15.0), ({'uv_filter': 1}, 15.0), ({'water_filter_adv': 1}, 12.0), ({'portable_water_purifier': 1}, 8.0), ({'toilet_paper': 1}, 50.0), ({'toilet_paper': 1}, 33.0), ({'toilet_paper': 1}, 15.0), ({'processed_cheese': 1}, 33.0), ({'toothpaste': 1}, 75.0), ({'water_filter': 1}, 75.0), ({'water_filter': 1}, 50.0), ({'water_filter': 1}, 33.0), ({'nutrifruit_seed_packet': 1}, 33.0), ({'water_test_container': 1}, 50.0), ({'water_tablet_container': 1}, 50.0), ({'energy_credit_ser1': 1}, 75.0), ({'energy_credit_ser2': 1}, 25.0), ({'box_cutter': 1}, 33.0), ({'kitchen_knife': 1}, 33.0), ({'hatchet': 1}, 25.0), ({'paper_towel': 1}, 33.0), ({'paper_towel': 1}, 33.0), ({'shampoo': 1}, 33.0), ({'shampoo': 1}, 33.0), ({'caffeine_pill': 1}, 33.0), ({'caffeine_pill': 1}, 33.0), ({'caffeine_pill': 1}, 33.0), ({'kotton_seed': 1}, 75.0), ({'kotton_seed': 1}, 50.0), ({'kotton_seed': 1}, 33.0), ({'hydroreed_seed': 1}, 75.0), ({'hydroreed_seed': 1}, 50.0), ({'module_bay_expansion_kit': 1}, 25.0), ({'nutrient_tablet': 1}, 50.0), ({'nutrient_tablet': 1}, 50.0), ({'nutrient_tablet': 1}, 50.0),
                        ({'galaxy_blend':90,'energy_drink':90,'soda_red':90,'cat_bar':90,'li_eat_snackbar':90,'red_beer':90,'processed_milk':90,'processed_juice':90,'processed_meat':90,'zerochew':90,'cup_noodle':90,'nudka':55,'beis_icecream':55}, 100),({'galaxy_blend':90,'energy_drink':90,'soda_red':90,'cat_bar':90,'li_eat_snackbar':90,'red_beer':90,'processed_milk':90,'processed_juice':90,'processed_meat':90,'zerochew':90,'cup_noodle':90,'nudka':55,'beis_icecream':55}, 100)],
                "物证柜": [({'skincare_cream': 1}, 4.0), ({'bottled_water_premium': 1}, 6.0), ({'neuroactive_perfume': 1}, 4.0), ({'pheromone_perfume': 1}, 6.0), ({'turbo_booster_adv': 1}, 6.0), ({'blue_blood_bag': 1}, 6.0), ({'scav_token': 1}, 15.0), ({'water_filter_adv': 1}, 6.0), ({'portable_water_purifier': 1}, 3.0), ({'large_purple_injector_fake': 1}, 25.0), ({'bottled_water_premium': 1}, 5.0), ({'heavy_handmade_pistol': 1}, 12.0), ({'handmade_pistol': 1}, 12.0), ({'cassette1d': 1}, 15.0), ({'kitchen_knife': 1}, 15.0), ({'combat_knife': 1}, 12.0), ({'glass_shard_shiv': 1}, 15.0), ({'kitchen_cleaver': 1}, 15.0), ({'hatchet': 1}, 12.0), ({'pipe_weapon': 1}, 15.0), ({'pink_injector': 1}, 25.0), ({'raw_meat': 1}, 25.0), ({'sec_keycard': 1}, 15.0), ({'med_keycard': 1}, 20.0), ({'eng_keycard': 1}, 20.0), ({'cmd_keycard': 1}, 10.0), ({'common_chemical': 1}, 75.0), ({'restricted_chemical': 1}, 50.0), ({'common_electronic': 1}, 33.0), ({'scratcher': 1}, 33.0), ({'processed_cheese': 1}, 25.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'unlicensed_phagimycin_pill': 1}, 33.0), ({'dream_dust': 1}, 50.0), ({'dream_dust': 1}, 50.0), ({'dream_dust': 1}, 50.0), ({'dream_dust': 1}, 50.0), ({'zyanide_pill': 1}, 33.0), ({'zyanide_pill': 1}, 33.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'fanta_pill': 1}, 50.0), ({'small_pistol_ammo': 1}, 33.0), ({'small_pistol_ammo_p': 1}, 33.0), ({'small_pistol_ammo_nl': 1}, 33.0), ({'heavy_pistol_ammo': 1}, 33.0), ({'heavy_pistol_ammo_p': 1}, 33.0), ({'heavy_pistol_ammo_nl': 1}, 33.0), ({'nudka': 1}, 25.0), ({'wine_yeast_red': 1}, 50.0), ({'wine_yeast_red': 1}, 50.0)]}
    COLOR_PALETTE = ["#4F9DDE", "#5FBF9F", "#8FBF4F", "#E9C46A", "#E07A5F", "#9B8EC4", "#E8A0BF", "#6BB7C4"]
    def __init__(self):
        super().__init__()
        self.setWindowTitle("深空当铺物资箱开箱模拟器")
        self.blocks = []          # 7 x 5 的 Block 二维列表
        self._init_ui()
        self._build_grid()
        self.refresh_colors()     # 初始化后刷新一次颜色
    def _init_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {MAIN_COLOR};
                color: #10333f;
                font-size: 14px;
            }}
            QLabel {{ background: transparent; }}
            QPushButton {{
                background-color: #8FD0E8;
                border: 1px solid #4E9CBB;
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
            }}
            QPushButton:hover  {{ background-color: #A8DDF0; }}
            QPushButton:pressed{{ background-color: #6FBDD9; }}
            QComboBox, QSpinBox {{
                background-color: #EAF7FC;
                border: 1px solid #4E9CBB;
                border-radius: 4px;
                padding: 3px 6px;
                min-width: 120px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #EAF7FC;
                selection-background-color: #8FD0E8;
            }}
        """)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("物资箱类型："))
        self.box_type_combo = QComboBox()
        self.box_type_combo.addItems(["工程箱", "治安箱", "医疗箱", "服务箱", "物证柜"])
        row1.addWidget(self.box_type_combo)
        row1.addStretch()
        main_layout.addLayout(row1)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("幸运值："))
        self.luck_spin = QSpinBox()
        self.luck_spin.setRange(-100, 100)
        self.luck_spin.setValue(0)
        row2.addWidget(self.luck_spin)
        row2.addStretch()
        main_layout.addLayout(row2)
        row3 = QHBoxLayout()
        self.open_btn = QPushButton("打开箱子")
        self.open_btn.clicked.connect(self.open_box)
        self.clear_btn = QPushButton("清空箱子")
        self.clear_btn.clicked.connect(self.clear_boxes)
        row3.addWidget(self.open_btn)
        row3.addWidget(self.clear_btn)
        row3.addStretch()
        main_layout.addLayout(row3)
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        main_layout.addWidget(self.grid_container, alignment=Qt.AlignCenter)
    @staticmethod
    def _rotate90(m): return [list(row) for row in zip(*m[::-1])]
    @staticmethod
    def _mirror_lr(m): return [row[::-1] for row in m]
    def _candidates(self, item):
        shapes, cur = [], [list(row) for row in item]
        for _ in range(4):
            shapes.append(cur)
            cur = self._rotate90(cur)
        cur = self._mirror_lr(item)
        for _ in range(4):
            shapes.append(cur)
            cur = self._rotate90(cur)
        return shapes
    def unique_candidates(self, item):
        seen, result = set(), []
        for shape in self._candidates(item):
            key = tuple(tuple(row) for row in shape)
            if key not in seen:
                seen.add(key)
                result.append(shape)
        return result
    def getshapeidmap(self):
        next_sid, shape_key_to_id, shape_id_map, place_cache = 0, {}, {}, {}
        for k, raw in self.shapedict.items():
            key = tuple(tuple(row) for row in raw)
            if key not in shape_key_to_id: place_cache[next_sid], shape_key_to_id[key], next_sid = {}, next_sid, next_sid+1
            shape_id_map[k] = shape_key_to_id[key]
        shapedict_candi = {k: self.unique_candidates(v) for k, v in self.shapedict.items()}
        shape_offsets = {}
        for k, shapes in shapedict_candi.items():
            sid = shape_id_map[k]
            if sid not in shape_offsets: shape_offsets[sid] = [(len(s), len(s[0]), [(i, j) for i in range(len(s)) for j in range(len(s[0])) if s[i][j]]) for s in shapes]
        shapes_candi = {k: shape_offsets[shape_id_map[k]] for k in self.shapedict}
        return shapes_candi
    @staticmethod
    def _can_place(box, shapes):
        for sh, sw, shape in shapes:
            for r in range(6 - sh): #len(box) - sh + 1
                for c in range(8 - sw): #len(box[0]) - sw + 1
                    if not any(box[r + i][c + j] for i,j in shape):
                        return [(r+i,c+j) for i,j in shape]
        return []
    @staticmethod
    def getrandomkindict(items_dict):
        if len(items_dict)==1: return (next(iter(items_dict)),0)
        keys, weights = list(items_dict.keys()), list(items_dict.values())
        idx = random.choices(range(len(keys)), weights=weights, k=1)[0]
        return (keys[idx], idx)
    def _build_grid(self):
        self.blocks = []
        for r in range(ROWS):
            row_blocks = []
            for c in range(COLS):
                blk = Block()
                blk.setFixedSize(BLOCK_SIZE, BLOCK_SIZE)
                self.grid_layout.addWidget(blk, r, c)
                row_blocks.append(blk)
            self.blocks.append(row_blocks)
        for r in range(ROWS):
            for c in range(COLS):
                blk = self.blocks[r][c]
                blk.up    = self.blocks[r - 1][c] if r > 0 else None
                blk.down  = self.blocks[r + 1][c] if r < ROWS - 1 else None
                blk.left  = self.blocks[r][c - 1] if c > 0 else None
                blk.right = self.blocks[r][c + 1] if c < COLS - 1 else None
    def refresh_colors(self):
        for row_blocks in self.blocks:
            for blk in row_blocks:
                blk.update()
    def build_color_dict(self, id_dict):
        unique_values = sorted(set(id_dict.values()), key=str)  # key=str 兼容混合类型
        color_dict = {}
        for value, hex_color in zip(unique_values, cycle(self.COLOR_PALETTE)):
            color_dict[value] = QColor(hex_color)
        return color_dict
    def getname(self, id, layer):
        if self.namedict.get(id,""): return self.namedict[id] 
        if id in ['system_module', 'system_module_c', 'system_module_l', 'system_module_t']: return self.namedict[f"system_module.{layer}"]
        if id in ['system_module_2', 'system_module_2_s', 'system_module_2_h']: return self.namedict[f"system_module_2.{layer}"]
    def open_box(self):
        mul, boxname = self.luck_spin.value()/100+1, self.box_type_combo.currentText()
        prob_arr, box, id_dict = [(d, mul*p/100) for d, p in self.box_prob.get(boxname, [])], [[0] * 7 for _ in range(5)], {}
        shapes_candi = self.getshapeidmap()
        for i, (items_dict, p_pct) in enumerate(prob_arr,1):
            if random.random() < p_pct:
                k, idx = self.getrandomkindict(items_dict)
                coords = self._can_place(box, shapes_candi[k])
                for r, c in coords: box[r][c] = (idx << 8) | (i & 0xFF)
                if coords: id_dict[(idx << 8) | (i & 0xFF)] = k
        color_dict = self.build_color_dict(id_dict)
        for r in range(ROWS):
            for c in range(COLS):
                blk, tag = self.blocks[r][c], box[r][c]
                if tag:
                    blk.value, blk.color = tag, color_dict[id_dict[tag]]
                    blk.name = f"{self.getname(id_dict[tag],tag & 0xFF)}\n{self.valuedict[id_dict[tag]]} 信用点"
                else: blk.name, blk.value, blk.color = "空", 0, QColor(DEFAULT_COLOR)
        self.refresh_colors()
    def clear_boxes(self):
        for row_blocks in self.blocks:
            for blk in row_blocks:
                blk.name, blk.value, blk.color = "空", 0, QColor(DEFAULT_COLOR)
        self.refresh_colors()
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.adjustSize()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()