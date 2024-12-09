# Malaria Detection Project

Ce projet utilise l'apprentissage automatique pour détecter le paludisme à partir d'images de cellules sanguines.

## Table des matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Installation

1. Clone le dépôt :
   ```bash
   git clone https://github.com/ton-utilisateur/malaria-detection.git
   cd malaria-detection   ```

2. Construis l'image Docker :
   ```bash
   docker-compose build   ```

3. Lance les conteneurs :
   ```bash
   docker-compose up   ```

## Utilisation

Une fois les conteneurs lancés, l'application sera accessible à l'adresse `http://localhost:5000`. Tu peux y télécharger des images de cellules sanguines pour détecter la présence de paludisme.

## Structure du projet

- `app/`: Contient le code source de l'application Flask.
- `scripts/`: Contient les scripts pour générer des graphiques et analyser les données.
- `docker-compose.yml`: Fichier de configuration pour Docker Compose.
- `requirements.txt`: Liste des dépendances Python.

## Contribuer

Les contributions sont les bienvenues ! Pour proposer des modifications, suis ces étapes :

1. Fork le projet
2. Crée une branche pour ta fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit tes modifications (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvre une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails. 