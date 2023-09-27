# Data Augmentation format Vertex IA

[Lien google](https://cloud.google.com/vertex-ai/docs/image-data/object-detection/prepare-data?hl=fr#csv)

# Install

```bash
git clone GIT_URL vertexAIDatasetAugmentation
cd vertexAIDatasetAugmentation
pip3 install -r requirements.txt
python3 pipeline.py ...params
```

# Principe

## In
L'outil prends en entrée un dataset sous forme:
- source_ds (dossier parent)
    - annotations.csv
    - images (dossier)

Exemple de annotation.csv est disponible [ici](./exemple_annotations.csv)

## Out

- un dossier "preproc_dt", qui représente le dataset apres là phase de preprocessing
- un dossier "dataug_dt", qui représente le dataset apres là phase d'augmentation
- un dossier "final_dt", qui représente le dataset avec les liens bucket

final_dt sera le dossier à importer dans vertex

# Usage

```
usage: pipeline.py [-h] [-i INPUT_DATASET] [-nc NO_CHECK] [-fc FORCE_DELETE] [-b BUCKET]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DATASET, --input-dataset INPUT_DATASET
                        Chemin du dossier du dataset source
  -nc NO_CHECK, --no-check NO_CHECK
                        Désactiver l'existence du dataset source
  -fc FORCE_DELETE, --force-delete FORCE_DELETE
                        Suppression des dossiers de sortie
  -b BUCKET, --bucket BUCKET
                        url du bucket
```

exemple d'augmentation sur le dossier inital "dataset" et pour le bucket "gs://monbucket"
```bash
python3 pipeline.py -i dataset -b "gs://monbucket"
```

# Attention

Pour le bucket.

**Oui**
- "gs://monbucket"
- "gs://monbucket/dossier"

**Non**

- gs://monbucket/
- "gs://monbucket/dossier/"