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
     
MySQL Database


#อธิบายแต่ละไฟล์

* main.py

Main Controller ของระบบ

หน้าที่:

GUI หลัก
* จัดการ DWS Clients
* รับคำสั่งจาก Feishu
* Broadcast เปลี่ยน Plan
* Monitor Client Status
* JMS Operations
* API Server
