# Feishu DWS & JMS Controller

Python desktop application สำหรับควบคุม DWS Sorting Plan และ JMS User Management ผ่าน Feishu Bot พร้อมระบบ Multi-Agent API, Real-time Controller, Remote Plan Switching และ User Automation

โปรแกรมถูกออกแบบสำหรับ warehouse automation และ operation support เพื่อให้สามารถควบคุม DWS Plan และจัดการ JMS User ผ่าน Feishu Chat Bot ได้แบบ centralized control

รองรับ:

- Feishu Bot Integration
- DWS Plan Switching
- JMS User Management
- Multi-Agent Controller
- Remote API Control
- Real-time Client Monitoring
- Multi-PC Synchronization
- System Tray Agent
- Config Management
- GUI Monitoring

---

# Features

- Feishu bot command control
- DWS plan switching
- JMS password reset
- JMS account unlock
- Multi-agent architecture
- FastAPI agent server
- Flask controller API
- Multi-client monitoring
- Dynamic plan loading
- Real-time GUI log
- System tray support
- Auto config generation
- Duplicate event protection
- Background threading
- Windows desktop GUI
- REST API integration
- Remote status monitoring
- Config hot reload

---

# Application Overview

ระบบนี้แบ่งออกเป็น 3 ส่วนหลัก:

## 1. Main Controller

ใช้สำหรับ:

- ควบคุม DWS ทุกเครื่อง
- รับคำสั่งจาก Feishu
- ส่ง API ไปยัง Agent
- ตรวจสอบสถานะแต่ละเครื่อง
- จัดการ JMS User

---

## 2. DWS Agent

ติดตั้งในแต่ละ DWS PC

ทำหน้าที่:

- เชื่อมต่อ Database
- เปลี่ยน Sorting Plan
- เปิด API Server
- Report Status กลับ Controller

---

## 3. Feishu Bot

ใช้สำหรับรับคำสั่งจาก Feishu Chat

ตัวอย่าง:

```text
@BOT เปลี่ยนแพลนบ่าย
@BOT รีรหัส app 999004T00001
@BOT รีรหัส jms 999004T00001
@BOT ปลดล็อค 999004T00001
```

---

# System Architecture

```text
Feishu User
    ↓
Feishu Bot
    ↓
Main Controller
    ↓
DWS Agent API
    ↓
Database
```

---

# Tech Stack

- Python
- Tkinter
- FastAPI
- Flask
- Waitress
- Uvicorn
- Requests
- PyMySQL
- PyStray
- Pillow
- Lark OpenAPI

---

# Project Structure

```text
project/
│
├── main.py
│
├── requirements.txt
├── config.ini
│
├── agents/
│   └── agent1.py.py
│   └── agent2.py.py
│
├── controller/
│   └── controller_api.py
│
├── core/
│   ├── config.py
│   ├── feishu_api.py
│   ├── jms_api.py
│   └── logger.py
│
└── logs/
    └── YYYY-MM-DD.log
```

---

# Main Components

## Main Controller

ไฟล์:

```text
main.py
```

หน้าที่:

- GUI Controller
- Feishu Bot Server
- DWS Monitoring
- Client Management
- JMS Automation
- API Gateway

---

## Agent Server

ไฟล์:

```text
agent1.py
agent2.py
```

หน้าที่:

- Database Connection
- Plan Switching
- API Server
- Tray Application
- Local Monitoring

---

## Controller API

ไฟล์:

```text
controller_api.py
```

ใช้ Flask API สำหรับ:

- status endpoint
- switch_plan endpoint
- refresh endpoint

---

## Feishu API

ไฟล์:

```text
feishu_api.py
```

ใช้สำหรับ:

- tenant access token
- send reply message
- Feishu authentication

---

## JMS API

ไฟล์:

```text
jms_api.py
```

ใช้สำหรับ:

- search user
- reset app password
- reset JMS password
- enable user

---

## Logger

ไฟล์:

```text
logger.py
```

ใช้สำหรับ:

- daily log file
- operation tracking
- audit log

---

# Multi-Agent Architecture

ระบบรองรับหลาย DWS PC

ตัวอย่าง:

```text
DWS1
DWS2
DWS3
...
DWS9-11
```

โดย Main Controller จะเชื่อมต่อผ่าน REST API

---

# Agent API

Agent เปิด FastAPI server

Default:

```text
DWS1-8  → Port 4000
DWS9-11 → Port 4001
```

รองรับ endpoint:

```text
/plans
/current_plan
/switch_plan
/status
```

---

# Database Integration

## Agent 1

ใช้ database:

```text
db_sds
```

Table:

```sql
sortplaninfos
```

---

## Agent 2

ใช้ database:

```text
dwsdb_thailand
```

Table:

```sql
tab_dws_cfg_sorting_plan
```

---

# Plan Switching Logic

Workflow:

```text
Receive Command
    ↓
Validate Plan
    ↓
Deactivate Current Plan
    ↓
Activate New Plan
    ↓
Commit Database
    ↓
Refresh Cache
    ↓
Update GUI
```

---

# Feishu Bot Commands

## Change Plan

```text
@BOT เปลี่ยนแพลนบ่าย
@BOT เปลี่ยนแพลนดึก
```

Result:

```text
DWSA
DWSB
```

---

## Reset APP Password

```text
@BOT รีรหัส app 999004T00001
```

---

## Reset JMS Password

```text
@BOT รีรหัส jms 999004T00001
```

---

## Unlock User

```text
@BOT ปลดล็อค 999004T00001
```

---

# Duplicate Event Protection

ระบบป้องกัน Feishu ส่ง event ซ้ำ

ใช้:

```python
processed_events = set()
```

เมื่อ event_id ซ้ำ:

```text
SKIP DUPLICATE
```

---

# Dynamic Plan Loading

Main Controller จะโหลด plan จาก agent อัตโนมัติ

Workflow:

```text
GET /plans
    ↓
Load Available Plan
    ↓
Populate Controller
```

หากโหลดไม่ได้:

```text
Fallback:
DWSA
DWSB
```

---

# GUI Overview

## DWS Tab

ประกอบด้วย:

- Plan Control
- Client Status Table
- Real-time Logs
- Start/Stop Bot
- Refresh Status

---

## JMS Tab

ประกอบด้วย:

- JMS Bot Control
- JMS Logs
- User Management

---

## Setting Tab

ประกอบด้วย:

- DWS Client Config
- Feishu Config
- JMS Config
- Save Config

---

# Client Monitoring Table

แสดง:

| Column | Description |
|---|---|
| PC | DWS Name |
| IP | IP Address |
| Port | API Port |
| Status | Online/Offline |
| Plan | Current Plan |
| Message | Response |

---

# Config System

ใช้:

```text
config.ini
```

รองรับ:

- DWS IP
- DWS Port
- Feishu APP_ID
- Feishu APP_SECRET
- BOT_PORT
- AUTH_TOKEN
- BOT_NAME

---

# Example Config

```ini
[FEISHU]
APP_ID=cli_xxxxx
APP_SECRET=xxxxx
VERIFY_TOKEN=mytoken
BOT_PORT=7000
BOT_NAME=BOT_JMSKKN
AUTH_TOKEN=xxxxx

[DWS1]
IP=10.30.32.32
PORT=4000
```

---

# Feishu Webhook

Endpoint:

```text
/feishu_event
```

รองรับ:

- URL Verification
- Event Message
- Reply Message
- Mention Detection

---

# Mention Protection

Bot จะตอบเฉพาะกรณีถูก mention ใน group

ตัวอย่าง:

```text
@BOT รีรหัส jms 999004T00001
```

หากไม่ mention:

```text
skip_no_mention
```

---

# JMS Workflow

```text
Receive Staff ID
    ↓
Search User
    ↓
Validate User
    ↓
Reset Password / Unlock
    ↓
Reply Result
```

---

# Threading Design

ระบบใช้:

```python
threading.Thread()
```

สำหรับ:

- API Server
- GUI
- Feishu Worker
- Refresh Worker
- Plan Switching
- JMS Processing

ช่วยให้:

- GUI ไม่ค้าง
- รองรับหลาย request
- ทำงาน background ได้

---

# Logging System

ระบบสร้าง log แยกตามวัน

```text
logs/YYYY-MM-DD.log
```

ตัวอย่าง:

```text
STATUS : SUCCESS
USER   : 999004T00001
ACTION : RESET JMS
DETAIL : Password Reset Complete
```

---

# System Tray Support

Agent รองรับ:

- minimize to tray
- background execution
- tray restore
- tray exit

ผ่าน:

```python
pystray
```

---

# Requirements

```text
fastapi
flask
waitress
uvicorn
requests
pymysql
pystray
pillow
lark-oapi
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourname/feishu-dws-controller.git
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Start Agent

```bash
python agent1.py
```

หรือ:

```bash
python agent2.py
```

---

## 4. Start Controller

```bash
python main.py
```

---

# Build EXE

ใช้ PyInstaller:

```bash
pyinstaller --onefile --windowed main.py
```

Agent:

```bash
pyinstaller --onefile --windowed agent1.py
```

---

# API Examples

## Status

```http
GET /status
```

---

## Switch Plan

```http
POST /switch_plan
Content-Type: application/json

{
    "plan": "DWSA"
}
```

---

# Error Handling

ระบบรองรับ:

- database connection failure
- invalid plan
- duplicate event
- invalid token
- offline client
- API timeout
- JMS API failure
- Feishu authentication failure
- cache update failure

---

# Security Notes

ระบบใช้:

- Feishu Tenant Token
- JMS Auth Token
- Local API Network
- Mention Validation

เพื่อป้องกัน:

- unauthorized command
- accidental execution
- duplicate request

---

# User Experience Features

- Real-time log viewer
- Online/offline monitoring
- Dynamic client refresh
- Background bot execution
- Auto config generation
- Multi-threaded API handling
- GUI status dashboard

---

# Future Improvements

- Web dashboard
- Multi-site controller
- Database audit history
- JWT authentication
- Docker deployment
- Role permission system
- WebSocket real-time sync
- Redis event queue
- Multi-bot support
- Auto backup config

---

# License

MIT License

---

# Author

Developed for warehouse automation, DWS sorting control, and JMS operation support workflow.

