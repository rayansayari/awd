import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

base_dir = r"C:\Users\RAYEN\.gemini\antigravity\scratch\CarRental-AWD"
pres_dir = os.path.join(base_dir, "Documentation", "Presentation")
diag_dir = os.path.join(base_dir, "Documentation", "Diagrams")
os.makedirs(pres_dir, exist_ok=True)

pptx_path = os.path.join(pres_dir, "Presentation_Seance4_CarRental.pptx")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5) # 16:9 widescreen format

# Professional Color Palette
C_PRIMARY = RGBColor(26, 54, 93)      # #1A365D - Deep Navy
C_SECONDARY = RGBColor(43, 108, 176)  # #2B6CB0 - Corporate Blue
C_ACCENT = RGBColor(221, 107, 32)     # #DD6B20 - Amber / Orange
C_BG_CARD = RGBColor(247, 250, 252)   # #F7FAFC - Light Gray/Blue
C_TEXT = RGBColor(45, 55, 72)         # #2D3748 - Dark Slate
C_MUTED = RGBColor(113, 128, 150)     # #718096 - Muted Gray
C_WHITE = RGBColor(255, 255, 255)

def create_header(slide, title_text, category_text="CARRENTAL • PROJET AWD (SÉANCE 4)"):
    # Header bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_PRIMARY
    top_bar.line.fill.background()

    # Category Text
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_ACCENT

    # Main Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE

def add_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text.strip()

# =========================================================================
# SLIDE 1 : TITRE
# =========================================================================
blank_layout = prs.slide_layouts[6]
s1 = prs.slides.add_slide(blank_layout)

bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_PRIMARY
bg1.line.fill.background()

# Title text box
tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(3.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "CarRental"
p1.font.size = Pt(48)
p1.font.bold = True
p1.font.color.rgb = C_WHITE

p2 = tf1.add_paragraph()
p2.text = "Plateforme Web de Location de Voitures en Microservices"
p2.font.size = Pt(24)
p2.font.color.rgb = RGBColor(190, 227, 248)
p2.space_before = Pt(10)

p3 = tf1.add_paragraph()
p3.text = "Soutenance de Validation Intermédiaire – Séance 4 • Module AWD (4DAS)"
p3.font.size = Pt(16)
p3.font.color.rgb = C_ACCENT
p3.space_before = Pt(15)

p4 = tf1.add_paragraph()
p4.text = "Équipe de 6 Étudiants : [Étudiant 1] • [Étudiant 2] • [Étudiant 3] • [Étudiant 4] • [Étudiant 5] • [Étudiant 6]"
p4.font.size = Pt(13)
p4.font.color.rgb = C_WHITE
p4.space_before = Pt(30)

add_notes(s1, """SPEECH INTRODUCTION (30 secondes - Chef d'équipe / Présentateur collectif) :
"Bonjour Monsieur / Madame. Nous sommes le groupe composé de 6 étudiants et nous avons le plaisir de vous présenter aujourd'hui l'architecture et la conception de notre projet AWD : CarRental, une plateforme web de location de voitures. 
Pour cette validation intermédiaire de séance 4, notre objectif est de vous démontrer la solidité de notre conception, la pertinence de notre découpage en 6 microservices métier et 1 service commun, la structure professionnelle de notre dépôt Git, ainsi que notre maîtrise des communications synchrones et asynchrones. 
Chacun d'entre nous présentera en 1 minute son microservice dédié, suivi des aspects transversaux." """)

# =========================================================================
# SLIDE 2 : PRÉSENTATION DU PROJET & OBJECTIFS
# =========================================================================
s2 = prs.slides.add_slide(blank_layout)
create_header(s2, "1. Présentation Générale & Vision Métier")

# Left Column (Concept)
b_left = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
b_left.fill.solid()
b_left.fill.fore_color.rgb = C_BG_CARD
b_left.line.color.rgb = C_SECONDARY

tb_l = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf_l = tb_l.text_frame
tf_l.word_wrap = True

p = tf_l.paragraphs[0]
p.text = "Le Concept CarRental"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

bullets_l = [
    "Plateforme unifiée reliant clients et réseau d'agences physiques.",
    "Recherche multicritère instantanée (marque, catégorie, prix, agence).",
    "Réservation en ligne en temps réel avec devis dynamique automatisé.",
    "Simulation bancaire sécurisée (statuts PAID, PENDING, CANCELLED).",
    "Gestion transparente des points de retrait et restitution de flotte.",
    "Évaluations clients vérifiées (notes 1 à 5 et commentaires modérés)."
]
for b in bullets_l:
    p_b = tf_l.add_paragraph()
    p_b.text = "• " + b
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = C_TEXT
    p_b.space_before = Pt(10)

# Right Column (Valeur Ajoutée)
b_right = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4))
b_right.fill.solid()
b_right.fill.fore_color.rgb = C_BG_CARD
b_right.line.color.rgb = C_SECONDARY

tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf_r = tb_r.text_frame
tf_r.word_wrap = True

p_r = tf_r.paragraphs[0]
p_r.text = "Objectifs de la Séance 4"
p_r.font.size = Pt(18)
p_r.font.bold = True
p_r.font.color.rgb = C_PRIMARY

bullets_r = [
    "Conception cohérente et validée à 100% avec les consignes.",
    "Découpage équilibré : 1 microservice dédié par étudiant.",
    "Service commun (API Gateway + Eureka + RabbitMQ) collectif.",
    "Diagrammes UML alignés exactement sur le code réel développé.",
    "Organisation Git professionnelle (Backend, Frontend, Documentation).",
    "Maîtrise totale des concepts théoriques et pratiques du cours."
]
for b in bullets_r:
    p_b = tf_r.add_paragraph()
    p_b.text = "✔ " + b
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = C_TEXT
    p_b.space_before = Pt(10)

add_notes(s2, """SPEECH (1 minute - Membre collectif) :
"CarRental résout une problématique concrète : permettre à des clients de louer des véhicules de façon fluide et fiable sans risque d'erreur ou de surréservation. 
Sur le plan académique, nous avons appliqué les meilleures pratiques de l'ingénierie logicielle distribuée : isolation stricte des contextes métier, pattern Database-per-Service, communication hybride synchrone et asynchrone, et sécurité centralisée. 
Pour ce jalon de séance 4, comme exigé par les consignes, nous présentons une conception mature, des contrats d'API complets, un dépôt Git structuré et une répartition claire des responsabilités au sein de nos 6 membres." """)

# =========================================================================
# SLIDE 3 : ACTEURS & CAS D'UTILISATION
# =========================================================================
s3 = prs.slides.add_slide(blank_layout)
create_header(s3, "2. Acteurs du Système & Cas d'Utilisation Métier")

actors = [
    ("Client / Visiteur", "• S'inscrire & se connecter (JWT)\n• Rechercher & filtrer les véhicules\n• Vérifier disponibilité temps réel\n• Réserver & payer en ligne\n• Télécharger factures PDF\n• Laisser des avis et notes (1-5)", C_SECONDARY),
    ("Employé d'Agence", "• Gérer la flotte de son agence\n• Mettre à jour les statuts (maintenance)\n• Valider prise en charge véhicule\n• Valider restitution véhicule\n• Consulter les réservations locales", RGBColor(47, 133, 90)),
    ("Administrateur", "• Superviser toute la flotte nationale\n• Gérer le réseau des agences\n• Assigner le personnel aux agences\n• Modérer les avis clients\n• Tableau de bord global d'activité", RGBColor(197, 48, 48))
]

for idx, (title, content, col) in enumerate(actors):
    x = Inches(0.8 + idx * 4.0)
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.7), Inches(5.4))
    card.fill.solid()
    card.fill.fore_color.rgb = C_BG_CARD
    card.line.color.rgb = col
    card.line.width = Pt(2)

    tb = s3.shapes.add_textbox(x + Inches(0.2), Inches(1.7), Inches(3.3), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = col

    p_c = tf.add_paragraph()
    p_c.text = content
    p_c.font.size = Pt(12)
    p_c.font.color.rgb = C_TEXT
    p_c.space_before = Pt(14)

add_notes(s3, """SPEECH (1 minute - Membre collectif) :
"Notre plateforme s'adresse à trois acteurs clairement différenciés :
1. Le Client Web, qui dispose d'un parcours 100% autonome : de la recherche filtrée jusqu'au paiement simulé et à la réception immédiate de sa facture.
2. L'Employé d'Agence, qui gère au quotidien le parc automobile local, suit les véhicules devant être préparés ou retournés, et actualise le statut de maintenance.
3. L'Administrateur, qui possède les droits les plus élevés pour piloter l'ensemble des agences, superviser les rôles et modérer les avis clients. 
Ces rôles sont garantis par Spring Security et propagés via les claims de nos jetons JWT." """)

# =========================================================================
# SLIDE 4 : ARCHITECTURE GLOBALE DES MICROSERVICES
# =========================================================================
s4 = prs.slides.add_slide(blank_layout)
create_header(s4, "3. Architecture Globale des Microservices")

img_arch = os.path.join(diag_dir, "architecture_globale.png")
if os.path.exists(img_arch):
    s4.shapes.add_picture(img_arch, Inches(0.8), Inches(1.4), width=Inches(8.0))

# Summary text box on right
tb_s4 = s4.shapes.add_textbox(Inches(9.1), Inches(1.4), Inches(3.8), Inches(5.5))
tf_s4 = tb_s4.text_frame
tf_s4.word_wrap = True

p_s4 = tf_s4.paragraphs[0]
p_s4.text = "Piliers d'Architecture :"
p_s4.font.size = Pt(16)
p_s4.font.bold = True
p_s4.font.color.rgb = C_PRIMARY

points_s4 = [
    "Frontend Angular (4200) : SPA réactive et moderne.",
    "API Gateway (8080) : Point d'entrée unique, filtre JWT, CORS.",
    "Eureka Server (8761) : Découverte dynamique de services.",
    "RabbitMQ (5672) : Bus d'événements asynchrones.",
    "6 Microservices Métier : Spring Boot 3.2+ totalement découplés.",
    "Database-per-Service : 5 instances PostgreSQL + 1 MongoDB."
]
for pt in points_s4:
    p = tf_s4.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT
    p.space_before = Pt(8)

add_notes(s4, """SPEECH (1 minute - Architecte / Membre collectif) :
"Voici le cœur architectural de CarRental. 
En façade, le Frontend Angular communique uniquement avec l'API Gateway sur le port 8080. Cela évite d'exposer nos services internes et masque la topologie réseau. 
La Gateway s'appuie sur Netflix Eureka pour localiser dynamiquement les 6 microservices métier sans adresses codées en dur. 
Nous appliquons rigoureusement le pattern Database-per-Service : aucune base de données n'est partagée. Chaque microservice possède son schéma dédié. 
Pour la communication, nous combinons les appels synchrones avec OpenFeign lorsque la réponse est immédiatement requise, et le bus RabbitMQ pour les notifications et les mises à jour asynchrones." """)

# =========================================================================
# SLIDE 5 : DÉCOUPAGE DES MICROSERVICES & BASES DE DONNÉES
# =========================================================================
s5 = prs.slides.add_slide(blank_layout)
create_header(s5, "4. Découpage Métier & Choix des Bases de Données")

# Table of microservices
rows = 7
cols = 4
left = Inches(0.8)
top = Inches(1.5)
width = Inches(11.733)
height = Inches(5.2)

table_shape = s5.shapes.add_table(rows, cols, left, top, width, height)
table = table_shape.table

headers = ["Microservice", "Port", "Base de Données", "Responsabilité Clé & Bounded Context"]
data = [
    ["1. User-Service", "8081", "PostgreSQL (user_db)", "Comptes, Inscription, Login, JWT, Rôles (CLIENT, AGENT, ADMIN)"],
    ["2. Vehicle-Service", "8082", "PostgreSQL (vehicle_db)", "Catalogue, Fiches véhicules, Catégories, Tarifs, Disponibilités"],
    ["3. Reservation-Service", "8083", "PostgreSQL (reservation_db)", "Dates, Devis, Cycle de vie (PENDING, CONFIRMED, CANCELLED)"],
    ["4. Payment-Service", "8084", "PostgreSQL (payment_db)", "Simulation paiement (PAID, FAILED), Factures PDF, Remboursements"],
    ["5. Agency-Service", "8085", "PostgreSQL (agency_db)", "Agences physiques, Adresses géographiques, Horaires, Personnel"],
    ["6. Review-Service", "8086", "MongoDB (review_db)", "Avis clients, Notes (1-5), Commentaires polymorphes, Modération"]
]

col_widths = [Inches(2.5), Inches(1.0), Inches(2.8), Inches(5.4)]
for i, w in enumerate(col_widths):
    table.columns[i].width = w

for j, h in enumerate(headers):
    cell = table.cell(0, j)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_PRIMARY
    p = cell.text_frame.paragraphs[0]
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

for i, row_data in enumerate(data):
    for j, val in enumerate(row_data):
        cell = table.cell(i+1, j)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(247, 250, 252) if i % 2 == 1 else C_WHITE
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT

add_notes(s5, """SPEECH (1 minute - Membre collectif) :
"Ce tableau résume notre découpage métier équilibré entre les 6 membres de l'équipe. 
Pourquoi PostgreSQL pour 5 services ? Parce que ces domaines gèrent des entités relationnelles fortes exigeant la conformité ACID et l'intégrité référentielle, notamment pour les paiements, les immatriculations uniques et les contrats de réservation.
Pourquoi MongoDB pour le Review-Service ? Les avis clients comportent des commentaires textuels de longueur variable et ciblent de façon polymorphe soit une agence, soit un véhicule. Le schéma NoSQL flexible de MongoDB et ses excellentes performances en lecture en font la solution idéale sans polluer nos bases relationnelles." """)

# =========================================================================
# SLIDE 6 : COMMUNICATION INTER-SERVICES
# =========================================================================
s6 = prs.slides.add_slide(blank_layout)
create_header(s6, "5. Communications Inter-Services : Synchrone vs Asynchrone")

img_comm = os.path.join(diag_dir, "communication_sync_async.png")
if os.path.exists(img_comm):
    s6.shapes.add_picture(img_comm, Inches(0.8), Inches(1.4), width=Inches(8.2))

tb_s6 = s6.shapes.add_textbox(Inches(9.2), Inches(1.4), Inches(3.7), Inches(5.5))
tf_s6 = tb_s6.text_frame
tf_s6.word_wrap = True

p = tf_s6.paragraphs[0]
p.text = "Règles Architecturales :"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

points_s6 = [
    "OpenFeign (Synchrone) : Utilisé uniquement lorsque la réponse immédiate est requise pour poursuivre (ex: vérifier le prix et créer la réservation).",
    "Circuit Breaker (Resilience4j) : Protège les appels Feign en cas de panne temporaire d'un service.",
    "RabbitMQ (Asynchrone) : Utilisé pour diffuser les événements métier à faible couplage (ex: reservation.confirmed).",
    "Persistance AMQP : Les messages patientent dans la queue si le consommateur est indisponible."
]
for pt in points_s6:
    p = tf_s6.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT
    p.space_before = Pt(8)

add_notes(s6, """SPEECH (1 minute - Membre collectif) :
"L'enseignant insiste particulièrement sur la distinction entre communication synchrone et asynchrone. 
Dans CarRental, nous ne faisons pas de tout-synchrone ni de tout-asynchrone :
Le synchrone avec OpenFeign est réservé aux étapes où le résultat immédiat est indispensable : le Reservation-Service doit connaître le prix exact et s'assurer que la voiture existe avant de valider le panier. 
En revanche, une fois la réservation confirmée, la notification et la mise à jour de statut du véhicule sont déléguées à RabbitMQ de manière asynchrone. Si le Vehicle-Service est ralenti, le message reste dans la queue sans bloquer l'utilisateur." """)

# =========================================================================
# SLIDES 7 À 12 : PRÉSENTATION INDIVIDUELLE (1 MINUTE PAR ÉTUDIANT)
# =========================================================================

# Slide 7 : Étudiant 1 - User Service
s7 = prs.slides.add_slide(blank_layout)
create_header(s7, "Partie Individuelle : 1. User-Service", "RESPONSABLE : ÉTUDIANT 1 - [NOM ÉTUDIANT 1]")

b_u = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
b_u.fill.solid()
b_u.fill.fore_color.rgb = C_BG_CARD
b_u.line.color.rgb = C_SECONDARY

tb_u = s7.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
tf_u = tb_u.text_frame
tf_u.word_wrap = True

p = tf_u.paragraphs[0]
p.text = "User-Service • Authentification, Sécurité & Profils"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

items_u = [
    ("Problématique & Rôle :", "Gérer de manière centralisée les identités, sécuriser l'accès et attribuer les autorisations (CLIENT, AGENT, ADMIN)."),
    ("Base de Données :", "PostgreSQL (user_db:5432) – Tables 'users', 'roles', 'user_roles' avec intégrité relationnelle et unicité des emails."),
    ("Sécurité JWT :", "Émission de jetons signés HMAC-SHA256 contenant userId, email et rôles. Vérification rapide sans réinterroger la DB."),
    ("Contrats d'API Clés :", "POST /api/auth/register (201 Created), POST /api/auth/login (200 OK + Token), GET /api/auth/validate, GET /api/users/{id}."),
    ("Gestion des Erreurs :", "GlobalExceptionHandler renvoyant des réponses RFC 7807 (400 Bad Request, 401 Unauthorized, 409 Conflict).")
]
for title, desc in items_u:
    p = tf_u.add_paragraph()
    p.text = title + " "
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_SECONDARY
    p.space_before = Pt(8)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

add_notes(s7, """SPEECH ÉTUDIANT 1 (1 minute chrono) :
"Bonjour, je suis [Nom Étudiant 1], responsable du User-Service. 
Mon service est le garant de la sécurité et de la gestion des identités dans CarRental. 
Il résout la problématique de l'authentification centralisée sans couplage fort en émettant des tokens sans état JWT signés. 
Lors de l'inscription ou de la connexion, les mots de passe sont chiffrés, les rôles comme ROLE_CLIENT ou ROLE_ADMIN sont attribués, et un token est retourné au client. 
J'ai choisi PostgreSQL pour garantir la cohérence stricte des comptes et l'unicité des adresses email. 
Mes endpoints principaux sont /api/auth/register et /api/auth/login. L'API Gateway valide ce token et propage l'identité aux autres services via des headers HTTP internes. 
Je suis prêt pour vos questions." """)

# Slide 8 : Étudiant 2 - Vehicle Service
s8 = prs.slides.add_slide(blank_layout)
create_header(s8, "Partie Individuelle : 2. Vehicle-Service", "RESPONSABLE : ÉTUDIANT 2 - [NOM ÉTUDIANT 2]")

b_v = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
b_v.fill.solid()
b_v.fill.fore_color.rgb = C_BG_CARD
b_v.line.color.rgb = RGBColor(47, 133, 90)

tb_v = s8.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
tf_v = tb_v.text_frame
tf_v.word_wrap = True

p = tf_v.paragraphs[0]
p.text = "Vehicle-Service • Gestion de Flotte, Catégories & Disponibilités"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(39, 103, 73)

items_v = [
    ("Problématique & Rôle :", "Fournir un catalogue précis, filtrable et à jour en temps réel des véhicules disponibles sur l'ensemble des agences."),
    ("Base de Données :", "PostgreSQL (vehicle_db:5433) – Tables 'vehicles', 'categories' avec indexation sur les marques, modèles et agences."),
    ("Entités & Statuts :", "Vehicle (marque, modèle, tarif/jour, km, statut: AVAILABLE, RENTED, MAINTENANCE, OUT_OF_SERVICE) et Category (SUV, Berline, Eco)."),
    ("Communication Synchrone :", "Appelé par Reservation-Service via OpenFeign pour vérifier instantanément le tarif et la disponibilité."),
    ("Communication Asynchrone :", "Écoute RabbitMQ sur l'événement 'reservation.confirmed' pour basculer automatiquement le véhicule à l'état RENTED."),
    ("Contrats d'API Clés :", "GET /api/vehicles, GET /api/vehicles/search?brand=...&agencyId=..., GET /api/vehicles/{id}/availability, POST /api/vehicles.")
]
for title, desc in items_v:
    p = tf_v.add_paragraph()
    p.text = title + " "
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = RGBColor(47, 133, 90)
    p.space_before = Pt(7)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

add_notes(s8, """SPEECH ÉTUDIANT 2 (1 minute chrono) :
"Bonjour, je suis [Nom Étudiant 2], responsable du Vehicle-Service. 
Mon microservice gère l'ensemble du parc automobile. La problématique est d'assurer un affichage réactif du catalogue avec un filtrage multicritère puissant par marque, agence et catégorie. 
J'ai conçu l'entité Vehicle avec un cycle d'état strict : AVAILABLE, RENTED, MAINTENANCE. 
En termes d'interactions, mon service est interrogé en synchrone par OpenFeign lors de la réservation pour confirmer le tarif journalier. 
De plus, il consomme de manière asynchrone l'événement RabbitMQ 'reservation.confirmed' pour passer le véhicule en RENTED sans impacter le temps de réponse de l'utilisateur. 
J'utilise PostgreSQL pour stocker les caractéristiques techniques et garantir l'unicité des plaques d'immatriculation." """)

# Slide 9 : Étudiant 3 - Reservation Service
s9 = prs.slides.add_slide(blank_layout)
create_header(s9, "Partie Individuelle : 3. Reservation-Service", "RESPONSABLE : ÉTUDIANT 3 - [NOM ÉTUDIANT 3]")

b_r = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
b_r.fill.solid()
b_r.fill.fore_color.rgb = C_BG_CARD
b_r.line.color.rgb = RGBColor(123, 52, 30)

tb_r = s9.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
tf_r = tb_r.text_frame
tf_r.word_wrap = True

p = tf_r.paragraphs[0]
p.text = "Reservation-Service • Cœur Métier, Devis & Cycle de Réservation"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(123, 52, 30)

items_r = [
    ("Problématique & Rôle :", "Orchestrer le cycle de location de bout en bout, calculer le montant exact et empêcher tout surbooking."),
    ("Base de Données :", "PostgreSQL (reservation_db:5434) – Table 'reservations' avec contraintes ACID et index temporels (startDate, endDate)."),
    ("Algorithme Anti-Surbooking :", "Contrôle d'intersection de dates via JPQL combiné à un verrouillage optimiste (@Version) évitant les collisions concurrentes."),
    ("Orchestration Métier :", "1. Appel Feign vers Vehicle-Service (tarif) -> 2. Création PENDING -> 3. Appel Feign vers Payment-Service (PAID) -> 4. CONFIRMED."),
    ("Publication Asynchrone :", "Émet 'reservation.confirmed' et 'reservation.cancelled' sur le Topic Exchange RabbitMQ."),
    ("Contrats d'API Clés :", "POST /api/reservations (201 Created), GET /api/reservations/{id}, GET /api/reservations/user/{userId}, PUT /{id}/cancel.")
]
for title, desc in items_r:
    p = tf_r.add_paragraph()
    p.text = title + " "
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = RGBColor(123, 52, 30)
    p.space_before = Pt(7)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

add_notes(s9, """SPEECH ÉTUDIANT 3 (1 minute chrono) :
"Bonjour, je suis [Nom Étudiant 3] et je pilote le Reservation-Service, le cœur névralgique de CarRental. 
Mon rôle est d'orchestrer la réservation. Lorsque le client valide ses dates, mon service calcule le nombre de jours, appelle Vehicle-Service via OpenFeign pour récupérer le prix journalier, enregistre la réservation avec le statut PENDING et déclenche le paiement en synchrone. 
Dès que le paiement réussit, la réservation passe à CONFIRMED et je publie un événement sur RabbitMQ. 
Pour éviter deux réservations simultanées pour le même véhicule, j'applique une requête de contrôle de chevauchement de dates et un verrouillage optimiste avec @Version. 
PostgreSQL est incontournable ici pour assurer la consistance transactionnelle ACID." """)

# Slide 10 : Étudiant 4 - Payment Service
s10 = prs.slides.add_slide(blank_layout)
create_header(s10, "Partie Individuelle : 4. Payment-Service", "RESPONSABLE : ÉTUDIANT 4 - [NOM ÉTUDIANT 4]")

b_p = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
b_p.fill.solid()
b_p.fill.fore_color.rgb = C_BG_CARD
b_p.line.color.rgb = RGBColor(107, 70, 193)

tb_p = s10.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
tf_p = tb_p.text_frame
tf_p.word_wrap = True

p = tf_p.paragraphs[0]
p.text = "Payment-Service • Simulation Financière & Facturation"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(107, 70, 193)

items_p = [
    ("Problématique & Rôle :", "Assurer les transactions financières et la facturation sans dépendance bancaire externe lourde."),
    ("Base de Données :", "PostgreSQL (payment_db:5435) – Tables 'payments' et 'invoices' avec relations 1-à-1 et auditabilité stricte."),
    ("Simulation Bancaire :", "Moteur réaliste simulant les statuts PAID (succès), PENDING (en attente), FAILED (refus) et REFUNDED (remboursement)."),
    ("Génération de Facture :", "Création automatique d'une référence unique (INV-XXXX) avec horodatage et montant TTC dès validation du paiement."),
    ("Gestion des Remboursements :", "Endpoint dédié POST /api/payments/refund/{resId} déclenché lors d'une annulation de réservation."),
    ("Contrats d'API Clés :", "POST /api/payments/process (201 Created), GET /api/payments/{id}, GET /api/payments/reservation/{resId}, POST /refund/{resId}.")
]
for title, desc in items_p:
    p = tf_p.add_paragraph()
    p.text = title + " "
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = RGBColor(107, 70, 193)
    p.space_before = Pt(7)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

add_notes(s10, """SPEECH ÉTUDIANT 4 (1 minute chrono) :
"Bonjour, je suis [Nom Étudiant 4], responsable du Payment-Service. 
Mon microservice prend en charge le traitement financier et la facturation. 
Comme demandé dans les consignes, nous avons développé une simulation bancaire complète gérant les états PAID, PENDING, FAILED et REFUNDED. 
Lorsque Reservation-Service soumet un paiement via OpenFeign, mon service valide la transaction, génère une référence unique de transaction TX-XXXX et produit immédiatement une facture numérotée INV-XXXX. 
En cas d'annulation de réservation par le client, mon service traite également le remboursement en passant le paiement en REFUNDED. 
La base PostgreSQL assure la traçabilité comptable et la rigueur financière." """)

# Slide 11 : Étudiant 5 - Agency Service
s11 = prs.slides.add_slide(blank_layout)
create_header(s11, "Partie Individuelle : 5. Agency-Service", "RESPONSABLE : ÉTUDIANT 5 - [NOM ÉTUDIANT 5]")

b_a = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
b_a.fill.solid()
b_a.fill.fore_color.rgb = C_BG_CARD
b_a.line.color.rgb = RGBColor(40, 94, 97)

tb_a = s11.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
tf_a = tb_a.text_frame
tf_a.word_wrap = True

p = tf_a.paragraphs[0]
p.text = "Agency-Service • Réseau d'Agences, Emplacements & Staff"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(40, 94, 97)

items_a = [
    ("Problématique & Rôle :", "Gérer le réseau physique des agences de location, les adresses de retrait/restitution et le personnel affecté."),
    ("Base de Données :", "PostgreSQL (agency_db:5436) – Tables 'agencies', 'agency_staff' avec objet valeur Address embarqué (@Embedded)."),
    ("Découplage Réseau :", "Les véhicules et réservations stockent uniquement un identifiant 'agencyId', évitant tout couplage SQL inter-services."),
    ("Recherche Géographique :", "Recherche simplifiée par ville via l'endpoint dédié /api/agencies/city/{city} pour orienter le client."),
    ("Gestion des Horaires :", "Stockage des plages d'ouverture pour valider la faisabilité de prise en charge d'un véhicule."),
    ("Contrats d'API Clés :", "GET /api/agencies, GET /api/agencies/{id}, GET /api/agencies/city/{city}, POST /api/agencies (201 Created), PUT /{id}.")
]
for title, desc in items_a:
    p = tf_a.add_paragraph()
    p.text = title + " "
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = RGBColor(40, 94, 97)
    p.space_before = Pt(7)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

add_notes(s11, """SPEECH ÉTUDIANT 5 (1 minute chrono) :
"Bonjour, je suis [Nom Étudiant 5], responsable de l'Agency-Service. 
Dans la location de véhicules, l'ancrage territorial est indispensable. Mon service répertorie les agences physiques, leurs adresses complètes, leurs coordonnées et les employés rattachés. 
Sur le plan architectural, mon service garantit un découplage total : les autres microservices ne font aucune jointure sur mes tables, ils référencent seulement un agencyId. 
J'ai implémenté un composant d'adresses embarqué Address avec ville et code postal, et exposé des endpoints optimisés pour rechercher les agences par ville. 
PostgreSQL me permet d'assurer l'intégrité des agences et l'unicité de leur code d'identification." """)

# Slide 12 : Étudiant 6 - Review Service
s12 = prs.slides.add_slide(blank_layout)
create_header(s12, "Partie Individuelle : 6. Review-Service", "RESPONSABLE : ÉTUDIANT 6 - [NOM ÉTUDIANT 6]")

b_rv = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
b_rv.fill.solid()
b_rv.fill.fore_color.rgb = C_BG_CARD
b_rv.line.color.rgb = RGBColor(116, 66, 16)

tb_rv = s12.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
tf_rv = tb_rv.text_frame
tf_rv.word_wrap = True

p = tf_rv.paragraphs[0]
p.text = "Review-Service • Avis Clients, Notations & Modération NoSQL"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(116, 66, 16)

items_rv = [
    ("Problématique & Rôle :", "Collecter et diffuser les avis clients (notes de 1 à 5 et commentaires) avec une performance maximale en lecture."),
    ("Base de Données NoSQL :", "MongoDB (review_db:27017) – Justifié par un schéma flexible semi-structuré et des requêtes de consultation très fréquentes."),
    ("Ciblage Polymorphe :", "L'avis s'applique de façon flexible soit à un véhicule (targetType: VEHICLE), soit à une agence (targetType: AGENCY)."),
    ("Modération des Avis :", "Gestion des états PENDING, APPROVED, REJECTED. Seuls les avis approuvés sont visibles sur le catalogue public."),
    ("Calcul des Moyennes :", "Agrégation dynamique des notes pour calculer la moyenne affichée sur la fiche descriptive du véhicule."),
    ("Contrats d'API Clés :", "POST /api/reviews (201 Created), GET /api/reviews/vehicle/{id}, GET /api/reviews/agency/{id}, GET /api/reviews/user/{id}.")
]
for title, desc in items_rv:
    p = tf_rv.add_paragraph()
    p.text = title + " "
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = RGBColor(116, 66, 16)
    p.space_before = Pt(7)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

add_notes(s12, """SPEECH ÉTUDIANT 6 (1 minute chrono) :
"Bonjour, je suis [Nom Étudiant 6], responsable du Review-Service. 
Mon service apporte la preuve sociale sur CarRental en permettant aux clients d'évaluer les véhicules et les agences avec des notes de 1 à 5 et des commentaires. 
Contrairement à mes camarades, j'ai fait le choix délibéré d'une base NoSQL MongoDB. 
Pourquoi ? Parce que les avis sont des données semi-structurées de taille variable, avec un ciblage polymorphe, et qu'ils subissent une charge de lecture massive. MongoDB offre d'excellentes performances d'agrégation pour calculer les notes moyennes sans ralentir nos bases transactionnelles. 
Mon service intègre également une modération simple pour rejeter les avis inappropriés." """)

# =========================================================================
# SLIDE 13 : SERVICE COMMUN & INFRASTRUCTURE
# =========================================================================
s13 = prs.slides.add_slide(blank_layout)
create_header(s13, "6. Microservice Commun & Infrastructure Développée Collectivement")

infra_cards = [
    ("API Gateway (8080)", "• Spring Cloud Gateway\n• Routage dynamique /api/**\n• Validation des jetons JWT\n• Propagation headers (X-User-Id)\n• CorsWebFilter réactif (localhost:4200)\n• Rate Limiting anti-DDoS", C_PRIMARY),
    ("Eureka Discovery (8761)", "• Netflix Eureka Server\n• Enregistrement automatique au boot\n• Heartbeat toutes les 30s\n• Load Balancing côté client\n• Tolérance aux pannes\n• Zéro IP en dur dans le code", C_SECONDARY),
    ("RabbitMQ & Docker", "• Broker AMQP (Port 5672/15672)\n• Topic Exchange 'carrental.topic'\n• Files durables (durable: true)\n• docker-compose.yml complet\n• Réseau bridge 'carrental-network'\n• 1 commande : docker-compose up", C_ACCENT)
]

for idx, (title, content, col) in enumerate(infra_cards):
    x = Inches(0.8 + idx * 4.0)
    card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.7), Inches(5.4))
    card.fill.solid()
    card.fill.fore_color.rgb = C_BG_CARD
    card.line.color.rgb = col
    card.line.width = Pt(2)

    tb = s13.shapes.add_textbox(x + Inches(0.2), Inches(1.7), Inches(3.3), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = col

    p_c = tf.add_paragraph()
    p_c.text = content
    p_c.font.size = Pt(12)
    p_c.font.color.rgb = C_TEXT
    p_c.space_before = Pt(14)

add_notes(s13, """SPEECH SERVICE COMMUN (1 minute - Membre collectif délégué) :
"Comme l'exigent les consignes de l'enseignant, notre projet comporte une composante commune développée collectivement par toute l'équipe. 
Cette infrastructure comprend :
1. L'API Gateway sous Spring Cloud Gateway, qui applique le filtre JWT réactif, gère les CORS pour notre frontend Angular, et assure le routage dynamique.
2. Le Discovery Server Eureka, qui enregistre nos services et permet d'équilibrer la charge côté client sans aucune IP codée en dur.
3. Le Broker RabbitMQ, configuré avec un Topic Exchange pour découpler les événements de réservation et de paiement.
Enfin, nous avons assemblé un docker-compose.yml complet qui permet à n'importe quel membre du groupe ou à l'enseignant de démarrer l'ensemble de la plateforme en une seule commande." """)

# =========================================================================
# SLIDE 14 : ORGANISATION GIT & GESTION DE PROJET
# =========================================================================
s14 = prs.slides.add_slide(blank_layout)
create_header(s14, "7. Organisation du Dépôt Git & Gestion de Projet")

b_git = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
b_git.fill.solid()
b_git.fill.fore_color.rgb = C_BG_CARD
b_git.line.color.rgb = C_SECONDARY

tb_g = s14.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf_g = tb_g.text_frame
tf_g.word_wrap = True

p = tf_g.paragraphs[0]
p.text = "Structure & Branches Git"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

bullets_g = [
    "Dépôt unique conforme au PDF de l'enseignant : Backend, Frontend, Documentation.",
    "Branche 'main' : Code stable prêt pour la soutenance.",
    "Branche 'develop' : Branche d'intégration continue collective.",
    "Branches de fonctionnalités : feature/user-auth, feature/vehicle-catalog, etc.",
    "Commits conventionnels : feat(...), fix(...), docs(uml).",
    "Fichier .gitignore complet excluant target/, node_modules/ et logs."
]
for b in bullets_g:
    p_b = tf_g.add_paragraph()
    p_b.text = "• " + b
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = C_TEXT
    p_b.space_before = Pt(8)

b_pm = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4))
b_pm.fill.solid()
b_pm.fill.fore_color.rgb = C_BG_CARD
b_pm.line.color.rgb = C_SECONDARY

tb_pm = s14.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf_pm = tb_pm.text_frame
tf_pm.word_wrap = True

p_pm = tf_pm.paragraphs[0]
p_pm.text = "Outils de Pilotage & Qualité"
p_pm.font.size = Pt(18)
p_pm.font.bold = True
p_pm.font.color.rgb = C_PRIMARY

bullets_pm = [
    "GitHub Projects (Kanban) : Suivi des tâches (To Do, In Progress, Review, Done).",
    "Postman Workspace partagé : Collection centralisée des requêtes API avec variables d'environnement.",
    "Revue de code systématique (Pull Requests) avant fusion dans 'develop'.",
    "Tests unitaires JUnit 5 et tests d'intégration Spring Boot.",
    "Documentation Markdown et Word (.docx) synchronisées en continu."
]
for b in bullets_pm:
    p_b = tf_pm.add_paragraph()
    p_b.text = "✔ " + b
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = C_TEXT
    p_b.space_before = Pt(8)

add_notes(s14, """SPEECH (1 minute - Membre collectif) :
"La rigueur méthodologique est un point clé évalué en séance 4. 
Notre dépôt respecte scrupuleusement l'arborescence demandée : Backend regroupant les 6 services et la Gateway, Frontend avec notre application Angular, et Documentation avec nos diagrammes, notre support de présentation et notre dossier technique. 
Nous appliquons le modèle GitFlow : aucune modification n'est poussée directement sur 'main'. Chaque membre travaille sur sa branche de feature et soumet une Pull Request avec des messages de commit conventionnels. 
Pour le suivi, nous utilisons un tableau Kanban GitHub Projects et une collection Postman partagée." """)

# =========================================================================
# SLIDE 15 : PLANNING PRÉVISIONNEL & RISQUES TECHNIQUES
# =========================================================================
s15 = prs.slides.add_slide(blank_layout)
create_header(s15, "8. Planning Prévisionnel & Gestion des Risques")

b_gantt = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
b_gantt.fill.solid()
b_gantt.fill.fore_color.rgb = C_BG_CARD
b_gantt.line.color.rgb = C_PRIMARY

tb_gt = s15.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf_gt = tb_gt.text_frame
tf_gt.word_wrap = True

p = tf_gt.paragraphs[0]
p.text = "Feuille de Route (Séances 1 à 8)"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

plan_items = [
    ("Séances 1-2 (Terminé) :", "Cadrage, découpage microservices & dépôt Git."),
    ("Séances 3-4 (Jalon Actuel) :", "Conception UML, squelettes compilables, APIs & soutenance intermédiaire."),
    ("Séance 5 :", "Finalisation persistance, jeux de données & Eureka."),
    ("Séance 6 :", "Communications Feign, Circuit Breakers & RabbitMQ."),
    ("Séance 7 :", "Intégration écrans Angular & tests d'intégration E2E."),
    ("Séance 8 :", "Optimisation globale & soutenance finale.")
]
for title, desc in plan_items:
    p = tf_gt.add_paragraph()
    p.text = title + " "
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_SECONDARY
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

b_rk = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.4))
b_rk.fill.solid()
b_rk.fill.fore_color.rgb = C_BG_CARD
b_rk.line.color.rgb = C_PRIMARY

tb_rk = s15.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf_rk = tb_rk.text_frame
tf_rk.word_wrap = True

p = tf_rk.paragraphs[0]
p.text = "Analyse & Maîtrise des Risques"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

risks = [
    ("Surbooking concurrent :", "Contrôle d'intersection de dates en transaction sérialisable + @Version JPA."),
    ("Panne synchrone :", "Circuit Breaker Resilience4j évitant le blocage de threads."),
    ("Perte de messages RabbitMQ :", "Files durables et acquittement manuel (Manual ACK)."),
    ("Échec de paiement :", "Pattern Saga avec transaction de compensation (annulation automatique)."),
    ("Problème CORS :", "CorsWebFilter réactif configuré centralement sur la Gateway.")
]
for title, desc in risks:
    p = tf_rk.add_paragraph()
    p.text = "⚠ " + title + " "
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(197, 48, 48)
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = desc
    r.font.bold = False
    r.font.color.rgb = C_TEXT

add_notes(s15, """SPEECH (1 minute - Membre collectif) :
"Pour garantir le succès du projet d'ici la séance 8, nous suivons un planning strict en 4 grandes phases. 
La séance 4 constitue notre jalon intermédiaire de validation de la conception. 
Nous avons également identifié les risques techniques majeurs et défini dès aujourd'hui nos solutions d'atténuation : 
le surbooking est empêché par des requêtes de chevauchement de dates et du verrouillage optimiste ; les pannes réseau sont contenues par des Circuit Breakers Resilience4j ; et les échecs de paiement sont compensés par des annulations automatiques suivant le pattern Saga." """)

# =========================================================================
# SLIDE 16 : CONCLUSION & QUESTIONS
# =========================================================================
s16 = prs.slides.add_slide(blank_layout)

bg16 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg16.fill.solid()
bg16.fill.fore_color.rgb = C_PRIMARY
bg16.line.fill.background()

tb16 = s16.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
tf16 = tb16.text_frame
tf16.word_wrap = True

p1 = tf16.paragraphs[0]
p1.text = "Merci pour votre attention !"
p1.font.size = Pt(40)
p1.font.bold = True
p1.font.color.rgb = C_WHITE

p2 = tf16.add_paragraph()
p2.text = "CarRental est prêt pour la phase d'implémentation avancée."
p2.font.size = Pt(20)
p2.font.color.rgb = RGBColor(190, 227, 248)
p2.space_before = Pt(12)

p3 = tf16.add_paragraph()
p3.text = "Place à la session de questions / réponses (10 minutes)"
p3.font.size = Pt(16)
p3.font.color.rgb = C_ACCENT
p3.space_before = Pt(25)

p4 = tf16.add_paragraph()
p4.text = "Tous les membres de l'équipe sont à votre disposition pour détailler leur microservice."
p4.font.size = Pt(13)
p4.font.color.rgb = C_WHITE
p4.space_before = Pt(20)

add_notes(s16, """SPEECH CONCLUSION (30 secondes - Chef d'équipe / Présentateur collectif) :
"En conclusion, l'équipe CarRental a mis en place l'ensemble des fondations d'un système distribué professionnel : 6 microservices découplés, une passerelle d'accès sécurisée, un bus d'événements AMQP, des bases de données indépendantes et une interface Angular prête à être connectée. 
Nous vous remercions pour votre attention et nous sommes désormais tous les 6 à votre entière disposition pour répondre à vos questions techniques." """)

prs.save(pptx_path)
print(f"PowerPoint presentation created successfully at {pptx_path}")
