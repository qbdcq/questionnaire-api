import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg

app = FastAPI()
load_dotenv()

DB_URL = os.environ["DATABASE_URL"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


@app.post("/api/questionnaire")
def submit_questionnaire(data: dict):
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO questionnaire
                    (device_id, rating, gender)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        data["device_id"],
                        data["rating"],
                        data["gender"]
                    )
                )

        return {
            "success": True,
            "message": "提交成功"
        }

    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"缺少字段: {e.args[0]}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="服务器内部错误"
        )