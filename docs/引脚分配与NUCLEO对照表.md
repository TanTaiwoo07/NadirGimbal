# NadirGimbal_R2 引脚分配与 NUCLEO-G431RB 对照表

依据：原理图 `kicad/NadirGimbal_R2.kicad_sch`（64 脚全覆盖）；NUCLEO-G431RB（MB1367）排针映射依据 ST 用户手册 UM2505 Table 16 / Figure 18。

## MCU 引脚分配总表（LQFP-64）

| 脚号 | 端口 | 网络 | 功能 |
|---|---|---|---|
| 1 | VBAT | 3V3 | 备份域供电（接 3V3，不用电池） |
| 2 | PC13 | LED_K | 状态灯（阴极，阳极经 1k 接 3V3） |
| 3–4 | PC14/PC15 | NC_PC14/15 | 预留 LSE（默认 NC） |
| 5–6 | PF0/PF1 | NC_PF0/1 | 预留 HSE（默认 NC） |
| 7 | NRST | NRST | 复位（10k 上拉 + 100nF） |
| 8 | PC0 | DRV1_nSLEEP | 横滚驱动 sleep |
| 9 | PC1 | DRV1_DRVOFF | 横滚驱动输出关断 |
| 10 | PC2 | DRV1_nSCS | 横滚驱动 SPI 片选 |
| 11 | PC3 | DRV2_nSCS | 俯仰驱动 SPI 片选 |
| 12 | PA0 | FC_PWM_ROLL | 飞控横滚 PWM 输入（TIM2_CH1） |
| 13 | PA1 | FC_PWM_PITCH | 飞控俯仰 PWM 输入（TIM2_CH2） |
| 14 | PA2 | DEBUG_TX | 调试串口发（LPUART1/USART2 复用） |
| 15 | VSS | GND | — |
| 16 | VDD | 3V3 | — |
| 17 | PA3 | DEBUG_RX | 调试串口收 |
| 18 | PA4 | IMU_CAM_nCS | 相机侧 IMU 片选（SPI1 软件 NSS） |
| 19 | PA5 | SPI1_SCK | SPI1 时钟（编码器×2） |
| 20 | PA6 | SPI1_MISO | SPI1 MISO |
| 21 | PA7 | SPI1_MOSI | SPI1 MOSI（TIM1_CH1N 冲突故不用互补 PWM） |
| 22 | PC4 | I1_B | 横滚相电流 B（ADC） |
| 23 | PC5 | I2_A | 俯仰相电流 A（ADC） |
| 24 | PB0 | VM_SENSE | 电池电压监测（ADC，100k/10k 分压） |
| 25 | PB1 | I1_A | 横滚相电流 A（ADC） |
| 26 | PB2 | DRV2_nSLEEP | 俯仰驱动 sleep |
| 27 | VSSA | GND | — |
| 28 | VREF+ | 3V3_ANA | ADC 基准（磁珠分网） |
| 29 | VDDA | 3V3_ANA | — |
| 30 | PB10 | TP_PB10 | 测试点/备用（TIM2_CH3） |
| 31 | VSS | GND | — |
| 32 | VDD | 3V3 | — |
| 33 | PB11 | I2_B | 俯仰相电流 B（ADC） |
| 34 | PB12 | DRV1_nFAULT | 横滚驱动故障输出 |
| 35 | PB13 | SPI2_SCK | SPI2 时钟（IMU×2） |
| 36 | PB14 | SPI2_MISO | SPI2 MISO |
| 37 | PB15 | SPI2_MOSI | SPI2 MOSI |
| 38 | PC6 | PWM_M2_U | 俯仰 U（TIM8_CH1，3xPWM） |
| 39 | PC7 | PWM_M2_V | 俯仰 V（TIM8_CH2） |
| 40 | PC8 | PWM_M2_W | 俯仰 W（TIM8_CH3） |
| 41 | PC9 | ENC_ROLL_nCS | 横滚编码器片选 |
| 42 | PA8 | PWM_M1_U | 横滚 U（TIM1_CH1，3xPWM） |
| 43 | PA9 | PWM_M1_V | 横滚 V（TIM1_CH2） |
| 44 | PA10 | PWM_M1_W | 横滚 W（TIM1_CH3） |
| 45 | PA11 | USB_DM | 原生 USB D− |
| 46 | PA12 | USB_DP | 原生 USB D+ |
| 47 | VSS | GND | — |
| 48 | VDD | 3V3 | — |
| 49 | PB3 | SPI3_SCK | SPI3 时钟（DRV×2 共用） |
| 50 | PB4 | SPI3_MISO | SPI3 MISO（两 DRV 的 SDO 线与门） |
| 51 | PB5 | SPI3_MOSI | SPI3 MOSI |
| 52 | PB6 | MAVLINK_TX | MAVLink 发（USART1_TX，接飞控） |
| 53 | PB7 | MAVLINK_RX | MAVLink 收 |
| 54 | PB8 | BOOT0 | BOOT0 专用（100k 下拉），不复用 |
| 55 | PB9 | DRV2_DRVOFF | 俯仰驱动输出关断 |
| 56 | VSS | GND | — |
| 57 | VDD | 3V3 | — |
| 58 | PA13 | SWDIO | 调试 |
| 59 | PA14 | SWCLK | 调试 |
| 60 | PA15 | IMU_BASE_nCS | 机体侧 IMU 片选 |
| 61 | PC10 | ENC_PITCH_nCS | 俯仰编码器片选 |
| 62 | PC11 | IMU_BASE_INT | 机体侧 IMU 数据就绪中断 |
| 63 | PC12 | IMU_CAM_INT | 相机侧 IMU 数据就绪中断 |
| 64 | PD2 | DRV2_nFAULT | 俯仰驱动故障输出 |

## NUCLEO-G431RB（MB1367）对照与注意事项

| 网络 | MCU 脚 | NUCLEO 排针 | 备注 |
|---|---|---|---|
| FC_PWM_ROLL | PA0 | CN7-28 | ⚠ USER 键 B1 经 SB21 默认接 PA0，验证 PWM 输入前断开 SB21 |
| FC_PWM_PITCH | PA1 | CN7-30 | |
| DEBUG_TX/RX | PA2/PA3 | CN10-35 / CN10-37 | 默认焊桥下已接 ST-LINK VCP（SB17/SB23 ON），printf 直接用 |
| SPI1_SCK (编码器) | PA5 | CN10-11 | ⚠ LD2 经 SB6 默认接 PA5，SPI 验证前断开 SB6 |
| SPI1_MISO/MOSI | PA6/PA7 | CN10-13 / CN10-15 | |
| IMU_CAM_nCS | PA4 | CN7-32 | |
| PWM_M1_U/V/W | PA8/9/10 | CN10-23 / 21 / 33 | TIM1，示波器看波最方便 |
| PWM_M2_U/V/W | PC6/7/8 | CN10-4 / 19 / 2 | TIM8 |
| USB_DM/DP | PA11/12 | CN10-14 / 12 | 与板上 ST-LINK USB 独立 |
| SWDIO/SWCLK | PA13/14 | CN7-13 / 15 | 已被板载 ST-LINK 占用，勿外接驱动 |
| IMU_BASE_nCS | PA15 | CN7-17 | SB7 ON 直连，无需处理 |
| VM_SENSE | PB0 | CN7-34 | |
| I1_A | PB1 | CN10-24 | |
| DRV2_nSLEEP | PB2 | CN10-22 | |
| SPI3_SCK/MISO/MOSI | PB3/4/5 | CN10-31 / 27 / 29 | |
| MAVLINK_TX/RX | PB6/7 | CN10-17 / CN7-21 | USART1 在 NUCLEO 上另经 PC4/PC5 接 Arduino D0/D1，PB6/PB7 空闲可用 |
| BOOT0 | PB8 | CN7-7 | 与 NUCLEO 同名网络，一致 |
| DRV1_DRVOFF | PB9 | CN10-5 | |
| TP_PB10 | PB10 | CN10-25 | |
| I2_B | PB11 | CN10-18 | ✅ 在 MB1367 排针上存在（旧版 Nucleo-64 没有，G4 这版有） |
| DRV1_nFAULT | PB12 | CN10-16 | |
| SPI2_SCK/MISO/MOSI | PB13/14/15 | CN10-30 / 28 / 26 | |
| DRV1_nSLEEP/DRVOFF/nSCS | PC0/1/2 | CN7-38 / 36 / 35 | |
| DRV2_nSCS | PC3 | CN7-37 | |
| I1_B / I2_A | PC4/5 | CN10-34 / CN10-6 | ⚠ PC4/PC5 与 VCP/Arduino D0-D1 的焊桥（SB12/13/33 等）有关，作 ADC 前先确认相关焊桥状态 |
| ENC_ROLL_nCS | PC9 | CN10-1 | |
| ENC_PITCH_nCS | PC10 | CN7-1 | |
| IMU_BASE_INT | PC11 | CN7-2 | |
| IMU_CAM_INT | PC12 | CN7-3 | |
| LED_K | PC13 | CN7-23 | |
| DRV2_nFAULT | PD2 | CN7-4 | |
| VBAT | — | CN7-33 | SB39 ON 时接 VDD |
| NRST | — | CN7-14 | |
| AGND | — | CN10-32 | |
| VREFP | — | CN10-7 | 经 JP8 跳线选择 VREF 来源 |

**过渡期接线要点**：NUCLEO + 成品模块（DRV8316 模块、AS5048A 模块、ICM-42688 模块）按上表跳线；编码器/IMU 的 SPI 经 33Ω 串阻排针引出；电机电流采样在 NUCLEO 阶段不可用模块替代，先只验证角度环。
