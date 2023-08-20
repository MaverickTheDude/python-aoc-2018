from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from db import (get_all_students, 
                create_a_student, 
                get_a_student_by_id,
                update_student_data,
                delete_student_data
)


'''
https://www.youtube.com/watch?v=jJXNchoT-gU
https://code.likeagirl.io/building-a-web-application-with-starlette-and-uvicorn-a-beginners-tutorial-24eb43360594
'''

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
    if request.method == "POST":
        student_data=await request.form()
        
        create_a_student(student_data)
        print("entered student data: ", student_data)
        
        return RedirectResponse(request.url_for("html_endpoint"), status_code=303)

    context={"request":request, "name":'default name (test)'}
    return templates.TemplateResponse("create.html", context)

async def update_a_student(request: Request):
    student_id=request.path_params.get("student_id")
    student_to_update=get_a_student_by_id(student_id)

    if request.method == "POST":
        student_update_data = await request.form() # without await returns object pointer instead of the dict

        update_student_data(student_id, student_update_data)
        print("UPDATED STUDENT DATA: ", student_update_data)
        return RedirectResponse(request.url_for("html_endpoint"), status_code=303)

    context = {"request": request, "student": student_to_update}
    print("student: ", student_to_update)
    return templates.TemplateResponse("update.html", context)

async def delete_student(request: Request):
    student_id=request.path_params.get("student_id")

    delete_student_data(student_id)

    return RedirectResponse(request.url_for("html_endpoint"), status_code=303)


routes = [
    Route("/json", endpoint=json_endpoint),
    Route("/plain/{student_id:int}/", endpoint=plain_text_endpoint), # ............ getting path parameters
    Route("/plain", endpoint=plain_text_endpoint),
    Route("/", endpoint=html_endpoint),
    Route("/create_students", endpoint=create_students, methods=["GET","POST"]),
    Route("/update_student/{student_id:int}/", endpoint=update_a_student, methods=["GET", "POST"]),
    Route("/delete/{student_id:int}/", endpoint=delete_student, methods=["GET", "DELETE"])
]
app = Starlette(
    routes=routes,
    debug=True
)