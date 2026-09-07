import sys
import os
import traceback

try:
    from app.main import app
except Exception as e:
    err_msg = traceback.format_exc()
    print(f"Error importing app.main: {err_msg}", file=sys.stderr)
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    
    app = FastAPI()
    
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(full_path: str = ""):
        return PlainTextResponse(
            f"Vercel Startup Error:\n{err_msg}\n\nWorking dir: {os.getcwd()}\nPython path: {sys.path}",
            status_code=500
        )
