# Dossier Technique d'Architecture & Conception Microservices - CarRental

> **Projet AWD (Architecture Web Distribuée) - Séance 4 (Validation Intermédiaire)**  
> **Classe :** 4DAS | **Équipe :** 6 Étudiants  
> **Document Word officiel :** [`Dossier_Technique_CarRental.docx`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/Technical_Document/Dossier_Technique_CarRental.docx)

---

## Sommaire
1. [Introduction Générale & Contexte](#1-introduction-générale)
2. [Problématique Métier & Objectifs](#2-problématique-métier--objectifs)
3. [Acteurs & Cas d'Utilisation](#3-acteurs--cas-dutilisation)
4. [Principales Fonctionnalités](#4-principales-fonctionnalités)
5. [Architecture Globale des Microservices](#5-architecture-globale-des-microservices)
6. [Justification du Découpage en Microservices](#6-justification-du-découpage-en-microservices)
7. [Spécifications Détaillées des 6 Microservices Métier + Commun](#7-spécifications-détaillées-des-microservices)
8. [Modèle de Communication : Synchrone vs Asynchrone](#8-modèle-de-communication-inter-services)
9. [Diagrammes de Séquence des Parcours Clés](#9-diagrammes-de-séquence)
10. [Stratégie de Persistance Polyglotte (PostgreSQL & MongoDB)](#10-stratégie-de-persistance-polyglotte)
11. [Sécurité Stateless & Propagation JWT](#11-sécurité-stateless--propagation-jwt)
12. [Organisation Git & Gestion de Projet](#12-organisation-git--gestion-de-projet)
13. [Répartition des Tâches entre les 6 Membres](#13-répartition-des-tâches)
14. [Planning Prévisionnel & Gestion des Risques Techniques](#14-planning-prévisionnel--gestion-des-risques)
15. [Conclusion & Perspectives](#15-conclusion--perspectives)

---

## 1. Introduction Générale
Le projet **CarRental** s'inscrit dans le cadre du module **Architecture Web Distribuée (AWD)** pour la validation intermédiaire (Séance 4). Il a pour objectif de concevoir une plateforme web robuste, scalable et résiliente pour la location de véhicules en ligne.
En mettant en relation directe les clients et un réseau d'agences physiques, la plateforme automatise la consultation de flotte, la vérification de disponibilité sans surbooking, le calcul de devis, le paiement sécurisé et la collecte d'avis clients.

---

## 2. Problématique Métier & Objectifs

### Problématique
- **Gestion de la concurrence critique :** Empêcher strictement la réservation simultanée du même véhicule sur un même intervalle de dates (surbooking).
- **Asymétrie des charges :** Le catalogue subit une très forte intensité de requêtes de lecture, alors que la réservation et le paiement nécessitent une forte consistance transactionnelle.
- **Résilience et isolation des pannes :** Une défaillance dans un composant annexe (avis, notifications) ne doit jamais empêcher la réservation d'un véhicule.
- **Découplage d'équipe :** Permettre à une équipe de 6 étudiants d'avancer de front sans blocage mutuel.

### Objectifs
- Découpage pur en 6 microservices métier + 1 service commun (Gateway + Eureka + RabbitMQ).
- Application du pattern **Database-per-Service** (5 bases PostgreSQL + 1 base NoSQL MongoDB).
- Communication hybride : **Synchrone** (OpenFeign / REST) et **Asynchrone** (RabbitMQ AMQP).
- Application cliente Single Page Application (SPA) en **Angular 17+**.
- Déploiement conteneurisé complet avec **Docker Compose**.

---

## 3. Acteurs & Cas d'Utilisation
- **Client / Visiteur :** Recherche de véhicules par critères, vérification de disponibilité, réservation, paiement simulé, téléchargement de facture et rédaction d'avis.
- **Employé d'Agence (Agent) :** Suivi des réservations rattachées à son agence, préparation des véhicules, validation de prise en charge et retour, mise à jour d'état (maintenance, révision).
- **Administrateur :** Gestion des agences, supervision de la flotte globale, gestion des rôles et modération des avis.

---

## 4. Principales Fonctionnalités
1. Inscription sécurisée, authentification stateless et gestion des rôles (`CLIENT`, `AGENT`, `ADMIN`).
2. Gestion du parc automobile avec fiches techniques et tarification journalière.
3. Recherche multicritère (marque, catégorie, agence, prix max).
4. Moteur de réservation avec vérification de chevauchement et calcul automatisé de la durée et du prix total.
5. Traitement/simulation de paiement immédiat avec génération automatique de facture (`INV-XXXX`).
6. Gestion des annulations et émission automatique d'avoirs de remboursement.
7. Localisation des agences physiques et gestion du personnel local.
8. Évaluation des véhicules et agences avec notes (1 à 5) et modération des commentaires.

---

## 5. Architecture Globale des Microservices

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
   PostgreSQL   PostgreSQL    PostgreSQL    PostgreSQL    PostgreSQL     MongoDB
```

---

## 6. Justification du Découpage en Microservices
- **User-Service (Étudiant 1) :** Isole la cryptographie, les tokens JWT et la persistance des comptes.
- **Vehicle-Service (Étudiant 2) :** Isole le catalogue automobile soumis à forte charge de consultation.
- **Reservation-Service (Étudiant 3) :** Cœur du système, isole le contrôle temporel et le calcul des devis.
- **Payment-Service (Étudiant 4) :** Isole la logique financière, les factures et les transactions.
- **Agency-Service (Étudiant 5) :** Isole les adresses physiques et le personnel d'agence.
- **Review-Service (Étudiant 6) :** Isole les commentaires libres sous MongoDB pour ne pas surcharger les bases relationnelles.
- **API Gateway + Discovery (Collectif) :** Mutualise la sécurité, le routage et la découverte.

---

## 7. Spécifications Détaillées des Microservices

### 7.1. User-Service (Étudiant 1 - [Nom Étudiant 1])
- **Base :** PostgreSQL (`user_db:5432`)
- **Entités :** `User`, `Role`, enum `RoleName`.
- **Endpoints :**
  - `POST /api/auth/register` (201 Created)
  - `POST /api/auth/login` (200 OK + JWT)
  - `GET /api/auth/validate?token=...` (200 OK)
  - `GET /api/users/{id}` (200 OK / 404 Not Found)

### 7.2. Vehicle-Service (Étudiant 2 - [Nom Étudiant 2])
- **Base :** PostgreSQL (`vehicle_db:5433`)
- **Entités :** `Vehicle`, `Category`, enums `VehicleStatus`, `FuelType`, `Transmission`.
- **Endpoints :**
  - `GET /api/vehicles` (200 OK)
  - `GET /api/vehicles/search?brand=...&agencyId=...` (200 OK)
  - `GET /api/vehicles/{id}/availability` (200 OK)
  - `POST /api/vehicles` (201 Created)
  - `PATCH /api/vehicles/{id}/status` (200 OK)

### 7.3. Reservation-Service (Étudiant 3 - [Nom Étudiant 3])
- **Base :** PostgreSQL (`reservation_db:5434`)
- **Entités :** `Reservation`, enum `ReservationStatus`.
- **Endpoints :**
  - `POST /api/reservations` (201 Created)
  - `GET /api/reservations/{id}` (200 OK)
  - `GET /api/reservations/user/{userId}` (200 OK)
  - `PUT /api/reservations/{id}/cancel` (200 OK)

### 7.4. Payment-Service (Étudiant 4 - [Nom Étudiant 4])
- **Base :** PostgreSQL (`payment_db:5435`)
- **Entités :** `Payment`, `Invoice`, enums `PaymentStatus`, `PaymentMethod`.
- **Endpoints :**
  - `POST /api/payments/process` (201 Created)
  - `GET /api/payments/{id}` (200 OK)
  - `GET /api/payments/reservation/{resId}` (200 OK)
  - `POST /api/payments/refund/{resId}` (200 OK)

### 7.5. Agency-Service (Étudiant 5 - [Nom Étudiant 5])
- **Base :** PostgreSQL (`agency_db:5436`)
- **Entités :** `Agency`, `Address` (Embedded), `AgencyStaff`.
- **Endpoints :**
  - `GET /api/agencies` (200 OK)
  - `GET /api/agencies/{id}` (200 OK)
  - `GET /api/agencies/city/{city}` (200 OK)
  - `POST /api/agencies` (201 Created)

### 7.6. Review-Service (Étudiant 6 - [Nom Étudiant 6])
- **Base :** MongoDB (`review_db:27017`)
- **Entités :** `Review`, enums `ReviewTargetType` (`VEHICLE`, `AGENCY`), `ModerationStatus`.
- **Endpoints :**
  - `POST /api/reviews` (201 Created)
  - `GET /api/reviews/vehicle/{vehicleId}` (200 OK)
  - `GET /api/reviews/agency/{agencyId}` (200 OK)
  - `GET /api/reviews/user/{userId}` (200 OK)

---

## 8. Modèle de Communication Inter-Services
- **Synchrone (OpenFeign) :** Pour les actions où la réponse immédiate conditionne la suite (vérification de tarif, disponibilité, validation de paiement).
- **Asynchrone (RabbitMQ) :** Pour les actions secondaires découplées (mise à jour d'état du véhicule après confirmation, notification, journalisation).
- **Résilience :** Intégration de Resilience4j (Circuit Breaker) pour éviter l'effet domino en cas de ralentissement d'un service.

---

## 9. Diagrammes de Séquence
Le parcours complet d'une réservation comprend 6 étapes :
1. Recherche de véhicules via Gateway vers Vehicle-Service.
2. Sélection et confirmation de la disponibilité.
3. Création de la réservation avec calcul de devis (Statut `PENDING`).
4. Appel Feign vers Payment-Service pour simulation bancaire et facture (Statut `PAID`).
5. Mise à jour de la réservation en `CONFIRMED` et publication de l'événement `reservation.confirmed` sur RabbitMQ.
6. Le Vehicle-Service consomme l'événement et marque le véhicule comme `RENTED`.

---

## 10. Stratégie de Persistance Polyglotte
- **PostgreSQL 15 :** Choisi pour 5 services pour respecter les propriétés ACID, les contraintes relationnelles d'unicité et la gestion financière.
- **MongoDB 6.0 :** Choisi pour le Review-Service afin de stocker des documents semi-structurés, permettre un ciblage polymorphe (véhicules ou agences) et offrir des performances de lecture optimales.

---

## 11. Sécurité Stateless & Propagation JWT
- Authentification unique auprès de `User-Service`.
- Retour d'un token JWT signé avec expiration et rôles.
- Injection par le Frontend Angular via `JwtInterceptor` (`Authorization: Bearer <token>`).
- Validation par l'API Gateway et propagation des claims internes (`X-User-Id`, `X-User-Roles`).

---

## 12. Organisation Git & Gestion de Projet
- Branches : `main` (stable), `develop` (intégration), `feature/<service>` (développement individuel).
- Commits conventionnels : `feat:`, `fix:`, `docs:`, `test:`.
- Outil de gestion : GitHub Projects (Kanban) et Postman.

---

## 13. Répartition des Tâches
| Membre | Service | Responsabilités Clés |
|---|---|---|
| **Étudiant 1** | User-Service | Auth, JWT, Rôles, Comptes utilisateurs |
| **Étudiant 2** | Vehicle-Service | Parc automobile, Disponibilités, Recherche |
| **Étudiant 3** | Reservation-Service | Dates, Devis, Coordination inter-services |
| **Étudiant 4** | Payment-Service | Simulation financière, Factures, Remboursements |
| **Étudiant 5** | Agency-Service | Points de retrait, Adresses, Employés locaux |
| **Étudiant 6** | Review-Service | Avis NoSQL MongoDB, Notes 1-5, Modération |
| **Collectif** | Gateway & Infra | Routage, Eureka, RabbitMQ, Docker Compose |

---

## 14. Planning Prévisionnel & Gestion des Risques
Progression en 8 séances avec jalon intermédiaire validé en séance 4.
Mitigations techniques :
- **Surbooking :** Requête d'exclusion d'intervalles + verrouillage optimiste `@Version`.
- **Panne synchrone :** Circuit Breaker Resilience4j avec méthode Fallback.
- **Perte de messages :** Files d'attente RabbitMQ durables et acquittement manuel.

---

## 15. Conclusion
Le système CarRental est pleinement cadré et conforme aux exigences académiques de la séance 4. L'équipe dispose d'une architecture claire, de squelettes de microservices compilables, de diagrammes UML exhaustifs et d'une répartition équilibrée pour aborder sereinement les séances de développement suivantes.
