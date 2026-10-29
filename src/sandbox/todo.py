"""SQLite-basierte Todo-Listen-Verwaltung."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3


@dataclass(frozen=True)
class TodoEintrag:
    """Repräsentiert einen einzelnen Eintrag in der Todo-Liste."""

    id: int
    text: str
    erledigt: bool = False

    def __getitem__(self, key: str) -> int | str | bool:
        if key in ("id", "text", "erledigt"):
            return getattr(self, key)
        raise KeyError(key)


class TodoListe:
    """Verwaltet eine Todo-Liste in einer SQLite-Datenbank."""

    def __init__(self, pfad: str | Path) -> None:
        self._pfad = Path(pfad)
        self._conn = sqlite3.connect(self._pfad)
        self._initialisiere_tabelle()

    def _initialisiere_tabelle(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    erledigt INTEGER NOT NULL DEFAULT 0
                )
                """
            )

    def hinzufuegen(self, text: str) -> int:
        """Fügt einen neuen Eintrag hinzu und gibt dessen ID zurück."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Der Text eines Todo-Eintrags darf nicht leer sein.")
        with self._conn:
            cursor = self._conn.execute(
                "INSERT INTO todos (text, erledigt) VALUES (?, ?)",
                (text, 0),
            )
            return int(cursor.lastrowid)

    def abhaken(self, eid: int) -> bool:
        """Markiert den Eintrag mit der gegebenen ID als erledigt.

        Gibt True zurück, wenn der Eintrag existiert hat, sonst False.
        """
        with self._conn:
            cursor = self._conn.execute(
                "UPDATE todos SET erledigt = ? WHERE id = ?",
                (1, eid),
            )
            return cursor.rowcount > 0

    def zuruecknehmen(self, eid: int) -> bool:
        """Markiert den Eintrag mit der gegebenen ID wieder als unerledigt.

        Gibt True zurück, wenn der Eintrag existiert hat, sonst False.
        """
        with self._conn:
            cursor = self._conn.execute(
                "UPDATE todos SET erledigt = ? WHERE id = ?",
                (0, eid),
            )
            return cursor.rowcount > 0

    def loeschen(self, eid: int) -> bool:
        """Löscht den Eintrag mit der gegebenen ID.

        Gibt True zurück, wenn der Eintrag gelöscht wurde, sonst False.
        """
        with self._conn:
            cursor = self._conn.execute(
                "DELETE FROM todos WHERE id = ?",
                (eid,),
            )
            return cursor.rowcount > 0

    def holen(self, eid: int) -> TodoEintrag | None:
        """Gibt den Eintrag mit der gegebenen ID zurück oder None, falls unbekannt."""
        cursor = self._conn.execute(
            "SELECT id, text, erledigt FROM todos WHERE id = ?",
            (eid,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return TodoEintrag(id=row[0], text=row[1], erledigt=bool(row[2]))

    def alle(self) -> list[TodoEintrag]:
        """Gibt alle Einträge der Todo-Liste zurück."""
        cursor = self._conn.execute(
            "SELECT id, text, erledigt FROM todos ORDER BY id ASC"
        )
        return [
            TodoEintrag(id=row[0], text=row[1], erledigt=bool(row[2]))
            for row in cursor.fetchall()
        ]

    def schliessen(self) -> None:
        """Schließt die Datenbankverbindung explizit."""
        self._conn.close()

    def __enter__(self) -> TodoListe:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.schliessen()
