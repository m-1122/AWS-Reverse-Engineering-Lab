# Case Study: Architektura Podsieci Prywatnych i Wychodzenie do Internetu (NAT)

## Problem Architektoniczny
Instancja EC2 lub baza danych RDS umieszczona w **podsieci prywatnej** nie ma dostępu do internetu (np. nie może pobrać aktualizacji systemowych), mimo że sieć posiada Internet Gateway. Ponadto bezpośredni ruch z zewnątrz do zasobów w podsieci prywatnej musi być zablokowany ze względów bezpieczeństwa.

## Rozwiązanie: NAT Gateway

1. **Lokalizacja komponentu:**
   - NAT Gateway musi zostać wdrożony w **podsieci publicznej**, która ma bezpośrednią ścieżkę do `igw-xxxx` (Internet Gateway).

2. **Konfiguracja Route Table (Tabela routingu podsieci prywatnej):**
   - Aby zasoby z prywatnej podsieci mogły wyjść na świat, ich tabela routingu musi wskazywać NAT Gateway jako cel dla ruchu globalnego:
     - Destination: `0.0.0.0/0`
     - Target: ID Twojego NAT Gateway (`nat-xxxxxxxx`)

3. **Zasada działania (Stateful Translation):**
   - Ruch wychodzący z bazy/aplikacji w sieci prywatnej trafia do NAT Gateway.
   - NAT zamienia prywatny adres IP na swój publiczny adres IP i wypuszcza pakiet przez Internet Gateway.
   - Odpowiedzi wracają do NAT Gateway, który bezpiecznie przekierowuje je z powrotem do wnętrza sieci prywatnej. Zewnętrzny świat widzi wyłącznie publiczne IP bramki NAT.
