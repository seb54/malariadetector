import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Créer le dossier pour les images si nécessaire
output_dir = Path('app/static/images')
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Graphique des métriques d'entraînement
plt.figure(figsize=(10, 6))
epochs = range(1, 11)
accuracy = [0.69, 0.92, 0.93, 0.93, 0.94, 0.94, 0.95, 0.94, 0.94, 0.95]
val_accuracy = [0.91, 0.94, 0.92, 0.93, 0.94, 0.95, 0.93, 0.95, 0.95, 0.94]

plt.plot(epochs, accuracy, 'b-', label='Précision entraînement')
plt.plot(epochs, val_accuracy, 'r-', label='Précision validation')
plt.title('Métriques d\'entraînement')
plt.xlabel('Epochs')
plt.ylabel('Précision')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(output_dir / 'training_metrics.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Distribution des classes
plt.figure(figsize=(8, 6))
classes = ['Non infecté', 'Infecté']
counts = [13779, 13779]  # Dataset équilibré
sns.barplot(x=classes, y=counts)
plt.title('Distribution des Classes')
plt.ylabel('Nombre d\'images')
plt.savefig(output_dir / 'class_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Exemple de prétraitement
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
fig.suptitle('Étapes de Prétraitement')

# Image originale (simulée)
img = np.random.rand(100, 100, 3)
axes[0].imshow(img)
axes[0].set_title('Image Originale')
axes[0].axis('off')

# Image redimensionnée
img_resized = np.random.rand(128, 128, 3)
axes[1].imshow(img_resized)
axes[1].set_title('Redimensionnée')
axes[1].axis('off')

# Image normalisée
img_normalized = (img_resized - 0.5) / 0.5
axes[2].imshow(img_normalized)
axes[2].set_title('Normalisée')
axes[2].axis('off')

plt.tight_layout()
plt.savefig(output_dir / 'preprocessing.png', dpi=300, bbox_inches='tight')
plt.close() 