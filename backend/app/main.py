import psycopg
from fastapi import FastAPI, HTTPException

from .config import DATABASE_URL
from .routers import auth


app = FastAPI(title="Crime Map API")

app.include_router(auth.router)


@app.get("/")
def root():
    return {"pesan": "Crime Map API berjalan"}


@app.get("/health")
def health():
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            postgis = conn.execute(
                "SELECT PostGIS_Version()"
            ).fetchone()[0]

            total = conn.execute(
                "SELECT COUNT(*) FROM crime_incidents"
            ).fetchone()[0]

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database belum siap: {e}"
        )

    return {
        "status": "ok",
        "postgis": postgis,
        "jumlah_kejadian": total
    }