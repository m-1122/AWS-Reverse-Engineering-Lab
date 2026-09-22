# Case Study: Amazon S3 – Optymalizacja Kosztów i Klasy Pamięci (Storage Classes)

## Problem Architektoniczny
Firma generuje terabajty danych (logi aplikacji, backupy, multimedia). Dane te są intensywnie używane przez pierwsze 30 dni, a potem rzadko lub wcale. Jednak z powodów prawnych (*compliance*) muszą być przechowywane nawet przez 5 lat. Trzymanie wszystkiego w drogiej klasie S3 Standard generuje gigantyczne, niepotrzebne koszty.

---

## Rozwiązanie: S3 Storage Classes + Lifecycle Policies

### 1. Kluczowe Klasy Pamięci S3 (Złoto z SAA-C03)
* **S3 Standard:** Najwyższa dostępność (99.999999999% trwałości - *11 nines*), najdroższy odczyt/zapis. Do danych często używanych ("hot data").
* **S3 Standard-IA (Infrequent Access):** Dla danych rzadziej używanych, ale wymagających natychmiastowego dostępu w milisekundach. Tańszy storage, ale płacisz za każdy gigabit pobranych danych.
* **S3 Glacier Instant Retrieval:** Archiwum, ale z dostępem w milisekundach (dobre na rzadko oglądane zdjęcia).
* **S3 Glacier Flexible Retrieval:** Archiwum z dostępem w kilka minut lub godzin (Standard: 3-5 godzin, Bulk: 5-12 godzin za grosze).
* **S3 Glacier Deep Archive:** Najtańsza opcja na rynku do trzymania backupów przez lata. Czas odzyskania danych: do 12 godzin.

### 2. Automatyzacja za pomocą Lifecycle Rules
Zamiast ręcznie przenosić pliki, konfigurujemy **S3 Lifecycle Policy**, która automatycznie:
* Po 30 dniach przenosi pliki z *S3 Standard* do *Standard-IA*.
* Po 90 dniach przerzuca je do *Glacier Flexible*.
* Po 365 dniach archiwizuje w *Glacier Deep Archive*.
* Po 5 latach automatycznie kasuje pliki (*Expiration*).

---

## Kluczowe Wnioski do Egzaminu (SAA-C03)
* S3 ma gwarantowaną trwałość danych na poziomie **11 dziewiątek** (99.999999999%) i jest rozproszone na minimum 3 Strefy Dostępności (AZ).
* Jeśli pytają o **najtańszą opcję archiwizacji długoterminowej** (np. backupy trzymane latami) $\rightarrow$ **S3 Glacier Deep Archive**.
* Jeśli pytają o dane rzadko używane, ale wymagające **natychmiastowego dostępu** (milisekundy) $\rightarrow$ **Standard-IA** lub **Glacier Instant Retrieval**.
