# Planning Prévisionnel & Gestion des Risques Techniques - CarRental

Ce document formalise la feuille de route du projet CarRental ainsi que l'analyse proactive des risques techniques, conformément aux attentes de l'enseignant pour la validation intermédiaire (Séance 4).

---

## 1. Planning Prévisionnel du Projet

Le projet s'étale sur 8 séances de travail encadré et de développement autonome en équipe :

```
Séance 1-2: Cadrage & Choix d'Architecture (TERMINÉ)
  ├── Définition du sujet CarRental
  ├── Découpage en 6 microservices + service commun
  └── Mise en place du dépôt Git & conventions

Séance 3-4: Conception & Validation Intermédiaire (JALON ACTUEL - SÉANCE 4)
  ├── Modélisation UML complète (Classes, Cas d'utilisation, Séquences)
  ├── Squelettes compilables Spring Boot & Angular
  ├── Contrats d'API REST & Documentation technique (.docx)
  └── Soutenance intermédiaire (Présentation 10-15 min)

Séance 5: Implémentation Avancée & Données
  ├── Implémentation complète de la couche Service & DAO
  ├── Mise en place des bases de données MySQL & MySQL avec Docker
  └── Intégration de Spring Cloud Eureka & Gateway

Séance 6: Communication Inter-Services & Sécurité
  ├── Mise en place de Spring Cloud OpenFeign & Circuit Breakers (Resilience4j)
  ├── Configuration du bus d'événements RabbitMQ (AMQP)
  └── Sécurisation JWT bout en bout (Gateway -> Services)

Séance 7: Intégration Frontend Angular & Tests
  ├── Finalisation des écrans Angular (Catalogue, Réservation, Dashboard)
  ├── Tests d'intégration de bout en bout (E2E)
  └── Simulation de pannes et résilience

Séance 8: Finalisation & Rendu Définitif
  ├── Optimisation des performances & build Docker final
  ├── Soutenance finale du projet
```

---

## 2. Diagramme de Gantt Synthétique

| Phase / Tâche | Sem. 1-2 | Sem. 3-4 (Validation) | Sem. 5 | Sem. 6 | Sem. 7 | Sem. 8 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Analyse & Découpage Microservices | 🟩 | | | | | |
| Diagrammes UML & Contrats d'API | | 🟩 | | | | |
| Squelette des 6 Services & Gateway | | 🟩 | | | | |
| Validation Intermédiaire (Séance 4) | | 🎯 | | | | |
| Persistance & Migrations SQL/Relationnel MySQL | | | 🟦 | | | |
| Communication Feign & RabbitMQ | | | | 🟦 | | |
| Authentification JWT & Sécurité | | | | 🟦 | | |
| Développement UI Angular | | | | 🟦 | 🟦 | |
| Tests d'Intégration & Résilience | | | | | 🟦 | |
| Validation Finale & Déploiement | | | | | | 🎯 |

---

## 3. Matrice d'Analyse et de Maîtrise des Risques Techniques

| # | Risque Identifié | Probabilité | Impact | Niveau | Stratégie d'Atténuation & Solution Retenue |
|---|---|:---:|:---:|:---:|---|
| **R1** | **Indisponibilité d'un microservice lors d'un appel synchrone (ex: Vehicle-Service inaccessible pendant une réservation)** | Moyenne | Élevé | 🔴 Critique | **Circuit Breaker & Fallback :** Intégration de *Resilience4j* avec OpenFeign. Si le service véhicule ne répond pas sous 1,5s, le Circuit Breaker s'ouvre et renvoie un message d'erreur convivial sans bloquer les ressources de la JVM. |
| **R2** | **Concurrence & Sur-réservation (Deux clients réservent le même véhicule aux mêmes dates)** | Élevée | Élevé | 🔴 Critique | **Verrouillage Optimiste & Contrainte Unique :** Utilisation de l'annotation `@Version` de JPA et d'une requête de contrôle d'intersection de dates dans une transaction ACID avec niveau d'isolation strict avant validation. |
| **R3** | **Perte de messages asynchrones lors d'un crash de RabbitMQ ou d'un service consommateur** | Faible | Élevé | 🟡 Modéré | **Persistance & Acquittement Manuel (Manual ACK) :** Configuration des files d'attente RabbitMQ en mode durable (`durable: true`) et messages persistants (`deliveryMode: 2`). Les messages ne sont acquittés qu'après traitement complet. |
| **R4** | **Incohérence de données distribuées en cas d'échec de paiement** | Moyenne | Moyen | 🟡 Modéré | **Modèle Saga / Compensation :** Si le Payment-Service échoue ou renvoie une erreur, Reservation-Service met à jour le statut en `CANCELLED` et émet un événement compensatoire pour remettre le véhicule en disponibilité immédiate. |
| **R5** | **Latence réseau cumulée lors des appels inter-services en chaîne** | Moyenne | Moyen | 🟡 Modéré | **Découplage Asynchrone :** Seuls les appels strictement nécessaires au commit de la réservation sont synchrones (disponibilité). Les actions secondaires (génération de reçu, mise à jour d'historique, email) sont déléguées à RabbitMQ en tâche de fond. |
| **R6** | **Désynchronisation des versions de contrats d'API entre étudiants** | Élevée | Moyen | 🟡 Modéré | **Spécification OpenAPI / Swagger centralisée :** Chaque étudiant documente ses DTOs et endpoints selon la convention stricte arrêtée dans le dossier technique. Revue systématique des PR (Pull Requests) avant fusion dans `develop`. |
| **R7** | **Problèmes de CORS ou de routage depuis le Frontend Angular** | Moyenne | Faible | 🟢 Faible | **Passerelle Unique :** Le Frontend ne communique qu'avec l'API Gateway sur `localhost:8080`. La Gateway intègre un `CorsWebFilter` réactif autorisant `localhost:4200` et propage le header `Authorization: Bearer <token>`. |
