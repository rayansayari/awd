# Questions & Réponses pour la Soutenance AWD (Séance 4) - CarRental

Ce document prépare l'équipe de 6 étudiants à la session de discussion technique de 10 minutes avec l'enseignant. Il regroupe **36 questions fondamentales et pointues**, réparties entre questions d'architecture générale des microservices et questions spécifiques au domaine métier de **CarRental**.

---

## 🏛️ PARTIE 1 : Architecture des Microservices & Principes Généraux

### Q1. Pourquoi avoir choisi une architecture microservices plutôt qu'un monolithe pour ce projet ?
**Réponse :**
1. **Découplage organisationnel :** Dans une équipe de 6 étudiants, chaque membre peut développer, tester, déployer et faire évoluer son propre service de façon totalement autonome, sans risque de conflits de merge permanents sur un monolithe partagé.
2. **Scalabilité ciblée :** Le service de consultation des véhicules subit une charge de lecture beaucoup plus intense que le service de paiement. En microservices, nous pouvons répliquer uniquement l'instance `Vehicle-Service` sans dupliquer tout le système.
3. **Résilience et isolation des pannes :** Une défaillance dans le module des avis clients (`Review-Service`) n'empêche absolument pas un utilisateur de rechercher un véhicule et de finaliser sa réservation.
4. **Polyglot persistence :** Possibilité d'adapter la base de données au besoin métier : MySQL (relationnel ACID) pour les transactions et réservations, et MySQL (orienté document flexible) pour les avis.

---

### Q2. Quel est le rôle exact de l'API Gateway et pourquoi ne pas laisser le Frontend contacter directement chaque microservice ?
**Réponse :**
L'API Gateway (Spring Cloud Gateway) sert de **point d'entrée unique** (port `8080`) pour le Frontend Angular. Sans elle :
- Le client devrait connaître les adresses IP et ports dynamiques de 6 services différents (`8081` à `8086`), ce qui violerait le principe d'encapsulation et compliquerait les politiques réseau.
- Elle centralise les aspects transversaux (*cross-cutting concerns*) : routage dynamique via Eureka, validation des jetons JWT, gestion des en-têtes CORS, rate limiting et logging d'audit.
- Elle réduit le bavardage réseau (*chatty I/O*) en permettant éventuellement d'agréger plusieurs requêtes en une seule.

---

### Q3. Comment fonctionne la découverte de services avec Netflix Eureka ?
**Réponse :**
Chaque microservice s'enregistre au démarrage auprès d'Eureka Server (`http://localhost:8761/eureka/`) en fournissant son nom applicatif (ex: `vehicle-service`) et ses métadonnées réseau. Périodiquement (toutes les 30 secondes par défaut), les services envoient un signal de battement de cœur (*heartbeat*). L'API Gateway et les clients OpenFeign interrogent Eureka pour obtenir la liste des instances saines et effectuent un équilibrage de charge côté client (*Client-Side Load Balancing* avec Spring Cloud LoadBalancer). Ainsi, aucune adresse IP n'est codée en dur.

---

### Q4. Pourquoi avoir choisi le pattern "Database-per-Service" ?
**Réponse :**
Le pattern Database-per-Service garantit le **découplage strict** des microservices :
- Aucune dépendance de schéma : une modification de table dans `vehicle_db` n'impacte pas le code du `Reservation-Service`.
- Aucune possibilité de faire des jointures SQL directes entre tables de domaines distincts, ce qui force une séparation nette des responsabilités via des APIs REST ou des événements.
- Autonomie totale des déploiements et des sauvegardes.

---

### Q5. Pourquoi avoir choisi MySQL 8.0 pour l'ensemble des 6 microservices ?
**Réponse :**
1. **Conformité transactionnelle ACID & Moteur InnoDB :** Tous les microservices (utilisateurs, véhicules, réservations, paiements, agences et avis) bénéficient de la robustesse du moteur InnoDB, garantissant des transactions atomiques, la gestion des verrous et une intégrité référentielle stricte.
2. **Standard industriel éprouvé & Homogénéité opérationnelle :** Utiliser MySQL 8.0 sur l'ensemble des services unifie la pile technologique : une seule compétence technique requise pour toute l'équipe de 6 étudiants, mêmes outils d'administration (phpMyAdmin disponible sur le port 8088, MySQL Workbench) et même connecteur JDBC officiel (mysql-connector-j).
3. **Gestion optimisée des avis sous MySQL :** L'entité Review utilise des colonnes typées avec index composite sur (targetType, targetId), assurant des temps de réponse instantanés en millisecondes pour charger les avis par véhicule ou par agence.
4. **Support d'encodage moderne :** Le jeu de caractères utf8mb4 supporte nativement tous les caractères internationaux et émojis dans les commentaires clients.

---

### Q6. Quelle est la différence fondamentale entre communication synchrone et asynchrone ?
**Réponse :**
- **Synchrone (Request/Response - REST / OpenFeign) :** Le service appelant émet une requête HTTP et suspend son traitement en attendant la réponse du service cible (bloquant ou réactif). C'est indispensable quand le résultat est immédiatement obligatoire pour poursuivre l'opération métier (ex: vérifier le tarif et la disponibilité d'un véhicule avant de créer la réservation).
- **Asynchrone (Event-Driven - RabbitMQ AMQP) :** Le service producteur publie un événement sur un échange (ex: `reservation.confirmed`) et reprend immédiatement son exécution sans attendre. Les consommateurs traitent le message quand ils sont disponibles. Cela favorise le découplage temporel et la résilience (si le consommateur est éteint, le message reste stocké dans la file d'attente).

---

### Q7. Comment gérez-vous la panne d'un microservice appelé en synchrone (ex: Vehicle-Service qui ne répond pas) ?
**Réponse :**
Nous utilisons le pattern **Circuit Breaker** (avec la bibliothèque Resilience4j intégrée à Spring Cloud OpenFeign) :
- Lorsqu'un certain seuil d'échecs ou de timeouts est atteint (ex: 50% d'échecs sur 10 requêtes), le circuit passe de l'état `CLOSED` à `OPEN`.
- Les appels suivants sont immédiatement redirigés vers une méthode de repli (*fallback*) sans attendre de timeout, préservant ainsi les threads de la machine.
- Après un délai déterminé, le circuit passe en `HALF-OPEN` pour tester si le service distant a récupéré.

---

### Q8. Comment fonctionne la sécurité et la propagation de l'identité dans votre architecture ?
**Réponse :**
Nous appliquons une sécurité basée sur des jetons **JWT (JSON Web Token)** sans état (*stateless*) :
1. Le client s'authentifie sur `POST /api/auth/login` auprès du `User-Service`.
2. Le `User-Service` valide les identifiants et renvoie un JWT signé avec une clé secrète (contenant l'ID utilisateur, l'email et ses rôles).
3. À chaque requête subséquente, le client envoie le header `Authorization: Bearer <token>`.
4. L'API Gateway intercepte la requête, vérifie la signature et la validité du token, puis extrait les claims et les injecte dans des headers HTTP internes (ex: `X-User-Id`, `X-User-Roles`) propagés aux microservices métier.

---

### Q9. Comment gérez-vous les transactions distribuées sans transaction SQL globale ?
**Réponse :**
Dans une architecture microservices, nous ne pouvons pas utiliser de transaction distribuée à deux phases (2PC / Two-Phase Commit) en raison de sa lenteur et de son couplage fort. Nous appliquons le **pattern Saga basé sur l'orchestration ou la chorégraphie** :
- Chaque service exécute sa transaction locale et émet un événement.
- Si une étape échoue (ex: échec du paiement), des **transactions de compensation** sont déclenchées : `Reservation-Service` passe le statut de la réservation à `CANCELLED` et émet un événement pour que `Vehicle-Service` remette le véhicule à l'état `AVAILABLE`.

---

### Q10. Comment garantissez-vous qu'une exception dans un microservice renvoie un message d'erreur standardisé ?
**Réponse :**
Chaque microservice implémente un `@RestControllerAdvice` avec une classe `GlobalExceptionHandler`. Elle intercepte les exceptions courantes (`MethodArgumentNotValidException`, `EntityNotFoundException`, `BusinessException`) et renvoie une réponse JSON normalisée conforme à la spécification **RFC 7807 (Problem Details for HTTP APIs)**, contenant :
- `timestamp`
- `status` (ex: 400, 404, 409)
- `error` (ex: "Not Found")
- `message` (ex: "Véhicule introuvable avec l'ID 12")
- `path` (l'URI appelée)

---

### Q11. Qu'est-ce que Spring Cloud OpenFeign et pourquoi l'utiliser plutôt que RestTemplate ?
**Réponse :**
Spring Cloud OpenFeign est un client REST déclaratif. Au lieu d'écrire du code verbeux avec `RestTemplate` ou `WebClient` (création manuelle d'URL, parsing de requêtes), nous déclarons simplement une interface Java annotée avec `@FeignClient(name = "vehicle-service")` et des annotations Spring MVC (`@GetMapping`, `@PathVariable`). Feign génère dynamiquement l'implémentation, intègre automatiquement la découverte Eureka et s'associe nativement avec Resilience4j pour le Circuit Breaker.

---

### Q12. Qu'est-ce que Docker Compose apporte dans votre architecture ?
**Réponse :**
Notre architecture compte plus de 10 composants (6 microservices métier, API Gateway, Eureka, RabbitMQ, 5 bases MySQL et 1 base MySQL). Docker Compose nous permet de décrire l'intégralité de cet écosystème dans un unique fichier `docker-compose.yml` et de démarrer toute la plateforme en une seule commande (`docker-compose up -d`) sur un réseau virtuel privé partagé (`carrental-network`), avec des volumes persistants pour chaque base de données.

---

## 🚗 PARTIE 2 : Questions Spécifiques au Domaine Métier CarRental

### Q13. Comment vérifiez-vous qu'une voiture est réellement disponible entre deux dates données ?
**Réponse :**
La vérification de disponibilité se fait à deux niveaux :
1. **Statut instantané :** Le `Vehicle-Service` vérifie que le statut du véhicule n'est ni `MAINTENANCE`, ni `OUT_OF_SERVICE`.
2. **Contrôle d'intersection de dates :** Le `Reservation-Service` exécute une requête JPQL sur la table `reservations` pour s'assurer qu'aucune réservation active ou confirmée n'entre en conflit avec l'intervalle demandé :
   ```sql
   SELECT r FROM Reservation r 
   WHERE r.vehicleId = :vehicleId 
     AND r.status IN ('CONFIRMED', 'ACTIVE')
     AND (r.startDate <= :reqEndDate AND r.endDate >= :reqStartDate)
   ```
   Si cette liste est vide, le véhicule est garanti disponible pour cette période.

---

### Q14. Comment évitez-vous qu'un même véhicule soit réservé simultanément par deux clients différents (problème de concurrence) ?
**Réponse :**
Nous combinons deux mécanismes :
1. **Verrouillage optimiste (`@Version`) :** Une colonne de versioning JPA empêche la validation concurrente si l'état a été altéré entre la lecture et la mise à jour.
2. **Transaction atomique avec verrouillage pessimiste ou contrainte d'exclusion :** Lors de la soumission de la réservation, nous utilisons un bloc transactionnel `@Transactional(isolation = Isolation.SERIALIZABLE)` ou une requête avec `Pessimistic Lock` sur le véhicule durant la création de la réservation. Le premier commit valide la réservation ; la deuxième requête concurrente échoue avec un code HTTP `409 Conflict`.

---

### Q15. Comment calculez-vous le prix total d'une réservation ?
**Réponse :**
Le calcul est orchestré par le `Reservation-Service` :
1. Calcul du nombre de jours de location : `days = ChronoUnit.DAYS.between(startDate, endDate)`. Si les dates de début et fin sont identiques, le minimum appliqué est de 1 jour.
2. Récupération du tarif journalier (`pricePerDay`) auprès du `Vehicle-Service`.
3. Calcul du montant de base : `totalPrice = pricePerDay * days`.
4. Éventuel calcul des options ou taxes (ex: TVA 20% ajoutée par le `Payment-Service` sur la facture).

---

### Q16. Quelle est la différence fondamentale entre le statut d'une réservation et le statut d'un paiement ?
**Réponse :**
Il s'agit de deux cycles de vie distincts :
- **Statut Réservation (`ReservationStatus`) :** Représente l'état contractuel de la location (`PENDING` en attente de paiement, `CONFIRMED` validée, `ACTIVE` voiture récupérée à l'agence, `COMPLETED` voiture restituée, `CANCELLED` annulée).
- **Statut Paiement (`PaymentStatus`) :** Représente l'état financier de la transaction (`PENDING` en cours de traitement bancaire, `PAID` fonds prélevés avec succès, `FAILED` carte refusée, `REFUNDED` fonds restitués au client).
Cette distinction évite toute ambiguïté (une réservation peut être confirmée avec un paiement payé, ou annulée avec un paiement remboursé).

---

### Q17. Comment gérez-vous le scénario où le paiement échoue lors de la création d'une réservation ?
**Réponse :**
1. Le client valide son panier, `Reservation-Service` enregistre la réservation avec le statut temporaire `PENDING`.
2. `Reservation-Service` appelle `Payment-Service` via OpenFeign.
3. Si le paiement échoue (carte refusée ou simulation `FAILED`), `Payment-Service` renvoie une erreur ou un code de statut adapté.
4. `Reservation-Service` capture l'erreur, bascule la réservation en `CANCELLED` (ou la supprime) et renvoie au client un code HTTP `400 Bad Request` ou `402 Payment Required` avec un message clair : "Échec de paiement : transaction refusée. La réservation n'a pas été confirmée." Le véhicule reste donc immédiatement disponible pour les autres clients.

---

### Q18. Comment fonctionne l'annulation d'une réservation et le remboursement associé ?
**Réponse :**
1. Le client appelle `PUT /api/reservations/{id}/cancel`.
2. `Reservation-Service` vérifie les conditions d'annulation (ex: annulation effectuée plus de 48 heures avant la date de début de location).
3. Si la condition est remplie, le statut de la réservation devient `CANCELLED`.
4. `Reservation-Service` appelle en synchrone `POST /api/payments/refund/{reservationId}` pour générer l'avoir et passer le paiement à `REFUNDED`.
5. Enfin, un événement asynchrone `reservation.cancelled` est publié sur RabbitMQ pour que `Vehicle-Service` remette la disponibilité du véhicule à jour.

---

### Q19. Comment les agences de location sont-elles rattachées aux véhicules ?
**Réponse :**
Dans une architecture microservices décorrélée, la table `vehicles` dans `vehicle_db` ne possède pas de clé étrangère SQL vers la table `agencies` de `agency_db`. Elle stocke simplement un attribut scalaire `agencyId` (de type `Long`). Lorsque l'application doit afficher les coordonnées de l'agence sur la fiche d'un véhicule, le Frontend ou la passerelle interroge l'endpoint `/api/agencies/{id}` du `Agency-Service`. Cela respecte le principe d'autonomie des schémas.

---

### Q20. Comment évitez-vous qu'un utilisateur ne consulte ou n'annule les réservations d'un autre utilisateur ?
**Réponse :**
Grâce au filtre d'autorisation :
- L'API Gateway extrait le claim `userId` et les rôles (`ROLE_CLIENT`, `ROLE_ADMIN`) du token JWT et les transmet dans l'en-tête `X-User-Id`.
- Le controller du `Reservation-Service` vérifie que le `userId` du token correspond bien au `userId` propriétaire de la réservation ciblée, sauf si l'utilisateur possède le rôle `ROLE_ADMIN` ou `ROLE_AGENT`. Si ce n'est pas le cas, le service renvoie immédiatement un code HTTP `403 Forbidden`.

---

### Q21. Pourquoi avoir créé un microservice séparé pour les Avis (Review-Service) ?
**Réponse :**
Les avis et notations ont un cycle de vie, des exigences de performance et un modèle de données totalement différents du cœur transactionnel :
- La volumétrie des avis peut croître très rapidement.
- Les requêtes sont presque exclusivement des lectures massives en consultation publique.
- En isolant ce service avec MySQL, une lenteur ou une indisponibilité temporaire du module d'avis n'a aucun impact sur la capacité d'un client à louer une voiture et payer sa commande.

---

### Q22. Comment fonctionne la modération des avis clients dans le Review-Service ?
**Réponse :**
Chaque nouvel avis créé via `POST /api/reviews` reçoit par défaut le statut `PENDING` ou `APPROVED` selon la politique choisie. L'administrateur ou l'agent dispose d'un endpoint `PATCH /api/reviews/{id}/status?status=REJECTED` pour masquer les commentaires inappropriés ou diffamatoires. Seuls les avis avec le statut `APPROVED` sont renvoyés aux visiteurs sur le catalogue public.

---

### Q23. Comment gérez-vous la pagination sur la liste des véhicules ?
**Réponse :**
La liste des véhicules pouvant comporter des centaines de voitures, le controller `VehicleController` utilise les objets `Pageable` et `Page<VehicleDTO>` de Spring Data JPA :
- Paramètres : `GET /api/vehicles?page=0&size=10&sort=pricePerDay,asc`.
- Avantage : économie de mémoire côté backend, réduction de la charge réseau et affichage fluide côté Angular avec un composant de pagination.

---

### Q24. Quels sont les codes de statut HTTP utilisés et respectez-vous la sémantique REST ?
**Réponse :**
Oui, nous appliquons rigoureusement la norme REST :
- `200 OK` : Lecture ou modification réussie.
- `201 Created` : Création réussie d'une ressource (utilisateur, véhicule, réservation, paiement) avec en-tête `Location`.
- `204 No Content` : Suppression réussie sans corps de réponse (ex: suppression d'une agence).
- `400 Bad Request` : Erreur de validation de corps JSON (champs obligatoires manquants, dates invalides).
- `401 Unauthorized` : Token JWT absent ou expiré.
- `403 Forbidden` : Droits insuffisants (ex: un client tente d'ajouter un véhicule).
- `404 Not Found` : Ressource introuvable avec l'identifiant spécifié.
- `409 Conflict` : Conflit d'état (ex: immatriculation déjà existante ou véhicule indisponible aux dates demandées).
- `500 Internal Server Error` : Défaillance technique inattendue capturée par le GlobalExceptionHandler.

---

### Q25. Comment le Frontend Angular gère-t-il l'authentification et l'injection du token JWT ?
**Réponse :**
Le Frontend Angular implémente un **HTTP Interceptor (`JwtInterceptor`)** :
- À chaque requête HTTP sortante émise via le `HttpClient`, l'intercepteur vérifie si un token JWT est présent dans le `localStorage`.
- Si oui, il clone la requête et ajoute automatiquement l'en-tête `Authorization: Bearer <token>`.
- De plus, un **`AuthGuard`** protège les routes nécessitant une connexion (ex: `/reservations/create`, `/admin/dashboard`) en redirigeant les utilisateurs non connectés vers `/login`.

---

### Q26. Comment fonctionne la communication asynchrone avec RabbitMQ dans votre architecture ?
**Réponse :**
Nous utilisons un **Topic Exchange** nommé `carrental.topic` :
- Le `Reservation-Service` publie un message sur la clé de routage `reservation.confirmed` avec la charge utile `{reservationId: 101, vehicleId: 5, startDate: "...", endDate: "..."}`.
- RabbitMQ route ce message vers la file d'attente `vehicle.reservation.queue` liée à ce pattern.
- Une méthode annotée `@RabbitListener(queues = "vehicle.reservation.queue")` dans `Vehicle-Service` consomme le message de manière asynchrone et met à jour le statut du véhicule sans bloquer l'utilisateur.

---

### Q27. Que se passe-t-il si un message RabbitMQ ne peut pas être traité par le service destinataire ?
**Réponse :**
Nous mettons en place une **Dead Letter Queue (DLQ)** :
- Si le traitement d'un message échoue après un nombre défini de tentatives (ex: 3 retries avec backoff exponentiel), le message est automatiquement rejeté (`basic.reject` ou `nack`) et dérouté vers le `Dead Letter Exchange`.
- Les messages dans la DLQ peuvent être analysés par l'équipe technique pour investiguer la cause de l'erreur (payload corrompu, bug de logique) sans bloquer le flux régulier des autres messages.

---

### Q28. Comment partagez-vous le code commun (DTOs partagés, événements) sans créer de dépendance monolithique ?
**Réponse :**
Nous appliquons le principe du **Shared Kernel minimal** :
- Soit chaque microservice définit ses propres DTOs découplés correspondant uniquement aux données dont il a besoin (pattern *Consumer-Driven Contracts*).
- Soit nous publions une bibliothèque Java commune très légère (`carrental-common`) contenant uniquement les interfaces d'événements AMQP immuables et les DTOs transversaux, sans logique métier.

---

### Q29. Comment simulez-vous le paiement dans le Payment-Service sans passer par une vraie banque ?
**Réponse :**
Le `Payment-Service` expose l'endpoint `POST /api/payments/process`. La méthode inspecte la requête :
- Si le montant est strictement positif et que le numéro de carte simulé ne se termine pas par `0000`, la méthode génère un numéro de transaction unique (`TX-XXXX`), passe le statut à `PAID`, génère un numéro de facture (`INV-XXXX`) et renvoie une réponse positive avec code `201 Created`.
- Si le numéro se termine par `0000`, la méthode simule un refus bancaire en renvoyant le statut `FAILED`.
Cette approche est réaliste, prévisible pour les tests et suffisante pour la validation intermédiaire.

---

### Q30. Comment assurez-vous la traçabilité des requêtes à travers l'ensemble des microservices (Distributed Tracing) ?
**Réponse :**
Nous utilisons **Micrometer Tracing** (le successeur de Spring Cloud Sleuth sous Spring Boot 3) couplé à **Zipkin** :
- L'API Gateway génère un `TraceId` unique lors de la réception d'une requête HTTP externe.
- Ce `TraceId` est automatiquement propagé dans les en-têtes HTTP de chaque appel OpenFeign et dans les métadonnées des messages RabbitMQ.
- Tous les logs des différents conteneurs affichent ce même `[traceId, spanId]`, ce qui permet de reconstituer instantanément l'intégralité du parcours d'une réservation à travers les 6 services.

---

### Q31. Comment gérez-vous les suppressions de véhicules qui ont déjà des réservations dans le passé ?
**Réponse :**
Nous appliquons le **Soft Delete (suppression logique)** :
- Au lieu d'exécuter un `DELETE` physique en base qui violerait l'historique ou les références dans les factures, l'attribut `status` du véhicule passe à `OUT_OF_SERVICE` ou un champ booléen `deleted = true` est activé.
- Les requêtes de recherche de véhicules disponibles filtrent automatiquement ces enregistrements, mais l'historique des réservations passées reste intact et consultable par les clients et les agences.

---

### Q32. Comment les employés d'agence peuvent-ils consulter les réservations de leur agence ?
**Réponse :**
L'endpoint `GET /api/reservations/agency/{agencyId}` dans `Reservation-Service` permet de récupérer toutes les réservations ayant pour agence de retrait (`pickupAgencyId`) ou de retour (`returnAgencyId`) l'identifiant de l'agence concernée. L'employé d'agence peut ainsi préparer les véhicules prévus pour la journée.

---

### Q33. Pourquoi avoir choisi Java 17 et Spring Boot 3.2 pour les microservices ?
**Réponse :**
- **Java 17 LTS :** Bénéficie d'un support à long terme, apporte des fonctionnalités modernes très utiles pour les APIs (Records immuables, Pattern Matching, Text Blocks pour requêtes JSON/SQL, performances accrues du Garbage Collector).
- **Spring Boot 3.2 :** Repose sur le standard Jakarta EE 10, supporte nativement Spring Cloud 2023, offre une meilleure intégration de l'observabilité avec Micrometer et prépare l'application à la compilation AOT / GraalVM si un démarrage ultra-rapide en conteneur est souhaité.

---

### Q34. Que contient le microservice commun développé collectivement ?
**Réponse :**
Le microservice commun est constitué du binôme **Spring Cloud Gateway (Passerelle)** et **Netflix Eureka (Serveur de découverte)**, complété par le bus d'événements **RabbitMQ** :
- Tous les étudiants ont contribué à configurer les routes de leurs services dans la Gateway.
- Le mécanisme de filtre JWT et la gestion CORS y sont configurés collectivement.
- L'orchestration dans le fichier `docker-compose.yml` garantit que chaque membre de l'équipe peut lancer l'ensemble du projet sans dépendre de l'ordinateur d'un camarade.

---

### Q35. Quelle est la prochaine étape de développement après cette validation intermédiaire (Séance 4) ?
**Réponse :**
Conformément aux consignes de l'enseignant, la séance 4 valide la conception, les diagrammes d'architecture, la structure Git et les squelettes d'APIs.
Pour la séance 5 et les suivantes, nos priorités sont :
1. Finaliser l'implémentation de la couche persistance avec des jeux de données réels (*seed data*) pour chaque agence et véhicule.
2. Brancher le bus RabbitMQ réel avec les écouteurs `@RabbitListener` pour tester les événements en conditions réelles.
3. Finaliser l'interface utilisateur Angular pour connecter les composants visuels aux endpoints REST de la Gateway.
4. Mettre en place les tests unitaires JUnit 5 et tests d'intégration avec Testcontainers.

---

### Q36. Si l'un des étudiants de l'équipe est absent le jour de la soutenance, que se passe-t-il ?
**Réponse :**
Chaque étudiant doit obligatoirement présenter son propre microservice en 1 minute. La consigne de l'enseignant stipule qu'une absence non justifiée est sanctionnée par un zéro. Cependant, grâce à notre dossier technique exhaustif et à ce document de questions/réponses, **l'ensemble des membres du groupe maîtrise la vision globale de l'architecture** et est capable d'expliquer comment le microservice manquant s'intègre avec le reste de la plateforme.
