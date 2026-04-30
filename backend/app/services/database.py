"""
PostgreSQL integration using asyncpg.
"""
import asyncpg
import json
from app.config import settings

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                dsn=settings.DATABASE_URL,
                min_size=2,
                max_size=10,
            )
            await _create_table()
            print("[DB] PostgreSQL connected.")
        except Exception as e:
            print(f"[DB] Connection failed: {e}")
            print("[DB] Running without database (results not saved).")
            _pool = None
    return _pool


async def _create_table():
    pool = await get_pool()
    if not pool:
        return
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS text_scans (
                id               SERIAL PRIMARY KEY,
                scan_id          TEXT UNIQUE NOT NULL,
                verdict          TEXT,
                threat_level     TEXT,
                confidence       FLOAT,
                confidence_level TEXT,
                agreement_score  INTEGER,
                stability_score  FLOAT,
                signals          JSONB,
                linguistic_profile JSONB,
                word_count       INTEGER,
                processing_time  TEXT,
                text_preview     TEXT,
                created_at       TIMESTAMPTZ DEFAULT NOW()
            );
            
            -- Ensure existing tables have new columns
            ALTER TABLE text_scans ADD COLUMN IF NOT EXISTS confidence_level TEXT;
            ALTER TABLE text_scans ADD COLUMN IF NOT EXISTS agreement_score  INTEGER;
            ALTER TABLE text_scans ADD COLUMN IF NOT EXISTS stability_score  FLOAT;
            ALTER TABLE text_scans ADD COLUMN IF NOT EXISTS stylometric_details JSONB;
        """)


async def save_scan(
    scan_id: str,
    verdict: str,
    threat_level: str,
    confidence: float,
    confidence_level: str,
    agreement_score: int,
    stability_score: float,
    signals: dict,
    linguistic_profile: dict,
    stylometric_details: dict,
    word_count: int,
    processing_time: str,
    text_preview: str,
):
    pool = await get_pool()
    if not pool:
        print("[DB] No database — skipping save.")
        return

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO text_scans
                (scan_id, verdict, threat_level, confidence,
                 confidence_level, agreement_score, stability_score,
                 signals, linguistic_profile, stylometric_details,
                 word_count, processing_time, text_preview)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
            ON CONFLICT (scan_id) DO NOTHING;
        """,
            scan_id, verdict, threat_level, confidence,
            confidence_level, agreement_score, stability_score,
            json.dumps(signals),
            json.dumps(linguistic_profile),
            json.dumps(stylometric_details),
            word_count, processing_time, text_preview
        )


async def get_scan_history(limit: int = 50) -> list:
    pool = await get_pool()
    if not pool:
        return []
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT scan_id, verdict, threat_level, confidence,
                   word_count, text_preview, created_at
            FROM text_scans
            ORDER BY created_at DESC
            LIMIT $1;
        """, limit)
        return [dict(r) for r in rows]


async def get_scan_by_id(scan_id: str) -> dict:
    pool = await get_pool()
    if not pool:
        return {}
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM text_scans WHERE scan_id = $1", scan_id
        )
        return dict(row) if row else {}
