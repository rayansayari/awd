# 🚗 CarRental - Plateforme Web de Location de Voitures

> **Projet AWD (Architecture Web Distribuée) - Validation Intermédiaire (Séance 4)**  
> **Équipe :** 6 Étudiants | **Architecture :** Microservices distribués avec Spring Boot 3 & Angular 17+

---

## 📌 1. Présentation Générale du Projet

**CarRental** est une plateforme web moderne et résiliente dédiée à la location de véhicules en ligne. Elle met en relation directe les clients avec un réseau d'agences physiques, leur permettant de :
- Rechercher et filtrer des véhicules par marque, modèle, catégorie, motorisation et tarif journalier.
- Vérifier en temps réel la disponibilité d'une voiture sur une période donnée.
- Effectuer une réservation multi-jours sécurisée avec calcul automatisé du montant.
- Simuler et valider le paiement en ligne (avec gestion des statuts `PENDING`, `PAID`, `CANCELLED`, `REFUNDED`).
- Noter et commenter les prestations des véhicules et des agences partenaires.
- Disposer d'un tableau de bord de supervision pour les employés d'agence et administrateurs.

---

## 🏛️ 2. Architecture Microservices

L'architecture repose sur **6 microservices métier** répartis équitablement entre les 6 membres de l'équipe, complétés par une **infrastructure commune** développée collectivement.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Frontend Client Angular 17+ (SPA :4200)               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST / JWT Bearer
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               API Gateway (Spring Cloud Gateway :8080)                 │
│               Filtre JWT • Routage Dynamique • CORS • Rate Limiting    │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼                                ▼
   ┌────────────────────────────────┐   ┌────────────────────────────────┐
   │ Eureka Discovery Server (:8761)│   │  RabbitMQ Message Broker (:5672)│
   └────────────────────────────────┘   └────────────────────────────────┘
                    │
      ┌─────────────┼─────────────┬─────────────┬─────────────┐
      ▼             ▼             ▼             ▼             ▼
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│1. User Srv│ │2. Vehicle │ │3. Reserv. │ │4. Payment │ │5. Agency  │ │6. Review  │
│   :8081   │ │   :8082   │ │   :8083   │ │   :8084   │ │   :8085   │ │   :8086   │
└─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
      │             │             │             │             │             │
      ▼             ▼             ▼             ▼             ▼             ▼
  [(user_db)]  [(veh_db)]    [(res_db)]    [(pay_db)]    [(agn_db)]   [(rev_db)]
   MySQL   MySQL    MySQL    MySQL    MySQL     MySQL
```

### 👥 Répartition des Microservices Métier

| # | Microservice | Responsable | Port | Base de Données | Responsabilités Clés |
|---|---|---|---|---|---|
| **1** | **User-Service** | *Étudiant 1* | `8081` | MySQL (`user_db`) | Inscription, Login, JWT, Gestion des comptes et rôles (`CLIENT`, `AGENT`, `ADMIN`) |
| **2** | **Vehicle-Service** | *Étudiant 2* | `8082` | MySQL (`vehicle_db`) | Flotte, catégories, tarifs, filtrage multicritère, statut et disponibilité |
| **3** | **Reservation-Service** | *Étudiant 3* | `8083` | MySQL (`reservation_db`) | Création, calcul de devis, cycle de vie des réservations, coordination inter-services |
| **4** | **Payment-Service** | *Étudiant 4* | `8084` | MySQL (`payment_db`) | Simulation de transaction bancaire, factures, statuts `PENDING`, `PAID`, `REFUNDED` |
| **5** | **Agency-Service** | *Étudiant 5* | `8085` | MySQL (`agency_db`) | Agences physiques, géolocalisation/adresses, horaires, affectation du personnel |
| **6** | **Review-Service** | *Étudiant 6* | `8086` | MySQL (`review_db`) | Avis clients, notes (1 à 5), commentaires, modération |
| **★** | **API Gateway + Discovery** | *Collectif* | `8080` / `8761` | - | Point d'entrée unique, registre Eureka, bus RabbitMQ, sécurité partagée |

---

## 🛠️ 3. Technologies Utilisées

- **Backend :** Java 17, Spring Boot 3.2+, Spring Cloud 2023 (Gateway, Eureka Discovery, OpenFeign), Spring Data JPA, Spring Data MySQL.
- **Frontend :** Angular 17+, TypeScript, HTML5 / SCSS, Bootstrap 5, RxJS.
- **Bases de données :** MySQL 8.0 (ACID relationnel pour transactions), MySQL 6 (Relationnel MySQL flexible pour les avis).
- **Communication Inter-services :**
  - **Synchrone :** REST / Spring Cloud OpenFeign (pour les vérifications de disponibilité et l'initialisation de paiement en temps réel).
  - **Asynchrone :** RabbitMQ (AMQP) (pour la publication d'événements : `reservation.confirmed`, `payment.completed`, `vehicle.status.updated`).
- **Conteneurisation :** MySQL Workbench & MySQL Workbench & Exécution Locale.
- **Gestion de versions & Outils :** Git, GitHub, Maven, Postman.

---

## 📂 4. Structure du Dépôt Git

Conformément aux consignes de l'enseignant pour la validation intermédiaire :

```
CarRental-AWD/
├── Backend/
│   ├── User-Service/           # Microservice Utilisateurs & Auth (Étudiant 1)
│   ├── Vehicle-Service/        # Microservice Véhicules & Disponibilités (Étudiant 2)
│   ├── Reservation-Service/    # Microservice Réservations (Étudiant 3)
│   ├── Payment-Service/        # Microservice Paiements & Factures (Étudiant 4)
│   ├── Agency-Service/         # Microservice Agences & Staff (Étudiant 5)
│   ├── Review-Service/         # Microservice Avis & Évaluations (Étudiant 6)
│   ├── API-Gateway/            # Microservice Commun : Passerelle & Routage
│   ├── pom.xml                 # POM parent multi-modules Maven
│   └── init_databases.sql (MySQL Workbench)      # Orchestration de tous les conteneurs
├── Frontend/                   # Application cliente Angular 17+
│   ├── src/                    # Composants, services, modèles, interceptors
│   ├── package.json
│   └── README.md
├── Documentation/
│   ├── Presentation/           # Support de présentation Séance 4 (.pptx) & Q&R
│   │   ├── Presentation_Seance4_CarRental.pptx
│   │   └── Questions_Reponses.md
│   ├── Diagrams/               # Sources PlantUML, Mermaid & images PNG
│   │   ├── Architecture_Globale.puml / .mmd / .png
│   │   ├── Cas_Utilisation_General.puml / .mmd / .png
│   │   ├── Sequence_Reservation_Complete.puml / .mmd / .png
│   │   ├── Sequence_Annulation_Paiement.puml
│   │   ├── Communication_Synchrone_Asynchrone.puml / .png
│   │   ├── Deploiement_MySQL Workbench.puml / .png
│   │   └── Classes_*.puml
│   └── Technical_Document/     # Document technique complet (.docx et .md)
│       └── Dossier_Technique_CarRental.docx
├── .gitignore
└── README.md
```

---

## 🚀 5. Installation et Exécution

### Prérequis
- MySQL Workbench et MySQL Workbench & Exécution Locale installés.
- Java 17 (JDK) et Maven 3.8+ (pour compilation locale).
- Node.js 18+ et npm (pour le frontend Angular).

### Option 1 : Démarrage Global via MySQL Workbench & Exécution Locale (Recommandé)
Pour lancer l'ensemble des conteneurs (Bases de données, RabbitMQ, Gateway et Microservices) :

```bash
cd Backend
-- Exécuter Backend/init_databases.sql dans MySQL Workbench
```

Vérifier l'état des conteneurs :
```bash
MySQL Workbench ps
```

### Option 2 : Exécution Locale par Service
1. **Démarrer les bases de données et RabbitMQ** via MySQL Workbench :
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15-alpine
   docker run -d --name mongo -p 27017:27017 mongo:6.0
   ```
2. **Compiler le backend complet** :
   ```bash
   cd Backend
   mvn clean install -DskipTests
   ```
3. **Lancer un microservice** (exemple Vehicle-Service) :
   ```bash
   cd Backend/Vehicle-Service
   mvn spring-boot:run
   ```
4. **Lancer le Frontend Angular** :
   ```bash
   cd Frontend
   npm install
   npm start
   ```
   L'interface est accessible sur `http://localhost:4200`.

---

## 🔗 6. Principaux Endpoints de l'API (via Gateway :8080)

| Service | Méthode | Endpoint | Description |
|---|---|---|---|
| **User** | `POST` | `/api/auth/register` | Inscription nouvel utilisateur |
| **User** | `POST` | `/api/auth/login` | Authentification et génération token JWT |
| **Vehicle** | `GET` | `/api/vehicles` | Liste complète des véhicules |
| **Vehicle** | `GET` | `/api/vehicles/search?brand=...&agencyId=...` | Filtrage multicritère de la flotte |
| **Vehicle** | `GET` | `/api/vehicles/{id}/availability` | Vérification de disponibilité immédiate |
| **Reservation** | `POST` | `/api/reservations` | Création d'une réservation (Appel Feign -> Vehicle & Payment) |
| **Reservation** | `GET` | `/api/reservations/user/{userId}` | Historique des réservations d'un client |
| **Reservation** | `PUT` | `/api/reservations/{id}/cancel` | Annulation et déclenchement remboursement |
| **Payment** | `POST` | `/api/payments/process` | Traitement/Simulation de paiement |
| **Payment** | `GET` | `/api/payments/reservation/{id}` | Consultation du paiement et facture associée |
| **Agency** | `GET` | `/api/agencies` | Liste des agences de location |
| **Agency** | `GET` | `/api/agencies/city/{city}` | Recherche d'agences par ville |
| **Review** | `POST` | `/api/reviews` | Dépôt d'un avis client avec note |
| **Review** | `GET` | `/api/reviews/vehicle/{vehicleId}` | Avis associés à un véhicule spécifique |

---

## 🤝 7. Workflow Git & Bonnes Pratiques

- **Branche principale `main` :** code stable, testé et validé.
- **Branche `develop` :** intégration continue des fonctionnalités.
- **Branches fonctionnelles :** `feature/user-auth`, `feature/vehicle-catalog`, `feature/reservation-flow`, etc.
- **Format des commits conventionnels :**
  - `feat(vehicle): add multi-criteria search endpoint`
  - `fix(reservation): correct price calculation for single-day rental`
  - `docs(uml): update sequence diagram for payment workflow`

---

## 📑 8. Livrables de la Séance 4

- 📄 **Dossier Technique Complet (Word .docx) :** [`Documentation/Technical_Document/Dossier_Technique_CarRental.docx`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/Technical_Document/Dossier_Technique_CarRental.docx)
- 📊 **Présentation Séance 4 (.pptx) :** [`Documentation/Presentation/Presentation_Seance4_CarRental.pptx`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/Presentation/Presentation_Seance4_CarRental.pptx)
- ❓ **Questions / Réponses de Soutenance (35+ Q&R) :** [`Documentation/Presentation/Questions_Reponses.md`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/Presentation/Questions_Reponses.md)
- 📋 **Checklist de Conformité Enseignant :** [`Documentation/CHECKLIST_VALIDATION.md`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/CHECKLIST_VALIDATION.md)
- 👥 **Répartition Détaillée des Tâches :** [`Documentation/REPARTITION_TACHES.md`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/REPARTITION_TACHES.md)
- 📅 **Planning Prévisionnel & Gestion des Risques :** [`Documentation/PLANNING_ET_RISQUES.md`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/PLANNING_ET_RISQUES.md)
