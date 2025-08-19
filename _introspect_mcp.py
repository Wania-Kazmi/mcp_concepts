import inspect
import mcp.server.models as models
from mcp.server import Server

print("models module:", models.__file__)
print("Options in models:", [n for n in dir(models) if "Options" in n or "Capabilities" in n])
print("Server.get_capabilities signature:")
print(inspect.signature(Server.get_capabilities))
