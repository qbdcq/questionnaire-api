from fastapi import FastAPI, HTTPException
import psycopg
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DB_URL = os.environ["DATABASE_URL"]

print("DB_URL prefix:", DB_URL[:15])

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
            detail=f"{type(e).__name__}: {str(e)}"
        )
