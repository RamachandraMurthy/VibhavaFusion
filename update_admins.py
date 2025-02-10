from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        user.is_admin = True
    db.session.commit()
    print(f"Updated {len(users)} users to admin status.") 