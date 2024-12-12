
# Rapport de Développement : Détecteur de Malaria

## 1. Introduction
Ce document présente le développement d'un modèle de classification d'images pour détecter la malaria à partir d'échantillons de cellules. Il décrit les choix techniques, les étapes de développement, et les résultats obtenus.

## 2. Choix Techniques

### 2.1 Architecture
- **Modèle :** Réseau de neurones convolutionnel (CNN).
- **Format final :** TensorFlow Lite (TFLite) avec optimisations pour appareils mobiles.

### 2.2 Technologies et Outils
- **Frameworks :** TensorFlow/Keras pour l'entraînement et la construction du modèle.
- **Visualisation :** `matplotlib` pour représenter les courbes d'apprentissage.
- **Optimisation :** TFLite pour conversion en modèles légers, zlib pour compression supplémentaire.
- **Justifications :**
  - TensorFlow est un standard de l'industrie pour le deep learning.
  - TFLite facilite le déploiement sur des appareils embarqués ou mobiles.
  - Compression pour réduire les besoins en stockage et accélérer les déploiements.

## 3. Étapes de Développement

### 3.1 Préparation des Données
- Chargement des données brutes et création de datasets d'entraînement et de validation.
- Augmentation des données pour améliorer la généralisation (rotation, redimensionnement, etc.).

### 3.2 Entraînement du Modèle
- **Hyperparamètres :**
  - Taille des images : 128x128 pixels.
  - Classes : 2 (infecté, non infecté).
- **Algorithme :** Optimiseur Adam avec fonction de perte `categorical_crossentropy`.
- **Résultats intermédiaires :**
  - Courbes d'apprentissage montrant la précision et la perte sur les datasets.

### 3.3 Optimisation et Compression
- Conversion en TensorFlow Lite :
  - Réduction de taille grâce à la quantification en `float16` et `int8`.
- Pruning (élagage) pour éliminer les poids inutiles.
- Compression supplémentaire avec zlib :
  - Taille finale : 5.27 Mo (taux de compression de 14.2x).

```mermaid
flowchart TD
    A[Chargement des Données] --> B[Construction du Modèle]
    B --> C[Entraînement]
    C --> D[Évaluation]
    D --> E[Optimisation (TFLite)]
    E --> F[Compression (zlib)]
```

## 4. Résultats Obtenus

### 4.1 Performances
- **Précision finale (validation) :** ~95%.
- **Perte finale (validation) :** ~0.15.
- **Optimisation :** Réduction de la taille de 74.66 Mo (Keras) à 5.27 Mo (TFLite compressé).

### 4.2 Visualisation
#### Courbes d'Apprentissage
![Courbes d'apprentissage](https://maleriadetector-edftabgyg9gae6fq.canadacentral-01.azurewebsites.net/static/learning_curves.png)

### 4.3 Enseignements Tirés
- La quantification et le pruning offrent des gains significatifs en taille sans compromis majeur sur la précision.
- Des datasets bien augmentés améliorent la robustesse du modèle.

### 4.4 Améliorations Potentielles
- **Exploration de nouvelles architectures :** Modèles préentraînés (EfficientNet).
- **Optimisation de pipeline :** Automatisation de la conversion et de la compression.

## 5. Références
- [Documentation TensorFlow](https://www.tensorflow.org/)
- [Tutoriel TFLite Optimization](https://www.tensorflow.org/lite/performance/model_optimization)
- [GitHub Repository](https://github.com/tensorflow/models)
