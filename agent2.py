import os
import sys
import threading
import logging
import configparser
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from fastapi import FastAPI
from pydantic import BaseModel
import pymysql
import requests
import uvicorn

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# =========================================
# CONFIG
# =========================================
CONFIG_FILE = "config.ini"

DEFAULT_CONFIG = {
    "SERVER": {
        "API_HOST": "0.0.0.0",
        "API_PORT": "4001"
    },
    "DATABASE": {
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "3306",
        "DB_USER": "root",
        "DB_PASSWORD": "root",
        "DB_NAME": "dwsdb_thailand"
    }
}

# =========================================
# FASTAPI
# =========================================
app = FastAPI()

# =========================================
# REQUEST MODEL
# =========================================
class PlanRequest(BaseModel):
    plan: str

# =========================================
# MAIN CLASS
# =========================================
class AgentGUI:

    def __init__(self):

        # =========================
        # CONFIG
        # =========================
        self.config = configparser.ConfigParser()

        self.create_default_config()
        self.load_config()

        # =========================
        # STATUS
        # =========================
        self.current_plan = "Unknown"
        self.last_action = "Idle"

        # =========================
        # TKINTER
        # =========================
        self.root = tk.Tk()

        self.root.title("SCADA Agent")
        self.root.geometry("720x520")
        self.root.resizable(False, False)

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.hide_window
        )

        # =========================
        # MAIN FRAME
        # =========================
        self.main_frame = ttk.Frame(
            self.root,
            padding=10
        )

        self.main_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # =========================
        # STATUS FRAME
        # =========================
        self.status_frame = ttk.LabelFrame(
            self.main_frame,
            text="Agent Status",
            padding=10
        )

        self.status_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=5
        )

        self.lbl_server = ttk.Label(
            self.status_frame,
            text="API Server : Starting..."
        )

        self.lbl_server.grid(
            row=0,
            column=0,
            sticky="w",
            pady=3
        )

        self.lbl_db = ttk.Label(
            self.status_frame,
            text="Database : Checking..."
        )

        self.lbl_db.grid(
            row=1,
            column=0,
            sticky="w",
            pady=3
        )

        self.lbl_plan = ttk.Label(
            self.status_frame,
            text="Current Plan : Unknown"
        )

        self.lbl_plan.grid(
            row=2,
            column=0,
            sticky="w",
            pady=3
        )

        self.lbl_last = ttk.Label(
            self.status_frame,
            text="Last Action : Idle"
        )

        self.lbl_last.grid(
            row=3,
            column=0,
            sticky="w",
            pady=3
        )

        # =========================
        # LOG FRAME
        # =========================
        self.log_frame = ttk.LabelFrame(
            self.main_frame,
            text="Logs",
            padding=10
        )

        self.log_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=5
        )

        self.log_text = ScrolledText(
            self.log_frame,
            height=20,
            state="disabled"
        )

        self.log_text.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # =========================
        # LOGGING
        # =========================
        logging.basicConfig(
            filename="agent.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # =========================
        # STARTUP
        # =========================
        self.test_database()
        self.get_current_plan()

        self.start_api_thread()

        # =========================
        # TRAY
        # =========================
        self.tray_icon = None
        self.create_tray_icon()
        # START HIDDEN
        self.root.after(
            3000,
            self.hide_window
        )

    # =====================================
    # CONFIG
    # =====================================
    def create_default_config(self):

        if os.path.exists(CONFIG_FILE):
            return

        config = configparser.ConfigParser()

        for section, values in DEFAULT_CONFIG.items():

            config[section] = values

        with open(CONFIG_FILE, "w") as f:

            config.write(f)

    def load_config(self):

        self.config.read(CONFIG_FILE)

        self.API_HOST = self.config.get(
            "SERVER",
            "API_HOST"
        )

        self.API_PORT = self.config.getint(
            "SERVER",
            "API_PORT"
        )

        self.DB_HOST = self.config.get(
            "DATABASE",
            "DB_HOST"
        )

        self.DB_PORT = self.config.getint(
            "DATABASE",
            "DB_PORT"
        )

        self.DB_USER = self.config.get(
            "DATABASE",
            "DB_USER"
        )

        self.DB_PASSWORD = self.config.get(
            "DATABASE",
            "DB_PASSWORD"
        )

        self.DB_NAME = self.config.get(
            "DATABASE",
            "DB_NAME"
        )

    # =====================================
    # LOG
    # =====================================
    def add_log(self, message):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        full_message = f"[{now}] {message}"

        self.log_text.config(state="normal")

        self.log_text.insert(
            tk.END,
            full_message + "\n"
        )

        self.log_text.see(tk.END)

        self.log_text.config(state="disabled")

        logging.info(message)

    # =====================================
    # DATABASE
    # =====================================
    def get_connection(self):

        return pymysql.connect(
            host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            database=self.DB_NAME,
            charset="utf8mb4"
        )

    def test_database(self):

        try:

            conn = self.get_connection()

            conn.close()

            self.lbl_db.config(
                text=f"Database : Connected ({self.DB_NAME})"
            )

            self.add_log(
                "[SYSTEM] Database Connected"
            )

        except Exception as e:

            self.lbl_db.config(
                text="Database : Failed"
            )

            self.add_log(
                f"[DB ERROR] {e}"
            )

    # =====================================
    # GET PLAN
    # =====================================
    def get_current_plan(self):

        try:

            conn = self.get_connection()

            cursor = conn.cursor()

            sql = """
            SELECT PlanName
            FROM tab_dws_cfg_sorting_plan
            WHERE IsSelected = 1
            LIMIT 1
            """

            cursor.execute(sql)

            row = cursor.fetchone()

            conn.close()

            if row:
                self.current_plan = row[0]
            else:
                self.current_plan = "None"

            self.lbl_plan.config(
                text=f"Current Plan : {self.current_plan}"
            )

        except Exception as e:

            self.add_log(
                f"[PLAN ERROR] {e}"
            )

    # =====================================
    # SWITCH PLAN
    # =====================================
    def switch_plan(self, target_plan):

        try:

            conn = self.get_connection()

            cursor = conn.cursor()

            check_sql = """
            SELECT COUNT(*)
            FROM tab_dws_cfg_sorting_plan
            WHERE PlanName = %s
            """

            cursor.execute(
                check_sql,
                (target_plan,)
            )

            count = cursor.fetchone()[0]

            if count == 0:

                conn.close()

                self.add_log(
                    f"[FAILED] Plan not found : {target_plan}"
                )

                return {
                    "success": False,
                    "message": "Plan not found"
                }

            reset_sql = """
            UPDATE tab_dws_cfg_sorting_plan
            SET IsSelected = 0
            WHERE PlanName != %s
            """

            cursor.execute(
                reset_sql,
                (target_plan,)
            )

            activate_sql = """
            UPDATE tab_dws_cfg_sorting_plan
            SET IsSelected = 1
            WHERE PlanName = %s
            """

            cursor.execute(
                activate_sql,
                (target_plan,)
            )

            conn.commit()
            self.add_log(
                "[SYSTEM] Database Commit Success"
            )
            
            # ================================= ====
            # UPDATE CACHE
            # =====================================

            update_cache_url = (
                "http://127.0.0.1:8089/dws/cfg/plan/update/cache?dbCode=2"
            )
            try:

                response = requests.get(
                    update_cache_url,
                    timeout=30
                )

                self.add_log(
                    f"[SYSTEM] UpdateCache : {response.status_code}"
                )

                self.add_log(
                    f"[SYSTEM] Cache Response : {response.text}"
                )
            except Exception as cache_error:

                self.add_log(
                    f"[CACHE ERROR] {cache_error}"
                )

            conn.close()

            self.current_plan = target_plan

            self.lbl_plan.config(
                text=f"Current Plan : {target_plan}"
            )

            self.lbl_last.config(
                text=f"Last Action : Changed to {target_plan}"
            )

            self.add_log(
                f"[SUCCESS] Plan changed to : {target_plan}"
            )

            return {
                "success": True,
                "current_plan": target_plan
            }

        except Exception as e:

            self.add_log(
                f"[ERROR] {e}"
            )

            return {
                "success": False,
                "message": str(e)
            }

    # =====================================
    # API
    # =====================================
    def start_api_thread(self):

        threading.Thread(
            target=self.start_api,
            daemon=True
        ).start()

    def start_api(self):

        self.lbl_server.config(
            text=f"API Server : Running ({self.API_HOST}:{self.API_PORT})"
        )

        self.add_log(
            "[SYSTEM] API Server Started"
        )

        uvicorn.run(
            app,
            host=self.API_HOST,
            port=self.API_PORT,
            reload=False,
            log_config=None
        )

    # =====================================
    # TRAY
    # =====================================
    def create_image(self):

        image = Image.new(
            "RGB",
            (64, 64),
            color=(0, 120, 215)
        )

        draw = ImageDraw.Draw(image)

        draw.rectangle(
            (16, 16, 48, 48),
            fill=(255, 255, 255)
        )

        return image

    def create_tray_icon(self):

        image = self.create_image()

        menu = (
            item(
                "Show",
                self.show_window
            ),
            item(
                "Exit",
                self.exit_app
            )
        )

        self.tray_icon = pystray.Icon(
            "SCADA_AGENT",
            image,
            "SCADA Agent",
            menu
        )

        threading.Thread(
            target=self.tray_icon.run,
            daemon=True
        ).start()

    def hide_window(self):

        self.root.withdraw()

    def show_window(self):

        self.root.after(
            0,
            self.root.deiconify
        )

    def exit_app(self):

        self.tray_icon.stop()

        self.root.destroy()

        sys.exit()

    # =====================================
    # RUN
    # =====================================
    def run(self):

        self.root.mainloop()

# =========================================
# FASTAPI ROUTE
# =========================================
gui = None

@app.get("/status")
def api_status():

    return {
        "success": True,
        "current_plan": gui.current_plan,
        "message": "Agent Online"
    }

@app.get("/plans")
def api_plans():

    try:

        conn = gui.get_connection()

        cursor = conn.cursor()

        sql = """
        SELECT PlanName
        FROM tab_dws_cfg_sorting_plan
        """

        cursor.execute(sql)

        rows = cursor.fetchall()

        conn.close()

        plans = [x[0] for x in rows]

        return {
            "success": True,
            "plans": plans
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@app.post("/switch_plan")
def api_switch_plan(data: PlanRequest):

    return gui.switch_plan(data.plan)

# =========================================
# MAIN
# =========================================
if __name__ == "__main__":

    gui = AgentGUI()

    gui.run()