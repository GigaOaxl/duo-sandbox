# Pilot-PRD duo-sandbox

Testrepo für Duo, kein produktiver Code.

R-1: Die Funktion health() in src/sandbox/health.py gibt das Wörterbuch {"status": "ok"} zurück. Sie braucht keine Argumente.

R-2: slug(text: str) -> str in src/sandbox/slug.py wandelt Text in einen URL-Slug. Leerer Text ergibt einen leeren String. Umlaute werden zu ae, oe, ue, ss. Sonderzeichen werden zu einem Bindestrich. Mehrfache Bindestriche werden zu einem. Die Ausgabe hat höchstens 100 Zeichen.

R-3: src/sandbox/todo.py verwaltet eine Todo-Liste mit sqlite3. Ein Eintrag lässt sich hinzufügen, abhaken (und wieder zurücknehmen) und löschen. Die Einträge liegen in einer SQLite-Datenbank, deren Pfad der Aufrufer übergibt. Ein Eintrag bleibt erhalten, wenn die Verbindung neu geöffnet wird.

R-4: Die Version des Pakets in pyproject.toml wird von 0.1.0 auf 0.2.0 angehoben. Alle anderen Angaben der Datei bleiben unverändert.
