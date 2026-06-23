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
import shutil
from urllib.parse import quote
from ddgs import DDGS
import signal
import winapps

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
            "get_running_processes":self.get_running_processes,
            "kill_process":self.kill_process,
            "get_installed_apps":self.get_installed_apps,
            "get_uptime":self.get_uptime,
            "open_url": self.open_url,
            "take_screenshot": self.take_screenshot,
            "list_files": self.list_files,
            "shutdown_pc":self.shutdown_pc,
            "restart_pc":self.restart_pc,
            "log_out":self.log_out,
            "search_web":self.search_web,
            "create_file":self.create_file,
            "delete_file":self.delete_file,
            "move_file":self.move_file,
            "copy_file":self.copy_file,
            "read_file":self.read_file,
            "write_file":self.write_file,
            "rename_file":self.rename_file,
            "append_to_file":self.append_to_file
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
            subprocess.Popen("cmd.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)            
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
    
    def get_running_processes(self):
     try:
      process_list = []
      for process in psutil.process_iter(['pid', 'name']):
        try:
            proc_info = {
                "pid": process.info['pid'],
                "name": process.info['name']
            }
            process_list.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

      return {
        "status": 200,
        "response": f"Processes running in your computer: {process_list}"
      }
     except Exception as error:
          return {
                "status":404,
                "response":f"An error has occured during get of running processes: {error}",
            }
    
    def kill_process(self, pid):
        try:
         os.kill(pid, signal.SIGKILL)
         return {
             "status":200,
             "response":f"The process with pid:{pid} has successfully killed"
         }
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during kill of running process with pid:{pid} error: {error}",
            }
        
    def get_installed_apps(self):
       try:
        apps = []
        for item in winapps.list_installed():
            apps.append(item)
        return {
            "status":200,
            "response":f"The installed apps in this computer is {apps}"
        }
       except Exception as error:
           return {
                "status":404,
                "response":f"An error has occured during get of installed apps: {error}",
            }
       
    def get_uptime(self):
       try:
        up_time = psutil.boot_time()
        return {
            "status":200,
            "response":f"The uptime of the computer is {up_time}"
        }
       except Exception as error:
           return {
                "status":404,
                "response":f"An error has occured during get of uptime: {error}",
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
    
    def create_file(self,path,content):
       try:
        with open(path,"w") as f:
            f.write(content)
        return {
            "status": 200,
            "response": f"The file has created succesfull"
        }
       except Exception as error:
           return {
               "status":404,
               "response": f"Failed to create file beacuse of an error:{error}"
           }
           
    def delete_file(self,path):
       try:
        os.remove(path)
        return {
            "status":200,
            "response":f"The file {path} has deleted succesfull"
        }
       except Exception as error:
           return {
               "status":404,
               "response": f"Failed to delete file beacuse of an error:{error}"
           }

    def move_file(self,source,destination):
       try: 
        shutil.move(source,destination)
        return {
            "status":200,
            "response":f"The file has moved from {source} to {destination}"
        }
       except Exception as error:
            return {
               "status":404,
               "response": f"Failed to move file beacuse of an error:{error}"
           }
    
    def copy_file(self, source, destination):
        try:
            shutil.copy(source,destination)
            return {
                "status":200,
                "response":f"The file has copied from {source} to {destination}"
            }
        except Exception as error:
            return {
               "status":404,
               "response": f"Failed to copy file beacuse of an error:{error}"
            }

    def read_file(self,path):
       try: 
        with open(path, encoding="utf-8") as f:
            content = f.read()
        return {
                "status":200,
                "response":f"The file {path} contains: {content}"
            }
       except Exception as error:
            return {
               "status":404,
               "response": f"Failed to read file beacuse of an error:{error}"
            }

    def write_file(self,path, content):
       try: 
        with open(path,'w') as f:
            f.write(content)
        return {
                "status":200,
                "response":f"The {content} has successfully write into {path}"
            }
       except Exception as error:
            return {
               "status":404,
               "response": f"Failed to write into file beacuse of an error:{error}"
            }
       
    def append_to_file(self, path, content):
       try: 
        with open(path,'a') as f:
            f.write(content)
        return {
                "status":200,
                "response":f"The {content} has successfully append into {path}"
            }
       except Exception as error:
            return {
               "status":404,
               "response": f"Failed to append into file beacuse of an error:{error}"
            }
    
    def rename_file(self,old_name, new_name):
       try:
          os.rename(old_name,new_name)
          return {
                "status":200,
                "response":f"The file has successfully renamed to {new_name}"
            }
       except Exception as error:
           return {
               "status":404,
               "response": f"Failed to rename file beacuse of an error:{error}"
            }

    def search_web(self, query=None):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=1))
                if results:
                    return {
                        "status": 200,
                        "response": results[0]['body']
                    }
                return {
                    "status": 404,
                    "response": "Information has not finded"
                }
        except Exception as e:
            return {
                "status": 500,
                "response": f"Error during the search: {str(e)}"
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
        You are created by Grigorios Iosifidis.
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
        - get_running_processes
        - get_installed_apps
        - get_uptime
        - take_screenshot
        - shutdown_pc
        - restart_pc
        - log_out


        Available tools (With Args):
        - open_url (args: url)
        - kill_process (args: pid)
        - list_files (args: path)
        - create_file (args: path, content)
        - delete_file (args: path)
        - move_file (args: source, destination)
        - copy_file (args: source, destination)
        - read_file (args: path)
        - write_file (args: path, content)
        - rename_file (args: old_name, new_name)
        - append_to_file (args: path, content)

        Available tools (For You With Args):
        - search_web (args: query of what you want to search): If you cant awnser to something you can search it using this tool in the web


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

        self.MAX_HISTORY = 8


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
            model="qwen2.5:3b-instruct",
            messages=messages,
            options={
                "temperature": 0.2,
                "num_ctx": 1024
            }
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

    print("\n====================")
    print("📩 USER MESSAGE:", message)

    response = model.ask(message)

    print("🤖 RAW MODEL RESPONSE:", response)

    try:
        data = json.loads(response)
        print("🧠 PARSED JSON:", data)

        if "tool" in data:
            print("🔧 TOOL REQUEST:", data["tool"])
            args = data.get("args", {})
            print("📦 TOOL ARGS:", args)

            result = tools.execute(data["tool"], args)
            print("⚙️ TOOL RESULT:", result)

            result_text = result.get("response", str(result))
            model.add_tool_result(result_text)

            final_response = model.ask(f"The user originally asked: '{message}'. The tool returned: '{result_text}'. Please provide a friendly, natural language answer based on this information. Do NOT use JSON.")
            
            print("✨ FINAL RESPONSE:", final_response)
            return jsonify({"reply": final_response})

    except json.JSONDecodeError as e:
        print("❌ JSON ERROR:", e)

        return jsonify({
            "reply": response
        })
    
@server.route("/api/ai/history", methods=["GET"])
def history_endpoint():
    history = []

    user_msg = None

    for item in model.history:
        if item["role"] == "user":
            user_msg = item["content"]

        elif item["role"] == "assistant" and user_msg:
            history.append({
                "prompt": user_msg,
                "response": item["content"]
            })
            user_msg = None

    return jsonify({
        "history": history
    })

if __name__ == "__main__":
    server.run(host="0.0.0.0",port="5000")

