# Case Study: Odporna architektura na bazie EC2 Spot Instances

## Problem Architektoniczny
Firma uruchamia ciężkie obliczenia analityczne, które generują ogromne koszty na standardowych instancjach EC2 On-Demand. Zarząd wymusił cięcie budżetu chmurowego o 70%, ale system musi być odporny na nagłe wywłaszczenie instancji (*Spot Interruption*) przez AWS.

## Analiza i Dekonstrukcja (Reverse Engineering)
* **Wyzwanie Spot:** AWS może odebrać instancję Spot dając zaledwie 2-minutowe ostrzeżenie.
* **Błąd wdrożeniowy:** Używanie pojedynczych instancji Spot do zadań ciągłych bez mechanizmów automatycznego odtwarzania stanu.

## Rozwiązanie Architektoniczne (To-Be)
1. **Auto Scaling Group (ASG) z wieloma typami instancji (Mixed Instances Policy):**
   * Zdefiniowanie puli różnych typów instancji (np. `c5.xlarge`, `c6i.xlarge`, `m5.xlarge`) w różnych strefach (Multi-AZ), codrastycznie zmniejsza szansę na brak zasobów u dostawcy.
2. **Wykorzystanie Spot Interruption Notices (EventBridge):**
   * Skonfigurowanie powiadomienia EventBridge reagującego na sygnał o 2-minutowym ostrzeżeniu, które wyzwala skrypt grace-shuttling / zapis stanu bazy na S3 przed zamknięciem maszyny.
3. **Stateless Workloads:**
   * Architektura bezstanowa – zadania są dzielone na mniejsze paczki i kolejkowane w SQS. Jeśli instancja padnie, wiadomość wraca do kolejki, a inna instancja podejmuje pracę.

## Kluczowe Wnioski pod SAA-C03
* Instancje Spot są idealne do zadań odpornych na przerwę (Batch processing, CI/CD, Big Data, kontenery bezstanowe).
* ASG automatycznie dba o dywersyfikację i zastępowanie wywłaszczonych instancji w ramach zdefiniowanej puli.
