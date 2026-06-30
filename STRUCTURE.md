# STRUCTURE — Bot_Feishu_Main_Controller

> ⚠️ **กฎการดูแลไฟล์นี้ (สำคัญ)**
> ทุกครั้งที่แก้ไขโค้ดใน repo นี้ — เพิ่ม/ลบ/ย้ายไฟล์, เปลี่ยน logic ฟังก์ชัน/คลาส, เพิ่ม/แก้ HTTP endpoint, เปลี่ยน config key หรือ SQL, หรือเปลี่ยน flow — **ต้องอัปเดต STRUCTURE.md นี้ให้ตรงกับโค้ดเสมอ**

## ภาพรวม
เวอร์ชัน "แยกส่วน controller + agent" ของระบบ DWS/JMS:
- **Controller** (`project/main.py`) = ตัวเดียวกับ `Bot_Feishu_All_In_One_Program/main.py` (Tkinter GUI + Feishu webhook + สั่งเปลี่ยนแพลน DWS + reset รหัส JMS)
- **Agent** (`project/agents/agent1.py`, `agent2.py`) = โปรแกรมที่รันบน **เครื่อง DWS แต่ละเครื่อง** เปิด FastAPI ให้ controller สั่งงาน และไปแก้ตาราง sorting plan ใน MySQL ของเครื่องนั้นโดยตรง

Controller ↔ Agent คุยกันผ่าน HTTP บน LAN

## วิธีรัน / Entry point
- **Controller:** `python project/main.py` → GUI + Flask controller API พอร์ต 6100; กด START BOT เปิด Feishu webhook (waitress, `BOT_PORT` default 7000)
- **Agent:** `python project/agents/agent1.py` (หรือ `agent2.py`) บนเครื่อง DWS → FastAPI (uvicorn) + Tkinter status window + system tray (เริ่มแบบซ่อนหน้าต่าง)

## โครงสร้างไฟล์
| ไฟล์ | หน้าที่ |
|------|---------|
| `project/main.py` | Controller GUI + Feishu webhook (เหมือน All-In-One) |
| `project/agents/agent1.py` | **Agent แบบ SCADA DB** — DB `db_sds`, ตาราง `sortplaninfos` (คอลัมน์ `Name`, `IsActivated`), API พอร์ต **4000** |
| `project/agents/agent2.py` | **Agent แบบ DWS Thailand** — DB `dwsdb_thailand`, ตาราง `tab_dws_cfg_sorting_plan` (คอลัมน์ `PlanName`, `IsSelected`), API พอร์ต **4001**, มี call `update/cache` หลังเปลี่ยนแพลน |
| `project/controller/controller_api.py` | Flask API พอร์ต 6100 ของ controller |
| `project/core/jms_api.py` | JMS J&T API (search/reset/enable user) |
| `project/core/feishu_api.py`, `config.py`, `logger.py` | helper เหมือนใน All-In-One |
| `requirements.txt` | dependency list |

## Agent API (FastAPI) — ทั้ง agent1 / agent2
- `GET /status` → `{success, current_plan, message}`
- `GET /plans` → รายการแพลนทั้งหมดจาก DB
- `POST /switch_plan` body `{plan}` → ตั้งแพลนนั้น active (UPDATE 2 query: reset อันอื่น = 0, set อันนี้ = 1)

ความต่างหลัก agent1 vs agent2 = **ชื่อ DB / ตาราง / คอลัมน์ / พอร์ต** (และ agent2 ยิง cache-update URL `127.0.0.1:8089/dws/cfg/plan/update/cache?dbCode=2`)

## Config (`config.ini`)
- Controller: `[FEISHU]` (เหมือน All-In-One) + `[DWS1]..[DWS9-11]` (IP/PORT)
- Agent: `[SERVER]` (`API_HOST`, `API_PORT`) + `[DATABASE]` (`DB_HOST/PORT/USER/PASSWORD/NAME`)

## Dependencies / บริการภายนอก
- Controller: `flask`, `waitress`, `requests`, `lark_oapi`, `tkinter`
- Agent: `fastapi`, `uvicorn`, `pymysql`, `pystray`, `Pillow`, `tkinter`
- MySQL บนเครื่อง DWS, Feishu OpenAPI, JMS J&T

## ข้อควรระวัง
- เลือก agent ให้ตรงชนิด DB ของเครื่องนั้น (SCADA = agent1, DWS Thailand = agent2)
- พอร์ต agent (4000/4001) ต้องตรงกับที่ตั้งใน config `[DWSx]` ฝั่ง controller
