"""Convert the generated GLB into a GIANTS Editor 8 import candidate (FBX).
Run with: blender --background --python Dorffeuerwache_Muehlberg/export_ge8_fbx.py
This is a GE8 import TEST, not a native I3D or a finished FS19 placeable.
"""
import bpy
import addon_utils
import os
import shutil
import zipfile

ROOT = os.getcwd()
SRC_DIR = os.path.join(ROOT, "Dorffeuerwache_Muehlberg_Nach_Zeichnung")
SOURCE = os.path.join(SRC_DIR, "Dorffeuerwache_Muehlberg_nach_Zeichnung.glb")
OUT_DIR = os.path.join(ROOT, "Muehlberg_GE8_FBX")
FBX = os.path.join(OUT_DIR, "Dorffeuerwache_Muehlberg_GE8_Test.fbx")
ZIP = os.path.join(ROOT, "Dorffeuerwache_Muehlberg_GE8_FBX_Test.zip")
os.makedirs(OUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SOURCE)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
if not meshes:
    raise RuntimeError("GLB import returned no meshes")
print("Imported", len(meshes), "meshes for GE8 FBX test")
# Blender 5 distributions may ship the FBX exporter disabled by default.
addon_utils.enable("io_scene_fbx", default_set=True)
print("FBX exporter enabled:", bpy.ops.export_scene.fbx.get_rna_type().identifier)
print("FBX props:", list(bpy.ops.export_scene.fbx.get_rna_type().properties.keys()))
# Blender 5.0's packaged FBX exporter exposes only a minimal set of options.
# Keep all PNGs next to the FBX for texture relinking in GE8.
bpy.ops.export_scene.fbx(filepath=FBX, axis_forward="-Z", axis_up="Y")
if not os.path.isfile(FBX) or os.path.getsize(FBX) < 10000:
    raise RuntimeError("FBX export failed or empty")

for filename in os.listdir(SRC_DIR):
    if filename.lower().endswith(".png"):
        shutil.copy2(os.path.join(SRC_DIR, filename), os.path.join(OUT_DIR, filename))

with open(os.path.join(OUT_DIR, "GE8_ANLEITUNG.txt"), "w", encoding="utf-8") as f:
    f.write(
        "Dorffeuerwache Muehlberg - GE8 FBX Importtest\n\n"
        "1. ZIP komplett in einen lokalen Ordner entpacken.\n"
        "2. GIANTS Editor 8.x starten.\n"
        "3. Datei > Importieren (File > Import) und die FBX auswaehlen.\n"
        "4. Bei fehlenden Texturen die PNG-Dateien aus diesem Ordner verwenden.\n"
        "5. Szene im Editor als I3D speichern und pruefen.\n\n"
        "Hinweis: FBX ist eine Test-Zwischenstufe, noch KEIN spielbereiter LS19-Mod.\n"
        "Materialien, Kollisionen und Platzierbarkeit muessen im GE8 ueberprueft werden.\n"
    )
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for filename in sorted(os.listdir(OUT_DIR)):
        archive.write(os.path.join(OUT_DIR, filename), arcname=filename)
print("GE8 FBX ZIP:", ZIP, os.path.getsize(ZIP))
