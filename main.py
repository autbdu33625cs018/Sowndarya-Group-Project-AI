from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import TextRequest, TextResponse, QuizResponse

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------------------------------
# HOME PAGE
# ---------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ---------------------------------------
# HEALTH CHECK
# ---------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "success",
        "message": "EduGenie is running"
    }


# ---------------------------------------
# QUESTION ANSWERING
# ---------------------------------------

@app.post("/qa", response_model=TextResponse)
async def qa(request: TextRequest):

    try:

        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        result = answer_question(request.text)

        return {
            "answer": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------
# EXPLANATION
# ---------------------------------------

@app.post("/explain", response_model=TextResponse)
async def explain(request: TextRequest):

    try:

        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Topic cannot be empty."
            )

        result = explain_topic(request.text)

        return {
            "answer": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------
# QUIZ
# ---------------------------------------

@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: TextRequest):

    try:

        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Content cannot be empty."
            )

        questions = generate_quiz(request.text)

        return {
            "questions": questions
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------
# SUMMARY
# ---------------------------------------

@app.post("/summarize", response_model=TextResponse)
async def summarize(request: TextRequest):

    try:

        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty."
            )

        result = summarize_text(request.text)

        return {
            "answer": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------
# LEARNING PATH
# ---------------------------------------

@app.post(
    "/learn/recommendations",
    response_model=TextResponse
)
async def learning_recommendations(
    request: TextRequest
):

    try:

        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Topic cannot be empty."
            )

        result = get_learning_recommendations(
            request.text
        )

        return {
            "answer": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )