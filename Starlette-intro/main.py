from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from db import get_all_students

templates = Jinja2Templates(directory="templates")

async def html_endpoint(request: Request):
    student_name = request.query_params.get("student_name") or "default name" # ... getting querry parameters
    students=get_all_students()
    context = {"request":request, "name":student_name, "students":students}

    return templates.TemplateResponse("index.html", context)

async def plain_text_endpoint(request: Request):
    student_id = request.path_params.get("student_id", "default_id") # ............ getting path parameters
    return PlainTextResponse(content=f"hello mf world, Mr. {student_id}")

async def json_endpoint(request: Request):
    # http://localhost:8000/?student_name=Maverick%20The%20Dude
    student_name = request.query_params.get("student_name") or "default name" # ... getting querry parameters
    return JSONResponse({"message": f"Hello, {student_name}!"})

async def create_students(request: Request):
    # context={"request":request}
    context={"request":request, "name":'generated name'}
    return templates.TemplateResponse("create.html", context)

routes = [
    Route("/", endpoint=json_endpoint),
    Route("/plain/{student_id:int}/", endpoint=plain_text_endpoint), # ............ getting path parameters
    Route("/plain", endpoint=plain_text_endpoint),
    Route("/html", endpoint=html_endpoint),
    Route('/create_students', endpoint=create_students, methods=["GET","POST"])
]
app = Starlette(
    routes=routes,
    debug=True
)