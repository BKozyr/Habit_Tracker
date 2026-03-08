# 📈 Habit Tracker (Django)

Prosta i przejrzysta aplikacja do śledzenia nawyków.
Projekt powstał głównie jako poligon doświadczalny do nauki frameworka Django, optymalizacji zapytań do bazy danych (Django ORM) oraz integracji backendu z frontendowym kodem w JavaScript.

## 📸 Zrzuty ekranu
<img width="2879" height="1347" alt="image" src="https://github.com/user-attachments/assets/c8f7038e-0401-420b-b15b-97b39cd930ce" />
<img width="2106" height="1296" alt="image" src="https://github.com/user-attachments/assets/5fafe162-9675-456f-9354-2004c2b5617a" />


## ✨ Co potrafi aplikacja?

* **Wizualny Kalendarz (Heatmapa):** Dynamicznie generowany wykres kafelkowy. Dane o aktywności są pobierane w tle z API napisanego w Django REST Framework i renderowane przy użyciu biblioteki Cal-Heatmap (D3.js).
* **Elastyczne skalowanie:** Aplikacja automatycznie dostosowuje odcienie zieleni na wykresie. Rozumie różnicę między celem "1 trening", a "100 stron książki".
* **Szybkie odhaczanie (Quick Complete):** Przycisk, który automatycznie weryfikuje obecny postęp z danego dnia i jednym kliknięciem "dobija" wynik do wymaganego celu.
* **Passa (Streak):** Aplikacja na bieżąco wylicza, ile dni z rzędu udało się utrzymać dany nawyk.
* **Prywatność:** System logowania (autentykacji) – każdy użytkownik widzi i modyfikuje wyłącznie własne dane.

## 🛠️ Wykorzystane technologie

**Backend:**
* Python
* Django
* Django REST Framework (użyty do budowy endpointów dla wykresów)
* SQLite (baza danych)

**Frontend:**
* HTML & CSS
* Bootstrap 5 (do szybkiego, responsywnego ułożenia elementów)
* JavaScript (Vanilla)
* D3.js + Cal-Heatmap




