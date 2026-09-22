# Case Study: Wysoka Dostępność (High Availability) i Skalowalność w AWS

## Problem
Aplikacja oparta na pojedynczej instancji EC2 jest podatna na awarie sprzętowe (Single Point of Failure) oraz nie radzi sobie z nagłymi skokami ruchu użytkowników.

## Rozwiązanie Architektoniczne
Połączenie **Application Load Balancer (ALB)** oraz **Auto Scaling Group (ASG)** rozproszonych w wielu Stazach Dostępności (Multi-AZ).

### Komponenty:
1. **ALB (Application Load Balancer):** 
   - Działa w warstwie 7 (HTTP/HTTPS).
   - Punkt wejścia dla ruchu, wykonuje kontrole stanu (*Health Checks*).
2. **ASG (Auto Scaling Group):**
   - Automatycznie skaluje liczbę instancji w górę lub w dół na podstawie zdefiniowanych metryk (np. CPU > 70%).
   - Wymusza Multi-AZ (odporność na awarię całego centrum danych).

## Kluczowe Wnioski do Egzaminu (SAA-C03)
- ALB rozdziela ruch na aplikacje (Layer 7), a Network Load Balancer (NLB) działa ultraszybko na warstwie 4 (TCP/UDP) przy milionach żądań na sekundę.
- ASG zawsze dba o minimalną, pożądaną liczbę maszyn i potrafi zastąpić uszkodzoną instancję w kilka minut.
