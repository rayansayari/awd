import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

diagram_dir = r"C:\Users\RAYEN\.gemini\antigravity\scratch\CarRental-AWD\Documentation\Diagrams"
os.makedirs(diagram_dir, exist_ok=True)

# 1. Architecture Globale
def generate_architecture_globale():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.6, "CarRental - Architecture Globale des Microservices", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1A365D')
    ax.text(7, 9.2, "Plateforme Web de Location de Voitures (AWD - Séance 4)", 
            ha='center', va='center', fontsize=12, color='#4A5568')

    # Frontend Client
    rect_client = patches.FancyBboxPatch((4.5, 7.8), 5, 0.9, boxstyle="round,pad=0.2", 
                                        ec="#2B6CB0", fc="#EBF8FF", lw=2)
    ax.add_patch(rect_client)
    ax.text(7, 8.25, "FRONTEND ANGULAR 17+\nClient SPA - Port 4200 (Dashboard, Réservations, Recherche)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#2B6CB0')

    # API Gateway & Infra
    rect_gw = patches.FancyBboxPatch((1.5, 6.2), 4.5, 0.9, boxstyle="round,pad=0.2", 
                                    ec="#C53030", fc="#FFF5F5", lw=2)
    ax.add_patch(rect_gw)
    ax.text(3.75, 6.65, "API GATEWAY (Spring Cloud)\nPort 8080 - Routage, Filtre JWT, CORS", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#9B2C2C')

    rect_eureka = patches.FancyBboxPatch((6.5, 6.2), 3.2, 0.9, boxstyle="round,pad=0.2", 
                                         ec="#D69E2E", fc="#FFFFF0", lw=2)
    ax.add_patch(rect_eureka)
    ax.text(8.1, 6.65, "EUREKA SERVER\nPort 8761 - Service Discovery", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#B7791F')

    rect_rabbit = patches.FancyBboxPatch((10.2, 6.2), 3.2, 0.9, boxstyle="round,pad=0.2", 
                                        ec="#DD6B20", fc="#FFFAF0", lw=2)
    ax.add_patch(rect_rabbit)
    ax.text(11.8, 6.65, "RABBITMQ BROKER\nPort 5672 - Events AMQP", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#C05621')

    # Services
    services = [
        ("1. User Service\n:8081 (Auth/JWT)", 0.5, 3.8, "#2C5282", "#EBF8FF"),
        ("2. Vehicle Service\n:8082 (Flotte/Dispo)", 2.7, 3.8, "#276749", "#F0FFF4"),
        ("3. Reservation Service\n:8083 (Réservations)", 4.9, 3.8, "#7B341E", "#FFFAF0"),
        ("4. Payment Service\n:8084 (Paiement/Facture)", 7.1, 3.8, "#6B46C1", "#FAF5FF"),
        ("5. Agency Service\n:8085 (Agences/Staff)", 9.3, 3.8, "#285E61", "#E6FFFA"),
        ("6. Review Service\n:8086 (Avis/Notes)", 11.5, 3.8, "#744210", "#FFFFF0"),
    ]

    for name, x, y, border_c, fill_c in services:
        r = patches.FancyBboxPatch((x, y), 2.0, 1.2, boxstyle="round,pad=0.15", 
                                   ec=border_c, fc=fill_c, lw=1.8)
        ax.add_patch(r)
        ax.text(x + 1.0, y + 0.6, name, ha='center', va='center', 
                fontsize=9, fontweight='bold', color=border_c)

    # Databases
    dbs = [
        ("user_db\n(PostgreSQL)", 0.5, 1.2, "#2C5282"),
        ("vehicle_db\n(PostgreSQL)", 2.7, 1.2, "#276749"),
        ("res_db\n(PostgreSQL)", 4.9, 1.2, "#7B341E"),
        ("payment_db\n(PostgreSQL)", 7.1, 1.2, "#6B46C1"),
        ("agency_db\n(PostgreSQL)", 9.3, 1.2, "#285E61"),
        ("review_db\n(MongoDB)", 11.5, 1.2, "#744210"),
    ]

    for name, x, y, color in dbs:
        r = patches.FancyBboxPatch((x, y), 2.0, 0.9, boxstyle="square,pad=0.1", 
                                   ec=color, fc="#EDF2F7", lw=1.5, ls="--")
        ax.add_patch(r)
        ax.text(x + 1.0, y + 0.45, name, ha='center', va='center', 
                fontsize=8.5, fontweight='bold', color=color)
        # Arrow DB
        ax.annotate("", xy=(x + 1.0, y + 0.9), xytext=(x + 1.0, 3.8),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=1.2))

    # Flow arrows
    ax.annotate("Requêtes REST / JWT", xy=(7, 7.8), xytext=(4, 7.1),
                arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=2, shrinkA=5, shrinkB=5))

    ax.annotate("", xy=(3.75, 6.2), xytext=(1.5, 5.0),
                arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))
    ax.annotate("", xy=(3.75, 6.2), xytext=(3.7, 5.0),
                arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))
    ax.annotate("", xy=(3.75, 6.2), xytext=(5.9, 5.0),
                arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))
    ax.annotate("", xy=(3.75, 6.2), xytext=(8.1, 5.0),
                arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))
    ax.annotate("", xy=(3.75, 6.2), xytext=(10.3, 5.0),
                arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))
    ax.annotate("", xy=(3.75, 6.2), xytext=(12.5, 5.0),
                arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5))

    # Inter-service sync arrows (Reservation -> Vehicle & Payment)
    ax.annotate("OpenFeign (Dispo)", xy=(4.7, 4.4), xytext=(4.9, 4.4),
                arrowprops=dict(arrowstyle="->", color="#C53030", lw=1.5))
    ax.annotate("OpenFeign (Paiement)", xy=(7.1, 4.4), xytext=(6.9, 4.4),
                arrowprops=dict(arrowstyle="->", color="#C53030", lw=1.5))

    # RabbitMQ async
    ax.annotate("Event: res.created", xy=(11.0, 6.2), xytext=(5.9, 5.0),
                arrowprops=dict(arrowstyle="->", color="#DD6B20", lw=1.5, ls=":"))
    ax.annotate("Event: pay.done", xy=(11.8, 6.2), xytext=(8.1, 5.0),
                arrowprops=dict(arrowstyle="->", color="#DD6B20", lw=1.5, ls=":"))

    # Legend
    ax.plot([0.5, 1.2], [0.4, 0.4], color="#2B6CB0", lw=2)
    ax.text(1.3, 0.4, "Requêtes Client / API REST", va='center', fontsize=8.5)
    ax.plot([4.0, 4.7], [0.4, 0.4], color="#C53030", lw=2)
    ax.text(4.8, 0.4, "Appel Synchrone (OpenFeign)", va='center', fontsize=8.5)
    ax.plot([8.0, 8.7], [0.4, 0.4], color="#DD6B20", lw=2, ls=":")
    ax.text(8.8, 0.4, "Événement Asynchrone (RabbitMQ)", va='center', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(os.path.join(diagram_dir, "architecture_globale.png"), dpi=300)
    plt.close()
    print("architecture_globale.png created.")

generate_architecture_globale()

# 2. Cas d'Utilisation
def generate_cas_utilisation():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, "Diagramme des Cas d'Utilisation Métier - CarRental", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1A365D')

    # Actors
    actors = [
        ("Client / Visiteur\n(Web)", 1.2, 7.5, "#2B6CB0"),
        ("Employé d'Agence\n(Gestion Locale)", 1.2, 4.5, "#2F855A"),
        ("Administrateur\n(Supervision)", 1.2, 1.8, "#C53030")
    ]
    for label, x, y, col in actors:
        r = patches.FancyBboxPatch((x-0.8, y-0.6), 1.6, 1.2, boxstyle="round,pad=0.1", ec=col, fc="#EDF2F7", lw=2)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color=col)

    # Use cases boxes
    boxes = [
        ("Module Utilisateurs & Profils", [
            "- S'inscrire / S'authentifier (JWT)",
            "- Gérer son profil & permis de conduire",
            "- Gérer les rôles et permissions"
        ], 3.8, 7.0, "#2B6CB0"),

        ("Module Véhicules & Catalogue", [
            "- Rechercher & filtrer les véhicules",
            "- Consulter caractéristiques & disponibilités",
            "- Gérer la flotte (Ajout, modif, maintenance)"
        ], 8.8, 7.0, "#276749"),

        ("Module Réservations & Planning", [
            "- Créer une réservation multi-jours",
            "- Consulter l'historique personnel",
            "- Modifier ou annuler une réservation"
        ], 3.8, 3.8, "#7B341E"),

        ("Module Paiements & Factures", [
            "- Simuler & régler en ligne (PENDING/PAID)",
            "- Générer & télécharger la facture PDF",
            "- Traiter les remboursements d'annulation"
        ], 8.8, 3.8, "#6B46C1"),

        ("Module Agences & Points de Retrait", [
            "- Localiser agences de prise en charge",
            "- Assigner les employés aux agences"
        ], 3.8, 0.8, "#285E61"),

        ("Module Avis & Modération", [
            "- Laisser note (1-5) et commentaire",
            "- Modérer les évaluations reçues"
        ], 8.8, 0.8, "#744210")
    ]

    for title, items, x, y, col in boxes:
        r = patches.FancyBboxPatch((x, y), 4.6, 2.4, boxstyle="round,pad=0.2", ec=col, fc="#FFFFFF", lw=1.5)
        ax.add_patch(r)
        ax.text(x + 2.3, y + 2.05, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=col)
        text_content = "\n".join(items)
        ax.text(x + 0.3, y + 1.0, text_content, ha='left', va='center', fontsize=9, color="#2D3748")

    # Connectors
    ax.annotate("", xy=(3.8, 7.9), xytext=(2.0, 7.5), arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=1.5))
    ax.annotate("", xy=(3.8, 5.0), xytext=(2.0, 7.5), arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=1.5))
    ax.annotate("", xy=(8.8, 7.9), xytext=(2.0, 7.5), arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=1.5))
    ax.annotate("", xy=(8.8, 5.0), xytext=(2.0, 7.5), arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=1.5))

    ax.annotate("", xy=(8.8, 7.5), xytext=(2.0, 4.5), arrowprops=dict(arrowstyle="->", color="#2F855A", lw=1.5))
    ax.annotate("", xy=(3.8, 4.5), xytext=(2.0, 4.5), arrowprops=dict(arrowstyle="->", color="#2F855A", lw=1.5))

    ax.annotate("", xy=(3.8, 2.0), xytext=(2.0, 1.8), arrowprops=dict(arrowstyle="->", color="#C53030", lw=1.5))
    ax.annotate("", xy=(8.8, 2.0), xytext=(2.0, 1.8), arrowprops=dict(arrowstyle="->", color="#C53030", lw=1.5))

    plt.tight_layout()
    plt.savefig(os.path.join(diagram_dir, "cas_utilisation.png"), dpi=300)
    plt.close()
    print("cas_utilisation.png created.")

generate_cas_utilisation()

# 3. Sequence Reservation
def generate_sequence_reservation():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')

    ax.text(7, 10.5, "Diagramme de Séquence - Parcours Complet de Réservation", 
            ha='center', va='center', fontsize=17, fontweight='bold', color='#1A365D')

    actors = [
        ("Client Web\n(Angular)", 1.2),
        ("API Gateway\n(:8080)", 3.6),
        ("Reservation Srv\n(:8083)", 6.2),
        ("Vehicle Srv\n(:8082)", 8.8),
        ("Payment Srv\n(:8084)", 11.2),
        ("RabbitMQ\nBroker", 13.0)
    ]

    for name, x in actors:
        r = patches.FancyBboxPatch((x-0.9, 9.3), 1.8, 0.8, boxstyle="round,pad=0.1", ec="#2B6CB0", fc="#EBF8FF", lw=1.5)
        ax.add_patch(r)
        ax.text(x, 9.7, name, ha='center', va='center', fontsize=9, fontweight='bold', color='#2B6CB0')
        ax.plot([x, x], [0.8, 9.3], color="#CBD5E0", linestyle="--", lw=1.2)

    steps = [
        (8.5, 1.2, 3.6, "1. POST /api/reservations (dates, vehicleId=5, JWT)", "#2B6CB0", False),
        (7.8, 3.6, 6.2, "2. Routage vers Reservation-Service", "#2B6CB0", False),
        (7.0, 6.2, 8.8, "3. [Feign Synchrone] GET /api/vehicles/5/availability", "#C53030", False),
        (6.3, 8.8, 6.2, "4. 200 OK {available: true, pricePerDay: 45€}", "#276749", True),
        (5.5, 6.2, 6.2, "5. Calcul total (5j x 45€ = 225€) & Sauvegarde statut PENDING", "#744210", None),
        (4.7, 6.2, 11.2, "6. [Feign Synchrone] POST /api/payments/process (225€)", "#C53030", False),
        (3.9, 11.2, 6.2, "7. 201 Created {status: PAID, invoiceNum: INV-101}", "#276749", True),
        (3.1, 6.2, 6.2, "8. Mise à jour statut Réservation -> CONFIRMED", "#744210", None),
        (2.3, 6.2, 13.0, "9. [RabbitMQ Asynchrone] Event: reservation.confirmed", "#DD6B20", False),
        (1.5, 13.0, 8.8, "10. Consommation événement -> statut véhicule = RENTED", "#DD6B20", True),
        (0.9, 6.2, 1.2, "11. 201 Created (Réservation confirmée + Facture)", "#276749", True)
    ]

    for y, x1, x2, label, color, is_return in steps:
        if is_return is None:
            r = patches.FancyBboxPatch((x1-1.8, y-0.25), 3.6, 0.5, boxstyle="square,pad=0.05", ec=color, fc="#FFFFF0", lw=1)
            ax.add_patch(r)
            ax.text(x1, y, label, ha='center', va='center', fontsize=8, color=color, fontweight='bold')
        else:
            style = "<-" if is_return else "->"
            ls = ":" if is_return else "-"
            ax.annotate("", xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle=style, color=color, lw=1.6, ls=ls))
            ax.text((x1 + x2)/2, y + 0.15, label, ha='center', va='bottom', fontsize=8.2, color=color, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(diagram_dir, "sequence_reservation.png"), dpi=300)
    plt.close()
    print("sequence_reservation.png created.")

generate_sequence_reservation()

# 4. Communication Synchrone vs Asynchrone
def generate_communication_sync_async():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, "Comparatif Architectural : Communication Synchrone vs Asynchrone", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A365D')

    r1 = patches.FancyBboxPatch((0.5, 1.0), 6.2, 7.8, boxstyle="round,pad=0.2", ec="#C53030", fc="#FFF5F5", lw=2)
    ax.add_patch(r1)
    ax.text(3.6, 8.4, "COMMUNICATION SYNCHRONE\n(REST / Spring Cloud OpenFeign)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#9B2C2C')

    sync_boxes = [
        ("Reservation Service", 1.2, 6.2, "#7B341E"),
        ("Vehicle Service", 1.2, 4.4, "#276749"),
        ("Payment Service", 1.2, 2.6, "#6B46C1")
    ]
    for name, x, y, col in sync_boxes:
        b = patches.FancyBboxPatch((x, y), 4.8, 0.8, boxstyle="round,pad=0.1", ec=col, fc="#FFFFFF", lw=1.5)
        ax.add_patch(b)
        ax.text(x+2.4, y+0.4, name, ha='center', va='center', fontsize=10, fontweight='bold', color=col)

    ax.annotate("Appel HTTP direct (Bloquant)\nGET /api/vehicles/{id}/availability", 
                xy=(3.6, 5.2), xytext=(3.6, 6.2),
                arrowprops=dict(arrowstyle="<->", color="#C53030", lw=2),
                ha='center', fontsize=8, color="#9B2C2C")

    ax.annotate("Simulation bancaire immédiate\nPOST /api/payments/process", 
                xy=(3.6, 3.4), xytext=(3.6, 4.4),
                arrowprops=dict(arrowstyle="<->", color="#C53030", lw=2),
                ha='center', fontsize=8, color="#9B2C2C")

    ax.text(3.6, 1.4, "* Avantages : Cohérence immédiate, réponse instantanée\n* Protection : Circuit Breaker (Resilience4j) en cas de panne", 
            ha='center', va='center', fontsize=8.5, color="#742A2A")

    r2 = patches.FancyBboxPatch((7.3, 1.0), 6.2, 7.8, boxstyle="round,pad=0.2", ec="#DD6B20", fc="#FFFAF0", lw=2)
    ax.add_patch(r2)
    ax.text(10.4, 8.4, "COMMUNICATION ASYNCHRONE\n(Event-Driven avec RabbitMQ AMQP)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#C05621')

    b_prod = patches.FancyBboxPatch((7.8, 6.2), 5.2, 0.8, boxstyle="round,pad=0.1", ec="#7B341E", fc="#FFFFFF", lw=1.5)
    ax.add_patch(b_prod)
    ax.text(10.4, 6.6, "Producteur : Reservation / Payment Srv", ha='center', va='center', fontsize=10, fontweight='bold', color='#7B341E')

    b_broker = patches.FancyBboxPatch((8.5, 4.3), 3.8, 0.9, boxstyle="round,pad=0.1", ec="#DD6B20", fc="#ED8936", lw=2)
    ax.add_patch(b_broker)
    ax.text(10.4, 4.75, "RabbitMQ Exchange (Topic)\n'carrental.events'", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF')

    b_cons = patches.FancyBboxPatch((7.8, 2.5), 5.2, 0.8, boxstyle="round,pad=0.1", ec="#276749", fc="#FFFFFF", lw=1.5)
    ax.add_patch(b_cons)
    ax.text(10.4, 2.9, "Consommateurs : Vehicle Srv / Notification", ha='center', va='center', fontsize=10, fontweight='bold', color='#276749')

    ax.annotate("Publication non-bloquante\n'reservation.confirmed'", xy=(10.4, 5.2), xytext=(10.4, 6.2),
                arrowprops=dict(arrowstyle="->", color="#DD6B20", lw=2),
                ha='center', fontsize=8.5, color="#C05621")

    ax.annotate("Consommation découplée (Queue)\n'vehicle.status.update'", xy=(10.4, 3.3), xytext=(10.4, 4.3),
                arrowprops=dict(arrowstyle="->", color="#DD6B20", lw=2),
                ha='center', fontsize=8.5, color="#C05621")

    ax.text(10.4, 1.4, "* Avantages : Découplage total, résilience garantie\n* Les messages patientent dans la queue si un service est éteint", 
            ha='center', va='center', fontsize=8.5, color="#9C4221")

    plt.tight_layout()
    plt.savefig(os.path.join(diagram_dir, "communication_sync_async.png"), dpi=300)
    plt.close()
    print("communication_sync_async.png created.")

generate_communication_sync_async()

# 5. Déploiement Docker
def generate_deploiement_docker():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, "Diagramme de Déploiement Conteneurisé - Docker & Docker Compose", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1A365D')

    r_host = patches.FancyBboxPatch((0.5, 0.5), 13.0, 8.5, boxstyle="round,pad=0.2", ec="#2B6CB0", fc="#F7FAFC", lw=2.5)
    ax.add_patch(r_host)
    ax.text(7, 8.6, "HÔTE DOCKER (Réseau Virtuel Bridge : carrental-network)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#2B6CB0')

    tier1 = [
        ("Nginx (Angular 17)\nPort: 4200:80", 1.0, 6.6, "#2B6CB0"),
        ("Spring Cloud Gateway\nPort: 8080:8080", 4.3, 6.6, "#C53030"),
        ("Eureka Server\nPort: 8761:8761", 7.6, 6.6, "#D69E2E"),
        ("RabbitMQ Broker\nPorts: 5672/15672", 10.9, 6.6, "#DD6B20")
    ]
    for name, x, y, col in tier1:
        b = patches.FancyBboxPatch((x, y), 2.2, 1.2, boxstyle="round,pad=0.1", ec=col, fc="#FFFFFF", lw=1.5)
        ax.add_patch(b)
        ax.text(x+1.1, y+0.6, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=col)

    tier2 = [
        ("User Service\n:8081", 0.8, 4.2, "#2C5282"),
        ("Vehicle Service\n:8082", 2.9, 4.2, "#276749"),
        ("Reservation Srv\n:8083", 5.0, 4.2, "#7B341E"),
        ("Payment Service\n:8084", 7.1, 4.2, "#6B46C1"),
        ("Agency Service\n:8085", 9.2, 4.2, "#285E61"),
        ("Review Service\n:8086", 11.3, 4.2, "#744210")
    ]
    for name, x, y, col in tier2:
        b = patches.FancyBboxPatch((x, y), 1.9, 1.1, boxstyle="round,pad=0.1", ec=col, fc="#FFFFFF", lw=1.5)
        ax.add_patch(b)
        ax.text(x+0.95, y+0.55, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=col)

    tier3 = [
        ("Postgres\nuser_db:5432", 0.8, 1.5, "#2C5282"),
        ("Postgres\nveh_db:5433", 2.9, 1.5, "#276749"),
        ("Postgres\nres_db:5434", 5.0, 1.5, "#7B341E"),
        ("Postgres\npay_db:5435", 7.1, 1.5, "#6B46C1"),
        ("Postgres\nagn_db:5436", 9.2, 1.5, "#285E61"),
        ("MongoDB\nrev_db:27017", 11.3, 1.5, "#744210")
    ]
    for name, x, y, col in tier3:
        b = patches.FancyBboxPatch((x, y), 1.9, 1.1, boxstyle="square,pad=0.1", ec=col, fc="#EDF2F7", lw=1.5, ls="--")
        ax.add_patch(b)
        ax.text(x+0.95, y+0.55, name, ha='center', va='center', fontsize=8, fontweight='bold', color=col)
        ax.annotate("", xy=(x+0.95, y+1.1), xytext=(x+0.95, 4.2), arrowprops=dict(arrowstyle="<->", color=col, lw=1.2))

    plt.tight_layout()
    plt.savefig(os.path.join(diagram_dir, "deploiement_docker.png"), dpi=300)
    plt.close()
    print("deploiement_docker.png created.")

generate_deploiement_docker()
