# Dorffeuerwache Mühlberg für LS19 (3D-Modell)

Dies ist ein **3D-Außenmodell nach der bereitgestellten Zeichnung**, noch **kein fertiger platzierbarer FS19-Mod**.

## Download der fertigen 3D-Dateien

1. Öffne [GitHub Actions: Dorffeuerwache Muehlberg 3D Download](https://github.com/Paul3409/fs19/actions/workflows/muehlberg-3d.yml).
2. Öffne den neuesten erfolgreichen Durchlauf.
3. Unter **Artifacts** lade `Dorffeuerwache_Muehlberg_3D_mit_Texturen` herunter.
4. Entpacke die Datei. Darin liegt das Modell als GLB (Texturen eingebettet), OBJ, MTL und PNG-Texturen.

Falls noch kein Lauf vorhanden ist: Rechts oben **Run workflow** auswählen und starten. Der Download ist nach erfolgreichem Lauf verfügbar. Für GitHub-Artefakte ist eine Anmeldung erforderlich.

## Selber bauen

Python 3.11, `pip install numpy pillow trimesh scipy` und anschließend:

```bash
python Dorffeuerwache_Muehlberg/Muehlberg_3D_Generator.py
```

Die Datei `Dorffeuerwache_Muehlberg_Nach_Zeichnung_3D.zip` wird im aktuellen Verzeichnis erzeugt.

Blender 2.93: **Datei → Importieren → glTF 2.0 (.glb)**.

Drei Doppeltore, roter Klinker, Schlauchturm, Dachreiter, Fenster und rückwärtiger Anbau. Die Rekonstruktion ist angenähert, ohne Innenräume, Toranimation oder LS19-Kollisionen.
