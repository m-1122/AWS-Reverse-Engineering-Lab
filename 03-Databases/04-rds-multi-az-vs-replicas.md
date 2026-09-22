# Case Study: Amazon RDS – Multi-AZ kontra Read Replicas

## Problem Architektoniczny
Aplikacja oparta na relacyjnej bazie danych (np. MySQL) zmaga się z dwoma problemami:
1. **Awaria sprzętowa (SPOF):** Jeśli serwer bazy danych w jednej serwerowni ulegnie awarii, cała aplikacja przestaje działać.
2. **Wydajność odczytu:** Tysiące użytkowników jednocześnie wysyła zapytania `SELECT`, co obciąża główną bazę danych i opóźnia operacje zapisu (`INSERT`/`UPDATE`).

---

## Rozwiązanie: Dwa różne mechanizmy do różnych celów

### 1. RDS Multi-AZ (Cel: Wysoka Dostępność / High Availability)
* **Jak działa:** AWS utrzymuje główną bazę (*Primary*) w jednej Strefie Dostępności (AZ) oraz jej synchroniczną kopię (*Standby*) w innej AZ. Każdy zapis jest natychmiast replikowany.
* **Failover:** W przypadku awarii głównej bazy, AWS automatycznie przekierowuje ruch na kopię zapasową (*Standby*). 
* **Zastosowanie:** Bezpieczeństwo i ochrona przed awarią fizycznej infrastruktury.

### 2. RDS Read Replicas (Cel: Skalowalność odczytu / Performance)
* **Jak działa:** Tworzysz do 15 asynchronicznych kopii bazy danych (*Read Replicas*). Cały ruch typu `SELECT` kierujesz na repliki, odciążając bazę główną, która obsługuje tylko zapisy.
* **Zastosowanie:** Skalowanie aplikacji przy dużym ruchu odczytującym.

---

## Kluczowe Wnioski do Egzaminu (SAA-C03)
* Chcesz **odporności na awarię**? $\rightarrow$ Wybierasz **Multi-AZ**.
* Chcesz **przyspieszyć zapytania odczytu**? $\rightarrow$ Wybierasz **Read Replicas**.
* Możesz połączyć oba rozwiązania: mieć bazę główną w trybie Multi-AZ, która posiada własne Read Replicas.
