-- =========================================================================
-- Script d'initialisation des bases de données CarRental pour MySQL Workbench
-- À exécuter dans MySQL Workbench connecté sur localhost:3306 (utilisateur root)
-- =========================================================================

-- 1. Base du User-Service (Authentification, Utilisateurs & Rôles)
CREATE DATABASE IF NOT EXISTS carrental_user_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 2. Base du Vehicle-Service (Véhicules, Flotte & Catégories)
CREATE DATABASE IF NOT EXISTS carrental_vehicle_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 3. Base du Reservation-Service (Réservations, Devis & Planning)
CREATE DATABASE IF NOT EXISTS carrental_reservation_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 4. Base du Payment-Service (Paiements, Transactions & Factures)
CREATE DATABASE IF NOT EXISTS carrental_payment_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 5. Base de l'Agency-Service (Agences physiques, Adresses & Staff)
CREATE DATABASE IF NOT EXISTS carrental_agency_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 6. Base du Review-Service (Avis clients, Notes & Modération)
CREATE DATABASE IF NOT EXISTS carrental_review_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Vérification des bases créées
SHOW DATABASES LIKE 'carrental_%';
