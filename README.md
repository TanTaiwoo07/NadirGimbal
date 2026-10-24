# NadirGimbal_R2 KiCad 原理图工程

Nadir 双轴（横滚+俯仰）云台主控：**STM32G431RBT6 + 双 DRV8316R + 双 AS5048A + 双 ICM-42688-P**。
目标：相机始终稳定朝正下方，机体偏航/偏摆全防住，为 AR0234 下视相机提供稳定采集平台。

## 目录结构

```
NadirGimbal_R2/
├── kicad/
│   ├── NadirGimbal_R2.kicad_sch   根图：MCU + 四块卫星小版接口
│   ├── pwr.kicad_sch              电源：12V 输入保护 + TPS54202 3V3
│   ├── drv.kicad_sch              双 DRV8316R 电机驱动
│   ├── comms.kicad_sch            通信：MAVLINK/FC PWM/USB/SWD/卫星板排线
│   ├── enc_roll.kicad_sch         编码器小版 ×1（横滚）
│   ├── enc_pitch.kicad_sch        编码器小版 ×1（俯仰）
│   ├── imu_base.kicad_sch         IMU 小版 ×1（机体侧）
│   ├── imu_cam.kicad_sch          IMU 小版 ×1（相机侧）
│   └── NadirGimbal_R2.kicad_pro   工程文件
├── scripts/
│   ├── gen_sch.py                 原理图生成脚本（源数据可改，改完重跑即再生成）
│   └── validate.py                静态校验（括号配平 / uuid 唯一 / 关键网络）
└── docs/
    ├── BOM.csv                    物料清单
    ├── 引脚分配与NUCLEO对照表.md    64 脚全表 + NUCLEO-G431RB 排针对照
    └── 采购清单.md                过渡期 / 打样两方案
```

## 打开方式

1. 安装 **KiCad 7 或更新版本**（https://www.kicad.org）
2. 打开 `kicad/NadirGimbal_R2.kicad_pro`
3. **第一件事：运行 检查 → ERC**。本工程由脚本生成，开发机上没有 KiCad，只做过格式级校验（括号配平、uuid 全局唯一、8 张图关键网络齐全），未做 ERC。

## 关键设计决策

- **3xPWM 模式**：两路电机各 3 根 PWM（TIM1_CH1/2/3=PA8/9/10，TIM8_CH1/2/3=PC6/7/8），INLx 经 0Ω 上拉 3V3。放弃互补输出的原因是 TIM8 的 CH1N 只有 PA7 可用，与 SPI1_MOSI 冲突。
- **DRV 内置 buck 默认禁用**：SPI 配置 BUCK_DIS=1，FB_BK/SW_BK 悬空；若启用需按图注释二选一改动，与 TPS54202 不要同时用。
- **双 DRV 共用 SPI3**：两颗 SDO 并到同一 MISO（各自 nSCS 高电平时 SDO 高阻，数据手册已确认），省一根引脚。
- **4 块卫星小版**：编码器/IMU 各两块小版经 JST-SH 排线连主控，方便贴在云台不同运动层上；IMU 的 INT1 走 7pin 排线。
- **电源链**：6S → 独立 BEC 12V → J1 → 5A 保险丝 → P-MOS 反接保护 → SMBJ15A TVS → VM；TPS54202 降压 3V3；磁珠分出 3V3_ANA 给 VDDA/VREF+。

## 打样前必须人工复核的 3 件事

1. **TPS54202 SOT-23-6 引脚号**：符号里引脚号写的是功能名（GND/SW/BST/FB/EN/VIN），画 PCB 封装时必须按 TI 数据手册核对 1–6 脚的实际顺序。
2. **DRV8316R VQFN-40 散热焊盘**：符号内 1EP 已带，PCB 封装用带 EP3.1×5.1 的版本并打过孔到地平面。
3. **ERC + 网络高亮**：在 KiCad 里逐个点亮 PWM_M1_U、SPI3_MISO、VM_SENSE 等网络，确认跨页连接正确。

## Bring-up 顺序（先 NUCLEO 后定制板）

1. **NUCLEO + 成品模块**（对照 `docs/引脚分配与NUCLEO对照表.md` 跳线）：
   - 注意 SB21（USER 键默认接 PA0=FC_PWM_ROLL）与 SB6（LD2 默认接 PA5=SPI1_SCK），验证对应功能前断开。
   - PA2/PA3 默认已接 ST-LINK 虚拟串口，printf 直接用。
2. 固件里程碑：SPI 读编码器角度 → 开环转电机 → FOC 电流环 → 双 IMU 姿态融合 → 角度环锁定正下方。
3. 跑通后再贴定制板，同一份固件直接迁移（引脚定义不变）。

## 重新生成

改设计时编辑 `scripts/gen_sch.py`，然后：

```bash
python scripts/gen_sch.py && python scripts/validate.py
```

注意：KiCad 打开工程后若手工改动原理图，**不要**再运行 gen_sch.py，否则覆盖手工修改。
