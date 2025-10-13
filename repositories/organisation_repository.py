import sqlite3
import json
from datetime import datetime, timezone
from typing import List, Optional
from repositories.base import IRepository
from models.entity import Organisation

class OrganisationRepository(IRepository[Organisation]):
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS organisations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    details TEXT,
                    name TEXT NOT NULL,
                    tags TEXT,
                    updated_at TEXT NOT NULL,
                    url TEXT
                )
            """)
            conn.commit()
    
    def _row_to_entity(self, row: sqlite3.Row) -> Organisation:
        return Organisation(
            id=row['id'],
            name=row['name'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']),
            details=row['details'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            url=row['url']
        )
    
    def get_all(self) -> List[Organisation]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM organisations")
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_id(self, id: int) -> Optional[Organisation]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM organisations WHERE id = ?", (id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
    
    def create(self, entity: Organisation) -> Organisation:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now(timezone.utc)
            
            cursor.execute("""
                INSERT INTO organisations (created_at, details, name, tags, updated_at, url)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                now.isoformat(),
                entity.details,
                entity.name,
                json.dumps(entity.tags),
                now.isoformat(),
                entity.url
            ))
            
            entity.id = cursor.lastrowid
            entity.created_at = now
            entity.updated_at = now
            conn.commit()
            
            return entity
    
    def update(self, id: int, entity: Organisation) -> Optional[Organisation]:
        existing = self.get_by_id(id)
        if not existing:
            return None
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now(timezone.utc)
            
            cursor.execute("""
                UPDATE organisations
                SET name = ?, details = ?, tags = ?, url = ?, updated_at = ?
                WHERE id = ?
            """, (
                entity.name,
                entity.details,
                json.dumps(entity.tags),
                entity.url,
                now.isoformat(),
                id
            ))
            
            conn.commit()
            
        return self.get_by_id(id)
    
    def delete(self, id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM organisations WHERE id = ?", (id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
