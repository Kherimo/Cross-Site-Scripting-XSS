# xss_demo/website1.py
from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# --- Thông tin cấu hình DB mới ---
# Chúng ta sẽ không dùng app.config của Flask cho việc này nữa
db_config = {
    'host': 'localhost',
    'user': 'root',           # <-- Thay bằng user của bạn
    'password': '123456',     # <-- Thay bằng password của bạn
    'database': 'xss_demo'      # <-- Đảm bảo DB này đã tồn tại
}

# --- Hàm để tạo kết nối DB ---
def get_db_connection():
    """Tạo và trả về một đối tượng kết nối đến DB."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Lỗi khi kết nối đến MySQL: {e}")
        return None

# --- Hàm khởi tạo bảng (chạy một lần nếu cần) ---
def setup_database():
    """Hàm này tạo bảng 'comments' nếu nó chưa tồn tại."""
    conn = get_db_connection()
    if conn is None:
        print("Không thể kết nối đến DB để khởi tạo bảng.")
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            content TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Khởi tạo bảng 'comments' thành công (nếu chưa có).")


# --- Route cho trang chủ ---
@app.route('/')
def index():
    return render_template('index.html')


# --- Lỗ hổng 1: Stored XSS ---
@app.route('/stored', methods=['GET', 'POST'])
def stored_xss():
    conn = get_db_connection()
    if conn is None:
        return "Lỗi: Không thể kết nối đến cơ sở dữ liệu.", 500

    cursor = conn.cursor()
    
    try:
        if request.method == 'POST':
            comment = request.form['comment']
            # Tham số hóa query để tránh SQL Injection (dù không phải trọng tâm)
            cursor.execute("INSERT INTO comments(content) VALUES (%s)", (comment,))
            conn.commit()

        cursor.execute("SELECT content FROM comments")
        # Lấy tất cả kết quả
        comments = [row[0] for row in cursor.fetchall()]
    
    except Error as e:
        print(f"Lỗi truy vấn: {e}")
        comments = []
    
    finally:
        # Rất quan trọng: Luôn đóng cursor và connection
        cursor.close()
        conn.close()
        
    return render_template('stored.html', comments=comments)


# --- Lỗ hổng 2: Reflected XSS ---
@app.route('/reflected')
def reflected_xss():
    query = request.args.get('q', '')
    return render_template('reflected.html', query=query)

# --- Lỗ hổng 3: DOM-Based XSS ---
@app.route('/dom')
def dom_based_xss():
    return render_template('dom.html')

if __name__ == '__main__':
    # Chạy hàm khởi tạo DB một lần khi ứng dụng bắt đầu
    setup_database()
    # Chạy ứng dụng Flask
    app.run(port=5001, debug=True)