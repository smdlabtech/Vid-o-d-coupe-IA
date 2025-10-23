
# SmartClip-AI - Plateforme Intelligente de Découpe Vidéo

SmartClip-AI est une application web moderne qui utilise l'intelligence artificielle pour automatiser la découpe et l'analyse de vidéos. Grâce à l'intégration de Whisper (OpenAI) pour la transcription et à une analyse fine des segments, cette solution permet d'extraire efficacement les moments clés de vos vidéos.

## ✨ Fonctionnalités

### 🎯 Fonctionnalités Principales
- **Upload intelligent** : Interface drag & drop avec validation complète des fichiers
- **Transcription automatique** : Utilisation de Whisper d'OpenAI pour une transcription précise
- **Découpage par segments** : Sélection interactive des parties à extraire
- **Génération de clips** : Export automatique des segments sélectionnés
- **Historique complet** : Suivi de toutes les vidéos traitées avec métadonnées

### 🔒 Sécurité & Production
- **Validation stricte des fichiers** : Vérification MIME, taille, format
- **Sanitisation des noms** : Protection contre les injections path traversal
- **Logging structuré** : Système de logs rotatifs avec niveaux appropriés
- **Gestion d'erreurs** : Messages clairs pour les utilisateurs, logs techniques pour le debug
- **Configuration flexible** : Variables d'environnement pour tous les paramètres

### 📊 Interface Moderne
- **Design Material 3** : Interface orange/gris moderne et responsive
- **Navigation intuitive** : Sidebar avec navigation fluide
- **États de chargement** : Feedback temps réel pour toutes les opérations
- **Notifications toast** : Messages d'information, succès et erreurs
- **Recherche et filtres** : Gestion avancée de l'historique des vidéos

## 🚀 Installation

### Prérequis
bash
# Python 3.11+
python --version

# FFmpeg (requis pour l'extraction audio et le découpage)
# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Télécharger depuis https://ffmpeg.org/download.html


### Configuration de l'environnement
bash
# Cloner le repository
git clone https://github.com/votre-username/smartclip-ai.git
cd smartclip-ai

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt


### Variables d'environnement
Créer un fichier `.env` à la racine du projet :

env
# OpenAI API (OBLIGATOIRE)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Configuration optionnelle
MAX_FILE_SIZE_MB=500
LOG_LEVEL=INFO
LOG_FILE=app.log
LOG_ROTATION=10 MB
LOG_RETENTION=7 days

# Formats supportés (séparés par des virgules)
SUPPORTED_FORMATS=video/mp4,video/webm,video/quicktime,video/x-msvideo,video/x-matroska


## 🎯 Lancement

### Mode Développement
bash
# Initialiser la base de données
reflex init

# Lancer l'application
reflex run


L'application sera accessible sur `http://localhost:3000`

### Mode Production
bash
# Build de l'application
reflex export

# Lancer en production
reflex run --env prod


## 📁 Structure du Projet


SmartClip-AI/
├── app/
│   ├── components/          # Composants réutilisables
│   │   ├── header.py       # En-tête de l'application
│   │   └── sidebar.py      # Navigation latérale
│   ├── pages/              # Pages de l'application
│   │   ├── home.py         # Page d'accueil
│   │   ├── upload.py       # Interface d'upload
│   │   ├── processing.py   # Traitement et visualisation
│   │   ├── videos.py       # Historique des vidéos
│   │   └── placeholder.py  # Pages en construction
│   ├── states/             # États Reflex (logique métier)
│   │   ├── processing_state.py  # Logique de traitement
│   │   └── videos_state.py      # Gestion de l'historique
│   ├── db/                 # Base de données
│   │   └── database.py     # Fonctions CRUD SQLite
│   ├── utils/              # Utilitaires
│   │   ├── config.py       # Configuration et variables d'env
│   │   ├── logger.py       # Système de logging
│   │   └── validators.py   # Validation et sécurité
│   ├── state.py           # État principal de l'application
│   └── app.py             # Point d'entrée et configuration
├── assets/                 # Ressources statiques
├── requirements.txt        # Dépendances Python
├── rxconfig.py            # Configuration Reflex
└── README.md              # Documentation


## 🔧 Utilisation

### 1. Upload d'une Vidéo
1. Accédez à la page **Upload**
2. Glissez-déposez votre fichier vidéo ou cliquez pour sélectionner
3. Formats supportés : MP4, MOV, AVI, MKV, WebM
4. Taille maximale : 500MB (configurable)

### 2. Traitement et Transcription
1. Cliquez sur **"Lancer le Traitement"**
2. L'application extrait l'audio automatiquement
3. Whisper transcrit le contenu avec timestamps
4. Les segments sont affichés avec leurs textes correspondants

### 3. Sélection et Découpage
1. Cochez les segments que vous souhaitez conserver
2. Utilisez **"Tout sélectionner"** ou **"Tout désélectionner"**
3. Cliquez sur **"Générer les Clips"**
4. Téléchargez les clips générés individuellement

### 4. Gestion de l'Historique
1. Accédez à **"Mes Vidéos"**
2. Recherchez par nom de fichier
3. Filtrez par statut (terminé, en_cours, erreur)
4. Consultez les détails ou supprimez des entrées

## 🔍 Monitoring et Logs

### Système de Logging
- **Niveau INFO** : Opérations normales (upload, traitement terminé)
- **Niveau WARNING** : Situations à surveiller (fichiers volumineux)
- **Niveau ERROR** : Erreurs avec stacktrace complet
- **Fichiers rotatifs** : Logs automatiquement archivés

### Métriques Clés
- Temps de traitement par vidéo
- Nombre de mots transcrits
- Taux de succès/échec des opérations
- Utilisation de l'API OpenAI

## ⚡ Optimisations Performance

### Grandes Vidéos
- Compression automatique si nécessaire
- Traitement par chunks pour économiser la mémoire
- Nettoyage automatique des fichiers temporaires

### Sécurité
- Validation stricte des types MIME
- Sanitisation des noms de fichiers
- Timeouts configurables sur les opérations longues
- Rate limiting sur les transcriptions

## 🐛 Résolution de Problèmes

### Erreurs Courantes

**"FFmpeg non trouvé"**
bash
# Vérifier l'installation
ffmpeg -version

# Réinstaller si nécessaire
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS


**"Clé API OpenAI non configurée"**
bash
# Vérifier la variable d'environnement
echo $OPENAI_API_KEY

# Configurer dans .env
OPENAI_API_KEY=sk-votre-cle-ici


**"Base de données non initialisée"**
bash
# Réinitialiser la base
reflex db init


### Logs de Debug
bash
# Activer les logs détaillés
export LOG_LEVEL=DEBUG

# Consulter les logs
tail -f app.log


## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commitez vos changements (`git commit -am 'Ajoute nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **OpenAI** pour l'API Whisper
- **Reflex** pour le framework Python full-stack
- **FFmpeg** pour le traitement audio/vidéo
- **Communauté open source** pour les outils et bibliothèques

## 📞 Support

- **Issues GitHub** : [github.com/votre-username/smartclip-ai/issues](https://github.com/votre-username/smartclip-ai/issues)
- **Email** : support@smartclip-ai.com
- **Documentation** : [docs.smartclip-ai.com](https://docs.smartclip-ai.com)

---

**SmartClip-AI** - Transformez vos vidéos en contenu exploitable grâce à l'IA ✨

