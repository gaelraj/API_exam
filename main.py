import json
from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse

app = FastAPI()


@app.get("/")
def root(request: Request):

    api_key = request.headers.get("x-api-key")

    if api_key != "12345678":
        return JSONResponse(
            status_code=403,
            content={"message": "Clé API non reconnue. Accès refusé."}
        )

    accept_header = request.headers.get("accept")
    if(accept_header not in ["text/html", "text/plain"]):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Type de format non supporté. Seuls 'text/html' ou 'text/plain' sont acceptés."
            }
        )

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    not_found_message = {"detail": f"Page '/{full_path}' not found"}
    return Response(content=json.dumps(not_found_message), status_code=404, media_type="application/json")

