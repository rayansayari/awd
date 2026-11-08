# Répartition des Rôles et des Tâches - CarRental AWD

Ce document détaille l'attribution des microservices et des responsabilités techniques pour chaque membre de l'équipe de 6 étudiants, conformément aux exigences de la validation intermédiaire (Séance 4).

Chaque étudiant dispose d'un microservice dédié, d'un périmètre précis de responsabilité, de ses diagrammes associés, de ses endpoints REST, et de son **speech oral calibré pour 1 minute**.

---

## Tableau Récapitulatif de la Répartition

| Membre de l'Équipe | Microservice Attribué | Rôle & Responsabilité Principale | Base de Données | Technologies Clés |
|---|---|---|---|---|
| **Étudiant 1**<br/>`[Nom Étudiant 1]` | **User-Service** | Authentification, JWT, Gestion des comptes, Rôles & Sécurité | MySQL (`user_db`) | Spring Boot, Spring Security, JJWT, JPA |
| **Étudiant 2**<br/>`[Nom Étudiant 2]` | **Vehicle-Service** | Parc automobile, Disponibilités, Filtres & Catégories | MySQL (`vehicle_db`) | Spring Boot, JPA, Hibernate Search |
| **Étudiant 3**<br/>`[Nom Étudiant 3]` | **Reservation-Service** | Cycle de vie des réservations, Devis, Coordination métier | MySQL (`reservation_db`) | Spring Boot, OpenFeign, RabbitMQ (Producer) |
| **Étudiant 4**<br/>`[Nom Étudiant 4]` | **Payment-Service** | Simulation de paiement, Facturation, Statuts transactions | MySQL (`payment_db`) | Spring Boot, OpenFeign, RabbitMQ (Producer) |
| **Étudiant 5**<br/>`[Nom Étudiant 5]` | **Agency-Service** | Agences physiques, Géolocalisation, Employés locaux | MySQL (`agency_db`) | Spring Boot, JPA, Spacial Queries |
| **Étudiant 6**<br/>`[Nom Étudiant 6]` | **Review-Service** | Évaluations, Notes (1-5), Commentaires, Modération | MySQL (`review_db`) | Spring Boot, Spring Data MySQL |
| **Collectif (Présenté par Étudiant 1 ou 3)** | **API Gateway + Discovery** | Routage centralisé, Enregistrement Eureka, Sécurité CORS, Docker | - | Spring Cloud Gateway, Netflix Eureka, Docker Compose |

---

## Fiches Individuelles par Microservice (1 Minute de Speech Oral)

---

### 👤 Étudiant 1 : User-Service (Authentification & Utilisateurs)
- **Étudiant responsable :** `[Nom Étudiant 1]`
- **Responsabilités :**
  - Inscription sécurisée des clients et employés.
  - Authentification par identifiant/email et mot de passe chiffré.
  - Émission et validation des jetons JWT (JSON Web Tokens).
  - Gestion des rôles : `ROLE_CLIENT`, `ROLE_AGENT`, `ROLE_ADMIN`.
- **Endpoints Clés :**
  - `POST /api/auth/register` (Code 201 Created)
  - `POST /api/auth/login` (Code 200 OK + JWT)
  - `GET /api/users/{id}` (Code 200 OK / 404 Not Found)
  - `PUT /api/users/{id}` (Code 200 OK)
  - `GET /api/auth/validate` (Code 200 OK)
- **Base de données :** MySQL (`user_db`) – Tables `users`, `roles`, `user_roles`.
- **Speech Oral (1 minute) :**
  > *"Bonjour, je suis [Nom Étudiant 1] et j'ai en charge le User-Service. Ce microservice est le garant de la sécurité et de l'identité au sein de CarRental. Il résout la problématique de la gestion centralisée des accès sans créer de couplage fort avec les autres services, grâce à l'émission de jetons stateless JWT. Lors de l'inscription ou de la connexion d'un client, le service vérifie les informations d'identification, attribue les rôles comme ROLE_CLIENT ou ROLE_ADMIN, et retourne un token signé. La base de données MySQL a été choisie pour garantir la rigueur relationnelle des rôles et l'intégrité des comptes. Ce token est ensuite validé au niveau de l'API Gateway pour sécuriser toutes les requêtes en aval. Mes endpoints principaux sont /api/auth/register et /api/auth/login. Je suis prêt pour vos questions techniques."*

---

### 🚗 Étudiant 2 : Vehicle-Service (Flotte & Véhicules)
- **Étudiant responsable :** `[Nom Étudiant 2]`
- **Responsabilités :**
  - Gestion du catalogue de véhicules (Marque, Modèle, Immatriculation, Année, Motorisation).
  - Gestion des catégories de voitures (Économique, Berline, SUV, Luxe) et de leurs tarifs journaliers de base.
  - Recherche multicritère et filtrage dynamique.
  - Vérification de l'état du véhicule (`AVAILABLE`, `RENTED`, `MAINTENANCE`, `OUT_OF_SERVICE`).
- **Endpoints Clés :**
  - `GET /api/vehicles` (Code 200 OK)
  - `GET /api/vehicles/search?brand=...&agencyId=...` (Code 200 OK)
  - `GET /api/vehicles/{id}/availability` (Code 200 OK)
  - `POST /api/vehicles` (Code 201 Created, réservé Admin/Agent)
  - `PATCH /api/vehicles/{id}/status` (Code 200 OK)
- **Base de données :** MySQL (`vehicle_db`) – Tables `vehicles`, `categories`.
- **Speech Oral (1 minute) :**
  > *"Bonjour, je suis [Nom Étudiant 2], responsable du Vehicle-Service. Mon service gère l'ensemble du parc automobile de la plateforme. La problématique métier centrale est de fournir aux clients un catalogue précis, filtrable et à jour en temps réel. J'ai conçu des endpoints de recherche multicritère par marque, agence et catégorie. En matière de communication inter-services, mon service est interrogé de manière synchrone par le service de réservation via OpenFeign pour vérifier la disponibilité et le tarif journalier du véhicule demandé. De plus, il écoute de manière asynchrone les événements émis par RabbitMQ : dès qu'une réservation est confirmée, le statut du véhicule bascule automatiquement à RENTED. J'utilise MySQL pour stocker les caractéristiques techniques de la flotte et assurer l'unicité des plaques d'immatriculation."*

---

### 📅 Étudiant 3 : Reservation-Service (Réservations)
- **Étudiant responsable :** `[Nom Étudiant 3]`
- **Responsabilités :**
  - Création et cycle de vie d'une réservation (`PENDING`, `CONFIRMED`, `ACTIVE`, `COMPLETED`, `CANCELLED`).
  - Calcul automatique de la durée (en jours) et du montant total en fonction du tarif journalier.
  - Contrôle des chevauchements de dates pour éviter les doubles réservations.
  - Orchestration synchrone vers le Vehicle-Service et le Payment-Service.
  - Émission d'événements asynchrones vers RabbitMQ.
- **Endpoints Clés :**
  - `POST /api/reservations` (Code 201 Created)
  - `GET /api/reservations/{id}` (Code 200 OK)
  - `GET /api/reservations/user/{userId}` (Code 200 OK)
  - `PUT /api/reservations/{id}/confirm` (Code 200 OK)
  - `PUT /api/reservations/{id}/cancel` (Code 200 OK)
- **Base de données :** MySQL (`reservation_db`) – Table `reservations`.
- **Speech Oral (1 minute) :**
  > *"Bonjour, je suis [Nom Étudiant 3] et je pilote le Reservation-Service, qui est le cœur fonctionnel de notre plateforme. Sa mission est d'orchestrer la réservation d'un véhicule de bout en bout. Lorsqu'un client soumet une demande avec des dates, mon service appelle d'abord Vehicle-Service en synchrone via OpenFeign pour s'assurer que le véhicule est libre et récupérer son tarif. Il calcule le montant total, enregistre la réservation avec le statut PENDING, puis sollicite immédiatement Payment-Service pour déclencher la simulation de paiement. Si le paiement réussit, la réservation passe à CONFIRMED et mon service publie un événement sur le broker RabbitMQ pour en informer les autres composants. MySQL est indispensable ici pour respecter les contraintes d'intégrité ACID lors des transactions de réservation."*

---

### 💳 Étudiant 4 : Payment-Service (Paiements & Factures)
- **Étudiant responsable :** `[Nom Étudiant 4]`
- **Responsabilités :**
  - Simulation de transaction bancaire (statuts `PENDING`, `PAID`, `FAILED`, `REFUNDED`).
  - Génération de factures associées avec référence unique (`INV-XXXX`).
  - Gestion des remboursements en cas d'annulation de réservation.
  - Publication des événements de paiement sur RabbitMQ.
- **Endpoints Clés :**
  - `POST /api/payments/process` (Code 201 Created)
  - `GET /api/payments/{id}` (Code 200 OK)
  - `GET /api/payments/reservation/{reservationId}` (Code 200 OK)
  - `POST /api/payments/refund/{reservationId}` (Code 200 OK)
- **Base de données :** MySQL (`payment_db`) – Tables `payments`, `invoices`.
- **Speech Oral (1 minute) :**
  > *"Bonjour, je suis [Nom Étudiant 4], en charge du Payment-Service. Ce service gère les transactions financières et la facturation. Conformément au cahier des charges, nous avons mis en place une simulation bancaire réaliste qui gère les statuts PENDING, PAID, FAILED et REFUNDED sans dépendre d'une passerelle bancaire externe lourde. Lorsque Reservation-Service envoie une requête de paiement, mon service génère un identifiant de transaction unique, valide le règlement et crée immédiatement une facture horodatée. Il prend également en charge le remboursement si le client annule sa location. J'ai choisi MySQL pour garantir l'auditabilité et la cohérence stricte des montants et des factures."*

---

### 🏢 Étudiant 5 : Agency-Service (Agences & Emplacements)
- **Étudiant responsable :** `[Nom Étudiant 5]`
- **Responsabilités :**
  - Répertoire des agences physiques de prise en charge et de restitution.
  - Coordonnées complètes, horaires d'ouverture et géolocalisation (Ville, Adresse, Code postal).
  - Gestion et rattachement des employés d'agence (`AgencyStaff`).
- **Endpoints Clés :**
  - `GET /api/agencies` (Code 200 OK)
  - `GET /api/agencies/{id}` (Code 200 OK)
  - `GET /api/agencies/city/{city}` (Code 200 OK)
  - `POST /api/agencies` (Code 201 Created)
  - `PUT /api/agencies/{id}` (Code 200 OK)
  - `DELETE /api/agencies/{id}` (Code 204 No Content)
- **Base de données :** MySQL (`agency_db`) – Tables `agencies`, `agency_staff`.
- **Speech Oral (1 minute) :**
  > *"Bonjour, je suis [Nom Étudiant 5] et je suis responsable de l'Agency-Service. Dans une plateforme de location, le lien physique est fondamental. Mon service permet aux clients d'identifier précisément les agences de départ et de retour selon la ville ou la zone géographique. Côté agence, il permet d'enregistrer les horaires d'ouverture, les coordonnées et les employés rattachés. Le service est découplé : un véhicule référence simplement un agencyId, ce qui évite les jointures inter-bases. La base MySQL permet de gérer la structure d'adresses et garantit l'unicité du code d'agence. Mes endpoints permettent notamment la recherche rapide par ville via /api/agencies/city/{city}."*

---

### ⭐ Étudiant 6 : Review-Service (Avis & Évaluations)
- **Étudiant responsable :** `[Nom Étudiant 6]`
- **Responsabilités :**
  - Collecte des notes (1 à 5 étoiles) et des avis rédigés par les clients.
  - Évaluations polymorphes : avis portant soit sur un véhicule (`VEHICLE`), soit sur une agence (`AGENCY`).
  - Calcul de la moyenne des notes et modération des avis (`PENDING`, `APPROVED`, `REJECTED`).
- **Endpoints Clés :**
  - `POST /api/reviews` (Code 201 Created)
  - `GET /api/reviews/vehicle/{vehicleId}` (Code 200 OK)
  - `GET /api/reviews/agency/{agencyId}` (Code 200 OK)
  - `GET /api/reviews/user/{userId}` (Code 200 OK)
- **Base de données :** MySQL (`review_db`) – Collection `reviews`.
- **Speech Oral (1 minute) :**
  > *"Bonjour, je suis [Nom Étudiant 6], responsable du Review-Service. Mon service gère les retours d'expérience et la réputation sur CarRental. Il permet aux clients ayant loué un véhicule d'attribuer une note de 1 à 5 étoiles et de rédiger un commentaire sur un véhicule ou sur une agence. J'ai modélisé l'entité Review sous Spring Data JPA avec une base relationnelle MySQL 8.0 dédiée carrental_review_db. L'utilisation d'un index composite sur le type et l'identifiant de la cible assure un chargement ultra-rapide des avis et le calcul de la moyenne. Le service intègre également une modération simple (APPROVED, REJECTED) pour masquer les avis inappropriés."*

---

### 🌐 Partie Collective : API Gateway & Infrastructure Commune
- **Présentée par :** `[Nom Étudiant 1 ou Nom Étudiant 3]` (délégation collective)
- **Responsabilités collectives :**
  - Configuration de **Spring Cloud Gateway** sur le port `8080`.
  - Intégration de **Netflix Eureka** sur le port `8761` pour la découverte dynamique sans IPs en dur.
  - Mise en place du broker **RabbitMQ** sur le port `5672`.
  - Configuration de la politique CORS pour autoriser le frontend Angular (`localhost:4200`).
  - Orchestration globale via le fichier `docker-compose.yml`.
