from flask import Flask, jsonify, request, render_template
from models import db, CustomerData
from datetime import datetime

app = Flask(__name__)

# Cấu hình SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo SQLAlchemy
db.init_app(app)

# Tạo bảng nếu chưa có
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

# API để thêm dữ liệu từ form
@app.route('/submit', methods=['POST'])
def submit():
    # Lấy dữ liệu từ request
    license_plate = request.form.get('license_plate')
    car_code = request.form.get('car_code')
    pickup_time = request.form.get('pickup_time')

    # Chuyển đổi pickup_time từ string sang datetime
    pickup_time = datetime.strptime(pickup_time, '%Y-%m-%dT%H:%M')

    # Tạo một bản ghi mới
    customer = CustomerData(
        license_plate=license_plate,
        car_code=car_code,
        pickup_time=pickup_time,
        parking_position='A1'  # Vị trí mặc định
    )
    db.session.add(customer)
    db.session.commit()

    message = 'Dữ liệu đã được lưu'
    return render_template('index.html', message=message)

# API để lấy danh sách dữ liệu
@app.route('/get-data', methods=['GET'])
def get_data():
    customers = CustomerData.query.all()
    return jsonify([customer.to_dict() for customer in customers])

# API để cập nhật trạng thái xe đã nhận
@app.route('/update-status/<int:customer_id>', methods=['PATCH'])
def update_status(customer_id):
    customer = CustomerData.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Không tìm thấy dữ liệu với ID này!'}), 404

    customer.received = True
    db.session.commit()
    return jsonify({'message': 'Cập nhật trạng thái thành công!', 'data': customer.to_dict()}), 200


if __name__ == "__main__":
    app.run(debug=True)
