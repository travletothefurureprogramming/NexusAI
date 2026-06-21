from flask import Flask, render_template, request, jsonify
from ollama import chat
from ollama import ChatResponse
from PIL import ImageGrab
import webbrowser
import json
import psutil
import time
import os
import subprocess
import datetime


server = Flask(__name__)



class Tools:
    def __init__(self):
        self.tools = {
            "open_chrome": self.open_chrome,
            "open_calculator":self.open_calculator,
            "open_file_explorer":self.open_explorer,
            "open_notepad":self.open_notepad,
            "open_task_manager":self.open_task_manager,
            "open_cmd":self.open_cmd,
            "get_cpu": self.get_cpu,
            "get_ram": self.get_ram,
            "get_disk_io_counters":self.get_disk_io_counters,
            "get_disk_usage":self.get_disk_usage,
            "get_network_usage":self.get_network_usage,
            "open_url": self.open_url,
            "take_screenshot": self.take_screenshot,
            "list_files": self.list_files,
            "shutdown_pc":self.shutdown_pc,
            "restart_pc":self.restart_pc,
            "log_out":self.log_out
        }
    
    def open_chrome(self):
        try:
         webbrowser.open("https://google.com")
         return {
             "status":200,
             "response":"Chrome opened successfully"
         }
        except Exception as error:
            return {
             "status":404,
             "response":f"Chrome has not opened successfully beacuse of an error: {error}",
            }
        
    def open_calculator(self):
        try:
         subprocess.Popen("calc.exe")
         return {
             "status":200,
             "response":"Calculator opened successfully"
         }
        except Exception as error:
            return {
             "status":404,
             "response":f"Calculator has not opened successfully beacuse of an error: {error}",
            }
    
    def open_notepad(self):
        try:
           subprocess.Popen("notepad.exe")
           return {
             "status":200,
             "response":"Notepad opened successfully"
           }
        except Exception as error:
            return {
             "status":404,
             "response":f"Notepad has not opened successfully beacuse of an error: {error}",
            }
        
    def open_explorer(self):
        try:
           subprocess.Popen("explorer.exe")
           return {
             "status":200,
             "response":"File Explorer opened successfully"
           }
        except Exception as error:
            return {
             "status":404,
             "response":f"File Explorer has not opened successfully beacuse of an error: {error}",
            }
        
    def open_task_manager(self):
        try:
            subprocess.Popen("taskmgr.exe")           
            return {
             "status":200,
             "response":"Task Manager opened successfully"
           }
        except Exception as error:
            return {
             "status":404,
             "response":f"Task Manager has not opened successfully beacuse of an error: {error}",
            }
    
    def open_cmd(self):
        try:
            subprocess.Popen("cmd.exe")           
            return {
             "status":200,
             "response":"Terminal opened successfully"
           }
        except Exception as error:
            return {
             "status":404,
             "response":f"Terminal has not opened successfully beacuse of an error: {error}",
            }
    
    
        
    def get_cpu(self):
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            return {
             "status":200,
             "response":f"Computer's CPU usage is {cpu}%"
            }
        except Exception as error:
            return {
             "status":404,
             "response":f"An error has occured during get of CPU usage: {error}",
            }
    
    def get_ram(self):
        try:
            ram = psutil.virtual_memory().percent
            return {
                "status": 200,
                "response":f"Computer's RAM usage is {ram}%"
            }
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during get of RAM usage: {error}",
            }
    
    def get_disk_io_counters(self):
        try:
            disk_write1 = psutil.disk_io_counters().write_bytes
            disk_read1 = psutil.disk_io_counters().read_bytes

            time.sleep(1)

            disk_write2 = psutil.disk_io_counters().write_bytes
            disk_read2 = psutil.disk_io_counters().read_bytes

            write_per_sec = disk_write2 - disk_write1
            read_per_sec = disk_read2 - disk_read1
            
            return {
                "status": 200,
                "response":f"Computer's disk io counters is Write:{write_per_sec} per second ,Read:{read_per_sec} per second."
            }
        
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during get of disk io counters: {error}",
            }
    

    def get_disk_usage(self):
        try:
            disk_usage = psutil.disk_usage(os.path.abspath(os.sep)).percent
            return {
                "status": 200,
                "response":f"Computer's disk usage is {disk_usage}%"
            }
        
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during get of disk usage: {error}",
            }

    def get_network_usage(self):
        try:
            bytes_sent1 = psutil.net_io_counters().bytes_sent
            bytes_recv1 = psutil.net_io_counters().bytes_recv

            time.sleep(1)

            bytes_sent2 = psutil.net_io_counters().bytes_sent
            bytes_recv2 = psutil.net_io_counters().bytes_recv

            bytes_sent_per_sec = bytes_sent2 - bytes_sent1
            bytes_recv_per_sec = bytes_recv2 - bytes_recv1

            return {
                "status": 200,
                "response":f"Computer's network io counters is Sent:{bytes_sent_per_sec} per second , Recv:{bytes_recv_per_sec} per second."
            }
        
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during get of network usage: {error}",
            }
        
    def open_url(self,url):
        try:
          webbrowser.open(url)
          return {
                "status": 200,
                "response":f"The url:{url} has oppended succesfull."
            }
        
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during opening of url:{url} error:{error}",
            }

    def take_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot.save(f"screenshot_{timestamp}.png")

            return {
                "status": 200,
                "response":f"The screenshot has succesfully taken and saved as screenshot.png"
            }
        
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during taken of screenshot:{error}",
            }
        
    def shutdown_pc(self):
        try:
            subprocess.run(["shutdown", "/s", "/t", "0"])

            return {
                "status": 200,
                "response": "Computer is shutting down."
            }

        except Exception as error:
            return {
                "status": 404,
                "response": f"Failed to shutdown computer: {error}"
            }
    
    def restart_pc(self):
        try:
            subprocess.run(["shutdown", "/r", "/t", "0"])

            return {
                "status": 200,
                "response": "Computer is restarting."
            }

        except Exception as error:
            return {
                "status": 404,
                "response": f"Failed to restart computer: {error}"
            }
    
    def log_out(self):
        try:
            subprocess.run(["shutdown", "/l"])


            return {
                "status": 200,
                "response": "User is loged out."
            }

        except Exception as error:
            return {
                "status": 404,
                "response": f"Failed to log out user: {error}"
            }
    
    def list_files(self, path):
      if os.path.exists(path):
       try:
        
        files = os.listdir(path)

        return {
            "status": 200,
            "response": f"Here is the files of {path}.\n{files}"
        }
       except Exception as error:
           return {
               "status":404,
               "response": f"Failed to list the files of {path} beacuse of an error:{error}"
           }
      else:
        return {
            "status": 404,
            "response": f"This path dont exist please select a valid one."
        }
    
    def execute(self,tool,args=None):
        if tool not in self.tools:
            return {
                "status": 404,
                "error": f"Unknown tool: {tool}"
            }
        if args:
            return self.tools[tool](**args)
        else:
            return self.tools[tool]()

tools = Tools()

class AI:

    def __init__(self):
        self.system_prompt = """
        You are NexusAI, a local desktop assistant.
        Be concise.

        Available tools (Without Args):
        - open_chrome
        - open_calculator
        - open_notepad
        - open_file_explorer
        - open_task_manager
        - open_cmd
        - get_cpu
        - get_ram
        - get_disk_io_counters
        - get_disk_usage
        - get_network_usage
        - take_screenshot
        - shutdown_pc
        - restart_pc
        - log_out


        Available tools (With Args):
        - open_url (args: url)
        - list_files (args: path)

        If a tool is needed answer ONLY in JSON:

        {
            "tool": "tool_name"
        }

        If a tool needs extra arguments answer ONLY in JSON:

        {
            "tool": "tool_name",
            "args": {
                "arg_name":"arg"
            }
        }

        When the execution of the tool has finished you will get the results wich you must tell it in the user

        Else response normally.
        Dont forget to be as concise as you can.
        """
        self.history = [

        ]

        self.MAX_HISTORY = 20


    def add_tool_result(self, result):
        self.history.append({
            "role": "system",
            "content": f"Tool result: {result}"
        })

    def ask(self, prompt):
        

        self.history.append({
            "role": "user",
            "content": prompt
        })


        if len(self.history) > self.MAX_HISTORY:
            self.history = self.history[-self.MAX_HISTORY:]

        messages = [
        {
            "role": "system",
            "content": self.system_prompt
        }
        ]

        messages.extend(self.history)

        response = chat(
            model="qwen3:8b",
            messages=messages
        )

        self.history.append({
            "role": "assistant",
            "content": response["message"]["content"]
        })


        return response["message"]["content"]

model = AI()

@server.route("/")
def web_site():
    return render_template("index.html")

@server.route("/api/ai", methods=["POST", "GET"])
def ai_endpoint():
    if request.method == "GET":
        return jsonify(
        {
         "status": 405,
         "error": "Method Not Allowed",
         "message": "The GET method is not supported for this endpoint. Please use POST.",
         "allowed_methods": ["POST"]
        
        }
        )
    
    else:
        message = request.json["message"]

        response = model.ask(message)

        try:
            data = json.loads(response)

            if "tool" in data:
                args = data.get("args", {})

                result = tools.execute(data["tool"], args)

                model.add_tool_result(result["response"])

                response = model.ask(
                    "Explain the tool result to the user."
                )

                return jsonify({
                    "type": "message",
                    "content": response
                })

        except json.JSONDecodeError:
            return jsonify({
                "type": "message",
                "content": response
            })

