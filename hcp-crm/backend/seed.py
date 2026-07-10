"""
Seed script — creates a demo admin user, hospital, doctor, and product so
the app has data to show immediately after setup.

Run with: python seed.py
"""
from app.db.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.hospital import Hospital
from app.models.doctor import Doctor
from app.models.product import Product
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if not db.query(User).filter(User.email == "admin@hcpcrm.com").first():
    admin = User(
        full_name="Admin User",
        email="admin@hcpcrm.com",
        hashed_password=hash_password("Admin@123"),
        role=UserRole.ADMIN,
    )
    db.add(admin)

hospital = db.query(Hospital).filter(Hospital.name == "Apollo Hospital").first()
if not hospital:
    hospital = Hospital(name="Apollo Hospital", city="Jaipur")
    db.add(hospital)
    db.commit()
    db.refresh(hospital)

if not db.query(Doctor).filter(Doctor.name == "Dr. Sharma").first():
    db.add(Doctor(name="Dr. Sharma", specialization="Endocrinology", city="Jaipur", hospital_id=hospital.id))

if not db.query(Product).filter(Product.name == "Glucomet").first():
    db.add(Product(name="Glucomet", category="Diabetes"))

db.commit()
db.close()
print("Seed complete. Login with admin@hcpcrm.com / Admin@123")
