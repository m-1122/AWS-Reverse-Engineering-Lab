# AWS SAA-C03 Ostateczna Lista Kontrolna (Cheat Sheet)

Kluczowe zagadnienia architektoniczne niezbędne do zdania egzaminu SAA-C03 oraz rozmów rekrutacyjnych z zakresu Cloud/SysAdmin.

---

## 1. Modele Disaster Recovery (DR) – Znamienne dla SAA-C03
Na egzaminie zawsze pytają o balans między **RTO (Recovery Time Objective)**, **RPO (Recovery Point Objective)** a **kosztami**:

1. **Backup and Restore (Najtańszy, najwyższe RTO/RPO):**
   * Dane są backupowane (S3, AWS Backup). W razie awarii infrastruktura jest stawiana od nowa z kopii. Długi czas przestoju.
2. **Pilot Light (Niski koszt, średnie RTO/RPO):**
   * Kluczowe elementy (np. baza danych jako replika) działają cały czas. Serwery aplikacyjne są wyłączone/skompresowane i uruchamiane dopiero w razie awarii.
3. **Warm Standby (Średni/wysoki koszt, niskie RTO/RPO):**
   * Okrojona wersja całego systemu działa w tle (np. mniejsze instancje EC2 na minimalnym ruchu). W przypadku awarii skala jest automatycznie zwiększana (ASG).
4. **Multi-Site Active/Active (Najwyższy koszt, RTO/RPO bliskie zeru):**
   * System działa w pełni w dwóch regionach jednocześnie. Ruch rozdzielany przez Route 53 (Latency / Failover routing).

---

## 2. Decoupling & Asynchroniczność (SQS, SNS, EventBridge)
Pytania o architekturę odporną na przeciążenia:
* **Amazon SQS (Simple Queue Service):**
  * Buforowanie żądań, decoupling mikroserwisów.
  * *Visibility Timeout:* Czas, przez który wiadomość jest niewidoczna dla innych workerów po jej pobraniu (zapobiega duplikacji przetwarzania).
  * *DLQ (Dead Letter Queue):* Kolejka na wiadomości, których worker nie potrafił przetworzyć po określonej liczbie prób.
* **Amazon SNS (Simple Notification Service):**
  * Model Pub/Sub (Publikuj i Subskrybuj) – jedna wiadomości trafia do wielu konsumentów (np. e-mail, Lambda, SQS).
* **Amazon EventBridge:**
  * Zaawansowany router zdarzeń oparty na zawartości (content-based filtering), idealny do integracji serverless i automatyzacji.

---

## 3. Caching & Performance
* **Amazon ElastiCache:**
  * **Redis:** Obsługuje złożone struktury danych, replikację (Multi-AZ), persistence (zapis na dysk). Idealny do sesji użytkowników i cache'u wymagającego trwałości.
  * **Memcached:** Prosty store typu klucz-wartość, wielowątkowy, brak persistencji i replikacji. Czysto ulotny cache pamięciowy.
* **DynamoDB Accelerator (DAX):**
  * In-memory cache dla bazy DynamoDB obniżający opóźnienia z milisekund do mikrosekund bez zmiany kodu aplikacji.
