# Case Study: Globalny Disaster Recovery i Compliance z S3 Cross-Region Replication (CRR)

## Problem Architektoniczny
Firma finansowa musi spełnić rygorystyczne wymagania prawne (Compliance), które nakazują przechowywanie kopii wrażliwych dokumentów w oddalonym geograficznie regionie AWS (oddalonym o ponad 500 mil) na wypadek awarii całego regionu podstawowego. Dodatkowo system musi zapewniać niski czas odzyskiwania danych (RPO bliskie zeru).

## Analiza i Dekonstrukcja (Reverse Engineering)
* **Wymaganie wersjonowania:** S3 Cross-Region Replication (CRR) **wymaga włączenia wersjonowania (Versioning)** zarówno na kubełku źródłowym, jak i docelowym.
* **Błąd konfiguracji:** Próba ustawienia replikacji bez IAM Role z odpowiednimi uprawnieniami do zapisywania w obcym regionie.

## Rozwiązanie Architektoniczne (To-Be)
1. **Włączenie Versioning na obu kubełkach:**
   * Zabezpieczenie przed przypadkowym nadpisaniem lub usunięciem obiektów (Delete Markers mogą być replikowane opcjonalnie).
2. **Konfiguracja S3 Cross-Region Replication (CRR):**
   * Automatyczne, asynchroniczne kopiowanie nowych obiektów z Regionu A (np. `eu-central-1` Frankfurt) do Regionu B (np. `eu-west-1` Irlandia).
3. **S3 Replication Time Control (S3 RTC):**
   * Dla danych o krytycznym znaczeniu biznesowym wdrożenie S3 RTC, które gwarantuje replikację 99.99% obiektów w ciągu 15 minut wraz ze specjalnym SLA.

## Kluczowe Wnioski pod SAA-C03
* S3 CRR wymaga włączonego wersjonowania na obu kubełkach.
* Replikacja dotyczy **nowych** obiektów tworzonych po skonfigurowaniu reguły (istniejące wcześniej pliki wymagają migracji za pomocą S3 Batch Replication).
* Do replikacji obiektów szyfrowanych kluczami niestandardowymi KMS wymagana jest specjalna konfiguracja uprawnień (KMS Key Policy).
