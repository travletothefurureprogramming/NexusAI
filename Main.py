from flask import Flask, render_template, request, jsonify
from ollama import chat
from ollama import ChatResponse
import webbrowser
import json

server = Flask(__name__)

class Tools:
    def __init__(self):
        self.tools = {
            "open_chrome": self.open_chrome
        }
    
    def open_chrome(self):
        try:
         webbrowser.open("https://google.com")
         return {
             "code":200,
             "response":"Chrome opened successfully"
         }
        except Exception as error:
            return {
             "code":200,
             "response":"Chrome opened successfully",
             "error":error
            }
        
    def execute(self,tool):
        if tool not in self.tools:
            return {
                "code": 404,
                "error": f"Unknown tool: {tool}"
            }
        return self.tools[tool]()

tools = Tools()

class AI:

    def __init__(self):
        self.system_prompt = """
        You are NexusAI, a local desktop assistant.
        Be concise.

        Available tools:
        - open_chrome
        - get_cpu

        If a tool is needed answer ONLY in JSON:

        {
            "tool": "tool_name"
        }
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
                result = tools.execute(data["tool"])

                return jsonify({
                    "type": "tool_result",
                    "result": result
                })

        except json.JSONDecodeError:
            return jsonify({
                "type": "message",
                "content": response
            })

