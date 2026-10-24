#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NadirGimbal_R2 原理图静态校验（本机无 KiCad，用格式严格性代替 ERC）：
1. 每个 .kicad_sch 括号配平、含 (kicad_sch 头与 (version 20230121)
2. 全部文件 uuid 全局唯一
3. .kicad_pro 可被 JSON 解析
4. 关键网络标签在预期文件中存在
"""
import os, re, json, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kicad")
errors, warnings = [], []

SCHS = ["NadirGimbal_R2.kicad_sch", "pwr.kicad_sch", "drv.kicad_sch",
        "comms.kicad_sch", "enc_roll.kicad_sch", "enc_pitch.kicad_sch",
        "imu_base.kicad_sch", "imu_cam.kicad_sch"]

all_uuids = {}
for name in SCHS:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        errors.append(f"缺少文件 {name}")
        continue
    txt = open(p, encoding="utf-8").read()
    # 1. 括号配平（去掉字符串字面量后再数）
    stripped = re.sub(r'"(?:[^"\\]|\\.)*"', '""', txt)
    bal = 0
    for i, ch in enumerate(stripped):
        if ch == '(':
            bal += 1
        elif ch == ')':
            bal -= 1
            if bal < 0:
                errors.append(f"{name}: 第{i}字符附近出现多余右括号")
                break
    if bal != 0:
        errors.append(f"{name}: 括号不配平，净剩 {bal}")
    if "(kicad_sch" not in txt:
        errors.append(f"{name}: 缺少 (kicad_sch 头")
    if "(version 20230121)" not in txt:
        warnings.append(f"{name}: 未找到 version 20230121 标记")
    # 2. uuid 唯一性
    for m in re.finditer(r'\(uuid ([0-9a-f-]{36})\)', txt):
        u = m.group(1)
        if u in all_uuids:
            errors.append(f"{name}: uuid {u} 与 {all_uuids[u]} 重复")
        else:
            all_uuids[u] = name

# 3. 工程文件 JSON
try:
    json.load(open(os.path.join(ROOT, "NadirGimbal_R2.kicad_pro"), encoding="utf-8"))
except Exception as e:
    errors.append(f"kicad_pro 解析失败: {e}")

# 4. 关键网络标签抽查
EXPECT = {
    "pwr.kicad_sch": ["VM", "3V3", "3V3_ANA", "GND", "VM_J1", "VM_FUSED", "VM_SENSE"],
    "drv.kicad_sch": ["PWM_M1_U", "PWM_M1_V", "PWM_M1_W", "PWM_M2_U", "PWM_M2_V", "PWM_M2_W",
                      "DRV1_nSCS", "DRV2_nSCS", "I1_A", "I1_B", "I2_A", "I2_B",
                      "SPI3_MISO", "SPI3_MOSI", "SPI3_SCK", "VM"],
    "comms.kicad_sch": ["MAVLINK_TX", "MAVLINK_RX", "USB_DP", "USB_DM", "FC_PWM_ROLL", "FC_PWM_PITCH",
                        "IMU_BASE_INT", "IMU_CAM_INT", "ENC_ROLL_nCS", "ENC_PITCH_nCS",
                        "IMU_BASE_nCS", "IMU_CAM_nCS", "SPI1_MISO", "SPI1_MOSI", "SPI2_MISO",
                        "SWDIO", "SWCLK", "NRST"],
    "enc_roll.kicad_sch": ["CSn", "SCK", "MISO", "MOSI"],
    "enc_pitch.kicad_sch": ["CSn", "SCK", "MISO", "MOSI"],
    "imu_base.kicad_sch": ["CSn", "SCK", "MISO", "MOSI", "INT1"],
    "imu_cam.kicad_sch": ["CSn", "SCK", "MISO", "MOSI", "INT1"],
}
for name, nets in EXPECT.items():
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        continue
    txt = open(p, encoding="utf-8").read()
    for n in nets:
        # 全局标签 / 层级标签 / 局部标签三种形态
        if not re.search(rf'\((?:global|hierarchical|label) [^)]*"{re.escape(n)}"', txt) and \
           f'"{n}"' not in txt:
            errors.append(f"{name}: 未找到网络 {n}")

print(f"校验文件 {len(SCHS)} 个，收集 uuid {len(all_uuids)} 个")
for w in warnings:
    print("WARN:", w)
if errors:
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)
print("全部通过 ✔（括号配平 / uuid 唯一 / JSON 可解析 / 关键网络齐）")
print("注意：本机无 KiCad，未做 ERC；请在 KiCad 7+ 中打开后运行 检查(ERC)。")
