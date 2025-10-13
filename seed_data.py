from repositories.organisation_repository import OrganisationRepository
from services.organisation_service import OrganisationService

DB_PATH = "organisations.db"

def seed_organisations():
    repository = OrganisationRepository(DB_PATH)
    service = OrganisationService(repository)
    
    sample_orgs = [
        {
            "name": "TechCorp Solutions",
            "details": "Leading provider of enterprise software solutions",
            "tags": ["technology", "enterprise", "software"],
            "url": "https://techcorp.example.com"
        },
        {
            "name": "Green Energy Co",
            "details": "Renewable energy and sustainability consulting",
            "tags": ["energy", "sustainability", "consulting"],
            "url": "https://greenenergy.example.com"
        },
        {
            "name": "HealthPlus Medical",
            "details": "Healthcare services and medical equipment supplier",
            "tags": ["healthcare", "medical", "equipment"],
            "url": "https://healthplus.example.com"
        },
        {
            "name": "EduTech Academy",
            "details": "Online learning platform for professional development",
            "tags": ["education", "e-learning", "professional"],
            "url": "https://edutech.example.com"
        },
        {
            "name": "FinanceHub Inc",
            "details": "Financial technology and payment processing solutions",
            "tags": ["fintech", "payments", "banking"],
            "url": "https://financehub.example.com"
        },
        {
            "name": "CloudNet Systems",
            "details": "Cloud infrastructure and hosting services",
            "tags": ["cloud", "infrastructure", "hosting"],
            "url": "https://cloudnet.example.com"
        },
        {
            "name": "FoodieExpress",
            "details": "Food delivery and restaurant management platform",
            "tags": ["food", "delivery", "restaurants"],
            "url": "https://foodieexpress.example.com"
        },
        {
            "name": "AutoDrive Motors",
            "details": "Automotive technology and electric vehicle manufacturer",
            "tags": ["automotive", "electric", "manufacturing"],
            "url": "https://autodrive.example.com"
        },
        {
            "name": "DataMinds Analytics",
            "details": "Big data analytics and business intelligence",
            "tags": ["data", "analytics", "AI"],
            "url": "https://dataminds.example.com"
        },
        {
            "name": "SecureVault Systems",
            "details": "Cybersecurity and data protection services",
            "tags": ["security", "cybersecurity", "protection"],
            "url": "https://securevault.example.com"
        },
        {
            "name": "TravelWise Agency",
            "details": "Travel booking and tourism management services",
            "tags": ["travel", "tourism", "booking"],
            "url": "https://travelwise.example.com"
        },
        {
            "name": "MediaPro Studios",
            "details": "Digital media production and content creation",
            "tags": ["media", "production", "content"],
            "url": "https://mediapro.example.com"
        }
    ]
    
    for org_data in sample_orgs:
        service.create_organisation(**org_data)
    
    print(f"Successfully seeded {len(sample_orgs)} organisations!")

if __name__ == "__main__":
    seed_organisations()
