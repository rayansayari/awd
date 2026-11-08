# CarRental Frontend - Application Client Angular 17+

Application cliente Web SPA (Single Page Application) développée avec le framework **Angular 17+** et stylisée avec **Bootstrap 5**.

Elle communique avec les 6 microservices backend via l'**API Gateway** centrale sur `http://localhost:8080`.

## Architecture du Frontend

```
Frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── guards/         # AuthGuard (protection routes)
│   │   │   ├── interceptors/   # JwtInterceptor (Bearer token injection)
│   │   │   ├── models/         # Modèles TypeScript
│   │   │   └── services/       # Services HTTP Angular (Auth, Vehicle, etc.)
│   │   ├── modules/
│   │   │   ├── auth/           # Connexion & Inscription
│   │   │   ├── vehicles/       # Catalogue, Recherche & Détails
│   │   │   ├── reservations/   # Réservation multi-jours & Récapitulatif
│   │   │   ├── agencies/       # Carte & Localisation des agences
│   │   │   └── admin/          # Dashboard de supervision & Gestion flotte
│   │   ├── shared/
│   │   │   ├── navbar/         # Barre de navigation responsive
│   │   │   └── footer/         # Pied de page
│   │   ├── app.routes.ts       # Routage Angular
│   │   └── app.component.ts    # Composant racine
│   ├── index.html
│   └── styles.css
├── angular.json
├── package.json
└── tsconfig.json
```

## Démarrage Rapide

1. Installer les dépendances :
   ```bash
   npm install
   ```
2. Lancer le serveur de développement :
   ```bash
   npm start
   ```
3. Accéder à l'application sur `http://localhost:4200`.
