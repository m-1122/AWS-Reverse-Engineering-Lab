# Case Study: Globalne guardrails i governance w AWS Organizations (SCPs)

## Problem Architektoniczny
Firma posiada strukturę wielu kont w ramach **AWS Organizations**. Pojawia się problem z "samowolką" administratorów na poszczególnych kontach roboczych – użytkownicy z uprawnieniami `AdministratorAccess` wyłączają usługi logowania (CloudTrail) lub tworzą kosztowne instancje EC2 w nieautoryzowanych regionach geograficznych. Standardowe polityki IAM nie wystarczają, ponieważ administrator konta może je zmodyfikować.

## Analiza i Dekonstrukcja (Reverse Engineering)
* **Ograniczenia tradycyjnego IAM:** Polityki IAM działają w obrębie jednego konta. Administrator konta może przypisać sobie pełne prawa i obejść lokalne restrykcje.
* **Rola AWS Organizations:** Centralne zarządzanie kontami wymaga mechanizmu nadrzędnego (*Guardrails*), który wymusi polityki bezpieczeństwa niezależnie od woli lokalnych administratorów.

## Rozwiązanie Architektoniczne (To-Be)
1. **Wdrożenie Service Control Policies (SCPs):**
   * Przypisanie polityk kontroli usług na poziomie Jednostki Organizacyjnej (OU) lub całego Roota organizacji.
2. **Explicit Deny (Jawna odmowa):**
   * Użycie reguł `Deny` w SCP (np. zakaz wyłączania CloudTrail, zakaz tworzenia zasobów poza wybranymi regionami, np. `eu-central-1`).
3. **Dziedziczenie uprawnień:**
   * SCP nie przyznają żadnych uprawnień (*No permissions granted by default*), a jedynie określają **maksymalny limit (boundary)** tego, co użytkownicy i role (w tym Root) mogą wykonać na podległych kontach.

## Kluczowe Wnioski pod SAA-C03
* SCP (Service Control Policies) działają jako nadrzędne filtry w AWS Organizations – **Explicit Deny w SCP zawsze wygrywa** i blokuje akcję, nawet jeśli lokalna polityka IAM na to zezwala.
* SCP nie dotyczą konta głównego (Management Account) – działają na kontach członkowskich (Member Accounts) oraz podrzędnych OU.
