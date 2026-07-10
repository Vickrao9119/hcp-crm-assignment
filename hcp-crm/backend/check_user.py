from app.db.database import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()
print(f'Total users: {len(users)}')
for u in users:
    print(f'Email: {u.email}, Role: {u.role}')
db.close()
