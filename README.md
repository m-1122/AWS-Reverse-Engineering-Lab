# AWS Reverse Engineering Lab (SAA-C03)

Moje poligonowe laboratorium architektoniczne do nauki i przygotowania do certyfikatu AWS Solutions Architect Associate (SAA-C03). Zamiast suchej teorii – praktyczne case studies: problem, architektura, konfiguracja i wnioski.

## 📂 Struktura Repozytorium

- **`01-Networking-VPC/`** – Sieci, routing, NAT Gateway, VPC, trasy i rozwiązywanie problemów z łącznością.
- **`02-Compute-Scaling/`** – Instancje EC2, Load Balancery (ALB) i Auto Scaling.
- **`03-Databases/`** – Amazon RDS (Multi-AZ vs Read Replicas), DynamoDB.
- **`04-Storage-Backup/`** – S3, EBS, EFS.
- **`05-Security-IAM/`** – IAM Users, Roles, Policies, bezpieczeństwo chmury.

---

## ⚡ Kluczowe Wnioski i Pułapki Egzaminacyjne (SAA-C03 Cheat Sheet)

Poniżej znajdują się najważniejsze wzorce architektoniczne i rozróżnienia, które najczęściej pojawiają się na egzaminie:

### 1. Networking & VPC
* **NAT Gateway vs NAT Instance:**
  * **NAT Gateway:** Managed przez AWS, automatyczna skalowalność, wysoka dostępność (High Availability) w ramach jednej AZ (zalecane wdrażanie w wielu AZ dla odporności na awarie).
  * **NAT Instance:** Instancja EC2 zarządzana przez Ciebie (musisz wyłączyć *Source/Destination Check*, dbać o patching i reguły `iptables`). Tańsza, ale wymaga ręcznej konfiguracji failoveru.
* **VPC Peering vs Transit Gateway:**
  * **VPC Peering:** Połączenie 1:1 między dwiema VPC. **Brak routingu przechodniego (No transitive routing)** – jeśli VPC A ma peering z VPC B, a VPC B z VPC C, to VPC A nie ma połączenia z VPC C przez VPC B.
  * **Transit Gateway:** Centralny hub łączący wiele VPC oraz sieci on-premise (VPN / Direct Connect). Obsługuje routing przechodni.

### 2. Compute & Load Balancing
* **ALB vs NLB vs GWLB:**
  * **ALB (Application Load Balancer):** Warstwa 7 (HTTP/HTTPS). Routing oparty na ścieżkach (`/images/*`), nagłówkach, obsługa WebSockets i kontenerów (ECS/EKS).
  * **NLB (Network Load Balancer):** Warstwa 4 (TCP/UDP/TLS). Ultra-wysoka wydajność (miliony zapytań/s), niezwykle niskie opóźnienie, zachowuje oryginalne IP źródłowe klienta, stały adres IP (Static IP).
  * **GWLB (Gateway Load Balancer):** Warstwa 3 (IP). Służy do wdrażania wirtualnych urządzeń bezpieczeństwa (np. zapór sieciowych / firewalli firm trzecich) w trybie inline.
* **Auto Scaling Group (ASG):**
  * Okresy rozgrzewcze (*Warm-up periods*) chronią nowo uruchomione instancje przed zbyt szybkim ocenianiem przez metryki CloudWatch podczas rozruchu aplikacji.

### 3. Databases
* **Multi-AZ vs Read Replicas:**
  * **Multi-AZ (RDS):** Służy do **Wysokiej Dostępności (High Availability) i Disaster Recovery**. Synchronizacja danych odbywa się synchronicznie do repliki w innej strefie (automatyczny failover w razie awarii).
  * **Read Replicas:** Służą do **Skalowania Wydajności Odczytu (Read Performance)** dla zapytań `SELECT`. Replikacja jest asynchroniczna. Mogą znajdować się w tej samej strefie, innej strefie, a nawet w innym regionie.
* **Aurora Global Database:** Idealna do globalnych aplikacji – replikacja międzyregionowa z opóźnieniem poniżej sekundy i szybkim failoverem globalnym (RTO < 1 minuta).

### 4. Storage & Backup
* **S3 Storage Classes & Lifecycle:**
  * **Standard** -> **Standard-IA** (rzadszy dostęp, niższy koszt magazynowania, opłata za pobranie danych) -> **Glacier Instant / Flexible / Deep Archive** (archiwizacja, najniższy koszt).
  * **Intelligent-Tiering:** Automatyczne przenoszenie obiektów między warstwami bez opłat za transfer i bez narzutu operacyjnego – najlepsze rozwiązanie, gdy wzorzec dostępu do danych jest nieprzewidywalny.
* **AWS Backup:** Jednolite, centralne zarządzanie politykami tworzenia kopii zapasowych dla zasobów rozsianych po EC2, EBS, RDS, EFS i DynamoDB.

### 5. Security & IAM
* **IAM Roles + STS (Security Token Service):**
  * Najlepsza praktyka architektoniczna do udzielania dostępu między różnymi kontami AWS (**Cross-Account Access**) oraz federacji tożsamości. **Nigdy nie tworzymy IAM Userów z długoterminowymi kluczami dostępu na obcych kontach.**
* **Security Groups vs NACL (Network ACL):**
  * **Security Groups:** Działają na poziomie **instancji (ENI)**. Są **stanowe (stateful)** – ruch powrotny jest automatycznie dozwolony, niezależnie od reguł wyjściowych.
  * **NACL:** Działają na poziomie **podsieci (Subnet)**. Są **bezstanowe (stateless)** – musisz jawnie zdefiniować reguły zarówno dla ruchu przychodzącego (Inbound), jak i wychodzącego (Outbound).
