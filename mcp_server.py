"""A minimal MCP server exposing two tools for this repository."""
 
import json
import subprocess
import sys
 
PROTOCOL_VERSION = "2024-11-05"
 
TOOLS = [
    {
        "name": "recent_commits",
        "description": "List the most recent commit subjects in this repository.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "How many to return."}
            },
        },
    },
    {
        "name": "test_summary",
        "description": "Run the unit test suite and report whether it passes.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]
 
 
def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return (result.stdout + result.stderr).strip()
 
 
def call_tool(name, arguments):
    if name == "recent_commits":
        count = arguments.get("count", 5)
        return run(["git", "log", "--oneline", "-n", str(count)])
    if name == "test_summary":
        return run([sys.executable, "-m", "unittest", "discover"])
    return "Unknown tool: " + name
 
 
def handle(request):
    method = request.get("method")
    if method == "initialize":
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "task-tracker", "version": "0.1.0"},
        }
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        params = request.get("params", {})
        text = call_tool(params.get("name"), params.get("arguments", {}))
        return {"content": [{"type": "text", "text": text}]}
    return None
 
 
def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        request = json.loads(line)
        result = handle(request)
        if request.get("id") is None:
            continue
        response = {"jsonrpc": "2.0", "id": request["id"], "result": result}
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
 
 
if __name__ == "__main__":
    main()
