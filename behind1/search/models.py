from datetime import datetime
from behind1.database import db


class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(255))
    time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<SearchHistory {self.keyword} {self.time}>'