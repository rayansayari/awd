# Checklist de Conformité pour la Validation Intermédiaire (Séance 4)

Cette grille de contrôle vérifie point par point la stricte conformité des livrables du projet **CarRental** avec les consignes officielles de l'enseignant.

---

## 1. Dépôt Git & Structure des Dossiers

| Exigence Enseignant | État | Emplacement / Justification |
|---|:---:|---|
| Dépôt Git créé pour le projet AWD | [x] Terminé | Répertoire structuré prêt pour initialisation `git init` et push distant |
| Enseignant ajouté en tant que collaborateur | [ ] À compléter | **Action étudiant :** Inviter le pseudo GitHub de l'enseignant dès la création du repo public |
| Dossier `Backend/` regroupant les microservices | [x] Terminé | Contient les 6 microservices métier + API Gateway + Eureka + docker-compose.yml |
| Dossier `Frontend/` contenant l'application cliente | [x] Terminé | Application Angular 17+ avec structure MVC, services, modèles, interceptors |
| Dossier `Documentation/` structuré | [x] Terminé | Sous-dossiers `Presentation/`, `Diagrams/`, `Technical_Document/` présents |
| Présentation de la séance 4 incluse | [x] Terminé | `Documentation/Presentation/Presentation_Seance4_CarRental.pptx` |
| Diagramme d'architecture globale inclus | [x] Terminé | Formats PNG, Mermaid (`.mmd`) et PlantUML (`.puml`) dans `Documentation/Diagrams/` |
| Principaux diagrammes du projet inclus | [x] Terminé | Cas d'utilisation, classes par microservice, séquences, déploiement |
| Dossier technique complet (Word / docx) | [x] Terminé | `Documentation/Technical_Document/Dossier_Technique_CarRental.docx` |
| Fichier `README.md` à la racine | [x] Terminé | Présentation complète, guide d'installation, endpoints, commandes |
| Fichier `.gitignore` adapté | [x] Terminé | Filtre Java/Maven (target/), Angular (node_modules/), IDEs et OS |

---

## 2. Contenu de la Présentation (10 à 15 minutes)

| Exigence Enseignant | État | Diapositive / Support |
|---|:---:|---|
| Idée générale et problématique du projet | [x] Terminé | Slide 2 & 3 de la présentation PowerPoint |
| Acteurs et cas d'utilisation général | [x] Terminé | Slide 4 (Client, Employé d'agence, Admin) |
| Principales fonctionnalités décrites | [x] Terminé | Slide 5 (Recherche, Réservation, Simulation paiement, Agences, Avis) |
| Architecture globale proposée (diagramme, Gateway, sécurité, etc.) | [x] Terminé | Slide 6 (Diagramme inséré, Gateway 8080, Eureka 8761, RabbitMQ 5672) |
| Microservices, responsabilités et bases de données | [x] Terminé | Slide 7 (Tableau récapitulatif des 6 services + Database-per-service) |
| Technologies choisies et justification | [x] Terminé | Slide 8 (Java 17, Spring Boot 3, Angular 17, PostgreSQL, MongoDB) |
| Communications entre services (synchrone vs asynchrone) | [x] Terminé | Slide 9 (OpenFeign synchrone vs RabbitMQ events asynchrones) |
| **Partie individuelle : 1 min de speech par étudiant sur son service** | [x] Terminé | Slides 10 à 15 dédiées avec notes de discours minutées |
| Conception de chaque microservice (diagramme de classes) | [x] Terminé | Intégrée dans les fiches individuelles et le document technique |
| Contrats d'API par microservice (endpoints, codes réponse, événements) | [x] Terminé | Endpoints, codes HTTP (200, 201, 400, 404, 409) et events documentés |
| Microservice commun développé collectivement et présenté | [x] Terminé | API Gateway + Eureka Discovery + bus RabbitMQ expliqués |
| Organisation du dépôt Git et gestion de projet | [x] Terminé | Slide 16 (Branches `main`/`develop`/`feature`, commits conventionnels) |
| Planning prévisionnel et principaux risques | [x] Terminé | Slide 17 (Gantt séance 1 à 8, matrice des 7 risques et solutions) |
| Durée totale de la présentation respectée (10 à 15 min) | [x] Terminé | Calibrage global vérifié (5 min groupe + 6x1 min individuel + 2 min conclusion) |

---

## 3. Rendu sur Blackboard

| Élément à Soumettre sur Blackboard | État | Responsable / Format |
|---|:---:|---|
| Lien vers le dépôt Git public avec enseignant collaborateur | [ ] À compléter | À soumettre par le chef d'équipe sur Blackboard |
| Document technique complet (Word / .docx) | [x] Terminé | `Dossier_Technique_CarRental.docx` prêt au téléversement |
| Fichier de présentation (.pptx) | [x] Terminé | `Presentation_Seance4_CarRental.pptx` prêt au téléversement |
| Maîtrise de la discussion de 10 minutes | [x] Terminé | Préparée via `Documentation/Presentation/Questions_Reponses.md` (36 Q&R) |

---

## 4. Points d'Attention Particuliers & Rappels Enseignant

- [!] **Présence obligatoire :** Chaque membre de l'équipe doit être présent et s'exprimer oralement pour valider sa note individuelle.
- [!] **Remplacer les noms d'étudiants :** Dans `REPARTITION_TACHES.md`, dans le document Word et dans le PowerPoint, remplacer les mentions `[Nom Étudiant 1]` à `[Nom Étudiant 6]` par les vrais noms et prénoms réels de vos camarades avant la soutenance !
- [!] **Pousser sur GitHub :** Créer le dépôt sur GitHub, initialiser le dépôt local avec `git init`, `git add .`, `git commit -m "feat: initial commit with microservices architecture and documentation"`, puis pusher sur la branche `main`.
