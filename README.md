# Wymagania:


## Komponenty:

frontend (vanilla .js/jQuery/dowolny framework)
backend (PHP/node.js/inna technologia)
baza danych (mongoDB/mySQL/inna)


## Funkcjonalności:

możliwość zalogowania jako admin, który ma możliwość ingerowania w użytkowników,
możliwość rejestracji użytkownika i późniejsze zalogowanie na konto,
użycie Cookies (np. mechanizm sesji),
manipulacja danymi (musi pojawić się jakiś CRUD poza operacjami na użytkownikach),
dane zapisywane w bazie,
mechanizmy zabezpieczeń aplikacji internetowych (np. CORS)


obsługa błędów
upiększanie
dodanie zarządzanie profilem przez użytkownika
logging on server


Jakie zabezpieczenia ma aplikacja:
- code injection (Szablony Jinja2)
- podział na role (admin, zalogowany, niezalogowany)
- ograniczanie dostępu do widoków aplikacji
- zapobieganie SQL-injection (SQLAlchemy)
- ochrona CSRF (Flask-WTF)
- zapobieganie wprowadzaniu skryptów XSS (Flask-WTF)
- zapobieganie ataką brute-force (Flask-Limiter)
- zapobieganie nadmiernym obciążeniem (DoS) - Flask-Limiter
- wymuszenie nagłówków HTTPS (Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) - Talisman
- silna ochrona nagłówków HTTP (Talisman)
