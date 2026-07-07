"""
API RAEE Colombia — FastAPI
Correr: uvicorn main:app --reload

Endpoints:
  GET  /tipos-raee
  GET  /puntos?lat=&lng=&radio=5000&tipo=
  GET  /puntos/{id}
  POST /reportes
  POST /entregas
"""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ── Configuración ─────────────────────────────────────────────────────────────

def _leer_env() -> tuple[str, str]:
    env_path = Path(__file__).parent.parent / "db" / ".env"
    config = {}
    if env_path.exists():
        for linea in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in linea and not linea.startswith("#"):
                k, v = linea.split("=", 1)
                config[k.strip()] = v.strip()
    url = os.environ.get("SUPABASE_URL") or config.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_KEY") or config.get("SUPABASE_SERVICE_KEY", "")
    return url.rstrip("/"), key

SUPABASE_URL, SUPABASE_KEY = _leer_env()

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="RAEEconecta API",
    description="Puntos de recolección de residuos electrónicos en Colombia — RAEEconecta",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Modelos ───────────────────────────────────────────────────────────────────

class Reporte(BaseModel):
    punto_id: int
    tipo: str  # cerrado | horario_incorrecto | direccion_incorrecta | otro
    detalle: Optional[str] = None


class Entrega(BaseModel):
    punto_id: int


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/tipos-raee", summary="Lista todos los tipos de RAEE")
async def get_tipos_raee():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/tipos_raee?select=id,nombre&order=nombre",
            headers=HEADERS,
        )
    if not resp.is_success:
        raise HTTPException(500, detail=resp.text)
    return resp.json()


@app.get("/puntos/todos", summary="Todos los puntos con coordenadas (para mapa global)")
async def get_todos_los_puntos():
    PAGE_SIZE = 1000  # límite máximo que Supabase devuelve por solicitud
    puntos = []
    offset = 0
    async with httpx.AsyncClient() as client:
        while True:
            resp = await client.get(
                f"{SUPABASE_URL}/rest/v1/v_puntos"
                "?select=id,nombre,ciudad,lat,lng,sistema,confianza_coords"
                f"&lat=not.is.null&activo=eq.true&offset={offset}&limit={PAGE_SIZE}",
                headers=HEADERS,
            )
            if not resp.is_success:
                raise HTTPException(500, detail=resp.text)
            pagina = resp.json()
            puntos.extend(pagina)
            if len(pagina) < PAGE_SIZE:
                break
            offset += PAGE_SIZE
    return puntos


@app.get("/puntos", summary="Puntos cercanos por ubicación y tipo de RAEE")
async def get_puntos(
    lat:   float = Query(..., description="Latitud del usuario"),
    lng:   float = Query(..., description="Longitud del usuario"),
    radio: int   = Query(5000, description="Radio de búsqueda en metros (default 5 km)"),
    tipo:  Optional[str] = Query(None, description="Tipo de RAEE a filtrar (ej: Pila, Celular)"),
):
    payload = {
        "_lat":          lat,
        "_lng":          lng,
        "_radio_metros": radio,
        "_tipo_raee":    tipo,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/rpc/puntos_cercanos",
            headers=HEADERS,
            json=payload,
        )
    if not resp.is_success:
        raise HTTPException(500, detail=resp.text)
    return resp.json()


@app.get("/puntos/{punto_id}", summary="Detalle de un punto")
async def get_punto(punto_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/v_puntos?id=eq.{punto_id}&select=*",
            headers=HEADERS,
        )
    if not resp.is_success:
        raise HTTPException(500, detail=resp.text)
    data = resp.json()
    if not data:
        raise HTTPException(404, detail="Punto no encontrado")
    return data[0]


@app.post("/reportes", status_code=201, summary="Reportar dato incorrecto en un punto")
async def post_reporte(reporte: Reporte):
    tipos_validos = {"cerrado", "horario_incorrecto", "direccion_incorrecta", "otro"}
    if reporte.tipo not in tipos_validos:
        raise HTTPException(400, detail=f"tipo debe ser uno de: {', '.join(tipos_validos)}")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/reportes",
            headers={**HEADERS, "Prefer": "return=minimal"},
            json=reporte.model_dump(),
        )
    if not resp.is_success:
        raise HTTPException(500, detail=resp.text)
    return {"ok": True}


@app.post("/entregas", status_code=201, summary="Registrar check-in voluntario de entrega")
async def post_entrega(entrega: Entrega):
    async with httpx.AsyncClient() as client:
        punto_resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/v_puntos?id=eq.{entrega.punto_id}&select=ciudad",
            headers=HEADERS,
        )
    if not punto_resp.is_success:
        raise HTTPException(500, detail=punto_resp.text)
    punto_data = punto_resp.json()
    if not punto_data:
        raise HTTPException(404, detail="Punto no encontrado")
    ciudad = punto_data[0].get("ciudad")

    async with httpx.AsyncClient() as client:
        ins_resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/entregas",
            headers={**HEADERS, "Prefer": "return=minimal"},
            json={"punto_id": entrega.punto_id, "ciudad": ciudad},
        )
    if not ins_resp.is_success:
        raise HTTPException(500, detail=ins_resp.text)

    conteo_zona = 0
    if ciudad:
        hace_30_dias = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        async with httpx.AsyncClient() as client:
            conteo_resp = await client.get(
                f"{SUPABASE_URL}/rest/v1/entregas"
                f"?ciudad=eq.{ciudad}&created_at=gte.{hace_30_dias}&select=id&limit=1",
                headers={**HEADERS, "Prefer": "count=exact"},
            )
        content_range = conteo_resp.headers.get("Content-Range", "0/0")
        try:
            conteo_zona = int(content_range.split("/")[-1])
        except ValueError:
            conteo_zona = 0

    return {"ok": True, "conteo_zona": conteo_zona}


@app.get("/", include_in_schema=False)
async def root():
    return {"status": "ok", "docs": "/docs"}
