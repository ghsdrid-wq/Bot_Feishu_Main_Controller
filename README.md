# DWS Central Controller & Feishu Automation Bot

A Python-based automation system for managing DWS sorting plans and JMS user operations through a centralized controller and Feishu Bot integration.

The system consists of:

* Central Controller GUI
* Distributed DWS Agent Clients
* Feishu Bot Integration
* JMS User Management Automation
* REST API Communication

This project allows operators to:

* Switch DWS sorting plans remotely
* Control multiple DWS clients simultaneously
* Reset JMS/App passwords
* Enable locked users
* Monitor client status in real-time
* Execute commands directly from Feishu chat

The architecture is designed for internal warehouse automation and operational support workflows.

# Flow การทำงาน

```text
Feishu User
     ↓    
Feishu Bot Webhook
     ↓     
Main Controller (main.py)
     ↓    
Controller API
     ↓     
DWS Agents (agent1.py / agent2.py)
     ↓
```     
MySQL Database

# อธิบายแต่ละไฟล์

main.py

Main Controller ของระบบ

หน้าที่:

GUI หลัก
* จัดการ DWS Clients
* รับคำสั่งจาก Feishu
* Broadcast เปลี่ยน Plan
* Monitor Client Status
* JMS Operations
* API Server


agent1.py

agent2.py

DWS Agent Client

หน้าที่:

* รันบนเครื่อง DWS แต่ละตัว
* เชื่อม MySQL
* เปลี่ยน Sorting Plan
* เปิด FastAPI รับคำสั่งจาก Controller
* แสดงสถานะผ่าน GUI
* System Tray Support

* controller_api.py

REST API สำหรับ Controller

Endpoints:

* status
* switch_plan
* refresh

ใช้ Flask API สำหรับ communication ระหว่างระบบ


jms_api.py

JMS Automation Module

Features:

* Search User
* Reset App Password
* Reset JMS Password
* Enable Locked User

เชื่อมต่อ JMS ผ่าน Internal API


feishu_api.py

Feishu Messaging Integration

Features:

* Generate Tenant Access Token
* Reply Message
* Bot Communication


config.py

Configuration Management

จัดการ:

* Config File
* Feishu Credential
* Ngrok Command
* Runtime Config


logger.py

Custom Logging System

เก็บ log แยกตามวัน

รูปแบบ:
* logs/YYYY-MM-DD.log

# Tech Stack
```text
Python
Tkinter
FastAPI
Flask
Waitress
MySQL
Feishu Open API
Requests
PyMySQL
Pystray
```
