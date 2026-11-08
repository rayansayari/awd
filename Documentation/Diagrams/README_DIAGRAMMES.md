# Répertoire des Diagrammes UML et Architecture - CarRental

Ce dossier regroupe l'ensemble des diagrammes d'architecture et de conception UML du projet **CarRental**, conformes aux exigences de la validation intermédiaire (Séance 4).

Chaque diagramme est disponible au format source **PlantUML (`.puml`)** et directement visualisable en **Mermaid** ci-dessous.

---

## 1. Diagramme d'Architecture Globale

```mermaid
graph TB
    subgraph CLIENT["Client Web"]
        ANGULAR["Frontend Angular 17+<br/>SPA Port 4200"]
    end

    subgraph INFRA["Infrastructure Commune"]
        GATEWAY["API Gateway (Spring Cloud)<br/>Port 8080<br/>Routage, JWT, CORS, Sécurité"]
        EUREKA["Eureka Server Discovery<br/>Port 8761"]
        RABBIT["RabbitMQ Message Broker<br/>Port 5672"]
    end

    subgraph SERVICES["Microservices Métier (Spring Boot 3.2)"]
        USER["User Service<br/>Port 8081"]
        VEHICLE["Vehicle Service<br/>Port 8082"]
        RES["Reservation Service<br/>Port 8083"]
        PAY["Payment Service<br/>Port 8084"]
        AGENCY["Agency Service<br/>Port 8085"]
        REVIEW["Review Service<br/>Port 8086"]
    end

    subgraph DATABASES["Bases de Données (Database-per-Service)"]
        DB_USER[("user_db (MySQL)")]
        DB_VEHICLE[("vehicle_db (MySQL)")]
        DB_RES[("reservation_db (MySQL)")]
        DB_PAY[("payment_db (MySQL)")]
        DB_AGENCY[("agency_db (MySQL)")]
        DB_REVIEW[("review_db (MySQL)")]
    end

    ANGULAR -->|HTTP / REST| GATEWAY
    GATEWAY --> EUREKA
    GATEWAY --> USER
    GATEWAY --> VEHICLE
    GATEWAY --> RES
    GATEWAY --> PAY
    GATEWAY --> AGENCY
    GATEWAY --> REVIEW

    RES -->|OpenFeign| VEHICLE
    RES -->|OpenFeign| PAY
    VEHICLE -->|OpenFeign| AGENCY

    RES -.->|Event reservation.confirmed| RABBIT
    PAY -.->|Event payment.completed| RABBIT
    RABBIT -.-> VEHICLE

    USER --- DB_USER
    VEHICLE --- DB_VEHICLE
    RES --- DB_RES
    PAY --- DB_PAY
    AGENCY --- DB_AGENCY
    REVIEW --- DB_REVIEW
```

---

## 2. Diagramme de Cas d'Utilisation Général

```mermaid
flowchart LR
    subgraph Acteurs
        Client["Visiteur / Client"]
        Agent["Employé d'Agence"]
        Admin["Administrateur"]
    end

    subgraph UserModule["User Service"]
        UC1["S'inscrire / Se connecter"]
        UC2["Gérer profil & rôles"]
    end

    subgraph VehicleModule["Vehicle Service"]
        UC3["Rechercher & filtrer véhicules"]
        UC4["Vérifier disponibilité"]
        UC5["Gérer le parc de véhicules"]
    end

    subgraph ReservationModule["Reservation Service"]
        UC6["Effectuer une réservation"]
        UC7["Consulter l'historique"]
        UC8["Modifier / Annuler réservation"]
        UC9["Valider prise en charge"]
    end

    subgraph PaymentModule["Payment Service"]
        UC10["Simuler / Valider paiement"]
        UC11["Consulter factures"]
        UC12["Traiter remboursements"]
    end

    subgraph AgencyModule["Agency Service"]
        UC13["Localiser les agences"]
        UC14["Gérer agences & personnels"]
    end

    subgraph ReviewModule["Review Service"]
        UC15["Laisser une note et un avis"]
        UC16["Consulter / Modérer les avis"]
    end

    Client --> UC1
    Client --> UC3
    Client --> UC4
    Client --> UC6
    Client --> UC7
    Client --> UC8
    Client --> UC10
    Client --> UC11
    Client --> UC13
    Client --> UC15

    Agent --> UC5
    Agent --> UC9
    Agent --> UC16

    Admin --> UC2
    Admin --> UC14
    Admin --> UC12
    Admin --> UC5
```

---

## 3. Diagrammes de Classes par Microservice

### 3.1. User Service
```mermaid
classDiagram
    class User {
        -Long id
        -String username
        -String email
        -String password
        -String firstName
        -String lastName
        -String phoneNumber
        -String driverLicenseNumber
        -Boolean enabled
        -LocalDateTime createdAt
    }
    class Role {
        -Long id
        -RoleName name
        -String description
    }
    class RoleName {
        <<enumeration>>
        ROLE_CLIENT
        ROLE_AGENT
        ROLE_ADMIN
    }
    User "1" *-- "1..*" Role : possède
    Role --> RoleName
```

### 3.2. Vehicle Service
```mermaid
classDiagram
    class Vehicle {
        -Long id
        -String brand
        -String model
        -Integer year
        -String licensePlate
        -BigDecimal pricePerDay
        -VehicleStatus status
        -Long agencyId
        -String imageUrl
    }
    class Category {
        -Long id
        -String name
        -String description
        -BigDecimal baseRate
    }
    class VehicleStatus {
        <<enumeration>>
        AVAILABLE
        RENTED
        MAINTENANCE
        OUT_OF_SERVICE
    }
    Vehicle "*" --> "1" Category : classifié dans
    Vehicle --> VehicleStatus
```

### 3.3. Reservation Service
```mermaid
classDiagram
    class Reservation {
        -Long id
        -String reservationNumber
        -Long userId
        -Long vehicleId
        -Long pickupAgencyId
        -Long returnAgencyId
        -LocalDate startDate
        -LocalDate endDate
        -Long totalDays
        -BigDecimal dailyRate
        -BigDecimal totalPrice
        -ReservationStatus status
        +calculateTotal() BigDecimal
    }
    class ReservationStatus {
        <<enumeration>>
        PENDING
        CONFIRMED
        ACTIVE
        COMPLETED
        CANCELLED
    }
    Reservation --> ReservationStatus
```

### 3.4. Payment Service
```mermaid
classDiagram
    class Payment {
        -Long id
        -String transactionId
        -Long reservationId
        -Long userId
        -BigDecimal amount
        -String currency
        -PaymentMethod paymentMethod
        -PaymentStatus status
        -LocalDateTime paymentDate
    }
    class Invoice {
        -Long id
        -String invoiceNumber
        -Long paymentId
        -Long reservationId
        -BigDecimal totalAmount
        -LocalDateTime issuedAt
    }
    class PaymentStatus {
        <<enumeration>>
        PENDING
        PAID
        FAILED
        REFUNDED
    }
    class PaymentMethod {
        <<enumeration>>
        CREDIT_CARD
        PAYPAL
        CASH_ON_PICKUP
    }
    Payment "1" -- "0..1" Invoice : génère
    Payment --> PaymentStatus
    Payment --> PaymentMethod
```

### 3.5. Agency Service
```mermaid
classDiagram
    class Agency {
        -Long id
        -String name
        -String code
        -String email
        -String phone
        -Address address
        -String openingHours
        -Boolean active
    }
    class Address {
        -String street
        -String city
        -String state
        -String zipCode
        -String country
        -Double latitude
        -Double longitude
    }
    class AgencyStaff {
        -Long id
        -Long userId
        -Long agencyId
        -String position
        -LocalDate hireDate
    }
    Agency *-- Address : localisée à
    Agency "1" -- "0..*" AgencyStaff : emploie
```

### 3.6. Review Service
```mermaid
classDiagram
    class Review {
        -String id
        -Long userId
        -ReviewTargetType targetType
        -Long targetId
        -Integer rating
        -String comment
        -ModerationStatus status
        -LocalDateTime createdAt
    }
    class ReviewTargetType {
        <<enumeration>>
        VEHICLE
        AGENCY
    }
    class ModerationStatus {
        <<enumeration>>
        PENDING
        APPROVED
        REJECTED
    }
    Review --> ReviewTargetType
    Review --> ModerationStatus
```

---

## 4. Diagramme de Séquence - Parcours Réservation Complet

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client (Angular)
    participant GW as API Gateway (:8080)
    participant VS as Vehicle Service (:8082)
    participant RS as Reservation Service (:8083)
    participant PS as Payment Service (:8084)
    participant MQ as RabbitMQ Broker

    Client->>GW: GET /api/vehicles/search?agency=1&cat=SUV
    GW->>VS: GET /api/vehicles/search
    VS-->>GW: 200 OK [Liste véhicules disponibles]
    GW-->>Client: 200 OK (Catalogue affiché)

    Client->>GW: POST /api/reservations (JWT, dates, vehicleId=5)
    GW->>RS: POST /api/reservations

    RS->>VS: [OpenFeign Synchrone] GET /api/vehicles/5
    VS-->>RS: 200 OK {pricePerDay: 45, status: AVAILABLE}
    Note over RS: Calcul montant (225€) & Sauvegarde (Statut PENDING)

    RS->>PS: [OpenFeign Synchrone] POST /api/payments/process (225€)
    Note over PS: Simulation succès -> Statut PAID + Facture #INV-101
    PS-->>RS: 201 Created {status: PAID, txId: TX-77892}

    Note over RS: Mise à jour Réservation -> CONFIRMED
    RS-)MQ: [Asynchrone] "reservation.confirmed" {resId: 101, vehicleId: 5}
    MQ-)VS: Consomme événement -> met à jour statut (RENTED)

    RS-->>GW: 201 Created (Réservation confirmée)
    GW-->>Client: 201 Created (Confirmation & Facture)
```

---

## 5. Diagramme de Communication Synchrone vs Asynchrone

```mermaid
flowchart TD
    subgraph SYNC["Communications Synchrones (REST / OpenFeign)"]
        direction LR
        RS1["Reservation Service"] -->|1. Vérifie disponibilité| VS1["Vehicle Service"]
        RS1 -->|2. Traitement paiement| PS1["Payment Service"]
        VS1 -->|3. Vérifie agence rattachement| AS1["Agency Service"]
    end

    subgraph ASYNC["Communications Asynchrones (RabbitMQ AMQP)"]
        direction LR
        RS2["Reservation Service"] -.->|Publie reservation.confirmed| EX["Exchange: carrental.topic"]
        PS2["Payment Service"] -.->|Publie payment.completed| EX
        EX -.->|Queue vehicle.events| VS2["Vehicle Service"]
        EX -.->|Queue notification.events| NOTIF["Notification Service"]
    end
```

---

## 6. Diagramme de Déploiement Conteneurisé

```mermaid
graph TB
    subgraph Host["Hôte Docker (Network: carrental-net)"]
        NGINX["Frontend Angular (Nginx) :4200"]
        GATEWAY["API Gateway :8080"]
        EUREKA["Eureka Server :8761"]
        RABBIT["RabbitMQ :5672 / :15672"]

        USER_S["User Service :8081"]
        VEH_S["Vehicle Service :8082"]
        RES_S["Reservation Service :8083"]
        PAY_S["Payment Service :8084"]
        AGN_S["Agency Service :8085"]
        REV_S["Review Service :8086"]

        DB1[("MySQL user_db :5432")]
        DB2[("MySQL vehicle_db :5433")]
        DB3[("MySQL res_db :5434")]
        DB4[("MySQL pay_db :5435")]
        DB5[("MySQL agency_db :5436")]
        DB6[("MySQL review_db :27017")]
    end

    NGINX --> GATEWAY
    GATEWAY --> EUREKA
    GATEWAY --> USER_S & VEH_S & RES_S & PAY_S & AGN_S & REV_S
    USER_S --> DB1
    VEH_S --> DB2
    RES_S --> DB3
    PAY_S --> DB4
    AGN_S --> DB5
    REV_S --> DB6
    RES_S & PAY_S -.-> RABBIT
    RABBIT -.-> VEH_S
```
