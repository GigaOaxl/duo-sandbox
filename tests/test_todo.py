"""Tests für die SQLite-basierte Todo-Liste (sandbox.todo)."""

from pathlib import Path
import tempfile
import unittest

from sandbox.todo import TodoEintrag, TodoListe


class TestTodoListe(unittest.TestCase):
    """Unittests für TodoListe mit temporärer SQLite-Datenbank."""

    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self.db_pfad = Path(self._temp_dir.name) / "test_todos.db"
        self.liste = TodoListe(self.db_pfad)

    def tearDown(self) -> None:
        self.liste.schliessen()
        self._temp_dir.cleanup()

    def test_eintrag_hinzufuegen(self) -> None:
        """A-1: Ein Eintrag lässt sich hinzufügen und ist in alle() enthalten."""
        eid = self.liste.hinzufuegen("Milch kaufen")
        self.assertIsInstance(eid, int)
        eintraege = self.liste.alle()
        self.assertEqual(len(eintraege), 1)
        self.assertEqual(
            eintraege[0],
            TodoEintrag(id=eid, text="Milch kaufen", erledigt=False),
        )

    def test_mehrere_eintraege_hinzufuegen(self) -> None:
        """Mehrere Einträge erhalten unterschiedliche IDs und werden vollständig gelistet."""
        eid1 = self.liste.hinzufuegen("Milch kaufen")
        eid2 = self.liste.hinzufuegen("Brot backen")
        self.assertNotEqual(eid1, eid2)
        texte = [e.text for e in self.liste.alle()]
        self.assertEqual(texte, ["Milch kaufen", "Brot backen"])

    def test_leerer_text_wird_abgelehnt(self) -> None:
        """Das Hinzufügen eines leeren oder nur aus Leerzeichen bestehenden Texts wirft ValueError."""
        with self.assertRaises(ValueError):
            self.liste.hinzufuegen("")
        with self.assertRaises(ValueError):
            self.liste.hinzufuegen("   ")

    def test_eintrag_abhaken(self) -> None:
        """A-2: Ein Eintrag lässt sich als erledigt abhaken."""
        eid = self.liste.hinzufuegen("Steuererklärung")
        erfolg = self.liste.abhaken(eid)
        self.assertTrue(erfolg)
        eintrag = self.liste.holen(eid)
        self.assertIsNotNone(eintrag)
        self.assertTrue(eintrag.erledigt)

    def test_eintrag_abhaken_und_zuruecknehmen(self) -> None:
        """A-2: Ein abgehakter Eintrag lässt sich wieder zurücknehmen."""
        eid = self.liste.hinzufuegen("Milch kaufen")
        self.assertTrue(self.liste.abhaken(eid))
        self.assertTrue(self.liste.holen(eid).erledigt)

        self.assertTrue(self.liste.zuruecknehmen(eid))
        eintrag = self.liste.holen(eid)
        self.assertIsNotNone(eintrag)
        self.assertFalse(eintrag.erledigt)

    def test_eintrag_loeschen(self) -> None:
        """A-3: Ein Eintrag lässt sich löschen und ist danach nicht mehr vorhanden."""
        eid = self.liste.hinzufuegen("Altpapier wegbringen")
        erfolg = self.liste.loeschen(eid)
        self.assertTrue(erfolg)
        self.assertEqual(self.liste.alle(), [])
        self.assertIsNone(self.liste.holen(eid))

    def test_persistenz_ueber_verbindungsneustart(self) -> None:
        """A-4: Einträge und ihr Status bleiben nach Schließen und erneutem Öffnen erhalten."""
        eid1 = self.liste.hinzufuegen("Milch kaufen")
        eid2 = self.liste.hinzufuegen("Brot kaufen")
        self.liste.abhaken(eid1)
        self.liste.schliessen()

        neue_liste = TodoListe(self.db_pfad)
        try:
            eintraege = neue_liste.alle()
            self.assertEqual(
                eintraege,
                [
                    TodoEintrag(id=eid1, text="Milch kaufen", erledigt=True),
                    TodoEintrag(id=eid2, text="Brot kaufen", erledigt=False),
                ],
            )
        finally:
            neue_liste.schliessen()

    def test_unbekannte_id_beim_abhaken_zuruecknehmen_loeschen_holen(self) -> None:
        """Operationen auf einer unbekannten ID geben definiert False bzw. None zurück."""
        unbekannte_id = 99999
        self.assertFalse(self.liste.abhaken(unbekannte_id))
        self.assertFalse(self.liste.zuruecknehmen(unbekannte_id))
        self.assertFalse(self.liste.loeschen(unbekannte_id))
        self.assertIsNone(self.liste.holen(unbekannte_id))

    def test_sonderzeichen_und_sql_injection_sicherheit(self) -> None:
        """Parametrisierte Abfragen speichern auch SQL-Sonderzeichen unverändert."""
        spezial_text = "'); DROP TABLE todos; --"
        eid = self.liste.hinzufuegen(spezial_text)
        eintrag = self.liste.holen(eid)
        self.assertIsNotNone(eintrag)
        self.assertEqual(eintrag.text, spezial_text)
        self.assertEqual(len(self.liste.alle()), 1)


if __name__ == "__main__":
    unittest.main()
