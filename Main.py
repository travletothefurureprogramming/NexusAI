from flask import Flask, render_template, request, jsonify
from ollama import chat
from ollama import ChatResponse
import webbrowser
import json
import psutil
import time
from PIL import ImageGrab


server = Flask(__name__)

class Tools:
    def __init__(self):
        self.tools = {
            "open_chrome": self.open_chrome,
            "get_cpu": self.get_cpu,
            "get_ram": self.get_ram,
            "get_disk_io_counters":self.get_disk_io_counters,
            "get_disk_usage":self.get_disk_usage,
            "get_network_usage":self.get_network_usage,
            "open_url": self.open_url,
            "take_screenshot": self.take_screenshot
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
            disk_usage = psutil.disk_usage("C:/").percent
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
            screenshot.save("screenshot.png")

            return {
                "status": 200,
                "response":f"The screenshot has succesfully taken and saved as screenshot.png"
            }
        
        except Exception as error:
            return {
                "status":404,
                "response":f"An error has occured during taken of screenshot:{error}",
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

        Available tools(Without Args):
        - open_chrome
        - get_cpu
        - get_ram
        - get_disk_io_counters
        - get_disk_usage
        - get_network_usage
        - take_screenshot

        Available tools (With Args):
        - open_url (args: url)

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

        Else response normally.
        Dont forget to be concise.
        """

    def ask(self, prompt):

        response = chat(
            model="qwen3:8b",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

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

                return jsonify({
                    "type": "tool_result",
                    "result": result
                })

        except json.JSONDecodeError:
            return jsonify({
                "type": "message",
                "content": response
            })

