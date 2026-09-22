# Case Study: AWS IAM – Bezpieczny dostęp między kontami (Cross-Account Access)

## Problem Architektoniczny
Firma posiada dwa osobne konta AWS:
1. **Konto A (Produkcyjne):** Znajdują się tam krytyczne dane w wiadrze S3.
2. **Konto B (Analityczne):** Zespół analityków z tego konta potrzebuje regularnego dostępu do tych danych w celach raportowania.

Tradycyjne rozwiązanie w postaci tworzenia IAM Usera z hasłem i kluczami dostępu dla analityków na koncie produkcyjnym stwarza ogromne ryzyko bezpieczeństwa (wyciek danych, kradzież kluczy).

---

## Rozwiązanie: IAM Roles + STS (Security Token Service)

Zamiast tworzyć użytkowników międzykontynentalnie, wykorzystujemy **IAM Role** skonfigurowaną pod *Cross-Account Access*:

1. **Konfiguracja na Koncie A (Zasób):**
   * Tworzymy **IAM Role** z polityką zaufania (*Trust Policy*), która zezwala konkretnemu ID Konta B na wejście w tę rolę.
   * Do roli przypisujemy politykę uprawnień (*Permissions Policy*) zezwalającą wyłącznie na odczyt z wybranego S3 (`GetObject`, `ListBucket`).

2. **Działanie (AssumeRole):**
   * Analityk z Konta B loguje się na swoje konto i wykonuje żądanie przyjęcia roli (*AssumeRole*) za pośrednictwem AWS STS.
   * AWS generuje **tymczasowe, krótkotrwałe poświadczenia** (ważne np. przez godzinę), które automatycznie wygasają.

---

## Kluczowe Wnioski do Egzaminu (SAA-C03)
* **Złota zasada bezpieczeństwa AWS:** Nigdy nie twórz IAM Userów dla innych kont ani nie przekazuj statycznych `Access Keys` i `Secret Keys`. Zawsze używaj **IAM Roles** do Cross-Account Access.
* **Zasada najmniejszego uprzywilejowania (Least Privilege):** Nadawaj tylko takie uprawnienia, jakie są absolutnie niezbędne do wykonania zadania.
* **Instancje EC2:** Jeśli aplikacja na EC2 potrzebuje dostępu do S3 lub DynamoDB, **nigdy** nie zapisuj kluczy w kodzie ani plikach konfiguracyjnych – użyj przypisanej do EC2 **IAM Role (Instance Profile)**.
