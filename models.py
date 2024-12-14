from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CustomerData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(50), nullable=False)
    car_code = db.Column(db.String(20), nullable=False)
    pickup_time = db.Column(db.DateTime, nullable=False)
    received = db.Column(db.Boolean, default=False)
    parking_position = db.Column(db.String(10), nullable=False, default='A1')

    def to_dict(self):
        return {
            'id': self.id,
            'Biển số xe': self.license_plate,
            'Mã số gửi xe': self.car_code,
            'Thời gian lấy xe': self.pickup_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Đã nhận xe': self.received,
            'Vị trí đỗ': self.parking_position
        }
