# Case Study: Skalowanie bazy danych przy nieprzewidywalnym ruchu (Aurora Serverless v2)

## Problem Architektoniczny
Aplikacja e-commerce doświadcza gwałtownych, skokowych wzrostów ruchu podczas kampanii promocyjnych (Flash Sales). Tradycyjna baza relacyjna (RDS Provisioned) albo marnuje zasoby przez 90% czasu (nadwymiarowanie), albo blokuje się z powodu wyczerpania połączeń i pamięci RAM (*Connection Exhaustion / Out of Memory*). Ręczne skalowanie instancji EC2/RDS pod obciążeniem trwa zbyt długo.

## Analiza i Dekonstrukcja (Reverse Engineering)
* **Wąskie gardło stałego rozmiaru:** Sztywne przypisanie klasy instancji RDS uniemożliwia elastyczne dostosowanie CPU/RAM w czasie rzeczywistym.
* **Ograniczenia Aurora Serverless v1:** Wolne skalowanie (zajmujące minuty) oraz brak wsparcia dla zaawansowanych funkcji pisania/odczytu w starszej wersji.

## Rozwiązanie Architektoniczne (To-Be)
1. **Wdrożenie Amazon Aurora Serverless v2:**
   * Konfiguracja puli ACU (Aurora Capacity Units), która potrafi skalować moc obliczeniową i pamięć **w ułamku sekundy (w górę i w dół)** w zależności od bieżącego obciążenia.
2. **Global Database + Read Scalability:**
   * Połączenie z punktami odczytu (Reader Endpoints), które automatycznie rozkładają ruch zapytań `SELECT` na repliki, podczas gdy zapisy trafiają do instancji głównej.
3. **Połączenie z Lambda / API Gateway:**
   * Architektura bezstanowa po stronie backendu, gdzie pule połączeń są zarządzane efektywnie przez RDS Proxy, chroniąc bazę przed zalaniem zbyt dużą liczbą jednoczesnych zapytań.

## Kluczowe Wnioski pod SAA-C03
* Aurora Serverless v2 automatycznie skaluje się na poziomie pojedynczych ACU, eliminując potrzebę ręcznego planowania pojemności (*Capacity Planning*).
* RDS Proxy jest kluczowym elementem przy architekturze Serverless/Lambda, ponieważ zarządza pulą połączeń do bazy i zapobiega jej przeciążeniu.
