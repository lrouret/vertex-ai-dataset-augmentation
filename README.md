# Pipeline

1. Vérification de tous les labels
2. Préprocessing
3. Data augmentation

# Attention

Pour le bucket.

**Oui**
- "gs://monbucket"
- "gs://monbucket/dossier"

**Non**

- gs://monbucket/
- "gs://monbucket/dossier/"

# Input

En entré le dataset vertex (par défault : "source_ds").

Sous forme de :
images (dossiers)
annotations.csv

# Output

preproc_dt = preprocessing
dataug_dt = data augmetantation
final_dt = dataset vers le bucket, pret pour l'importation