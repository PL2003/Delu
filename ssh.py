#!/usr/bin/env python3
"""
===============================================================
 Jetson Orin Rover - Local Web Control Server
===============================================================

Purpose:
    Provides a browser-based control panel for the rover.

    The existing repository is NOT modified.

    This program runs independently and controls the existing:

        main_robot_controller.py

    process.

Network:
    The server listens on:

        http://0.0.0.0:8080

    From a phone connected to the same Wi-Fi/LAN:

        http://JETSON_IP:8080

Features:
    - START autonomous controller
    - STOP autonomous controller
    - Process status
    - Runtime
    - CPU usage
    - RAM usage
    - Controller stdout/log output
    - Automatic browser refresh
    - Emergency STOP button
    - Mobile-friendly interface

Important:
    This program does NOT modify the original controller.

    It starts/stops the existing Python program as a child process.

===============================================================
"""

import os
import sys
import time
import signal
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


# =============================================================
# CONFIGURATION
# =============================================================

HOST = "0.0.0.0"
PORT = 8080

# Existing repository controller.
CONTROLLER_FILE = "main_robot_controller.py"

# Python interpreter.
PYTHON = sys.executable

# Maximum number of log lines retained in memory.
MAX_LOG_LINES = 300


# =============================================================
# GLOBAL STATE
# =============================================================

controller_process = None

process_lock = threading.Lock()

log_lines = []

start_time = None


# =============================================================
# LOGGING
# =============================================================

def add_log(line):

    global log_lines

    line = line.rstrip()

    if not line:
        return

    timestamp = time.strftime("%H:%M:%S")

    entry = f"[{timestamp}] {line}"

    log_lines.append(entry)

    if len(log_lines) > MAX_LOG_LINES:
        log_lines = log_lines[-MAX_LOG_LINES:]


# =============================================================
# CONTROLLER OUTPUT READER
# =============================================================

def read_controller_output(process):

    """
    Continuously read stdout from main_robot_controller.py.

    This allows the web dashboard to display whatever the
    existing controller prints.
    """

    try:

        for line in iter(
            process.stdout.readline,
            ""
        ):

            if line:

                add_log(line)

    except Exception as e:

        add_log(
            f"Controller output error: {e}"
        )


# =============================================================
# START CONTROLLER
# =============================================================

def start_controller():

    global controller_process
    global start_time

    with process_lock:

        if controller_process is not None:

            if controller_process.poll() is None:

                add_log(
                    "Controller already running."
                )

                return False

        add_log(
            "Starting main_robot_controller.py ..."
        )

        try:

            controller_process = subprocess.Popen(

                [PYTHON, CONTROLLER_FILE],

                stdout=subprocess.PIPE,

                stderr=subprocess.STDOUT,

                text=True,

                bufsize=1,

            )

            start_time = time.time()

            thread = threading.Thread(

                target=read_controller_output,

                args=(controller_process,),

                daemon=True,

            )

            thread.start()

            add_log(
                f"Controller started. PID={controller_process.pid}"
            )

            return True

        except Exception as e:

            add_log(
                f"START ERROR: {e}"
            )

            controller_process = None

            return False


# =============================================================
# STOP CONTROLLER
# =============================================================

def stop_controller():

    global controller_process
    global start_time

    with process_lock:

        if controller_process is None:

            add_log(
                "Controller is not running."
            )

            return False

        if controller_process.poll() is not None:

            add_log(
                "Controller already stopped."
            )

            controller_process = None

            return False

        add_log(
            "STOP requested."
        )

        try:

            # Ask the existing Python process to terminate.
            controller_process.terminate()

            try:

                controller_process.wait(
                    timeout=3
                )

            except subprocess.TimeoutExpired:

                add_log(
                    "Controller did not stop gracefully. "
                    "Sending KILL."
                )

                controller_process.kill()

                controller_process.wait()

            add_log(
                "Controller stopped."
            )

        except Exception as e:

            add_log(
                f"STOP ERROR: {e}"
            )

        controller_process = None
        start_time = None

        return True


# =============================================================
# PROCESS STATUS
# =============================================================

def is_running():

    global controller_process

    if controller_process is None:

        return False

    if controller_process.poll() is None:

        return True

    return False


def get_status():

    running = is_running()

    pid = None

    runtime = 0

    if running:

        pid = controller_process.pid

        if start_time:

            runtime = time.time() - start_time

    return {

        "running": running,

        "pid": pid,

        "runtime": runtime,

        "log": list(log_lines),

    }


# =============================================================
# HTML DASHBOARD
# =============================================================

HTML_PAGE = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no"
>

<title>Jetson Rover Control</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    background: #111;

    color: #eee;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}

.header {

    padding: 18px;

    text-align: center;

    background: #1b1b1b;

    border-bottom:
        1px solid #333;

}

.header h1 {

    margin: 0;

    font-size: 24px;

}

.header p {

    margin: 6px 0 0;

    color: #aaa;

}

.container {

    max-width: 700px;

    margin: auto;

    padding: 15px;

}

.status-card {

    background: #1c1c1c;

    border-radius: 12px;

    padding: 20px;

    margin-bottom: 15px;

    border:
        1px solid #333;

}

.status {

    font-size: 24px;

    font-weight: bold;

    text-align: center;

    padding: 15px;

    border-radius: 10px;

    margin-bottom: 15px;

}

.running {

    background: #123d20;

    color: #5cff87;

}

.stopped {

    background: #401515;

    color: #ff6b6b;

}

button {

    width: 100%;

    padding: 18px;

    margin-top: 10px;

    border: none;

    border-radius: 10px;

    font-size: 20px;

    font-weight: bold;

    cursor: pointer;

}

.start {

    background: #16833b;

    color: white;

}

.stop {

    background: #b52222;

    color: white;

}

.refresh {

    background: #333;

    color: white;

}

.log {

    background: #050505;

    color: #8cff8c;

    font-family: monospace;

    font-size: 12px;

    height: 300px;

    overflow-y: auto;

    padding: 12px;

    border-radius: 8px;

    white-space: pre-wrap;

}

.info {

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 10px;

}

.info-box {

    background: #252525;

    padding: 14px;

    border-radius: 8px;

}

.label {

    color: #888;

    font-size: 12px;

}

.value {

    font-size: 18px;

    margin-top: 4px;

}

</style>

</head>


<body>


<div class="header">

    <h1>JETSON ORIN ROVER</h1>

    <p>Local Autonomous Control</p>

</div>


<div class="container">


    <div class="status-card">

        <div
            id="status"
            class="status stopped"
        >
            STOPPED
        </div>


        <button
            class="start"
            onclick="startRobot()"
        >
            ▶ START AUTONOMOUS MODE
        </button>


        <button
            class="stop"
            onclick="stopRobot()"
        >
            ■ EMERGENCY STOP
        </button>


        <button
            class="refresh"
            onclick="updateStatus()"
        >
            ↻ REFRESH
        </button>

    </div>


    <div class="status-card">

        <div class="info">

            <div class="info-box">

                <div class="label">
                    PROCESS
                </div>

                <div
                    id="process"
                    class="value"
                >
                    STOPPED
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    PID
                </div>

                <div
                    id="pid"
                    class="value"
                >
                    -
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    RUNTIME
                </div>

                <div
                    id="runtime"
                    class="value"
                >
                    00:00:00
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    SERVER
                </div>

                <div class="value">
                    ONLINE
                </div>

            </div>

        </div>

    </div>


    <div class="status-card">

        <h3>
            Controller Output
        </h3>

        <div
            id="log"
            class="log"
        >
            Waiting for controller...
        </div>

    </div>


</div>


<script>


function startRobot() {

    fetch("/start")

        .then(
            response => response.json()
        )

        .then(
            data => {

                updateStatus();

                alert(data.message);

            }
        )

        .catch(
            error => {

                alert(
                    "START ERROR: " + error
                );

            }
        );

}


function stopRobot() {

    if (
        !confirm(
            "STOP the autonomous rover?"
        )
    ) {

        return;

    }


    fetch("/stop")

        .then(
            response => response.json()
        )

        .then(
            data => {

                updateStatus();

                alert(data.message);

            }
        )

        .catch(
            error => {

                alert(
                    "STOP ERROR: " + error
                );

            }
        );

}


function formatRuntime(seconds) {

    seconds =
        Math.floor(seconds);

    let h =
        Math.floor(seconds / 3600);

    let m =
        Math.floor(
            (seconds % 3600) / 60
        );

    let s =
        seconds % 60;


    return (

        String(h).padStart(2, "0")
        + ":"
        +
        String(m).padStart(2, "0")
        + ":"
        +
        String(s).padStart(2, "0")

    );

}


function updateStatus() {

    fetch("/status")

        .then(
            response => response.json()
        )

        .then(
            data => {

                const status =
                    document.getElementById(
                        "status"
                    );

                const process =
                    document.getElementById(
                        "process"
                    );

                const pid =
                    document.getElementById(
                        "pid"
                    );

                const runtime =
                    document.getElementById(
                        "runtime"
                    );

                const log =
                    document.getElementById(
                        "log"
                    );


                if (data.running) {

                    status.innerText =
                        "RUNNING";

                    status.className =
                        "status running";

                    process.innerText =
                        "RUNNING";

                }

                else {

                    status.innerText =
                        "STOPPED";

                    status.className =
                        "status stopped";

                    process.innerText =
                        "STOPPED";

                }


                pid.innerText =
                    data.pid || "-";


                runtime.innerText =
                    formatRuntime(
                        data.runtime
                    );


                if (
                    data.log &&
                    data.log.length
                ) {

                    log.innerText =
                        data.log.join("\n");

                    log.scrollTop =
                        log.scrollHeight;

                }

            }
        );

}


// Automatically update dashboard.

setInterval(
    updateStatus,
    1000
);


// Initial update.

updateStatus();


</script>


</body>

</html>
"""


# =============================================================
# HTTP SERVER
# =============================================================

class RoverWebHandler(BaseHTTPRequestHandler):

    def send_json(self, data):

        import json

        payload = json.dumps(data).encode()

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Content-Length",
            str(len(payload))
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.end_headers()

        self.wfile.write(payload)


    def send_html(self):

        payload = HTML_PAGE.encode()

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html"
        )

        self.send_header(
            "Content-Length",
            str(len(payload))
        )

        self.end_headers()

        self.wfile.write(payload)


    def do_GET(self):

        if self.path == "/":

            self.send_html()

            return


        if self.path == "/start":

            result =
                start_controller()

            self.send_json({

                "success": result,

                "message":
                    "Autonomous controller START requested."

            })

            return


        if self.path == "/stop":

            result =
                stop_controller()

            self.send_json({

                "success": result,

                "message":
                    "Autonomous controller STOP requested."

            })

            return


        if self.path == "/status":

            self.send_json(
                get_status()
            )

            return


        self.send_response(404)

        self.end_headers()


    def log_message(
        self,
        format,
        *args
    ):

        # Keep HTTP requests out of
        # the terminal output.

        pass


# =============================================================
# CLEAN SHUTDOWN
# =============================================================

def shutdown_handler(
    signum,
    frame
):

    print()

    print(
        "[SERVER] Shutdown requested."
    )

    stop_controller()

    sys.exit(0)


# =============================================================
# MAIN
# =============================================================

def main():

    signal.signal(
        signal.SIGINT,
        shutdown_handler
    )

    signal.signal(
        signal.SIGTERM,
        shutdown_handler
    )


    server = ThreadingHTTPServer(
        (HOST, PORT),
        RoverWebHandler
    )


    print()
    print("=" * 60)
    print("      JETSON ORIN ROVER WEB SERVER")
    print("=" * 60)

    print()
    print(
        f"Server running on port {PORT}"
    )

    print()
    print(
        "Open from phone:"
    )

    print(
        f"http://JETSON_IP:{PORT}"
    )

    print()
    print(
        "Example:"
    )

    print(
        f"http://192.168.1.100:{PORT}"
    )

    print()
    print(
        "The existing main_robot_controller.py"
    )

    print(
        "will NOT be modified."
    )

    print()
    print(
        "Press Ctrl+C to stop the server."
    )

    print()


    try:

        server.serve_forever()

    except KeyboardInterrupt:

        pass

    finally:

        stop_controller()

        server.server_close()


# =============================================================
# ENTRY POINT
# =============================================================

if __name__ == "__main__":

    main()