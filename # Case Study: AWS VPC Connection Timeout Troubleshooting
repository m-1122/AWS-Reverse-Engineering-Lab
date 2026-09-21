# Case Study: AWS VPC Connection Timeout Troubleshooting

## Opis problemu (The Incident)
Wystąpienie błędu `ERR_CONNECTION_TIMED_OUT` podczas próby połączenia z instancją EC2 wystawioną w publicznym podsieci customowego VPC, mimo posiadania publicznego adresu IP.

## Święta Trójca Diagnostyki Sieciowej (Root Cause Checklist)

1. **Route Table (Tabela routingu)**
   - *Problem:* Podsieć nie ma zdefiniowanej trasy wyjściowej do świata.
   - *Fix:* Sprawdź, czy przypisana tabela routingu zawiera wpis:
     - Destination: `0.0.0.0/0`
     - Target: ID Twojego Internet Gateway (`igw-xxxxxxxx`)

2. **Internet Gateway (IGW)**
   - *Problem:* Bramka internetowa istnieje, ale nie jest podpięta do VPC.
   - *Fix:* Zweryfikuj status IGW w konsoli. Musi mieć status `Attached` do konkretnego `app-vpc`.

3. **Firewall (Security Groups & NACL)**
   - *Problem:* Ruch jest blokowany na poziomie zapory sieciowej.
   - *Fix:* 
     - Sprawdź reguły *Inbound* w **Security Group** przypisanej do EC2 (musi przepuszczać port 80/443 z `0.0.0.0/0`).
     - Pamiętaj: Security Groups są **stanowe (Stateful)**, więc ruch powrotny obsługiwany jest automatycznie. W przypadku NACL (bezstanowych) musisz pamiętać o portach efemerycznych na wyjściu.
