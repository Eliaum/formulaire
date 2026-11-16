"""Crée un petit jeu d'images synthétiques pour tester le notebook de bout en bout.

Le jeu reproduit volontairement les pièges rencontrés avec le jeu PlantVillage d'origine :
copie imbriquée (doublons), ancien dossier ``train/``, fichier corrompu, fichier sans extension
et classe trop petite.

Usage : python creer_donnees_test.py <dossier_de_sortie>
"""

import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

CLASSES = {
    "Pepper__bell___healthy": (40, 160, 40),
    "Potato___Early_blight": (150, 100, 30),
    "Tomato_Leaf_Mold": (60, 60, 170),
}
IMAGES_PAR_CLASSE = 24


def creer(racine: Path) -> None:
    rng = np.random.default_rng(0)
    for nom, couleur in CLASSES.items():
        dossier = racine / nom
        dossier.mkdir(parents=True)
        for i in range(IMAGES_PAR_CLASSE):
            pixels = np.clip(np.array(couleur) + rng.normal(0, 25, (80, 80, 3)), 0, 255)
            Image.fromarray(pixels.astype("uint8")).save(dossier / f"{nom[:6]}_{i:03d}.JPG")

    # Copie imbriquée : ses images doivent être ignorées comme doublons.
    shutil.copytree(racine / "Pepper__bell___healthy", racine / "PlantVillage" / "Pepper__bell___healthy")
    # Ancien dossier train/ : ses images doivent être reprises dans leur classe.
    ancien = racine / "train" / "Tomato_Leaf_Mold"
    ancien.mkdir(parents=True)
    for i in range(4):
        Image.fromarray(np.full((80, 80, 3), CLASSES["Tomato_Leaf_Mold"], "uint8")).save(
            ancien / f"old_{i}.JPG"
        )
    # Fichiers à écarter.
    (racine / "Tomato_Leaf_Mold" / "corrompu.jpg").write_bytes(b"pas une image")
    autre = racine / "Tomato__Tomato_YellowLeaf__Curl_Virus"
    autre.mkdir()
    (autre / "svn-r6Yb5c").write_bytes(b"x")
    # Classe trop petite : doit être écartée avec un avertissement.
    petite = racine / "Potato___healthy"
    petite.mkdir()
    for i in range(3):
        Image.fromarray(np.zeros((80, 80, 3), "uint8")).save(petite / f"s{i}.png")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sortie = Path(sys.argv[1])
    if sortie.exists():
        sys.exit(f"{sortie} existe déjà.")
    creer(sortie)
    print(f"Jeu de test créé dans {sortie}")
