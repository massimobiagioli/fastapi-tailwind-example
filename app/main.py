import aiofiles
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,    
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],    
)

app.add_middleware(GZipMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("pages/home.html", {"request": request})


@app.get("/data")
async def data() -> dict:
    return {"data": "Hello World"}


@app.get("/component", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("component.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, doc: UploadFile = File(...)) -> HTMLResponse:
    async with aiofiles.open(f'upload/{doc.filename}', 'wb') as out_file:
        content = await doc.read()
        await out_file.write(content)

    response = templates.TemplateResponse("base.html", {"request": request})
    response.headers['HX-Redirect'] = '/'

    return response