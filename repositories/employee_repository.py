import sqlite3
from datetime import datetime, timezone, date
from typing import List, Optional
from repositories.base import IRepository
from models.employee import Employee

class EmployeeRepository(IRepository[Employee]):
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
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    location TEXT NOT NULL,
                    organisation_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (organisation_id) REFERENCES organisations(id)
                )
            """)
            conn.commit()
    
    def _row_to_entity(self, row: sqlite3.Row) -> Employee:
        return Employee(
            id=row['id'],
            name=row['name'],
            last_name=row['last_name'],
            age=row['age'],
            date_of_birth=date.fromisoformat(row['date_of_birth']),
            location=row['location'],
            organisation_id=row['organisation_id'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )
    
    def get_all(self) -> List[Employee]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_id(self, id: int) -> Optional[Employee]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
    
    def create(self, entity: Employee) -> Employee:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now(timezone.utc)
            
            cursor.execute("""
                INSERT INTO employees (name, last_name, age, date_of_birth, location, organisation_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entity.name,
                entity.last_name,
                entity.age,
                entity.date_of_birth.isoformat(),
                entity.location,
                entity.organisation_id,
                now.isoformat(),
                now.isoformat()
            ))
            
            entity.id = cursor.lastrowid
            entity.created_at = now
            entity.updated_at = now
            conn.commit()
            
            return entity
    
    def update(self, id: int, entity: Employee) -> Optional[Employee]:
        existing = self.get_by_id(id)
        if not existing:
            return None
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now(timezone.utc)
            
            cursor.execute("""
                UPDATE employees
                SET name = ?, last_name = ?, age = ?, date_of_birth = ?, location = ?, organisation_id = ?, updated_at = ?
                WHERE id = ?
            """, (
                entity.name,
                entity.last_name,
                entity.age,
                entity.date_of_birth.isoformat(),
                entity.location,
                entity.organisation_id,
                now.isoformat(),
                id
            ))
            
            conn.commit()
            
        return self.get_by_id(id)
    
    def delete(self, id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
