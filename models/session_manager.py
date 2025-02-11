from .db_setup import SessionLocal


class DataBaseSessionManager:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, traceback):
        if self.session:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
            self.session.close()
