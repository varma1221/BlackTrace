from app.database.connection import SessionLocal

def get_db():
    db = SessionLocal() #Open Connection
    
    try:
        yield db #Request happens
        
    finally:
        db.close() #Close Connection
