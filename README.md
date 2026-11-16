# formulaire

Ce dépôt contient **deux travaux indépendants** :

1. **Une application Django « Alerte et investigation »** (mai 2023) : un formulaire web pour saisir des alertes sanitaires (source, horaires, équipe d'investigation) et les enregistrer en base.
2. **Un notebook Google Colab**, [`Modele_InceptionV3_et_MobileNetV2.ipynb`](Modele_InceptionV3_et_MobileNetV2.ipynb) (mai 2024) : classification d'images de feuilles du jeu PlantVillage par apprentissage par transfert avec InceptionV3 et MobileNetV2.

> **État du dépôt (vérifié le 16/11/2026)**
> - **Application Django** : elle ne démarre pas telle quelle, car le projet hôte est absent et un import est cassé. Une fois intégrée dans un projet, la page s'affiche, mais **le formulaire est refusé à chaque soumission** et aucune alerte n'est jamais enregistrée. Voir [§ 1.4](#14-état-vérifié) et [§ 1.5](#15-problèmes-connus).
> - **Notebook** : il dépend d'un Google Drive privé. Les résultats enregistrés ne portent que sur **4 classes sur les 15 prévues**, et il n'a **jamais été évalué sur un jeu de test**. Voir [§ 2.5](#25-limites-et-interprétation).

## Sommaire

- [Contenu du dépôt](#contenu-du-dépôt)
- [1. Application Django « Alerte et investigation »](#1-application-django--alerte-et-investigation-)
- [2. Notebook InceptionV3 / MobileNetV2](#2-notebook-inceptionv3--mobilenetv2)
- [3. Pistes d'amélioration](#3-pistes-damélioration)
- [Méthode de vérification](#méthode-de-vérification)
- [Références](#références)
- [Licence](#licence)

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `models.py` | Modèle `AlerteInvestigation` (11 champs) |
| `forms.py` | `AlerteInvestigationForm` (`ModelForm` et mise en page *crispy-forms*) |
| `widget_caseacocher.py` | Widget `CustomCheckbox` (case à cocher et script d'affichage conditionnel) |
| `views.py` | Vue `alerte_investigation` (affichage en GET, enregistrement en POST) |
| `urls.py` | Route `''` vers la vue |
| `apps.py` | `AlerteInvestigationConfig` (`name = "alerte_investigation"`) |
| `admin.py`, `tests.py`, `__init__.py` | Fichiers vides générés par Django |
| `manage.py` | Utilitaire Django ; il pointe vers `monprojet.settings`, absent du dépôt |
| `alerte_investigation.html` | Gabarit de la page (Bootstrap 5.3.0-alpha1, jQuery 3.6.0, Font Awesome 5.15.4, chargés depuis des CDN) |
| `style.css` | Styles du bouton, de la grille et des cases à cocher |
| `script.js` | Ouverture et fermeture du formulaire ; fonction `initCustomCheckbox` |
| `Modele_InceptionV3_et_MobileNetV2.ipynb` | Notebook Colab : 48 cellules, ≈ 2,9 Mo, dont ≈ 93 % de sorties enregistrées |

Le dépôt ne contient ni `requirements.txt`, ni `settings.py`, ni migrations, ni licence.

---

## 1. Application Django « Alerte et investigation »

### 1.1 Fonction

La page affiche un bouton **ALERTE ET INVESTIGATION** qui ouvre un formulaire. À la soumission, la vue valide les données et les enregistre dans la table `AlerteInvestigation`.

### 1.2 Données saisies

| Champ (`models.py`) | Libellé affiché | Type | Contrainte |
|---|---|---|---|
| `identifiant_alerte` | ID Alerte | texte (9) | exactement 9 caractères alphanumériques |
| `date_notification` | Date de notification | date | — |
| `numero_telephone` | N°Tél | texte (20) | au moins 7 caractères |
| `heure_alerte` | Heure de l'alerte | heure | — |
| `personne_structure_transmis_alerte` | Personne (ou structure) ayant transmis l'alerte | texte (255) | — |
| `source_alerte` | Source d'alerte | choix | Centre d'appel, Suivi des contacts, EIIR, Point d'entrée, ASC, Communauté, FOSA, Autre |
| `heure_information_equipe` | Heure à laquelle l'équipe d'investigation a été informée | heure | — |
| `heure_arrivee_site` | Heure à laquelle l'équipe a notifié son arrivée sur le site | heure | — |
| `date_investigation` | Date d'investigation | date | postérieure ou égale à `date_notification` (contrôlée dans `save()`) |
| `heure_investigation` | Heure d'investigation | heure | — |
| `nom_equipe_investigateur` | Nom de l'équipe/investigateur | texte (255) | — |

Tous les champs sont facultatifs.

Le code ne définit pas les sigles des sources. Leur sens usuel en santé publique francophone est le suivant (interprétation à confirmer) :
- **ASC** : agent de santé communautaire ;
- **FOSA** : formation sanitaire ;
- **Point d'entrée** : port, aéroport ou poste-frontière.

Le sens d'**EIIR** n'est précisé nulle part.

### 1.3 Installation

Les fichiers sont tous à la racine du dépôt. Le code suppose pourtant un package `alerte_investigation` (imports relatifs, `apps.py`), placé dans un projet nommé `monprojet` (`manage.py`). Il attend aussi le gabarit et les fichiers statiques à des emplacements précis.

La procédure ci-dessous a été testée avec Python 3.13, Django 5.2.19, django-crispy-forms 2.7 et crispy-bootstrap5 2026.9. Exécutez-la depuis le dossier **parent** du dépôt cloné.

1. Créez un environnement virtuel et installez les dépendances :

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install "django>=5,<6" django-crispy-forms crispy-bootstrap5
```

2. Créez le projet hôte, puis placez les fichiers aux emplacements attendus :

```bash
mkdir site && cd site
```

```bash
django-admin startproject monprojet .
```

```bash
mkdir -p alerte_investigation/templates/alerte_investigation alerte_investigation/static/css alerte_investigation/static/js
```

```bash
cp ../formulaire/{__init__,admin,apps,forms,models,tests,urls,views,widget_caseacocher}.py alerte_investigation/
```

```bash
cp ../formulaire/alerte_investigation.html alerte_investigation/templates/alerte_investigation/
```

```bash
cp ../formulaire/style.css alerte_investigation/static/css/ && cp ../formulaire/script.js alerte_investigation/static/js/
```

3. Corrigez l'import de `forms.py` (ligne 5). Sans cette correction, Django lève `ModuleNotFoundError: No module named 'widget_caseacocher'`.

```bash
sed -i 's/^from widget_caseacocher import/from .widget_caseacocher import/' alerte_investigation/forms.py
```

4. Dans `monprojet/settings.py`, ajoutez les applications et choisissez le jeu de gabarits Bootstrap 5 :

```python
INSTALLED_APPS = [
    # ... applications django.contrib.* existantes ...
    "crispy_forms",
    "crispy_bootstrap5",
    "alerte_investigation",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

5. Dans `monprojet/urls.py`, branchez les routes de l'application :

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("alerte_investigation.urls")),
]
```

6. Créez la base de données, puis lancez le serveur :

```bash
python manage.py makemigrations alerte_investigation && python manage.py migrate
```

```bash
python manage.py runserver
```

La page s'affiche à l'adresse <http://127.0.0.1:8000/>. **Après ces étapes, aucune soumission n'aboutit encore** ; la cause est décrite au § 1.5, point 1.

### 1.4 État vérifié

| Vérification | Résultat |
|---|---|
| `python manage.py check` lancé dans le dépôt tel quel | Échec : `ModuleNotFoundError: No module named 'monprojet'` |
| Import de `forms.py` dans un package `alerte_investigation` | Échec : `ModuleNotFoundError: No module named 'widget_caseacocher'` |
| Après la procédure du § 1.3 : `check`, `makemigrations`, `migrate` | Réussite : 0 problème signalé, migration `0001_initial` générée |
| `GET /`, `style.css` et `script.js` | Réponse 200 ; les 11 champs sont affichés |
| Soumission avec la case « source » cochée, décochée, ou avec la valeur `FOSA` | **Toujours refusée** : « Sélectionnez un choix valide. True (ou False) n'en fait pas partie. » Aucun enregistrement créé |
| `save()` avec une date de notification postérieure à la date d'investigation | `ValueError` levée par le modèle, sans erreur de formulaire |
| Téléphone `abcdefg` | Accepté (seule la longueur minimale de 7 caractères est contrôlée) |
| Enregistrement entièrement vide | Accepté par le modèle |

### 1.5 Problèmes connus

Les problèmes sont classés du plus grave au moins grave.

1. **Le formulaire ne peut jamais être validé.** Le champ à choix `source_alerte` utilise le widget `CustomCheckbox`, qui hérite de `forms.CheckboxInput` (`widget_caseacocher.py:3`). Or ce widget est booléen :
   - il n'affiche qu'une seule case, et les 8 sources possibles n'apparaissent pas sur la page ;
   - il renvoie `True` ou `False`, deux valeurs absentes de `SOURCE_ALERT_CHOICES`.

   Correction possible : utiliser `forms.RadioSelect` ou `forms.Select`.
2. **Le projet n'est pas exécutable tel quel** :
   - le projet `monprojet` référencé par `manage.py:9` n'existe pas ;
   - l'arborescence attendue par le code n'est pas respectée (voir § 1.3) ;
   - l'import de `forms.py:5` est absolu alors qu'il devrait être relatif ;
   - il n'y a ni migrations ni liste de dépendances.
3. **Le contrôle des dates est fait dans `save()`** (`models.py:90-94`), qui lève une `ValueError`. Une fois le point 1 corrigé, une saisie de dates incohérentes produira donc une erreur serveur 500 au lieu d'un message dans le formulaire. Ce contrôle devrait être déplacé dans `clean()`, sur le modèle ou sur le formulaire.
4. **L'affichage conditionnel est sans effet.** `initCustomCheckbox` (`script.js:4`) affiche ou masque des champs nommés `centre_appel`, `suivi_contacts`, etc., qui n'existent pas dans le formulaire.
5. **Le gabarit HTML est mal formé.** Il contient 17 balises `<div>` ouvrantes pour 18 fermantes. La balise en trop, `alerte_investigation.html:61`, ferme la carte avant le dernier champ et le bouton « Soumettre ».
6. **La mise en page crispy n'est jamais utilisée.** Le `FormHelper` défini dans `forms.py:43-59` est ignoré, car le gabarit affiche les champs un par un avec `|as_crispy_field`. Conséquence : l'attribut `minlength=9` du téléphone (`forms.py:49`) n'est jamais appliqué. Il contredit d'ailleurs `MinLengthValidator(7)` (`models.py:27`).
7. **La vue ne redirige pas après un enregistrement** (`views.py:9-11`) et n'affiche aucun message de confirmation. Recharger la page après un envoi renvoie donc le formulaire une seconde fois (après confirmation du navigateur).
8. **Points mineurs** :
   - aucun test (`tests.py` est vide) ;
   - le modèle n'est pas déclaré dans l'administration (`admin.py` est vide) ;
   - aucun champ n'est obligatoire, et le téléphone accepte des lettres ;
   - `style.css` redéfinit des classes de Bootstrap (`.row`, `.col-md-*`, `.mt-4`, `.mb-3`) ;
   - Bootstrap est chargé dans une version alpha (`5.3.0-alpha1`).

---

## 2. Notebook InceptionV3 / MobileNetV2

### 2.1 Objectif

Le notebook vise à classer des photos de feuilles de poivron, de pomme de terre et de tomate en 15 classes, saines ou malades, issues du jeu PlantVillage [1]. Il compare deux réseaux pré-entraînés sur ImageNet et adaptés par apprentissage par transfert : InceptionV3 et MobileNetV2.

### 2.2 Exécution

- **Environnement** : Google Colab avec GPU T4 et TensorFlow 2.15.0 (versions lues dans les sorties enregistrées). Le badge « Open in Colab » en tête du notebook l'ouvre directement.
- **Données** : le notebook ne télécharge rien. Il attend l'un des deux emplacements suivants :
  - le dossier `My Drive/Datasets/PlantVillage/`, avec un sous-dossier par classe ;
  - l'archive `My Drive/archive.zip`, qu'il extrait automatiquement.
- ⚠️ **La cellule « Répartition des données » déplace les images** (`shutil.move`) vers `train/` et `val/`. Une seconde exécution ne trouve donc plus aucune image à répartir. Faites une copie du jeu de données avant de la lancer.

### 2.3 Pipeline

| Étape | Contenu |
|---|---|
| 1. Préparation | Vérification du GPU, montage de Drive, extraction, suppression d'un sous-dossier `PlantVillage/PlantVillage` redondant, comptage des images, contrôle d'intégrité (PIL), aperçu aléatoire |
| 2. Prétraitement | Découpage 80 % / 20 % classe par classe (`train_test_split`, `random_state=42`), suppression d'un fichier qui n'est pas une image, augmentation de données (cisaillement, zoom, retournement horizontal) |
| 3. Modèles | Réseau pré-entraîné sans sa couche de classification, puis `GlobalAveragePooling2D`, `Dropout(0.5)` et `Dense(15, softmax)`. Toutes les couches sont entraînables |
| 4. Entraînement | RMSprop (taux d'apprentissage 1e-3), entropie croisée, images en 224 × 224, lots de 32, 20 époques au maximum. `EarlyStopping(val_loss, patience=10, restore_best_weights=True)`, `ReduceLROnPlateau(facteur 0,2, patience 5, minimum 1e-4)`. Sauvegarde `.h5` sur Drive à chaque époque |
| 5. Évaluation | Évaluation sur la validation, puis sur un dossier `test/` : **ces deux cellules n'ont jamais été exécutées**, et le dossier `test/` n'est jamais créé |

### 2.4 Données utilisées et résultats enregistrés

D'après les sorties du notebook, **seuls 4 des 15 dossiers de classe contenaient des images** :

| Classe | Images | Entraînement | Validation |
|---|---:|---:|---:|
| `Pepper__bell___Bacterial_spot` | 997 | 797 | 200 |
| `Pepper__bell___healthy` | 1 478 | 1 182 | 296 |
| `Potato___Early_blight` | 758 | 606 | 152 |
| `Tomato_healthy` | 15 | 12 | 3 |
| 11 autres classes | 0 | 0 | 0 |
| **Total** | **3 248** | **2 597** | **651** |

Le tableau suivant reprend les résultats de la cellule d'entraînement. Chaque évaluation de validation porte sur 20 lots, soit 640 des 651 images.

| Modèle | Époques effectuées | Meilleure `val_loss` | `val_accuracy` | Poids finaux en mémoire |
|---|---|---|---|---|
| InceptionV3 | 20 / 20 | 1,77 × 10⁻⁴ (époque 18) | 1,000 de l'époque 11 à 20, sauf l'époque 15 (0,998) | Ceux de l'époque 20 |
| MobileNetV2 | 11 / 20 (arrêt anticipé) | 2,63 (époque 1) | 0,758 à l'époque 1 ; de 0,30 à 0,34 aux époques 2 à 9 ; 0,794 à l'époque 11 | Ceux de l'époque 1, restaurés par `EarlyStopping` (val_accuracy 0,758) |

Les modèles finaux sont enregistrés par `model.save('model_*.h5')` dans le répertoire de travail de Colab, qui est effacé en fin de session. Seuls les points de contrôle de chaque époque sont conservés sur Drive. Aucun modèle n'est versionné dans le dépôt.

### 2.5 Limites et interprétation

- **Le problème réellement traité compte 4 classes, et non 15.** Les scores de 100 % portent sur ces 4 classes, dont l'une (`Tomato_healthy`) n'a que 3 images de validation. Les 11 classes vides occupent malgré tout 11 sorties de la couche finale. Cause probable, non vérifiée : une copie incomplète du jeu sur Drive, PlantVillage comptant plus de 50 000 images [1].
- **Aucune estimation indépendante des performances.** Le jeu de validation sert aussi à l'arrêt anticipé et à l'ajustement du taux d'apprentissage. Le jeu de test n'a jamais été créé. Les 100 % obtenus en validation ne mesurent donc pas la capacité du modèle à se généraliser.
- **Le prétraitement ne correspond pas à celui des poids pré-entraînés.** L'entraînement normalise les pixels dans [0, 1] (`rescale=1./255`). Or `preprocess_input` ramène les pixels dans [-1, 1] (`x / 127.5 - 1`) pour InceptionV3 comme pour MobileNetV2 [2]. Cette fonction est importée dans une cellule antérieure, mais elle n'est pas utilisée pour l'entraînement.
- **Instabilité observée.** La `val_loss` d'InceptionV3 vaut 10 473 à l'époque 1. La `val_accuracy` de MobileNetV2 reste autour de 0,31 aux époques 2 à 9, soit environ la proportion de `Pepper__bell___Bacterial_spot` dans la validation (200 / 651 = 0,307). Cela suggère que le réseau prédit alors une seule classe. Le décalage de prétraitement, combiné à un réentraînement complet avec un taux d'apprentissage de 1e-3, pourrait expliquer cette instabilité. Cette hypothèse n'a pas été testée.
- **La comparaison des deux architectures n'est pas concluante.** Chaque modèle n'a été entraîné qu'une fois, sans graine fixée, et MobileNetV2 a été conservé dans son état de l'époque 1.
- **Reproductibilité limitée** :
  - les chemins Drive sont écrits en dur et les versions des bibliothèques ne sont pas figées ;
  - deux cellules portent des sorties sans numéro d'exécution, signe qu'elles ont été lancées lors d'une session antérieure ;
  - certaines cellules sont obsolètes : un premier `create_model` à 10 classes, un générateur d'images jamais utilisé ;
  - le message « Aucun N fichiers corrompus trouvés » s'affiche même quand des fichiers corrompus sont trouvés.
- **Taille du notebook.** Environ 1,5 Mo de journaux texte (la liste de chaque fichier déplacé, celle de chaque chemin d'image, deux résumés de modèles) et 1,2 Mo d'images encodées. Effacer les sorties avant de le versionner le rendrait plus léger et plus lisible.

---

## 3. Pistes d'amélioration

Ces propositions n'ont pas été mises en œuvre.

**Application Django**
1. Remplacer `CustomCheckbox` par `forms.RadioSelect`.
2. Restructurer le dépôt en projet Django complet, avec `requirements.txt` et migrations.
3. Déplacer le contrôle des dates dans `clean()`.
4. Rediriger après l'enregistrement et afficher un message de confirmation.
5. Ajouter des tests : rendu de la page, soumission valide, soumission invalide.

**Notebook**
1. Récupérer les 15 classes complètes.
2. Utiliser le `preprocess_input` propre à chaque modèle.
3. Entraîner d'abord la nouvelle couche de classification avec le réseau gelé, puis réentraîner le réseau entier avec un taux d'apprentissage faible.
4. Créer un jeu de test séparé avant tout entraînement.
5. Mesurer les performances classe par classe : matrice de confusion, rappel, F1.
6. Copier les images au lieu de les déplacer.
7. Effacer les sorties avant de versionner.

**Dépôt**
- Séparer les deux projets, dans deux dossiers ou deux dépôts distincts.
- Ajouter une licence.

## Méthode de vérification

- **Application Django** : elle a été exécutée le 16/11/2026 dans un projet de test construit selon le § 1.3, avec le client de test Django et `runserver`. Les résultats du § 1.4 viennent de ces exécutions.
- **Notebook** : il n'a pas été réexécuté, car ses données se trouvent sur un Drive privé. Les § 2.3 à 2.5 s'appuient sur son code et sur ses sorties enregistrées. Le comportement de `EarlyStopping` et de `preprocess_input` a été vérifié dans le code source de Keras 2.15.0, la version livrée avec TensorFlow 2.15.

## Références

1. D. P. Hughes et M. Salathé, *An open access repository of images on plant health to enable the development of mobile disease diagnostics*, arXiv:1511.08060, 2015. <https://arxiv.org/abs/1511.08060>
2. Documentation TensorFlow 2.15, `tf.keras.applications.inception_v3.preprocess_input`. <https://www.tensorflow.org/versions/r2.15/api_docs/python/tf/keras/applications/inception_v3/preprocess_input>. Le code source de Keras 2.15.0 applique le même mode `"tf"` à MobileNetV2 (`keras/src/applications/mobilenet_v2.py`).

## Licence

Le dépôt ne contient aucun fichier de licence : par défaut, tous les droits sont réservés à l'auteur. Pour autoriser la réutilisation du code, il faut ajouter une licence, par exemple MIT ou Apache-2.0.
