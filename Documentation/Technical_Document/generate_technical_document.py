import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_dir = r"C:\Users\RAYEN\.gemini\antigravity\scratch\CarRental-AWD"
doc_dir = os.path.join(base_dir, "Documentation", "Technical_Document")
diag_dir = os.path.join(base_dir, "Documentation", "Diagrams")
os.makedirs(doc_dir, exist_ok=True)

docx_path = os.path.join(doc_dir, "Dossier_Technique_CarRental.docx")

doc = Document()

# Set page margins
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Colors
C_PRIMARY = RGBColor(26, 54, 93)     # #1A365D
C_SECONDARY = RGBColor(43, 108, 176) # #2B6CB0
C_TEXT = RGBColor(45, 55, 72)        # #2D3748
C_MUTED = RGBColor(113, 128, 150)    # #718096

def set_para_font(p, name="Calibri", size=11, color=C_TEXT, bold=False, italic=False):
    for r in p.runs:
        r.font.name = name
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.italic = italic

def add_styled_heading(text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    if level == 1:
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        set_para_font(h, size=15, color=C_PRIMARY, bold=True)
    elif level == 2:
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        set_para_font(h, size=12.5, color=C_SECONDARY, bold=True)
    elif level == 3:
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        set_para_font(h, size=11, color=C_PRIMARY, bold=True)
    return h

def add_body_p(text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_PRIMARY
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = C_TEXT
    return p

def add_bullet_p(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_PRIMARY
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = C_TEXT
    return p

def add_diagram_image(img_name, caption_text, width_inches=6.0):
    img_path = os.path.join(diag_dir, img_name)
    if os.path.exists(img_path):
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        doc.add_picture(img_path, width=Inches(width_inches))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = C_MUTED

def style_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        shading = parse_xml(r'<w:shd {} w:fill="2B6CB0"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        fill_color = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
            row_cells[col_idx]._tc.get_or_add_tcPr().append(shd)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.color.rgb = C_TEXT

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

# =========================================================================
# PAGE DE GARDE
# =========================================================================
p_title_pre = doc.add_paragraph()
p_title_pre.paragraph_format.space_before = Pt(40)
r = p_title_pre.add_run("PROJET D'ARCHITECTURE WEB DISTRIBUÉE (AWD)\nVALIDATION INTERMÉDIAIRE – SÉANCE 4")
r.font.name = "Calibri"
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = C_MUTED
p_title_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_main_title = doc.add_paragraph()
p_main_title.paragraph_format.space_before = Pt(20)
p_main_title.paragraph_format.space_after = Pt(10)
r_title = p_main_title.add_run("CarRental\nPlateforme Web de Location de Voitures")
r_title.font.name = "Calibri"
r_title.font.size = Pt(26)
r_title.font.bold = True
r_title.font.color.rgb = C_PRIMARY
p_main_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("Dossier Technique d'Architecture & de Conception Microservices\nSpring Boot 3 • Angular 17 • Spring Cloud • PostgreSQL • MongoDB • RabbitMQ")
r_sub.font.name = "Calibri"
r_sub.font.size = Pt(12)
r_sub.font.italic = True
r_sub.font.color.rgb = C_SECONDARY
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_before = Pt(50)
p_meta.paragraph_format.space_after = Pt(20)
meta_text = """Équipe de Réalisation (Groupe de 6 Étudiants) :
• Étudiant 1 : [Nom Étudiant 1] – Responsable User-Service (Auth & JWT)
• Étudiant 2 : [Nom Étudiant 2] – Responsable Vehicle-Service (Flotte & Dispo)
• Étudiant 3 : [Nom Étudiant 3] – Responsable Reservation-Service (Réservations & Devis)
• Étudiant 4 : [Nom Étudiant 4] – Responsable Payment-Service (Paiements & Facturation)
• Étudiant 5 : [Nom Étudiant 5] – Responsable Agency-Service (Agences & Staff)
• Étudiant 6 : [Nom Étudiant 6] – Responsable Review-Service (Avis NoSQL MongoDB)
• Service Commun (Collectif) : API Gateway (Spring Cloud) + Eureka Server + RabbitMQ

Encadrant Enseignant : Équipe Pédagogique AWD
Classe / Spécialité : 4DAS (4ème Année Ingénierie Informatique)
Année Universitaire : 2026 - 2027"""
r_m = p_meta.add_run(meta_text)
r_m.font.name = "Calibri"
r_m.font.size = Pt(10.5)
r_m.font.color.rgb = C_TEXT
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# =========================================================================
# SOMMAIRE
# =========================================================================
add_styled_heading("Sommaire Général du Document", level=1)
toc_items = [
    "1. Introduction Générale & Contexte du Projet",
    "2. Problématique Métier & Objectifs",
    "3. Acteurs du Système & Diagramme de Cas d'Utilisation Général",
    "4. Principales Fonctionnalités du Système",
    "5. Architecture Globale des Microservices",
    "6. Justification du Découpage en 6 Microservices Métier + 1 Commun",
    "7. Analyse Détaillée de Chaque Microservice Métier (avec Diagrammes de Classes UML & Contrats d'API)",
    "    7.1. User-Service (Authentification, Sécurité & Rôles)",
    "    7.2. Vehicle-Service (Catalogue & Flotte Automobile)",
    "    7.3. Reservation-Service (Cycle de Vie des Réservations)",
    "    7.4. Payment-Service (Simulation Financière & Facturation)",
    "    7.5. Agency-Service (Points de Retrait Physiques & Personnel)",
    "    7.6. Review-Service (Avis Clients, Notes & Modération NoSQL)",
    "    7.7. API Gateway & Infrastructure Commune (Eureka & RabbitMQ)",
    "8. Modèle de Communication Inter-Microservices : Synchrone vs Asynchrone",
    "9. Diagrammes de Séquence des Parcours Clés (Réservation & Annulation)",
    "10. Diagramme de Déploiement Conteneurisé (Docker & Docker Compose)",
    "11. Stratégie de Persistance Polyglotte (PostgreSQL & MongoDB)",
    "12. Architecture de Sécurité (Stateless JWT & Propagation de Contexte)",
    "13. Organisation Git & Conventions de Travail en Équipe",
    "14. Répartition Précise des Tâches entre les 6 Membres",
    "15. Planning Prévisionnel & Analyse Proactive des Risques",
    "16. Conclusion & Perspectives pour la Soutenance Finale"
]
for item in toc_items:
    add_bullet_p(item)

doc.add_page_break()

# =========================================================================
# 1 & 2. INTRODUCTION & OBJECTIFS
# =========================================================================
add_styled_heading("1. Introduction Générale & Présentation du Projet", level=1)
add_body_p("Le projet CarRental s'inscrit dans le cadre du module Architecture Web Distribuée (AWD) pour les étudiants de 4ème année d'ingénierie informatique (classe 4DAS). Il a pour objectif de concevoir, architecturer et déployer une plateforme moderne de location de véhicules en ligne, en appliquant les principes fondamentaux des systèmes distribués à base de microservices.")
add_body_p("Dans l'industrie contemporaine de la mobilité, les agences de location font face à des pics saisonniers de fréquentation, des recherches intenses et la nécessité d'une coordination parfaite entre plusieurs points de vente physiques. CarRental offre une solution web réactive, intuitive et sécurisée, permettant aux clients de rechercher des véhicules, vérifier leur disponibilité en temps réel, effectuer des réservations multi-jours et régler en ligne en toute simplicité.")

add_styled_heading("2. Problématique Métier & Objectifs", level=1)
add_styled_heading("2.1. Problématique", level=2)
add_body_p("La conception d'une plateforme de location de voitures soulève plusieurs défis majeurs propres aux architectures logicielles :")
add_bullet_p("Éviter impérativement le surbooking (double réservation simultanée d'un véhicule pour un même intervalle de dates).", bold_prefix="Gestion de la concurrence critique : ")
add_bullet_p("Le catalogue et les disponibilités subissent des centaines de consultations par minute, tandis que la création de réservation et le paiement exigent une consistance stricte mais représentent une volumétrie moindre.", bold_prefix="Asymétrie de charge de travail : ")
add_bullet_p("Une panne sur le module de notation ou sur la consultation des avis ne doit en aucun cas bloquer le processus d'achat ou la recherche de voitures.", bold_prefix="Résilience & Haute Disponibilité : ")
add_bullet_p("Le système doit s'adapter à une organisation d'équipe de 6 développeurs travaillant en parallèle sans blocage mutuel.", bold_prefix="Découplage organisationnel : ")

add_styled_heading("2.2. Objectifs Poursuivis", level=2)
add_bullet_p("Mettre en place une architecture microservices pure, respectant le principe de responsabilité unique (SRP) et le pattern Database-per-Service.")
add_bullet_p("Fournir une API Gateway centrale gérant le routage dynamique, la sécurité JWT, le filtrage CORS et la résilience.")
add_bullet_p("Intégrer à la fois la communication synchrone (REST via Spring Cloud OpenFeign) et asynchrone (Event-Driven avec RabbitMQ).")
add_bullet_p("Construire une interface utilisateur Single Page Application (SPA) réactive en Angular 17+.")
add_bullet_p("Assurer une traçabilité et une documentation exemplaire conforme à 100% aux exigences de la validation intermédiaire (Séance 4).")

# =========================================================================
# 3 & 4. ACTEURS, CAS D'UTILISATION & FONCTIONNALITÉS
# =========================================================================
add_styled_heading("3. Acteurs du Système & Diagramme de Cas d'Utilisation Général", level=1)
add_body_p("Le système CarRental interagit avec trois catégories d'acteurs distincts :")
add_bullet_p("Recherche des véhicules par critères, consulte les disponibilités, réserve, paie en ligne (simulation), télécharge ses factures, consulte son historique et rédige des avis.", bold_prefix="Client / Visiteur : ")
add_bullet_p("Consulte les réservations rattachées à son agence physique, valide la prise en charge et la restitution des véhicules, et met à jour l'état de la flotte locale (entretien, kilométrage).", bold_prefix="Employé d'Agence (Agent) : ")
add_bullet_p("Supervise l'ensemble de la flotte nationale, gère le réseau d'agences, administre les comptes utilisateurs, modère les avis clients et analyse les métriques globales de l'entreprise.", bold_prefix="Administrateur : ")

add_diagram_image("Cas_Utilisation_General.png", "Figure 1 : Diagramme de Cas d'Utilisation Général UML de la Plateforme CarRental", width_inches=6.2)

add_styled_heading("4. Principales Fonctionnalités du Système", level=1)
features_headers = ["Module Fonctionnel", "Fonctionnalités Offertes", "Bénéfice Utilisateur"]
features_data = [
    ["Authentification & Sécurité", "Inscription, connexion, émission JWT, gestion des rôles (CLIENT, AGENT, ADMIN)", "Accès sécurisé et rôles stricts"],
    ["Gestion de Flotte Automobile", "Fiches techniques, catégorisation, suivi kilométrique, statut (AVAILABLE, RENTED, MAINTENANCE)", "Catalogue clair et à jour"],
    ["Moteur de Réservation", "Calcul automatique du montant (tarif x jours), vérification de chevauchement, annulation", "Devis instantané sans surbooking"],
    ["Simulation de Paiement", "Simulation bancaire réaliste (PAID, PENDING, FAILED), facturation PDF immédiate, avoirs", "Transactions transparentes"],
    ["Réseau d'Agences", "Répertoire géolocalisé des agences de retrait/retour, horaires, affectation des employés", "Retrait physique facilité"],
    ["Avis & Évaluations", "Notation 1 à 5 étoiles, retours d'expérience vérifiés, modération administrative", "Confiance et transparence"]
]
t_feat = doc.add_table(rows=1, cols=3)
style_table(t_feat, [1.8, 3.2, 1.8], features_headers, features_data)

doc.add_page_break()

# =========================================================================
# 5 & 6. ARCHITECTURE GLOBALE & DÉCOUPAGE
# =========================================================================
add_styled_heading("5. Architecture Globale des Microservices", level=1)
add_body_p("L'architecture globale de CarRental repose sur une décomposition modulaire en microservices indépendants, orchestrés par des composants d'infrastructure Spring Cloud éprouvés :")

add_diagram_image("Architecture_Globale.png", "Figure 2 : Diagramme d'Architecture Globale UML (Composants, Gateway, Eureka, RabbitMQ, Services et DBs)", width_inches=6.4)

add_styled_heading("Composants Clés de l'Architecture :", level=2)
add_bullet_p("Application SPA responsive développée sous Angular 17+, communiquant exclusivement avec l'API Gateway via HTTP/REST et jetons Bearer JWT.", bold_prefix="1. Frontend Angular (Port 4200) : ")
add_bullet_p("Développée avec Spring Cloud Gateway, elle constitue le point d'entrée unique (Port 8080). Elle gère le routage dynamique, valide les tokens JWT, autorise les requêtes CORS et implémente le rate-limiting.", bold_prefix="2. API Gateway (Port 8080) : ")
add_bullet_p("Serveur Netflix Eureka (Port 8761) maintenant un annuaire en temps réel de toutes les instances de services saines. Permet un équilibrage de charge côté client (Client-side Load Balancing).", bold_prefix="3. Service Discovery Eureka (Port 8761) : ")
add_bullet_p("Broker AMQP (Port 5672) permettant la diffusion d'événements asynchrones à faible couplage (ex: confirmation de réservation, mise à jour d'état du véhicule).", bold_prefix="4. RabbitMQ Message Broker (Port 5672) : ")
add_bullet_p("Chaque microservice métier possède son propre conteneur de données dédié, évitant tout couplage de schéma.", bold_prefix="5. Pattern Database-per-Service : ")

add_styled_heading("6. Justification du Découpage en Microservices", level=1)
add_body_p("Le découpage initial proposé de 6 microservices métier et d'un microservice commun a été rigoureusement analysé et validé par notre équipe d'architecture :")
add_bullet_p("Isole la cryptographie, les tokens JWT et la persistance des utilisateurs. Aucun autre service n'a accès direct aux mots de passe chiffrés.", bold_prefix="User-Service (Étudiant 1) : ")
add_bullet_p("Isole le catalogue des véhicules, soumis à des pics de lecture massifs. Peut être mis à l'échelle (scalabilité horizontale) sans dupliquer le reste de l'application.", bold_prefix="Vehicle-Service (Étudiant 2) : ")
add_bullet_p("Constitue le coordinateur du cœur métier. Isole la logique temporelle des dates de location et le calcul des devis.", bold_prefix="Reservation-Service (Étudiant 3) : ")
add_bullet_p("Isole la gestion comptable, les factures et les statuts financiers. Une défaillance bancaire ou un changement de passerelle de paiement n'impacte que ce module.", bold_prefix="Payment-Service (Étudiant 4) : ")
add_bullet_p("Isole la structure physique territoriale. Un véhicule ne stocke qu'une référence 'agencyId', garantissant l'indépendance des bases.", bold_prefix="Agency-Service (Étudiant 5) : ")
add_bullet_p("Isole les commentaires libres et notes. L'utilisation d'une base NoSQL MongoDB est hautement justifiée ici, évitant d'alourdir les bases relationnelles avec des textes volumineux.", bold_prefix="Review-Service (Étudiant 6) : ")
add_bullet_p("Regroupe l'API Gateway, le serveur Eureka et le broker RabbitMQ, mutualisant la tuyauterie technique au profit de toute l'équipe.", bold_prefix="Infrastructure Commune (Collectif) : ")

doc.add_page_break()

# =========================================================================
# 7. ANALYSE DÉTAILLÉE DE CHAQUE MICROSERVICE (AVEC CLASSES UML)
# =========================================================================
add_styled_heading("7. Analyse Détaillée de Chaque Microservice Métier", level=1)

# 7.1 User Service
add_styled_heading("7.1. User-Service (Responsable : Étudiant 1 - [Nom Étudiant 1])", level=2)
add_bullet_p("Gestion des identités, inscription, authentification, émission des jetons JWT et attribution des rôles applicatifs.", bold_prefix="1. Nom & Responsabilité : ")
add_bullet_p("Centraliser la sécurité et fournir une authentification unique sans état (stateless) réutilisable par l'ensemble de la plateforme.", bold_prefix="2. Problématique résolue : ")
add_bullet_p("Inscription client, connexion sécurisée, génération de JWT, validation de token, consultation et mise à jour de profil.", bold_prefix="3. Fonctionnalités : ")
add_bullet_p("Entité User reliée en Many-to-Many à Role. Rôles : ROLE_CLIENT, ROLE_AGENT, ROLE_ADMIN.", bold_prefix="4. Entités & Relations : ")
add_bullet_p("PostgreSQL (user_db:5432). Justification : rigueur relationnelle, contraintes d'unicité strictes sur emails et noms d'utilisateur, respect ACID.", bold_prefix="5. Base de données : ")

add_diagram_image("Classes_User_Service.png", "Figure 3 : Diagramme de Classes UML - User Service (Entités, DTOs, Repositories, Services, Controllers)", width_inches=5.8)

add_body_p("Contrats d'API REST du User-Service (Port 8081) :", bold_prefix="Contrats d'API : ")
u_headers = ["Méthode", "Endpoint", "Paramètres / Body", "Codes HTTP", "Description"]
u_data = [
    ["POST", "/api/auth/register", "RegisterRequest (JSON)", "201, 400, 409", "Création de compte client avec mot de passe haché"],
    ["POST", "/api/auth/login", "LoginRequest (JSON)", "200, 400, 401", "Authentification et émission du jeton JWT"],
    ["GET", "/api/auth/validate", "?token=string", "200, 400", "Validation de la signature et expiration du token"],
    ["GET", "/api/users/{id}", "Path: id (Long)", "200, 404", "Consultation des informations de profil"],
    ["PUT", "/api/users/{id}", "Path: id, RegisterRequest", "200, 400, 404", "Mise à jour des coordonnées personnelles"]
]
t_u = doc.add_table(rows=1, cols=5)
style_table(t_u, [0.8, 1.8, 1.6, 1.0, 1.6], u_headers, u_data)

# 7.2 Vehicle Service
add_styled_heading("7.2. Vehicle-Service (Responsable : Étudiant 2 - [Nom Étudiant 2])", level=2)
add_bullet_p("Gestion du parc automobile, fiches techniques, tarification journalière, catégorisation et état de disponibilité.", bold_prefix="1. Nom & Responsabilité : ")
add_bullet_p("Offrir un catalogue performant et consultable en temps réel sans blocage, avec recherche multicritère par marque, agence et catégorie.", bold_prefix="2. Problématique résolue : ")
add_bullet_p("Ajout/modification de véhicules, recherche filtrée, vérification de disponibilité, mise à jour d'état (AVAILABLE, RENTED, MAINTENANCE, OUT_OF_SERVICE).", bold_prefix="3. Fonctionnalités : ")
add_bullet_p("Entité Vehicle reliée en Many-to-One à Category (name, baseRate). Énumérations VehicleStatus, FuelType, Transmission.", bold_prefix="4. Entités & Relations : ")
add_bullet_p("PostgreSQL (vehicle_db:5433). Justification : unicité des immatriculations, indexation B-Tree performante sur les marques et statuts.", bold_prefix="5. Base de données : ")

add_diagram_image("Classes_Vehicle_Service.png", "Figure 4 : Diagramme de Classes UML - Vehicle Service", width_inches=5.8)

add_body_p("Contrats d'API REST du Vehicle-Service (Port 8082) :", bold_prefix="Contrats d'API : ")
v_headers = ["Méthode", "Endpoint", "Paramètres / Body", "Codes HTTP", "Description"]
v_data = [
    ["GET", "/api/vehicles", "Pagination optionnelle", "200", "Liste complète des véhicules"],
    ["GET", "/api/vehicles/search", "?brand=...&agencyId=...", "200", "Recherche filtrée multicritère"],
    ["GET", "/api/vehicles/{id}", "Path: id", "200, 404", "Fiche détaillée d'un véhicule"],
    ["GET", "/api/vehicles/{id}/availability", "Path: id", "200, 404", "Vérification temps réel du statut et prix"],
    ["POST", "/api/vehicles", "VehicleDTO (JSON)", "201, 400", "Ajout d'un nouveau véhicule (Agent/Admin)"],
    ["PATCH", "/api/vehicles/{id}/status", "Path: id, ?status=...", "200, 400, 404", "Changement de statut (ex: passage en MAINTENANCE)"]
]
t_v = doc.add_table(rows=1, cols=5)
style_table(t_v, [0.8, 2.0, 1.4, 1.0, 1.6], v_headers, v_data)

# 7.3 Reservation Service
add_styled_heading("7.3. Reservation-Service (Responsable : Étudiant 3 - [Nom Étudiant 3])", level=2)
add_bullet_p("Orchestration de la réservation, calcul de prix, contrôle des chevauchements de dates et cycle de vie du contrat.", bold_prefix="1. Nom & Responsabilité : ")
add_bullet_p("Empêcher le surbooking, coordonner de façon résiliente la vérification de véhicule et le paiement sans transaction distribuée lourde.", bold_prefix="2. Problématique résolue : ")
add_bullet_p("Création d'une réservation, calcul de durée et tarif, annulation avec conditions, suivi de statut (PENDING, CONFIRMED, ACTIVE, COMPLETED, CANCELLED).", bold_prefix="3. Fonctionnalités : ")
add_bullet_p("Entité Reservation (reservationNumber, userId, vehicleId, pickupAgencyId, returnAgencyId, startDate, endDate, totalDays, dailyRate, totalPrice, status).", bold_prefix="4. Entités & Relations : ")
add_bullet_p("PostgreSQL (reservation_db:5434). Justification : consistance transactionnelle ACID primordiale pour les contrats de location.", bold_prefix="5. Base de données : ")

add_diagram_image("Classes_Reservation_Service.png", "Figure 5 : Diagramme de Classes UML - Reservation Service", width_inches=5.8)

add_body_p("Contrats d'API REST du Reservation-Service (Port 8083) :", bold_prefix="Contrats d'API : ")
r_headers = ["Méthode", "Endpoint", "Paramètres / Body", "Codes HTTP", "Description"]
r_data = [
    ["POST", "/api/reservations", "ReservationRequest (JSON)", "201, 400, 409", "Création et initialisation du flux de réservation"],
    ["GET", "/api/reservations/{id}", "Path: id", "200, 404", "Détail d'une réservation"],
    ["GET", "/api/reservations/user/{userId}", "Path: userId", "200", "Historique complet des locations d'un client"],
    ["PUT", "/api/reservations/{id}/confirm", "Path: id", "200, 404", "Confirmation manuelle par l'agence"],
    ["PUT", "/api/reservations/{id}/cancel", "Path: id", "200, 400, 404", "Annulation avec déclenchement de remboursement"]
]
t_r = doc.add_table(rows=1, cols=5)
style_table(t_r, [0.8, 2.0, 1.4, 1.0, 1.6], r_headers, r_data)

# 7.4 Payment Service
add_styled_heading("7.4. Payment-Service (Responsable : Étudiant 4 - [Nom Étudiant 4])", level=2)
add_bullet_p("Simulation et traitement des flux financiers, génération des factures horodatées et gestion des remboursements.", bold_prefix="1. Nom & Responsabilité : ")
add_bullet_p("Fournir un moteur de paiement sans dépendance externe, simulant fidèlement les états PAID, PENDING, FAILED et REFUNDED.", bold_prefix="2. Problématique résolue : ")
add_bullet_p("Traitement de paiement, émission automatique de facture (INV-XXXX), consultation de reçu, émission d'avoirs de remboursement.", bold_prefix="3. Fonctionnalités : ")
add_bullet_p("Entité Payment reliée en One-to-One à Invoice. Énumérations PaymentStatus, PaymentMethod (CREDIT_CARD, PAYPAL, CASH_ON_PICKUP).", bold_prefix="4. Entités & Relations : ")
add_bullet_p("PostgreSQL (payment_db:5435). Justification : traçabilité financière, conformité fiscale et auditabilité stricte.", bold_prefix="5. Base de données : ")

add_diagram_image("Classes_Payment_Service.png", "Figure 6 : Diagramme de Classes UML - Payment Service", width_inches=5.8)

add_body_p("Contrats d'API REST du Payment-Service (Port 8084) :", bold_prefix="Contrats d'API : ")
p_headers = ["Méthode", "Endpoint", "Paramètres / Body", "Codes HTTP", "Description"]
p_data = [
    ["POST", "/api/payments/process", "PaymentRequest (JSON)", "201, 400", "Simulation bancaire et génération facture"],
    ["GET", "/api/payments/{id}", "Path: id", "200, 404", "Consultation d'une transaction"],
    ["GET", "/api/payments/reservation/{resId}", "Path: resId", "200, 404", "Récupération du paiement lié à une réservation"],
    ["POST", "/api/payments/refund/{resId}", "Path: resId", "200, 400, 404", "Traitement de remboursement et émission d'avoir"]
]
t_p = doc.add_table(rows=1, cols=5)
style_table(t_p, [0.8, 2.0, 1.4, 1.0, 1.6], p_headers, p_data)

# 7.5 Agency Service
add_styled_heading("7.5. Agency-Service (Responsable : Étudiant 5 - [Nom Étudiant 5])", level=2)
add_bullet_p("Gestion du réseau physique d'agences de départ/restitution, adresses, coordonnées et rattachement des employés.", bold_prefix="1. Nom & Responsabilité : ")
add_bullet_p("Permettre la localisation des agences et affecter le personnel local sans mélanger les données avec les véhicules ou réservations.", bold_prefix="2. Problématique résolue : ")
add_bullet_p("Répertoire des agences, filtrage par ville, gestion des horaires d'ouverture, gestion du staff d'agence.", bold_prefix="3. Fonctionnalités : ")
add_bullet_p("Entité Agency avec Address embarquée (@Embedded), reliée à AgencyStaff.", bold_prefix="4. Entités & Relations : ")
add_bullet_p("PostgreSQL (agency_db:5436). Justification : intégrité des données d'adresses, requêtes géographiques.", bold_prefix="5. Base de données : ")

add_diagram_image("Classes_Agency_Service.png", "Figure 7 : Diagramme de Classes UML - Agency Service", width_inches=5.8)

add_body_p("Contrats d'API REST de l'Agency-Service (Port 8085) :", bold_prefix="Contrats d'API : ")
a_headers = ["Méthode", "Endpoint", "Paramètres / Body", "Codes HTTP", "Description"]
a_data = [
    ["GET", "/api/agencies", "Optionnel: ?active=true", "200", "Liste de toutes les agences actives"],
    ["GET", "/api/agencies/{id}", "Path: id", "200, 404", "Fiche détaillée d'une agence"],
    ["GET", "/api/agencies/city/{city}", "Path: city", "200", "Recherche des agences disponibles par ville"],
    ["POST", "/api/agencies", "AgencyDTO (JSON)", "201, 400", "Création d'une nouvelle agence (Admin)"],
    ["PUT", "/api/agencies/{id}", "Path: id, AgencyDTO", "200, 400, 404", "Mise à jour des coordonnées et horaires"]
]
t_a = doc.add_table(rows=1, cols=5)
style_table(t_a, [0.8, 2.0, 1.4, 1.0, 1.6], a_headers, a_data)

# 7.6 Review Service
add_styled_heading("7.6. Review-Service (Responsable : Étudiant 6 - [Nom Étudiant 6])", level=2)
add_bullet_p("Gestion des avis, commentaires, notes et modération des retours d'expérience clients.", bold_prefix="1. Nom & Responsabilité : ")
add_bullet_p("Stocker et servir de gros volumes d'évaluations textuelles sans saturer les bases relationnelles transactionnelles.", bold_prefix="2. Problématique résolue : ")
add_bullet_p("Dépôt d'avis avec note (1 à 5), consultation des avis par véhicule ou agence, calcul de moyenne, modération (APPROVED, REJECTED).", bold_prefix="3. Fonctionnalités : ")
add_bullet_p("Document MongoDB Review (id, userId, targetType: VEHICLE / AGENCY, targetId, rating, comment, status, createdAt).", bold_prefix="4. Modèle de Données : ")
add_bullet_p("MongoDB (review_db:27017). Justification : schéma NoSQL flexible, ciblage polymorphe, haute performance en lecture.", bold_prefix="5. Base de données : ")

add_diagram_image("Classes_Review_Service.png", "Figure 8 : Diagramme de Classes UML - Review Service (MongoDB)", width_inches=5.8)

add_body_p("Contrats d'API REST du Review-Service (Port 8086) :", bold_prefix="Contrats d'API : ")
rv_headers = ["Méthode", "Endpoint", "Paramètres / Body", "Codes HTTP", "Description"]
rv_data = [
    ["POST", "/api/reviews", "ReviewRequest (JSON)", "201, 400", "Dépôt d'un avis client (vérifié par token)"],
    ["GET", "/api/reviews/vehicle/{vehicleId}", "Path: vehicleId", "200", "Liste des avis approuvés pour un véhicule"],
    ["GET", "/api/reviews/agency/{agencyId}", "Path: agencyId", "200", "Liste des avis approuvés pour une agence"],
    ["GET", "/api/reviews/user/{userId}", "Path: userId", "200", "Historique des avis laissés par un utilisateur"]
]
t_rv = doc.add_table(rows=1, cols=5)
style_table(t_rv, [0.8, 2.0, 1.4, 1.0, 1.6], rv_headers, rv_data)

doc.add_page_break()

# =========================================================================
# 8, 9 & 10. COMMUNICATIONS, SÉQUENCES & DÉPLOIEMENT
# =========================================================================
add_styled_heading("8. Modèle de Communication Inter-Microservices", level=1)
add_body_p("CarRental utilise un modèle hybride équilibré, tirant parti des forces de la communication synchrone et asynchrone :")

add_diagram_image("Communication_Synchrone_Asynchrone.png", "Figure 9 : Diagramme de Communication Inter-Services UML (Synchrone OpenFeign vs Asynchrone RabbitMQ)", width_inches=6.2)

add_styled_heading("9. Diagrammes de Séquence des Parcours Clés", level=1)
add_body_p("Le diagramme de séquence ci-dessous illustre le parcours complet d'une réservation avec vérification de disponibilité, calcul de devis, simulation de paiement et émission d'événement asynchrone :")

add_diagram_image("Sequence_Reservation_Complete.png", "Figure 10 : Diagramme de Séquence UML du Parcours Complet de Réservation", width_inches=6.4)

add_body_p("En cas d'annulation de la location par le client, le scénario suivant s'exécute avec émission d'avoir et remise en disponibilité du véhicule :")

add_diagram_image("Sequence_Annulation_Paiement.png", "Figure 11 : Diagramme de Séquence UML du Parcours d'Annulation et de Remboursement", width_inches=6.2)

add_styled_heading("10. Diagramme de Déploiement Conteneurisé (Docker)", level=1)
add_body_p("L'ensemble des composants applicatifs et des bases de données sont encapsulés dans des conteneurs Docker reliés par le réseau virtuel 'carrental-network' :")

add_diagram_image("Deploiement_Docker.png", "Figure 12 : Diagramme de Déploiement UML Conteneurisé avec Docker Compose", width_inches=6.2)

# =========================================================================
# 11, 12, 13, 14 & 15. PERSISTANCE, SÉCURITÉ, GIT, PLANNING, CONCLUSION
# =========================================================================
add_styled_heading("11. Sécurité & Authentification Stateless JWT", level=1)
add_body_p("L'architecture implémente une sécurité par jetons JWT (JSON Web Tokens) signés en HMAC-SHA256 :")
add_bullet_p("L'utilisateur s'authentifie une seule fois auprès du User-Service. Le service vérifie le mot de passe haché et retourne un token signé contenant l'ID utilisateur, l'email et ses rôles.", bold_prefix="1. Émission Stateless : ")
add_bullet_p("Le client Angular injecte automatiquement le header 'Authorization: Bearer <token>' grâce à son JwtInterceptor.", bold_prefix="2. Injection Automatique : ")
add_bullet_p("L'API Gateway valide la signature du token à la volée. Elle extrait les claims (userId, rôles) et les injecte dans des en-têtes HTTP internes ('X-User-Id', 'X-User-Roles') transmis aux microservices métier.", bold_prefix="3. Propagation Gateway : ")

add_styled_heading("12. Organisation du Dépôt Git & Gestion de Projet", level=1)
add_body_p("L'équipe applique le modèle GitFlow adapté aux microservices :")
add_bullet_p("Branche de production contenant uniquement le code stable et validé en revue.", bold_prefix="• main : ")
add_bullet_p("Branche d'intégration continue où sont fusionnées les fonctionnalités de chaque étudiant.", bold_prefix="• develop : ")
add_bullet_p("Branches de travail individuelles (ex: feature/user-auth, feature/vehicle-catalog, feature/reservation-flow).", bold_prefix="• feature/<nom> : ")
add_bullet_p("Format conventionnel des messages de commit : 'feat(service): description', 'fix(service): description', 'docs(uml): description'.", bold_prefix="• Convention de commits : ")

add_styled_heading("13. Répartition des Tâches entre les Membres de l'Équipe", level=1)
team_headers = ["Étudiant", "Microservice Dédié", "Responsabilité Clé", "Livrables Produits"]
team_data = [
    ["Étudiant 1 : [Nom Étudiant 1]", "User-Service", "Auth, JWT, Rôles, Chiffrement", "Code Java, Controller, JPA, Tests JWT"],
    ["Étudiant 2 : [Nom Étudiant 2]", "Vehicle-Service", "Flotte, Catégories, Filtres, Disponibilités", "Catalogue, Feign Client, Endpoints recherche"],
    ["Étudiant 3 : [Nom Étudiant 3]", "Reservation-Service", "Calcul Devis, Dates, Coordination métier", "Gestion chevauchement, Events RabbitMQ"],
    ["Étudiant 4 : [Nom Étudiant 4]", "Payment-Service", "Simulation paiement, Factures, Avoirs", "Moteur simulation, Reçus PDF, Statuts"],
    ["Étudiant 5 : [Nom Étudiant 5]", "Agency-Service", "Agences, Adresses, Personnel local", "Fiches agences, Requêtes géographiques"],
    ["Étudiant 6 : [Nom Étudiant 6]", "Review-Service", "Avis, Notes 1-5, Modération NoSQL", "Modèle MongoDB, Endpoints d'évaluations"],
    ["Collectif (Tous)", "API Gateway + Infra", "Routage, Eureka, RabbitMQ, Docker", "Gateway, Eureka, Docker-Compose, Rapport"]
]
t_team = doc.add_table(rows=1, cols=4)
style_table(t_team, [1.6, 1.4, 2.0, 1.8], team_headers, team_data)

add_styled_heading("14. Planning Prévisionnel & Analyse des Risques Techniques", level=1)
risk_headers = ["Risque Technique Identifié", "Niveau", "Impact", "Stratégie de Résolution Adoptée"]
risk_data = [
    ["Indisponibilité d'un service lors d'un appel synchrone", "🔴 Élevé", "Blocage de commande", "Circuit Breaker Resilience4j avec méthode Fallback"],
    ["Concurrence sur le même véhicule (Surbooking)", "🔴 Élevé", "Deux clients pour une voiture", "Contrôle d'intersection de dates + Verrouillage optimiste @Version"],
    ["Perte de message lors d'un crash de RabbitMQ", "🟡 Moyen", "Désynchronisation d'état", "Files durables (durable: true) et acquittement manuel (Manual ACK)"],
    ["Échec de paiement lors d'une réservation", "🟡 Moyen", "Incohérence de données", "Transaction de compensation (Pattern Saga) : annulation immédiate"],
    ["Problèmes de CORS depuis le Frontend Angular", "🟢 Faible", "Requêtes bloquées par browser", "CorsWebFilter réactif configuré centralement sur l'API Gateway"]
]
t_risk = doc.add_table(rows=1, cols=4)
style_table(t_risk, [2.2, 0.9, 1.5, 2.2], risk_headers, risk_data)

add_styled_heading("15. Conclusion & Perspectives", level=1)
add_body_p("Cette validation intermédiaire (Séance 4) démontre la maturité de la conception architecturale de CarRental. L'ensemble des 6 microservices métier et du service commun dispose d'un périmètre d'action clairement délimité, de diagrammes UML conformes aux standards académiques, de contrats d'API normalisés et d'un environnement de déploiement conteneurisé prêt à l'emploi.")
add_body_p("Les prochaines séances seront consacrées à la finalisation de l'implémentation des couches métier, au branchement définitif des écouteurs RabbitMQ, à l'interconnexion complète avec le Frontend Angular et à la réalisation de tests d'intégration de bout en bout avant la soutenance finale du projet AWD.")

try:
    doc.save(docx_path)
    print(f'Technical document saved at {docx_path}')
except Exception as e:
    alt_path = os.path.join(doc_dir, 'Dossier_Technique_CarRental_UML.docx')
    doc.save(alt_path)
    print(f'Original file was locked (open in Word). Saved updated version with authentic UML at {alt_path}')
print(f"Technical document with authentic UML diagrams saved at {docx_path}")
