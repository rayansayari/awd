# Support de Présentation - Séance 4 (Validation Intermédiaire) - CarRental

> **Format :** Présentation PowerPoint 16:9 • Durée : 10 à 15 minutes + 10 min de questions  
> **Fichier binaire officiel :** [`Presentation_Seance4_CarRental.pptx`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/Presentation/Presentation_Seance4_CarRental.pptx)  
> **Questions / Réponses de Soutenance :** [`Questions_Reponses.md`](file:///C:/Users/RAYEN/.gemini/antigravity/scratch/CarRental-AWD/Documentation/Presentation/Questions_Reponses.md)

---

## 📌 Déroulé et Chronométrage de la Présentation (10 à 15 minutes)

| Slide | Titre de la Diapositive | Intervenant | Durée Estimée |
|:---:|---|---|:---:|
| **1** | Page de Titre & Présentation de l'Équipe | Présentateur Collectif / Chef de groupe | 30 s |
| **2** | 1. Présentation Générale & Vision Métier | Membre Collectif | 1 min |
| **3** | 2. Acteurs du Système & Cas d'Utilisation Métier | Membre Collectif | 1 min |
| **4** | 3. Architecture Globale des Microservices | Architecte / Membre Collectif | 1 min |
| **5** | 4. Découpage Métier & Choix des Bases de Données | Membre Collectif | 1 min |
| **6** | 5. Communications Inter-Services (Synchrone vs Asynchrone) | Membre Collectif | 1 min |
| **7** | **Partie Individuelle : 1. User-Service** | **Étudiant 1 : [Nom Étudiant 1]** | **1 min** |
| **8** | **Partie Individuelle : 2. Vehicle-Service** | **Étudiant 2 : [Nom Étudiant 2]** | **1 min** |
| **9** | **Partie Individuelle : 3. Reservation-Service** | **Étudiant 3 : [Nom Étudiant 3]** | **1 min** |
| **10** | **Partie Individuelle : 4. Payment-Service** | **Étudiant 4 : [Nom Étudiant 4]** | **1 min** |
| **11** | **Partie Individuelle : 5. Agency-Service** | **Étudiant 5 : [Nom Étudiant 5]** | **1 min** |
| **12** | **Partie Individuelle : 6. Review-Service** | **Étudiant 6 : [Nom Étudiant 6]** | **1 min** |
| **13** | 6. Microservice Commun & Infrastructure Développée Collectivement | Membre Collectif Délégué | 1 min |
| **14** | 7. Organisation du Dépôt Git & Gestion de Projet | Membre Collectif | 1 min |
| **15** | 8. Planning Prévisionnel & Gestion des Risques Techniques | Membre Collectif | 1 min |
| **16** | Conclusion & Ouverture vers les Questions | Équipe entière | 30 s |
| **TOTAL**| **Présentation Globale** | **6 Étudiants** | **~13 min 30 s** |

---

## Contenu Diapositive par Diapositive & Notes de Discours Oral

---

### Diapositive 1 : Titre & Introduction
- **Titre :** CarRental - Plateforme Web de Location de Voitures en Microservices
- **Sous-titre :** Soutenance de Validation Intermédiaire – Séance 4 • Module AWD (4DAS)
- **Équipe de 6 Étudiants :** [Étudiant 1] • [Étudiant 2] • [Étudiant 3] • [Étudiant 4] • [Étudiant 5] • [Étudiant 6]
- **Notes de discours (30s) :**
  > *"Bonjour Monsieur / Madame. Nous sommes le groupe composé de 6 étudiants et nous avons le plaisir de vous présenter aujourd'hui l'architecture et la conception de notre projet AWD : CarRental, une plateforme web de location de voitures. Pour cette validation intermédiaire de séance 4, notre objectif est de vous démontrer la solidité de notre conception, la pertinence de notre découpage en 6 microservices métier et 1 service commun, la structure professionnelle de notre dépôt Git, ainsi que notre maîtrise des communications inter-services. Chacun d'entre nous présentera en 1 minute son microservice dédié, suivi des aspects transversaux."*

---

### Diapositive 2 : Présentation Générale & Vision Métier
- **Contenu :**
  - Plateforme reliant clients et agences physiques.
  - Recherche multicritère instantanée (marque, modèle, catégorie, tarif, agence).
  - Réservation en ligne en temps réel avec devis dynamique automatisé.
  - Simulation bancaire sécurisée (statuts `PAID`, `PENDING`, `CANCELLED`).
  - Gestion transparente des points de retrait et de restitution.
  - Évaluations clients vérifiées (notes 1 à 5 et commentaires modérés).
- **Notes de discours (1 min) :**
  > *"CarRental résout une problématique concrète : permettre à des clients de louer des véhicules de façon fluide et fiable sans risque d'erreur ou de surréservation. Sur le plan académique, nous avons appliqué les meilleures pratiques de l'ingénierie logicielle distribuée : isolation stricte des contextes métier, pattern Database-per-Service, communication hybride synchrone et asynchrone, et sécurité centralisée. Pour ce jalon de séance 4, comme exigé par les consignes, nous présentons une conception mature, des contrats d'API complets, un dépôt Git structuré et une répartition claire des responsabilités au sein de nos 6 membres."*

---

### Diapositive 3 : Acteurs du Système & Cas d'Utilisation Métier
- **Contenu :**
  - **Client / Visiteur :** Inscription, recherche, disponibilité temps réel, réservation, simulation paiement, téléchargement facture, avis clients.
  - **Employé d'Agence :** Gestion flotte locale, statuts de maintenance, validation de prise en charge et restitution.
  - **Administrateur :** Supervision de la flotte globale, gestion du réseau d'agences, assignation du staff, modération des avis.
- **Notes de discours (1 min) :**
  > *"Notre plateforme s'adresse à trois acteurs clairement différenciés : Le Client Web, qui dispose d'un parcours 100% autonome : de la recherche jusqu'au paiement simulé et à la réception immédiate de sa facture. L'Employé d'Agence, qui gère au quotidien le parc automobile local, prépare les véhicules et enregistre les retours. Et l'Administrateur, qui possède les droits les plus élevés pour piloter les agences et modérer les avis clients. Ces rôles sont garantis par Spring Security et propagés via les claims de nos jetons JWT."*

---

### Diapositive 4 : Architecture Globale des Microservices
- **Contenu :** Schéma d'architecture globale inséré (Frontend Angular :4200, API Gateway :8080, Eureka :8761, RabbitMQ :5672, 6 microservices métier, 6 bases de données dédiées).
- **Notes de discours (1 min) :**
  > *"Voici le cœur architectural de CarRental. En façade, le Frontend Angular communique uniquement avec l'API Gateway sur le port 8080. Cela évite d'exposer nos services internes et masque la topologie réseau. La Gateway s'appuie sur Netflix Eureka pour localiser dynamiquement les 6 microservices métier sans adresses codées en dur. Nous appliquons rigoureusement le pattern Database-per-Service : aucune base de données n'est partagée. Pour la communication, nous combinons les appels synchrones avec OpenFeign lorsque la réponse est immédiatement requise, et le bus RabbitMQ pour les notifications et les mises à jour asynchrones."*

---

### Diapositive 5 : Découpage Métier & Choix des Bases de Données
- **Contenu :** Tableau des 6 services, ports, bases et responsabilités clés (5 PostgreSQL + 1 MongoDB).
- **Notes de discours (1 min) :**
  > *"Ce tableau résume notre découpage métier équilibré entre les 6 membres de l'équipe. Pourquoi PostgreSQL pour 5 services ? Parce que ces domaines gèrent des entités relationnelles fortes exigeant la conformité ACID et l'intégrité référentielle, notamment pour les paiements, les immatriculations uniques et les contrats de réservation. Pourquoi MongoDB pour le Review-Service ? Les avis clients comportent des commentaires textuels de longueur variable et ciblent de façon polymorphe soit une agence, soit un véhicule. Le schéma NoSQL flexible de MongoDB et ses excellentes performances en lecture en font la solution idéale sans polluer nos bases relationnelles."*

---

### Diapositive 6 : Communications Inter-Services : Synchrone vs Asynchrone
- **Contenu :** Schéma comparatif OpenFeign vs RabbitMQ Topic Exchange.
- **Notes de discours (1 min) :**
  > *"L'enseignant insiste particulièrement sur la distinction entre communication synchrone et asynchrone. Dans CarRental, nous ne faisons pas de tout-synchrone ni de tout-asynchrone : Le synchrone avec OpenFeign est réservé aux étapes où le résultat immédiat est indispensable : le Reservation-Service doit connaître le prix exact et s'assurer que la voiture existe avant de valider le panier. En revanche, une fois la réservation confirmée, la notification et la mise à jour de statut du véhicule sont déléguées à RabbitMQ de manière asynchrone. Si le Vehicle-Service est ralenti, le message reste dans la queue sans bloquer l'utilisateur."*

---

### Diapositive 7 : Partie Individuelle - 1. User-Service (Étudiant 1)
- **Responsable :** `[Nom Étudiant 1]`
- **Points clés :** Authentification stateless, JWT HMAC-SHA256, rôles, PostgreSQL `user_db:5432`, endpoints `/api/auth/register` et `/api/auth/login`.
- **Notes de discours (1 min) :**
  > *"Bonjour, je suis [Nom Étudiant 1], responsable du User-Service. Mon service est le garant de la sécurité et de la gestion des identités dans CarRental. Il résout la problématique de l'authentification centralisée sans couplage fort en émettant des tokens sans état JWT signés. Lors de l'inscription ou de la connexion, les mots de passe sont chiffrés, les rôles comme ROLE_CLIENT ou ROLE_ADMIN sont attribués, et un token est retourné au client. J'ai choisi PostgreSQL pour garantir la cohérence stricte des comptes et l'unicité des adresses email. Mes endpoints principaux sont /api/auth/register et /api/auth/login. L'API Gateway valide ce token et propage l'identité aux autres services via des headers HTTP internes. Je suis prêt pour vos questions."*

---

### Diapositive 8 : Partie Individuelle - 2. Vehicle-Service (Étudiant 2)
- **Responsable :** `[Nom Étudiant 2]`
- **Points clés :** Parc automobile, catégories, disponibilités, PostgreSQL `vehicle_db:5433`, appels Feign et écoute RabbitMQ `reservation.confirmed`.
- **Notes de discours (1 min) :**
  > *"Bonjour, je suis [Nom Étudiant 2], responsable du Vehicle-Service. Mon microservice gère l'ensemble du parc automobile. La problématique est d'assurer un affichage réactif du catalogue avec un filtrage multicritère puissant par marque, agence et catégorie. J'ai conçu l'entité Vehicle avec un cycle d'état strict : AVAILABLE, RENTED, MAINTENANCE. En termes d'interactions, mon service est interrogé en synchrone par OpenFeign lors de la réservation pour confirmer le tarif journalier. De plus, il consomme de manière asynchrone l'événement RabbitMQ 'reservation.confirmed' pour passer le véhicule en RENTED sans impacter le temps de réponse de l'utilisateur. J'utilise PostgreSQL pour stocker les caractéristiques techniques et garantir l'unicité des plaques d'immatriculation."*

---

### Diapositive 9 : Partie Individuelle - 3. Reservation-Service (Étudiant 3)
- **Responsable :** `[Nom Étudiant 3]`
- **Points clés :** Orchestration de réservation, algorithme anti-surbooking, devis, statuts (PENDING, CONFIRMED, CANCELLED), PostgreSQL `reservation_db:5434`.
- **Notes de discours (1 min) :**
  > *"Bonjour, je suis [Nom Étudiant 3] et je pilote le Reservation-Service, le cœur névralgique de CarRental. Mon rôle est d'orchestrer la réservation. Lorsque le client valide ses dates, mon service calcule le nombre de jours, appelle Vehicle-Service via OpenFeign pour récupérer le prix journalier, enregistre la réservation avec le statut PENDING et déclenche le paiement en synchrone. Dès que le paiement réussit, la réservation passe à CONFIRMED et je publie un événement sur RabbitMQ. Pour éviter deux réservations simultanées pour le même véhicule, j'applique une requête de contrôle de chevauchement de dates et un verrouillage optimiste avec @Version. PostgreSQL est incontournable ici pour assurer la consistance transactionnelle ACID."*

---

### Diapositive 10 : Partie Individuelle - 4. Payment-Service (Étudiant 4)
- **Responsable :** `[Nom Étudiant 4]`
- **Points clés :** Simulation bancaire (PAID, PENDING, FAILED, REFUNDED), facturation automatique `INV-XXXX`, PostgreSQL `payment_db:5435`.
- **Notes de discours (1 min) :**
  > *"Bonjour, je suis [Nom Étudiant 4], responsable du Payment-Service. Mon microservice prend en charge le traitement financier et la facturation. Comme demandé dans les consignes, nous avons développé une simulation bancaire complète gérant les états PAID, PENDING, FAILED et REFUNDED. Lorsque Reservation-Service soumet un paiement via OpenFeign, mon service valide la transaction, génère une référence unique de transaction TX-XXXX et produit immédiatement une facture numérotée INV-XXXX. En cas d'annulation de réservation par le client, mon service traite également le remboursement en passant le paiement en REFUNDED. La base PostgreSQL assure la traçabilité comptable et la rigueur financière."*

---

### Diapositive 11 : Partie Individuelle - 5. Agency-Service (Étudiant 5)
- **Responsable :** `[Nom Étudiant 5]`
- **Points clés :** Points de retrait physiques, coordonnées, `Address` embarquée, horaires, PostgreSQL `agency_db:5436`.
- **Notes de discours (1 min) :**
  > *"Bonjour, je suis [Nom Étudiant 5], responsable de l'Agency-Service. Dans la location de véhicules, l'ancrage territorial est indispensable. Mon service répertorie les agences physiques, leurs adresses complètes, leurs coordonnées et les employés rattachés. Sur le plan architectural, mon service garantit un découplage total : les autres microservices ne font aucune jointure sur mes tables, ils référencent seulement un agencyId. J'ai implémenté un composant d'adresses embarqué Address avec ville et code postal, et exposé des endpoints optimisés pour rechercher les agences par ville. PostgreSQL me permet d'assurer l'intégrité des agences et l'unicité de leur code d'identification."*

---

### Diapositive 12 : Partie Individuelle - 6. Review-Service (Étudiant 6)
- **Responsable :** `[Nom Étudiant 6]`
- **Points clés :** Avis clients, notes 1 à 5, commentaires polymorphes (véhicule ou agence), MongoDB NoSQL `review_db:27017`.
- **Notes de discours (1 min) :**
  > *"Bonjour, je suis [Nom Étudiant 6], responsable du Review-Service. Mon service apporte la preuve sociale sur CarRental en permettant aux clients d'évaluer les véhicules et les agences avec des notes de 1 à 5 et des commentaires. Contrairement à mes camarades, j'ai fait le choix délibéré d'une base NoSQL MongoDB. Pourquoi ? Parce que les avis sont des données semi-structurées de taille variable, avec un ciblage polymorphe, et qu'ils subissent une charge de lecture massive. MongoDB offre d'excellentes performances d'agrégation pour calculer les notes moyennes sans ralentir nos bases transactionnelles. Mon service intègre également une modération simple pour rejeter les avis inappropriés."*

---

### Diapositive 13 : Microservice Commun & Infrastructure Développée Collectivement
- **Contenu :** API Gateway (Spring Cloud, :8080), Eureka Server (:8761), RabbitMQ (:5672), docker-compose.yml.
- **Notes de discours (1 min) :**
  > *"Comme l'exigent les consignes de l'enseignant, notre projet comporte une composante commune développée collectivement par toute l'équipe. Cette infrastructure comprend : 1. L'API Gateway sous Spring Cloud Gateway, qui applique le filtre JWT réactif, gère les CORS pour notre frontend Angular, et assure le routage dynamique. 2. Le Discovery Server Eureka, qui enregistre nos services et permet d'équilibrer la charge côté client sans aucune IP codée en dur. 3. Le Broker RabbitMQ, configuré avec un Topic Exchange pour découpler les événements de réservation et de paiement. Enfin, nous avons assemblé un docker-compose.yml complet qui permet à n'importe quel membre du groupe ou à l'enseignant de démarrer l'ensemble de la plateforme en une seule commande."*

---

### Diapositive 14 : Organisation du Dépôt Git & Gestion de Projet
- **Contenu :** Dépôt unique Backend/Frontend/Documentation, branches Git (`main`, `develop`, `feature/*`), conventions de commits, GitHub Projects, Postman.
- **Notes de discours (1 min) :**
  > *"La rigueur méthodologique est un point clé évalué en séance 4. Notre dépôt respecte scrupuleusement l'arborescence demandée : Backend regroupant les 6 services et la Gateway, Frontend avec notre application Angular, et Documentation avec nos diagrammes, notre support de présentation et notre dossier technique. Nous appliquons le modèle GitFlow : aucune modification n'est poussée directement sur 'main'. Chaque membre travaille sur sa branche de feature et soumet une Pull Request avec des messages de commit conventionnels. Pour le suivi, nous utilisons un tableau Kanban GitHub Projects et une collection Postman partagée."*

---

### Diapositive 15 : Planning Prévisionnel & Gestion des Risques
- **Contenu :** Feuille de route en 8 séances (Séance 4 = validation intermédiaire), matrice des 5 risques techniques majeurs (surbooking, panne synchrone, perte AMQP, échec paiement, CORS).
- **Notes de discours (1 min) :**
  > *"Pour garantir le succès du projet d'ici la séance 8, nous suivons un planning strict en 4 grandes phases. La séance 4 constitue notre jalon intermédiaire de validation de la conception. Nous avons également identifié les risques techniques majeurs et défini dès aujourd'hui nos solutions d'atténuation : le surbooking est empêché par des requêtes de chevauchement de dates et du verrouillage optimiste ; les pannes réseau sont contenues par des Circuit Breakers Resilience4j ; et les échecs de paiement sont compensés par des annulations automatiques suivant le pattern Saga."*

---

### Diapositive 16 : Conclusion & Session de Questions / Réponses
- **Contenu :** Remerciements, CarRental prêt pour l'implémentation avancée, ouverture de la discussion de 10 minutes avec l'enseignant.
- **Notes de discours (30s) :**
  > *"En conclusion, l'équipe CarRental a mis en place l'ensemble des fondations d'un système distribué professionnel : 6 microservices découplés, une passerelle d'accès sécurisée, un bus d'événements AMQP, des bases de données indépendantes et une interface Angular prête à être connectée. Nous vous remercions pour votre attention et nous sommes désormais tous les 6 à votre entière disposition pour répondre à vos questions techniques."*
