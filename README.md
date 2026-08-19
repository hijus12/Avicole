# Avicole API

API d'authentification construite avec Django, Django REST Framework, Djoser et Simple JWT. Elle est conçue pour être consommée par un frontend séparé, par exemple une application React ou Vue.

## Fonctionnalités

- Création et gestion des utilisateurs avec Djoser
- Authentification JWT avec cookies `access` et `refresh`
- Rafraîchissement et vérification des tokens
- Déconnexion avec suppression des cookies JWT
- Authentification des requêtes protégées depuis les cookies
- CORS configuré pour un frontend local
- Base de données SQLite pour le développement

## Prérequis

- Python 3.12 ou version compatible
- Git
- Un environnement virtuel Python recommandé

## Installation

```bash
git clone https://github.com/hijus12/Avicole.git
cd Avicole
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

Appliquer les migrations :

```bash
python manage.py migrate
```

Créer un compte administrateur si nécessaire :

```bash
python manage.py createsuperuser
```

## Configuration

Le projet lit sa configuration depuis les variables d'environnement. En développement, les valeurs par défaut autorisent le frontend sur `localhost:3000` et `127.0.0.1:3000`.

Exemple de configuration locale :

```env
DJANGO_SECRET_KEY=change-me
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
AUTH_COOKIE_SECURE=False
AUTH_COOKIE_SAMESITE=Lax
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Ne publiez jamais une vraie clé secrète dans le dépôt. Le fichier `.env.local` est ignoré par Git.

## Lancer le serveur

```bash
python manage.py runserver
```

L'API est alors disponible sur `http://127.0.0.1:8000`.

## Endpoints JWT

| Méthode | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/jwt/create/` | Connexion et création des tokens |
| `POST` | `/api/jwt/refresh/` | Rafraîchissement du token d'accès avec le cookie `refresh` |
| `POST` | `/api/jwt/verify/` | Vérification du token d'accès |
| `POST` | `/api/jwt/logout/` | Suppression des cookies `access` et `refresh` |

La connexion attend les identifiants de l'utilisateur Django :

```json
{
  "username": "alice",
  "password": "mot-de-passe"
}
```

Après une connexion réussie, les tokens sont renvoyés dans des cookies HttpOnly. Le frontend ne doit donc pas essayer de les lire directement.

## Endpoints utilisateurs Djoser

| Méthode | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/users/` | Créer un utilisateur |
| `GET` | `/api/users/me/` | Récupérer l'utilisateur connecté |
| `PUT/PATCH` | `/api/users/me/` | Modifier l'utilisateur connecté |
| `DELETE` | `/api/users/me/` | Supprimer l'utilisateur connecté |
| `POST` | `/api/users/set_password/` | Modifier le mot de passe |
| `POST` | `/api/users/reset_password/` | Demander une réinitialisation du mot de passe |
| `POST` | `/api/users/activation/` | Activer un compte |

Les autres routes Djoser disponibles sont exposées sous `/api/users/`.

## Connexion depuis un frontend

Avec `fetch`, il faut inclure les cookies dans les requêtes :

```js
const response = await fetch("http://127.0.0.1:8000/api/jwt/create/", {
  method: "POST",
  credentials: "include",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    username: "alice",
    password: "mot-de-passe"
  })
});
```

Pour appeler une route protégée :

```js
const response = await fetch("http://127.0.0.1:8000/api/users/me/", {
  credentials: "include"
});
```

Avec Axios, utilisez `withCredentials: true` :

```js
axios.defaults.withCredentials = true;
```

## Production

Avant un déploiement :

```env
DEBUG=False
DJANGO_SECRET_KEY=une-cle-secrete-forte
DJANGO_ALLOWED_HOSTS=api.example.com
AUTH_COOKIE_SECURE=True
AUTH_COOKIE_SAMESITE=None
CORS_ALLOWED_ORIGINS=https://frontend.example.com
```

Le mode production doit utiliser HTTPS, notamment parce que les cookies `Secure` et `SameSite=None` l'exigent dans les navigateurs modernes.

## Tests et vérifications

Vérifier la configuration Django :

```bash
python manage.py check
```

Lancer les tests :

```bash
python manage.py test
```

## Structure principale

```text
avicole/
├── full_auth/          # Configuration Django et routes principales
├── users/              # Authentification JWT et routes utilisateurs
├── db.sqlite3          # Base locale de développement
├── manage.py           # Commandes Django
├── requirement.txt     # Dépendances Python
└── .gitignore          # Fichiers exclus du dépôt
```
