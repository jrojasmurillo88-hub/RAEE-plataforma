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

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pywebpush import WebPushException, webpush

from catalogo_pesos import calcular_peso_total


# ── Configuración ─────────────────────────────────────────────────────────────

def _leer_env() -> dict[str, str]:
    env_path = Path(__file__).parent.parent / "db" / ".env"
    config = {}
    if env_path.exists():
        for linea in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in linea and not linea.startswith("#"):
                k, v = linea.split("=", 1)
                config[k.strip()] = v.strip()
    return config

_config = _leer_env()

def _env(nombre: str, default: str = "") -> str:
    return os.environ.get(nombre) or _config.get(nombre, default)

SUPABASE_URL = _env("SUPABASE_URL").rstrip("/")
SUPABASE_KEY = _env("SUPABASE_SERVICE_KEY")
VAPID_PRIVATE_KEY = _env("VAPID_PRIVATE_KEY")
VAPID_CLAIM_EMAIL = _env("VAPID_CLAIM_EMAIL", "mailto:jrojasmurillo88@gmail.com")
CRON_SECRET = _env("CRON_SECRET")

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
    items: Optional[list[str]] = None  # ids del catálogo en catalogo_pesos.py


class Evento(BaseModel):
    tipo: str  # seleccion_punto | intencion_descarte
    punto_id: Optional[int] = None
    tipo_raee: Optional[str] = None
    session_id: Optional[str] = None


class PushSuscripcionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSuscripcion(BaseModel):
    endpoint: str
    keys: PushSuscripcionKeys


class PushProgramar(BaseModel):
    endpoint: str
    punto_id: int
    nombre_punto: str
    horas_espera: int = 24


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

    items = entrega.items or []
    peso_gramos = calcular_peso_total(items) if items else None

    payload = {"punto_id": entrega.punto_id, "ciudad": ciudad}
    if items:
        payload["items"] = items
        payload["peso_gramos"] = peso_gramos

    async with httpx.AsyncClient() as client:
        ins_resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/entregas",
            headers={**HEADERS, "Prefer": "return=minimal"},
            json=payload,
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

    return {"ok": True, "conteo_zona": conteo_zona, "peso_gramos": peso_gramos}


@app.post("/eventos", status_code=201, summary="Registrar evento de comportamiento (selección de punto, intención de descarte)")
async def post_evento(evento: Evento):
    tipos_validos = {"seleccion_punto", "intencion_descarte"}
    if evento.tipo not in tipos_validos:
        raise HTTPException(400, detail=f"tipo debe ser uno de: {', '.join(tipos_validos)}")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/eventos",
            headers={**HEADERS, "Prefer": "return=minimal"},
            json=evento.model_dump(),
        )
    if not resp.is_success:
        raise HTTPException(500, detail=resp.text)
    return {"ok": True}


# ── Notificaciones push ────────────────────────────────────────────────────────

@app.post("/push/suscribir", status_code=201, summary="Registrar una suscripción push del navegador")
async def post_push_suscribir(sub: PushSuscripcion):
    payload = {
        "endpoint": sub.endpoint,
        "p256dh": sub.keys.p256dh,
        "auth": sub.keys.auth,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/push_subscriptions",
            headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=minimal"},
            params={"on_conflict": "endpoint"},
            json=payload,
        )
    if not resp.is_success:
        raise HTTPException(500, detail=resp.text)
    return {"ok": True}


@app.post("/push/programar", status_code=201, summary="Programar el recordatorio push de check-in 24h después")
async def post_push_programar(datos: PushProgramar):
    fire_at = (datetime.now(timezone.utc) + timedelta(hours=datos.horas_espera)).isoformat()
    payload = {
        "endpoint": datos.endpoint,
        "punto_id": datos.punto_id,
        "nombre_punto": datos.nombre_punto,
        "fire_at": fire_at,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/notificaciones_programadas",
            headers={**HEADERS, "Prefer": "return=minimal"},
            json=payload,
        )
    if not resp.is_success:
        raise HTTPException(500, detail=resp.text)
    return {"ok": True}


@app.post("/push/enviar-pendientes", summary="Envía las notificaciones push cuya hora ya llegó (disparado por cron externo)")
async def post_push_enviar_pendientes(x_cron_secret: Optional[str] = Header(None)):
    if not CRON_SECRET or x_cron_secret != CRON_SECRET:
        raise HTTPException(401, detail="No autorizado")
    if not VAPID_PRIVATE_KEY:
        raise HTTPException(500, detail="VAPID_PRIVATE_KEY no configurada")

    ahora = datetime.now(timezone.utc).isoformat()
    async with httpx.AsyncClient() as client:
        pendientes_resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/notificaciones_programadas"
            f"?enviada=eq.false&fire_at=lte.{ahora}&select=*",
            headers=HEADERS,
        )
    if not pendientes_resp.is_success:
        raise HTTPException(500, detail=pendientes_resp.text)
    pendientes = pendientes_resp.json()

    enviadas, fallidas, expiradas = 0, 0, 0
    async with httpx.AsyncClient() as client:
        for n in pendientes:
            sub_resp = await client.get(
                f"{SUPABASE_URL}/rest/v1/push_subscriptions?endpoint=eq.{n['endpoint']}&select=*",
                headers=HEADERS,
            )
            sub_data = sub_resp.json() if sub_resp.is_success else []
            if not sub_data:
                await _marcar_notificacion_enviada(client, n["id"])
                fallidas += 1
                continue
            sub = sub_data[0]
            try:
                webpush(
                    subscription_info={
                        "endpoint": sub["endpoint"],
                        "keys": {"p256dh": sub["p256dh"], "auth": sub["auth"]},
                    },
                    data=json.dumps({
                        "titulo": "¿Botaste tu RAEE?",
                        "cuerpo": f"Cuéntanos si entregaste en {n.get('nombre_punto') or 'el punto que elegiste'}",
                        "puntoId": n.get("punto_id"),
                    }),
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims={"sub": VAPID_CLAIM_EMAIL},
                )
                enviadas += 1
            except WebPushException as e:
                # 404/410 = la suscripción ya no existe en el navegador (se desinstaló, etc.)
                if e.response is not None and e.response.status_code in (404, 410):
                    await client.delete(
                        f"{SUPABASE_URL}/rest/v1/push_subscriptions?endpoint=eq.{sub['endpoint']}",
                        headers=HEADERS,
                    )
                    expiradas += 1
                else:
                    fallidas += 1
            await _marcar_notificacion_enviada(client, n["id"])

    return {"ok": True, "enviadas": enviadas, "fallidas": fallidas, "suscripciones_expiradas": expiradas}


async def _marcar_notificacion_enviada(client: httpx.AsyncClient, notif_id: int):
    await client.patch(
        f"{SUPABASE_URL}/rest/v1/notificaciones_programadas?id=eq.{notif_id}",
        headers={**HEADERS, "Prefer": "return=minimal"},
        json={"enviada": True},
    )


@app.get("/", include_in_schema=False)
async def root():
    return {"status": "ok", "docs": "/docs"}
