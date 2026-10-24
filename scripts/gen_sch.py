#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NadirGimbal_R2 KiCad schematic generator  (v2)
Root: MCU. Children: pwr / drv / comms (all-global labels, zero-pin sheets);
      enc_roll / enc_pitch / imu_base / imu_cam (hierarchical ports).
Every pin: 2.54 mm stub + label. Power nets: VM / 3V3 / GND / 3V3_ANA.
"""
import hashlib, os, json

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kicad")
os.makedirs(OUT, exist_ok=True)

def uuid(key: str) -> str:
    h = lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()
    return f"{h(key)[:8]}-{h('b'+key)[:4]}-{h('c'+key)[:4]}-{h('d'+key)[:4]}-{h('e'+key)[:12]}"

FONT_NJ = '(effects (font (size 1.27 1.27)))'
PWR_IN, PWR_OUT, IN, DIR_OUT, BIDIR, PASSIVE = "power_in", "power_out", "input", "output", "bidirectional", "passive"

SYMS = {}
def add_sym(name, prefix, w, h, left, right):
    SYMS[name] = dict(prefix=prefix, w=w, h=h, left=left, right=right)

add_sym("MCU_STM32G431RBT6", "U", 40, 180,
    [(1,"VBAT",PWR_IN),(2,"PC13",BIDIR),(3,"PC14-OSC32_IN",BIDIR),(4,"PC15-OSC32_OUT",BIDIR),
     (5,"PF0-OSC_IN",IN),(6,"PF1-OSC_OUT",DIR_OUT),(7,"PG10-NRST",BIDIR),(8,"PC0",BIDIR),
     (9,"PC1",BIDIR),(10,"PC2",BIDIR),(11,"PC3",BIDIR),(12,"PA0",BIDIR),(13,"PA1",BIDIR),
     (14,"PA2",BIDIR),(15,"VSS",PWR_IN),(16,"VDD",PWR_IN),(17,"PA3",BIDIR),(18,"PA4",BIDIR),
     (19,"PA5",BIDIR),(20,"PA6",BIDIR),(21,"PA7",BIDIR),(22,"PC4",BIDIR),(23,"PC5",BIDIR),
     (24,"PB0",BIDIR),(25,"PB1",BIDIR),(26,"PB2",BIDIR),(27,"VSSA",PWR_IN),(28,"VREF+",PWR_IN),
     (29,"VDDA",PWR_IN),(30,"PB10",BIDIR),(31,"VSS",PWR_IN),(32,"VDD",PWR_IN)],
    [(33,"PB11",BIDIR),(34,"PB12",BIDIR),(35,"PB13",BIDIR),(36,"PB14",BIDIR),(37,"PB15",BIDIR),
     (38,"PC6",BIDIR),(39,"PC7",BIDIR),(40,"PC8",BIDIR),(41,"PC9",BIDIR),(42,"PA8",BIDIR),
     (43,"PA9",BIDIR),(44,"PA10",BIDIR),(45,"PA11",BIDIR),(46,"PA12",BIDIR),(47,"VSS",PWR_IN),
     (48,"VDD",PWR_IN),(49,"PB3",BIDIR),(50,"PB4",BIDIR),(51,"PB5",BIDIR),(52,"PB6",BIDIR),
     (53,"PB7",BIDIR),(54,"PB8-BOOT0",BIDIR),(55,"PB9",BIDIR),(56,"VSS",PWR_IN),(57,"VDD",PWR_IN),
     (58,"PA13",BIDIR),(59,"PA14",BIDIR),(60,"PA15",BIDIR),(61,"PC10",BIDIR),(62,"PC11",BIDIR),
     (63,"PC12",BIDIR),(64,"PD2",BIDIR)])

add_sym("DRV8316R", "U", 30, 110,
    [(1,"NC",PASSIVE),(2,"AGND",PWR_IN),(3,"FB_BK",PASSIVE),(4,"GND_BK",PWR_IN),
     (5,"SW_BK",PASSIVE),(6,"CPL",PASSIVE),(7,"CPH",PASSIVE),(8,"CP",PASSIVE),
     (9,"VM",PWR_IN),(10,"VM",PWR_IN),(11,"VM",PWR_IN),(12,"PGND",PWR_IN),
     (13,"OUTA",PWR_OUT),(14,"OUTA",PWR_OUT),(15,"PGND",PWR_IN),(16,"OUTB",PWR_OUT),
     (17,"OUTB",PWR_OUT),(18,"PGND",PWR_IN),(19,"OUTC",PWR_OUT),(20,"OUTC",PWR_OUT)],
    [(21,"DRVOFF",IN),(22,"nFAULT",OUT),(23,"nSLEEP",IN),(24,"NC",PASSIVE),
     (25,"AVDD",PWR_OUT),(26,"AGND",PWR_IN),(27,"INHA",IN),(28,"INLA",IN),
     (29,"INHB",IN),(30,"INLB",IN),(31,"INHC",IN),(32,"INLC",IN),(33,"SDO",BIDIR),
     (34,"SDI",IN),(35,"SCLK",IN),(36,"nSCS",IN),(37,"VREF",PWR_IN),(38,"SOC",DIR_OUT),
     (39,"SOB",DIR_OUT),(40,"SOA",DIR_OUT)])

add_sym("AS5048A", "U", 20, 40,
    [(1,"CSn",IN),(2,"CLK",IN),(3,"MISO",OUT),(4,"MOSI",IN),(5,"TEST_GND",PWR_IN)],
    [(14,"PWM",OUT),(13,"GND",PWR_IN),(12,"VDD3V",PWR_IN),(11,"VDD5V",PWR_IN),
     (10,"TEST_NC",PASSIVE),(9,"TEST_NC",PASSIVE),(8,"TEST_NC",PASSIVE),
     (7,"TEST_NC",PASSIVE),(6,"TEST_NC",PASSIVE)])

add_sym("ICM42688P", "U", 20, 40,
    [(1,"AP_SDO",OUT),(2,"RESV",PASSIVE),(3,"RESV",PASSIVE),(4,"INT1",OUT),
     (5,"VDDIO",PWR_IN),(6,"GND",PWR_IN),(7,"RESV_GND",PWR_IN)],
    [(14,"AP_SDA_SDI",IN),(13,"AP_SCLK",IN),(12,"AP_CS",IN),(11,"RESV",PASSIVE),
     (10,"RESV",PASSIVE),(9,"INT2_FSYNC",IN),(8,"VDD",PWR_IN)])

add_sym("TPS54202", "U", 20, 24,
    [("GND","GND",PWR_IN),("SW","SW",PWR_OUT),("BST","BST",PASSIVE)],
    [("FB","FB",IN),("EN","EN",IN),("VIN","VIN",PWR_IN)])

add_sym("PMOS_SOT23", "Q", 14, 14,
    [("G","G",PASSIVE)],
    [("D","D",PASSIVE),("S","S",PASSIVE)])

add_sym("R", "R", 10, 4, [("1","1",PASSIVE)], [("2","2",PASSIVE)])
add_sym("C", "C", 10, 4, [("1","1",PASSIVE)], [("2","2",PASSIVE)])
add_sym("L", "L", 10, 4, [("1","1",PASSIVE)], [("2","2",PASSIVE)])
add_sym("D_Schottky", "D", 10, 4, [("K","K",PASSIVE)], [("A","A",PASSIVE)])
add_sym("D_TVS", "D", 10, 4, [("K","K",PASSIVE)], [("A","A",PASSIVE)])
add_sym("LED", "D", 10, 4, [("K","K",PASSIVE)], [("A","A",PASSIVE)])
add_sym("FB", "FB", 10, 4, [("1","1",PASSIVE)], [("2","2",PASSIVE)])
add_sym("Conn_01x02", "J", 10, 10, [("1","1",PASSIVE)], [("2","2",PASSIVE)])
add_sym("Conn_01x03", "J", 10, 15, [("1","1",PASSIVE)], [("3","3",PASSIVE),("2","2",PASSIVE)])
add_sym("Conn_01x04", "J", 10, 20, [("1","1",PASSIVE)], [("4","4",PASSIVE),("3","3",PASSIVE),("2","2",PASSIVE)])
add_sym("Conn_01x05", "J", 10, 25, [("1","1",PASSIVE)], [("5","5",PASSIVE),("4","4",PASSIVE),("3","3",PASSIVE),("2","2",PASSIVE)])
add_sym("Conn_01x06", "J", 10, 30, [("1","1",PASSIVE)], [("6","6",PASSIVE),("5","5",PASSIVE),("4","4",PASSIVE),("3","3",PASSIVE),("2","2",PASSIVE)])
add_sym("Conn_01x07", "J", 10, 35, [("1","1",PASSIVE)], [("7","7",PASSIVE),("6","6",PASSIVE),("5","5",PASSIVE),("4","4",PASSIVE),("3","3",PASSIVE),("2","2",PASSIVE)])
add_sym("USB_MicroB", "J", 16, 20,
    [(1,"VBUS",PWR_IN),(2,"D-",BIDIR),(3,"D+",BIDIR),(4,"ID",PASSIVE)],
    [(5,"GND",PWR_IN)])

def lib_symbol(name):
    s = SYMS[name]; h, w = s["h"], s["w"]
    L = [f'(symbol "NGR2:{name}" (pin_names (offset 0.508)) (in_bom yes) (on_board yes)',
         f'  (property "Reference" "{s["prefix"]}" (at {w/2+2} {h/2+3} 0) {FONT_NJ})',
         f'  (property "Value" "{name}" (at {w/2+2} {h/2+1} 0) {FONT_NJ})',
         f'  (property "Footprint" "" (at 0 0 0) {FONT_NJ})',
         f'  (symbol "{name}_0_1"',
         f'    (rectangle (start 0 {-h/2}) (end {w} {h/2}) (stroke (width 0) (type default)) (fill (type background))))',
         f'  (symbol "{name}_1_1"']
    n_l, n_r = len(s["left"]), len(s["right"])
    for i, (num, nm, et) in enumerate(s["left"]):
        y = h/2 - (i+1) * h/(n_l+1)
        L += [f'    (pin {et} (at -2.54 {y:.2f} 0) (length 2.54)',
              f'      (name "{nm}" {FONT_NJ}) (number "{num}" {FONT_NJ}))']
    for i, (num, nm, et) in enumerate(s["right"]):
        y = -h/2 + (i+1) * h/(n_r+1)
        L += [f'    (pin {et} (at {w+2.54:.2f} {y:.2f} 180) (length 2.54)',
              f'      (name "{nm}" {FONT_NJ}) (number "{num}" {FONT_NJ}))']
    L.append('))')
    return "\n".join(L)

class Sheet:
    def __init__(self, fname, title):
        self.fname, self.title = fname, title
        self.items, self.used, self.symlib = [], set(), set()
    def text(self, x, y, s, size=1.5, bold=False):
        fx = f'(font (size {size} {size})' + (' (bold) yes)' if bold else ')')
        self.items.append(f'(text "{s}" (at {x} {y} 0) (effects {fx} (justify left)) (uuid {uuid(self.fname+"t"+str(x)+str(y)+s[:14])}))')
    def wire(self, x1, y1, x2, y2):
        self.items.append(f'(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid {uuid(self.fname+f"w{x1},{y1},{x2},{y2}")}))')
    def _label(self, kind, x, y, net, shape, rot):
        just = "left" if rot == 0 else "right"
        self.items.append(f'({kind} "{net}" (shape {shape}) (at {x} {y} {rot}) (effects (font (size 1.27 1.27)) (justify {just})) (uuid {uuid(self.fname+kind+str(x)+str(y)+net)}))')
    def glabel(self, x, y, net, shape="bidirectional", rot=0): self._label("global_label", x, y, net, shape, rot)
    def hlabel(self, x, y, net, shape="bidirectional", rot=0): self._label("hierarchical_label", x, y, net, shape, rot)
    def symbol(self, x, y, name, ref, value=None, dnp=False, fp=""):
        self.symlib.add(name)
        s = SYMS[name]
        dnpf = "yes" if dnp else "no"
        pins_xml = "".join(f'(pin "{n}" (uuid {uuid(self.fname+ref+"pin"+str(n))}))' for n, _, _ in s["left"]+s["right"])
        self.items.append(
            f'(symbol (lib_id "NGR2:{name}") (at {x} {y} 0) (unit 1) (exclude_from_sim no) '
            f'(in_bom yes) (on_board yes) (dnp {dnpf}) (fields_autoplaced yes) (uuid {uuid(self.fname+ref)}) '
            f'(property "Reference" "{ref}" (at {x+s["w"]/2} {y+s["h"]/2+3.5} 0) {FONT_NJ}) '
            f'(property "Value" "{value or name}" (at {x+s["w"]/2} {y+s["h"]/2+1.5} 0) {FONT_NJ}) '
            f'(property "Footprint" "{fp}" (at {x} {y} 0) {FONT_NJ}) {pins_xml})')
        pins = {}
        n_l, n_r = len(s["left"]), len(s["right"])
        for i, (num, nm, et) in enumerate(s["left"]):
            pins[str(num)] = (x-2.54, y + s["h"]/2 - (i+1)*s["h"]/(n_l+1), "L")
        for i, (num, nm, et) in enumerate(s["right"]):
            pins[str(num)] = (x+s["w"]+2.54, y - s["h"]/2 + (i+1)*s["h"]/(n_r+1), "R")
        return pins
    def _stub(self, px, py, side, kind, net, shape):
        if side == "L":
            self.wire(px, py, px-2.54, py)
            getattr(self, kind)(px-2.54, py, net, shape)
        else:
            self.wire(px, py, px+2.54, py)
            getattr(self, kind)(px+2.54, py, net, shape)
    def pin_label(self, pins, num, net, shape="bidirectional"):
        px, py, side = pins[str(num)]; self._stub(px, py, side, "glabel", net, shape)
    def pin_hlabel(self, pins, num, net, shape="bidirectional"):
        px, py, side = pins[str(num)]; self._stub(px, py, side, "hlabel", net, shape)
    def sheet(self, x, y, name, fname, w=50, h=50, pins=()):
        pl, out = [], {}
        for pname, side, frac in pins:
            py = y + h/2 - frac*h; px = x if side == "L" else x+w
            just = "right" if side == "L" else "left"
            pl.append(f'(pin "{pname}" (uuid {uuid(self.fname+name+"sp"+pname)}) (at {px:.2f} {py:.2f} 0) (effects (font (size 1.27 1.27)) (justify {just})))')
            out[pname] = (px, py, side)
        self.items.append(
            f'(sheet (at {x} {y}) (size {w} {h}) (fields_autoplaced) '
            f'(stroke (width 0.1524) (type solid)) (fill (type background)) (uuid {uuid(self.fname+"sh"+name)}) '
            f'(property "Sheetname" "{name}" (at {x} {y+h/2+2.5} 0) (effects (font (size 1.27 1.27) (bold) yes) (justify left bottom))) '
            f'(property "Sheetfile" "{fname}" (at {x} {y-h/2-2.5} 0) (effects (font (size 1.27 1.27)) (justify left top))) '
            + "".join(pl) + ')')
        return out
    def sheet_pin_glabel(self, sp, pinname, net, shape="bidirectional"):
        px, py, side = sp[pinname]; self._stub(px, py, side, "glabel", net, shape)
    def render(self):
        lib = "\n".join(lib_symbol(n) for n in sorted(self.symlib))
        return f'''(kicad_sch (version 20230121) (generator eeschema)
  (uuid {uuid("file-"+self.fname)})
  (paper "A3")
  (title_block (title "{self.title}") (date "2026-10-24") (rev "R2-draft") (company "TanTaiwoo07") (comment 2 "Author: TanTaiwoo07") (comment1 "设计草图：打样前请在 KiCad 7+ 中运行 ERC 并按数据手册复核"))
  (lib_symbols
{lib}
  )
{chr(10).join(self.items)}
)
'''

# nets
VM, V33, GND, V33A = "VM", "3V3", "GND", "3V3_ANA"
M1U, M1V, M1W = "PWM_M1_U", "PWM_M1_V", "PWM_M1_W"
M2U, M2V, M2W = "PWM_M2_U", "PWM_M2_V", "PWM_M2_W"
S3S, S3MI, S3MO = "SPI3_SCK", "SPI3_MISO", "SPI3_MOSI"
S1S, S1MI, S1MO = "SPI1_SCK", "SPI1_MISO", "SPI1_MOSI"
S2S, S2MI, S2MO = "SPI2_SCK", "SPI2_MISO", "SPI2_MOSI"
E1CS, E2CS = "ENC_ROLL_nCS", "ENC_PITCH_nCS"
I1CS, I2CS = "IMU_BASE_nCS", "IMU_CAM_nCS"
I1INT, I2INT = "IMU_BASE_INT", "IMU_CAM_INT"
D1S, D1O, D1F, D1CS = "DRV1_nSLEEP", "DRV1_DRVOFF", "DRV1_nFAULT", "DRV1_nSCS"
D2S, D2O, D2F, D2CS = "DRV2_nSLEEP", "DRV2_DRVOFF", "DRV2_nFAULT", "DRV2_nSCS"
I1A, I1B, I2A, I2B, VMS = "I1_A", "I1_B", "I2_A", "I2_B", "VM_SENSE"
U1TX, U1RX = "MAVLINK_TX", "MAVLINK_RX"
U2TX, U2RX = "DEBUG_TX", "DEBUG_RX"
PDM, PDP = "USB_DM", "USB_DP"
PIN1, PIN2 = "FC_PWM_ROLL", "FC_PWM_PITCH"
SWDIO, SWCLK, NRST, BOOT0 = "SWDIO", "SWCLK", "NRST", "BOOT0"
LEDK = "LED_K"

# ---------------------------------------------------------------- PWR
def build_pwr():
    sh = Sheet("pwr.kicad_sch", "电源输入保护 + 3V3")
    sh.text(-180, 130, "电源链：6S -> 独立 BEC 12V -> J1（禁止从飞控取电）-> 保险丝 -> P-MOS 反接保护 -> TVS -> VM 母线。", 2, True)
    sh.text(-180, 124, "TPS54202: 12V->3.3V/2A；3V3_ANA 经磁珠给 VDDA/VREF+。分压 100k/10k 监测 VM。", 1.5)
    j1 = sh.symbol(-170, 90, "Conn_01x02", "J1", "POWER_IN JST-GH-2/XT30", fp="Connector_JST:JST_GH_BM02B-GHS-TBT")
    sh.pin_label(j1, "1", VM, "power"); sh.pin_label(j1, "2", GND, "power")
    f1 = sh.symbol(-140, 90, "Conn_01x02", "F1", "FUSE 5A 慢断 1206", fp="Fuse:Fuse_1206_3216Metric")
    sh.pin_label(f1, "1", "VM_J1", "power"); sh.pin_label(f1, "2", "VM_FUSED", "power")
    q1 = sh.symbol(-110, 90, "PMOS_SOT23", "Q1", "AO3401A 反接保护", fp="Package_TO_SOT_SMD:SOT-23")
    sh.pin_label(q1, "S", "VM_FUSED", "power"); sh.pin_label(q1, "D", VM, "power"); sh.pin_label(q1, "G", GND, "power")
    d1 = sh.symbol(-80, 90, "D_TVS", "D1", "SMBJ15A", fp="Diode_SMD:D_SMB")
    sh.pin_label(d1, "K", VM, "power"); sh.pin_label(d1, "A", GND, "power")
    cb = sh.symbol(-55, 90, "C", "CB1", "100uF/35V", fp="Capacitor_SMD:CP_Elec_8x10")
    sh.pin_label(cb, "1", VM, "power"); sh.pin_label(cb, "2", GND, "power")
    c0 = sh.symbol(-40, 90, "C", "C0", "100nF", fp="Capacitor_SMD:C_0402_1005Metric")
    sh.pin_label(c0, "1", VM, "power"); sh.pin_label(c0, "2", GND, "power")
    # VM sense divider
    rv1 = sh.symbol(-20, 60, "R", "RV1", "100k", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rv1, "1", VM, "power"); sh.pin_label(rv1, "2", VMS)
    rv2 = sh.symbol(-20, 40, "R", "RV2", "10k", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rv2, "1", VMS); sh.pin_label(rv2, "2", GND, "power")
    # buck
    u8 = sh.symbol(20, 70, "TPS54202", "U8", "TPS54202 12V->3V3", fp="Package_TO_SOT_SMD:SOT-23-6")
    sh.pin_label(u8, "VIN", VM, "power"); sh.pin_label(u8, "GND", GND, "power")
    sh.pin_label(u8, "EN", "V33_EN"); sh.pin_label(u8, "SW", "SW_BUCK"); sh.pin_label(u8, "BST", "BST_BUCK"); sh.pin_label(u8, "FB", "FB_BUCK")
    l1 = sh.symbol(50, 70, "L", "L1", "4.7uH/2A", fp="Inductor_SMD:L_1008_2520Metric")
    sh.pin_label(l1, "1", "SW_BUCK"); sh.pin_label(l1, "2", V33, "power")
    d2 = sh.symbol(50, 45, "D_Schottky", "D2", "SS210", fp="Diode_SMD:D_SMA")
    sh.pin_label(d2, "A", GND, "power"); sh.pin_label(d2, "K", "SW_BUCK")
    cbst = sh.symbol(35, 95, "C", "CBST", "100nF", fp="Capacitor_SMD:C_0402_1005Metric")
    sh.pin_label(cbst, "1", "BST_BUCK"); sh.pin_label(cbst, "2", "SW_BUCK")
    ren = sh.symbol(75, 85, "R", "REN", "100k EN 上拉", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(ren, "1", VM, "power"); sh.pin_label(ren, "2", "V33_EN")
    rup = sh.symbol(75, 60, "R", "RUP", "100k", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rup, "1", V33, "power"); sh.pin_label(rup, "2", "FB_BUCK")
    rdn = sh.symbol(75, 40, "R", "RDN", "22.1k", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rdn, "1", "FB_BUCK"); sh.pin_label(rdn, "2", GND, "power")
    cv1 = sh.symbol(95, 70, "C", "CV1", "22uF", fp="Capacitor_SMD:C_0805_2012Metric")
    sh.pin_label(cv1, "1", V33, "power"); sh.pin_label(cv1, "2", GND, "power")
    cv2 = sh.symbol(95, 50, "C", "CV2", "100nF", fp="Capacitor_SMD:C_0402_1005Metric")
    sh.pin_label(cv2, "1", V33, "power"); sh.pin_label(cv2, "2", GND, "power")
    fb1 = sh.symbol(115, 70, "FB", "FB1", "磁珠 600R@100MHz", fp="Inductor_SMD:L_0603_1608Metric")
    sh.pin_label(fb1, "1", V33, "power"); sh.pin_label(fb1, "2", V33A, "power")
    cav = sh.symbol(130, 70, "C", "CVA", "100nF VDDA", fp="Capacitor_SMD:C_0402_1005Metric")
    sh.pin_label(cav, "1", V33A, "power"); sh.pin_label(cav, "2", GND, "power")
    sh.text(-180, 10, "注：DRV8316 内置 buck 默认不启用（SPI 配 BUCK_DIS=1）。若启用：按 TI 数据手册加 47uH+FB 分压，", 1.5)
    sh.text(-180, 6, "其输出经 0R（默认不焊）接 3V3，与 TPS54202 二选一，禁止两路同时焊接并联输出。", 1.5)
    return sh

# ---------------------------------------------------------------- DRV
def build_drv():
    sh = Sheet("drv.kicad_sch", "双路 DRV8316R 电机驱动")
    sh.text(-180, 132, "DRV8316R ×2，3x PWM 模式（INLx 经 0R×3 上拉至 3V3），20kHz FOC；SDO 挂共用 SPI3 MISO（nSCS 高时 Hi-Z）。", 2, True)
    sh.text(-180, 126, "每路：VM 3×100nF + bulk；CP 1uF/16V→VM；CPH-CPL 47nF；AVDD 1uF；VREF 0.1uF（0R 接 3V3）。", 1.5)
    def block(ux, uy, ref, m, jref, nu, nv, nw, inl, dS, dO, dF, dCS, soa, sob, note):
        p = sh.symbol(ux, uy, "DRV8316R", ref, "DRV8316R", fp="Package_DFN_QFN:VQFN-40-1EP_5x7mm_P0.5mm_EP3.1x5.1mm")
        for pn in ("9", "10", "11"): sh.pin_label(p, pn, VM, "power")
        for pn in ("2", "4", "12", "15", "18", "26"): sh.pin_label(p, pn, GND, "power")
        sh.pin_label(p, "8", f"{ref}_CP"); sh.pin_label(p, "7", f"{ref}_CPH"); sh.pin_label(p, "6", f"{ref}_CPL")
        sh.pin_label(p, "25", f"{ref}_AVDD"); sh.pin_label(p, "37", f"{ref}_VREF")
        sh.pin_label(p, "27", nu); sh.pin_label(p, "29", nv); sh.pin_label(p, "31", nw)
        for pn in ("28", "30", "32"): sh.pin_label(p, pn, inl)
        sh.pin_label(p, "23", dS); sh.pin_label(p, "21", dO); sh.pin_label(p, "22", dF)
        sh.pin_label(p, "36", dCS); sh.pin_label(p, "35", S3S); sh.pin_label(p, "34", S3MO); sh.pin_label(p, "33", S3MI)
        sh.pin_label(p, "40", f"{ref}_SOA"); sh.pin_label(p, "39", f"{ref}_SOB")
        for pn in ("1", "24"): sh.pin_label(p, pn, f"NC_{ref}_{pn}")
        for pn in ("3", "5"): sh.pin_label(p, pn, f"NC_{ref}_{pn}")   # FB_BK/SW_BK：buck 禁用时悬空
        sh.pin_label(p, "38", f"NC_{ref}_SOC")
        for pn in ("13", "14"): sh.pin_label(p, pn, nu, "power")
        for pn in ("16", "17"): sh.pin_label(p, pn, nv, "power")
        for pn in ("19", "20"): sh.pin_label(p, pn, nw, "power")
        # passives left column
        for i, (yy, rr, vv) in enumerate([(45, f"C{ref}V", "100nF ×3 VM 就近"), (32, f"C{ref}CP", "1uF/16V CP->VM"),
                                          (19, f"C{ref}H", "47nF CPH-CPL"), (6, f"C{ref}A", "1uF AVDD"),
                                          (-7, f"C{ref}R", "100nF VREF"), (-20, f"R{ref}REF", "0R VREF<-3V3"),
                                          (-33, f"R{ref}INL", "0R×3 INL->3V3")]):
            sym = "C" if rr[0] == "C" else "R"
            t = sh.symbol(ux-40, uy+yy, sym, rr, vv, fp="Capacitor_SMD:C_0402_1005Metric" if sym == "C" else "Resistor_SMD:R_0402_1005Metric")
            if rr == f"C{ref}V": sh.pin_label(t, "1", VM, "power"); sh.pin_label(t, "2", GND, "power")
            elif rr == f"C{ref}CP": sh.pin_label(t, "1", f"{ref}_CP"); sh.pin_label(t, "2", VM, "power")
            elif rr == f"C{ref}H": sh.pin_label(t, "1", f"{ref}_CPH"); sh.pin_label(t, "2", f"{ref}_CPL")
            elif rr == f"C{ref}A": sh.pin_label(t, "1", f"{ref}_AVDD"); sh.pin_label(t, "2", GND, "power")
            elif rr == f"C{ref}R": sh.pin_label(t, "1", f"{ref}_VREF"); sh.pin_label(t, "2", GND, "power")
            elif rr == f"R{ref}REF": sh.pin_label(t, "1", f"{ref}_VREF"); sh.pin_label(t, "2", V33, "power")
            else: sh.pin_label(t, "1", inl); sh.pin_label(t, "2", V33, "power")
        # passives right column
        for yy, rr, vv, n1, n2 in [
            (45, f"R{ref}SL", "100k nSLEEP 下拉", dS, GND), (32, f"R{ref}OF", "100k DRVOFF 下拉", dO, GND),
            (19, f"R{ref}FL", "10k nFAULT 上拉", dF, V33), (6, f"R{ref}CS", "10k nSCS 上拉", dCS, V33),
            (-7, f"R{ref}DO", "10k SDO 上拉", S3MI, V33),
            (-20, f"R{ref}SA", "100Ω SOA 串联", f"{ref}_SOA", soa), (-33, f"R{ref}SB", "100Ω SOB 串联", f"{ref}_SOB", sob)]:
            t = sh.symbol(ux+50, uy+yy, "R", rr, vv, fp="Resistor_SMD:R_0402_1005Metric")
            sh.pin_label(t, "1", n1); sh.pin_label(t, "2", n2, "power" if n2 in (GND, V33) else "bidirectional")
        for yy, cc, nn in [(-20, f"C{ref}SA", soa), (-33, f"C{ref}SB", sob)]:
            t = sh.symbol(ux+70, uy+yy, "C", cc, "2.2nF", fp="Capacitor_SMD:C_0402_1005Metric")
            sh.pin_label(t, "1", nn); sh.pin_label(t, "2", GND, "power")
        jm = sh.symbol(ux-70, uy-55, "Conn_01x03", jref, f"MOTOR {note} JST-GH-3", fp="Connector_JST:JST_GH_BM03B-GHS-TBT")
        sh.pin_label(jm, "1", nu, "power"); sh.pin_label(jm, "2", nv, "power"); sh.pin_label(jm, "3", nw, "power")
        sh.text(ux-15, uy-75, note, 1.5)
    block(-110, 40, "U1", "M1", "J4", M1U, M1V, M1W, "M1_INL", D1S, D1O, D1F, D1CS, I1A, I1B, "M1 = 横滚电机（GM3506）")
    block(60, 40, "U2", "M2", "J5", M2U, M2V, M2W, "M2_INL", D2S, D2O, D2F, D2CS, I2A, I2B, "M2 = 俯仰电机（GM3506）")
    sh.text(-180, -70, "SOC（第三相）未接：FOC 双相重建第三相。OUTx 每相预留 1nF/100V 对地 + 磁珠焊盘（DNP），视装机 EMI 实测决定是否焊接。", 1.5)
    sh.text(-180, -75, "功率地 PGND 单点汇接至母线电容，与 AGND 在驱动下方过孔阵列汇接（评审第 7 节散热/地平面建议）。", 1.5)
    return sh

# ---------------------------------------------------------------- COMMS
def build_comms():
    sh = Sheet("comms.kicad_sch", "通信与传感器接口")
    sh.text(-180, 132, "MAVLink v2：USART1(PB6/PB7)→J2 飞控 TELEM；调试：USART2(PA2/PA3)+J11 USB-Micro；PWM 回退输入：TIM2(PA0/PA1)→J3。", 2, True)
    j2 = sh.symbol(-170, 90, "Conn_01x04", "J2", "MAVLINK JST-GH-4", fp="Connector_JST:JST_GH_BM04B-GHS-TBT")
    sh.pin_label(j2, "1", V33, "power"); sh.pin_label(j2, "2", U1TX); sh.pin_label(j2, "3", U1RX); sh.pin_label(j2, "4", GND, "power")
    j3 = sh.symbol(-135, 90, "Conn_01x03", "J3", "FC PWM-IN GH-3", fp="Connector_JST:JST_GH_BM03B-GHS-TBT")
    sh.pin_label(j3, "1", PIN1); sh.pin_label(j3, "2", PIN2); sh.pin_label(j3, "3", GND, "power")
    j10 = sh.symbol(-100, 90, "Conn_01x05", "J10", "SWD GH-5", fp="Connector_JST:JST_GH_BM05B-GHS-TBT")
    sh.pin_label(j10, "1", V33, "power"); sh.pin_label(j10, "2", SWDIO); sh.pin_label(j10, "3", SWCLK); sh.pin_label(j10, "4", GND, "power"); sh.pin_label(j10, "5", NRST)
    usb = sh.symbol(-60, 90, "USB_MicroB", "J11", "USB-Micro 调试", fp="Connector_USB:USB_Micro-B_Molex_47346-0001")
    sh.pin_label(usb, "1", "USB_VBUS", "power"); sh.pin_label(usb, "5", GND, "power")
    sh.pin_label(usb, "2", PDM); sh.pin_label(usb, "3", PDP); sh.pin_label(usb, "4", "NC_USBID")
    rv = sh.symbol(-35, 100, "R", "RVB", "10k VBUS 检测", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rv, "1", "USB_VBUS"); sh.pin_label(rv, "2", "USB_VBUS_DET")
    def shconn(x, y, ref, n, fp, nets):
        c = sh.symbol(x, y, f"Conn_01x0{n}", ref, f"{ref} SH-{n}", fp=fp)
        for num, net in nets: sh.pin_label(c, num, net, "power" if net in (V33, GND) else "bidirectional")
    shconn(-170, 20, "J6", 6, "Connector_JST:JST_SH_SM06B-SRSS-TB",
           [("1", V33), ("2", GND), ("3", S1S), ("4", S1MI), ("5", S1MO), ("6", E1CS)])
    shconn(-130, 20, "J7", 6, "Connector_JST:JST_SH_SM06B-SRSS-TB",
           [("1", V33), ("2", GND), ("3", S1S), ("4", S1MI), ("5", S1MO), ("6", E2CS)])
    shconn(-90, 20, "J8", 7, "Connector_JST:JST_SH_SM07B-SRSS-TB",
           [("1", V33), ("2", GND), ("3", S2S), ("4", S2MI), ("5", S2MO), ("6", I1CS), ("7", I1INT)])
    shconn(-50, 20, "J9", 7, "Connector_JST:JST_SH_SM07B-SRSS-TB",
           [("1", V33), ("2", GND), ("3", S2S), ("4", S2MI), ("5", S2MO), ("6", I2CS), ("7", I2INT)])
    for i, (net, rr) in enumerate([(S1S, "R1S"), (S2S, "R2S")]):
        r = sh.symbol(-10+i*15, 30, "R", rr, "33Ω SCK 串联", fp="Resistor_SMD:R_0402_1005Metric")
        sh.pin_label(r, "1", net+"_MCU"); sh.pin_label(r, "2", net)
    sh.text(-180, -40, "跨关节线束用 FPC 排线 + 松弛环，与电机相线分槽走；SH 带锁扣；线束 ≤20cm；SPI 错误计数进遥测（评审 P1）。", 1.5)
    sh.text(-180, -46, "J2/J3/J10 走机架侧线束；J6-J9 走关节线束。", 1.5)
    return sh

# ---------------------------------------------------------------- satellites
def build_encoder(fname, title, ref):
    sh = Sheet(fname, title)
    sh.text(-165, 95, "AS5048A 磁编码小版（贴电机轴端）。磁钢 Ø6×2.5 径向充磁，气隙 0.5-1mm，端跳<0.05mm（定心工装保证）。", 1.5, True)
    u = sh.symbol(-100, 40, "AS5048A", ref, "AS5048A", fp="Package_SO:TSSOP-14_4.4x5mm_P0.65mm")
    sh.pin_hlabel(u, "1", "CSn")
    sh.pin_hlabel(u, "2", "SCK")
    sh.pin_hlabel(u, "3", "MISO")
    sh.pin_hlabel(u, "4", "MOSI")
    sh.pin_label(u, "5", GND, "power")
    for pn in ("6", "7", "8", "9", "10"): sh.pin_label(u, pn, f"NC_{ref}_{pn}")
    sh.pin_label(u, "11", V33, "power"); sh.pin_label(u, "12", V33, "power"); sh.pin_label(u, "13", GND, "power")
    sh.pin_label(u, "14", f"NC_{ref}_PWM")
    c1 = sh.symbol(-40, 60, "C", f"C{ref}", "100nF", fp="Capacitor_SMD:C_0402_1005Metric")
    sh.pin_label(c1, "1", V33, "power"); sh.pin_label(c1, "2", GND, "power")
    sh.text(-165, -25, "3.3V 供电模式：VDD5V 与 VDD3V 并接 3V3；PWM 脚悬空。SPI mode 1（CPOL=0/CPHA=1），≤10MHz。", 1.5)
    return sh

def build_imu(fname, title, ref, where):
    sh = Sheet(fname, title)
    sh.text(-165, 95, f"ICM-42688-P 六轴 IMU（{where}）。SPI 4 线 ≤24MHz；INT1 数据就绪中断接 MCU；ODR 建议 2-8kHz。", 1.5, True)
    u = sh.symbol(-100, 40, "ICM42688P", ref, "ICM-42688-P", fp="Package_LGA:LGA-14_2.5x3mm_P0.5mm_LayoutBorder1x6y")
    sh.pin_hlabel(u, "12", "CSn")
    sh.pin_hlabel(u, "13", "SCK")
    sh.pin_hlabel(u, "14", "MOSI")
    sh.pin_hlabel(u, "1", "MISO")
    sh.pin_hlabel(u, "4", "INT1")
    sh.pin_label(u, "8", V33, "power"); sh.pin_label(u, "5", V33, "power")
    sh.pin_label(u, "6", GND, "power"); sh.pin_label(u, "7", GND, "power"); sh.pin_label(u, "9", GND, "power")
    sh.pin_label(u, "2", f"NC_{ref}_2"); sh.pin_label(u, "3", f"NC_{ref}_3")
    sh.pin_label(u, "10", f"NC_{ref}_10"); sh.pin_label(u, "11", f"NC_{ref}_11")
    for x, y, rr, vv in [(-40, 62, f"C{rr if False else ref}A", "100nF VDD"), (-25, 62, f"C{ref}B", "2.2uF VDD"),
                         (-40, 46, f"C{ref}C", "10nF VDDIO"), (-25, 46, f"C{ref}D", "100nF VDDIO")]:
        c = sh.symbol(x, y, "C", rr, vv, fp="Capacitor_SMD:C_0402_1005Metric")
        sh.pin_label(c, "1", V33, "power"); sh.pin_label(c, "2", GND, "power")
    sh.text(-165, -30, "LGA-14 需回流焊；调试期可用成品 ICM-42688 模块经 SH 排线连 J8/J9。", 1.5)
    return sh

# ---------------------------------------------------------------- ROOT
def build_root():
    sh = Sheet("NadirGimbal_R2.kicad_sch", "NadirGimbal_R2 主控板")
    sh.text(-195, 135, "NadirGimbal_R2 —— STM32G431RBT6 + 双 DRV8316R ｜ nadir 双轴（横滚+俯仰）云台主控 ｜ 原理图设计草图", 2.5, True)
    sh.text(-195, 129, "跨页信号全部走全局网络标签（VM/3V3/GND/3V3_ANA 及各路信号）；卫星小版（编码器/IMU）经层级端口接入。", 1.5)
    sh.sheet(-150, 80, "PWR", "pwr.kicad_sch", 55, 45, pins=())
    sh.sheet(-60, 80, "DRV", "drv.kicad_sch", 55, 55, pins=())
    sh.sheet(30, 80, "COMMS", "comms.kicad_sch", 55, 55, pins=())
    sp1 = sh.sheet(110, 105, "ENC_ROLL", "enc_roll.kicad_sch", 45, 32,
        [("CSn", "L", 0.2), ("SCK", "L", 0.4), ("MISO", "L", 0.6), ("MOSI", "L", 0.8),
         ("3V3", "R", 0.3), ("GND", "R", 0.7)])
    for pn, net in [("CSn", E1CS), ("SCK", S1S), ("MISO", S1MI), ("MOSI", S1MO), ("3V3", V33), ("GND", GND)]:
        sh.sheet_pin_glabel(sp1, pn, net, "power" if net in (V33, GND) else "bidirectional")
    sp2 = sh.sheet(165, 105, "ENC_PITCH", "enc_pitch.kicad_sch", 45, 32,
        [("CSn", "L", 0.2), ("SCK", "L", 0.4), ("MISO", "L", 0.6), ("MOSI", "L", 0.8),
         ("3V3", "R", 0.3), ("GND", "R", 0.7)])
    for pn, net in [("CSn", E2CS), ("SCK", S1S), ("MISO", S1MI), ("MOSI", S1MO), ("3V3", V33), ("GND", GND)]:
        sh.sheet_pin_glabel(sp2, pn, net, "power" if net in (V33, GND) else "bidirectional")
    sp3 = sh.sheet(110, 45, "IMU_BASE", "imu_base.kicad_sch", 45, 36,
        [("CSn", "L", 0.15), ("SCK", "L", 0.32), ("MISO", "L", 0.48), ("MOSI", "L", 0.64), ("INT1", "L", 0.85),
         ("3V3", "R", 0.3), ("GND", "R", 0.7)])
    for pn, net in [("CSn", I1CS), ("SCK", S2S), ("MISO", S2MI), ("MOSI", S2MO), ("INT1", I1INT), ("3V3", V33), ("GND", GND)]:
        sh.sheet_pin_glabel(sp3, pn, net, "power" if net in (V33, GND) else "bidirectional")
    sp4 = sh.sheet(165, 45, "IMU_CAM", "imu_cam.kicad_sch", 45, 36,
        [("CSn", "L", 0.15), ("SCK", "L", 0.32), ("MISO", "L", 0.48), ("MOSI", "L", 0.64), ("INT1", "L", 0.85),
         ("3V3", "R", 0.3), ("GND", "R", 0.7)])
    for pn, net in [("CSn", I2CS), ("SCK", S2S), ("MISO", S2MI), ("MOSI", S2MO), ("INT1", I2INT), ("3V3", V33), ("GND", GND)]:
        sh.sheet_pin_glabel(sp4, pn, net, "power" if net in (V33, GND) else "bidirectional")

    # ---- MCU pin map (pin#, net, shape) —— 64 脚全覆盖 ----
    P = "power"
    mcu_map = [
        (1, V33, P), (2, LEDK, "bidirectional"), (3, "NC_PC14", "bidirectional"), (4, "NC_PC15", "bidirectional"),
        (5, "NC_PF0", "bidirectional"), (6, "NC_PF1", "bidirectional"), (7, NRST, "bidirectional"),
        (8, D1S, "bidirectional"), (9, D1O, "bidirectional"), (10, D1CS, "bidirectional"),
        (11, D2CS, "bidirectional"), (12, PIN1, "bidirectional"), (13, PIN2, "bidirectional"),
        (14, U2TX, "bidirectional"), (15, GND, P), (16, V33, P), (17, U2RX, "bidirectional"),
        (18, I2CS, "bidirectional"), (19, S1S, "bidirectional"), (20, S1MI, "bidirectional"),
        (21, S1MO, "bidirectional"), (22, I1B, "bidirectional"), (23, I2A, "bidirectional"),
        (24, VMS, "bidirectional"), (25, I1A, "bidirectional"), (26, D2S, "bidirectional"),
        (27, GND, P), (28, V33A, P), (29, V33A, P), (30, "TP_PB10", "bidirectional"),
        (31, GND, P), (32, V33, P), (33, I2B, "bidirectional"), (34, D1F, "bidirectional"),
        (35, S2S, "bidirectional"), (36, S2MI, "bidirectional"), (37, S2MO, "bidirectional"),
        (38, M2U, "bidirectional"), (39, M2V, "bidirectional"), (40, M2W, "bidirectional"),
        (41, E1CS, "bidirectional"), (42, M1U, "bidirectional"), (43, M1V, "bidirectional"),
        (44, M1W, "bidirectional"), (45, PDM, "bidirectional"), (46, PDP, "bidirectional"),
        (47, GND, P), (48, V33, P), (49, S3S, "bidirectional"), (50, S3MI, "bidirectional"),
        (51, S3MO, "bidirectional"), (52, U1TX, "bidirectional"), (53, U1RX, "bidirectional"),
        (54, BOOT0, "bidirectional"), (55, D2O, "bidirectional"), (56, GND, P), (57, V33, P),
        (58, SWDIO, "bidirectional"), (59, SWCLK, "bidirectional"), (60, I1CS, "bidirectional"),
        (61, E2CS, "bidirectional"), (62, I1INT, "bidirectional"), (63, I2INT, "bidirectional"),
        (64, D2F, "bidirectional"),
    ]
    assert sorted(p[0] for p in mcu_map) == list(range(1, 65)), "MCU 引脚未全覆盖"
    m = sh.symbol(-110, -40, "MCU_STM32G431RBT6", "U3", "STM32G431RBT6", fp="Package_QFP:LQFP-64_10x10mm_P0.5mm")
    for pin, net, shape in mcu_map:
        sh.pin_label(m, str(pin), net, shape)

    # decoupling & reset & boot & LED
    for i, x in enumerate([-175, -164, -153]):
        c = sh.symbol(x, -128, "C", f"CD{i}", "100nF", fp="Capacitor_SMD:C_0402_1005Metric")
        sh.pin_label(c, "1", V33, P); sh.pin_label(c, "2", GND, P)
    ca = sh.symbol(-142, -128, "C", "CD3", "4.7uF", fp="Capacitor_SMD:C_0805_2012Metric")
    sh.pin_label(ca, "1", V33, P); sh.pin_label(ca, "2", GND, P)
    cvd = sh.symbol(-131, -128, "C", "CD4", "100nF VDDA", fp="Capacitor_SMD:C_0402_1005Metric")
    sh.pin_label(cvd, "1", V33A, P); sh.pin_label(cvd, "2", GND, P)
    rn = sh.symbol(-115, -128, "R", "RNR", "10k NRST 上拉", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rn, "1", NRST); sh.pin_label(rn, "2", V33, P)
    cn = sh.symbol(-104, -128, "C", "CNR", "100nF NRST", fp="Capacitor_SMD:C_0402_1005Metric")
    sh.pin_label(cn, "1", NRST); sh.pin_label(cn, "2", GND, P)
    rb = sh.symbol(-93, -128, "R", "RBO", "100k BOOT0 下拉", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rb, "1", BOOT0); sh.pin_label(rb, "2", GND, P)
    led = sh.symbol(-78, -125, "LED", "D3", "LED 状态", fp="LED_SMD:LED_0402_1005Metric")
    sh.pin_label(led, "K", LEDK); sh.pin_label(led, "A", "LED_A")
    rl = sh.symbol(-65, -125, "R", "RLD", "1k", fp="Resistor_SMD:R_0402_1005Metric")
    sh.pin_label(rl, "1", "LED_A"); sh.pin_label(rl, "2", V33, P)
    for i, (x, nn) in enumerate([(-45, PDM), (-34, PDP)]):
        c = sh.symbol(x, -125, "C", f"CU{i}", "22pF", fp="Capacitor_SMD:C_0402_1005Metric")
        sh.pin_label(c, "1", nn); sh.pin_label(c, "2", GND, P)
    sh.text(-195, -105, "时钟：HSI16→PLL 170MHz；USB 用 HSI48+CRS 免晶振；PC14/15、PF0/1 预留 LSE/HSE 焊盘（默认 NC）。", 1.5)
    sh.text(-195, -110, "PB8 为 BOOT0 专用（100k 下拉），不兼任其他功能；BOOT0 高电平 + 复位 = 进系统 bootloader（USB 可刷机）。", 1.5)
    sh.text(-195, -115, "VCAP：按 ST 参考设计加 4.7uF（范围 2.2-10uF）靠近芯片（已在 CD3 预留，布局时紧贴 VCAP 脚）。", 1.5)
    return sh

def main():
    sheets = [build_pwr(), build_drv(), build_comms(),
              build_encoder("enc_roll.kicad_sch", "编码器小版 - 横滚", "U9"),
              build_encoder("enc_pitch.kicad_sch", "编码器小版 - 俯仰", "U10"),
              build_imu("imu_base.kicad_sch", "IMU 小版 - 机体侧", "U11", "机体侧·隔振层之下"),
              build_imu("imu_cam.kicad_sch", "IMU 小版 - 相机侧", "U12", "相机侧·随动内框"),
              build_root()]
    for s in sheets:
        path = os.path.join(OUT, s.fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s.render())
        print("wrote", path)
    proj = {
        "board": {"design_settings": {}, "ipc2581": {}},
        "boards": [],
        "cvpcb": {"footprint": {}},
        "erc": {"erc_exclusions": []},
        "libraries": {},
        "meta": {"filename": "NadirGimbal_R2.kicad_pro", "version": 1},
        "net_settings": {},
        "pcbnew": {"last_paths": {}},
        "schematic": {"annotate_start_num": 0, "bom_fmt_settings": {}, "bom_presets": [],
                       "connection_grid_size": 50.8, "drawing": {"dashed_lines_dash_length_ratio": 12.0,
                       "dashed_lines_gap_length_ratio": 3.0, "default_line_thickness": 6.0,
                       "default_text_size": 50.0, "field_names": [], "intersheets_ref_own_page": False,
                       "intersheets_ref_prefix": "", "intersheets_ref_short": False, "intersheets_ref_show": False,
                       "intersheets_ref_suffix": "", "junction_size_choice": 3, "page_layout_descr_file": "",
                       "pin_symbol_size": 25.0, "subref_id_padding": 0, "text_offset_ratio": 0.08},
                       "legacy_lib_dir": "", "legacy_lib_list": [], "meta": {"version": 1},
                       "net_format_name": "", "page_layout_descr_file": "", "plot_directory": "",
                       "spice_adjust_passive_values": False, "spice_current_sheet_as_root": False,
                       "spice_external_command": "spice \"%I\"", "spice_model_current_sheet_as_root": True,
                       "spice_save_all_currents": False, "spice_save_all_dissipations": False,
                       "spice_save_all_voltages": False, "subpart_first_id": 65, "subpart_id_separator": 0},
        "sheets": [["cc34056f-1f05-4ac5-9a2e-3f62a09c5f2c", "根目录"]],
        "text_variables": {}
    }
    with open(os.path.join(OUT, "NadirGimbal_R2.kicad_pro"), "w", encoding="utf-8") as f:
        json.dump(proj, f, ensure_ascii=False, indent=2)
    print("wrote project file")

if __name__ == "__main__":
    main()
