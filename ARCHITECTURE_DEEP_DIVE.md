AWS Reverse Engineering Lab — SAA-C03
Nie uczę się AWS przez bezmyślne klikanie. Widzę objaw, rozbieram architekturę na części, znajduję wąskie gardło i dobieram usługę, która usuwa konkretny problem. Na egzaminie nie pytam tylko: „Co robi ta usługa?”, ale przede wszystkim: „Jaki problem ona rozwiązuje i dlaczego pozostałe odpowiedzi są gorsze?”.

Jak z tego korzystam
Czytam jeden fragment na głos, zasłaniam tekst i odtwarzam go własnymi słowami. Samo ponowne czytanie daje mniej niż aktywne wydobywanie informacji z pamięci, a informacja zwrotna po odpowiedzi dodatkowo wzmacnia naukę.

Czytanie na głos pomaga zapamiętać treść, ale nie gwarantuje jej zrozumienia, dlatego po każdym fragmencie odpowiadam na pytanie „dlaczego?”. Powtarzam materiał w odstępach, na przykład po jednym, trzech, siedmiu, czternastu i trzydziestu dniach; badania wspierają łączenie testowania się z nauką rozłożoną w czasie.

Mój schemat myślenia
Kiedy czytam zadanie SAA-C03, najpierw wyszukuję słowa-klucze. „Wysoka dostępność” oznacza, że system ma przetrwać awarię. „Skalowanie” oznacza obsłużenie większego ruchu. „Najniższy koszt” oznacza, że nie wybieram najmocniejszej usługi, tylko najtańszą usługę spełniającą wymagania. „Najmniej pracy administracyjnej” kieruje mnie w stronę usługi zarządzanej.

Następnie zadaję sobie cztery pytania: co dokładnie się zepsuło, na której warstwie jest problem, jakie wymaganie jest najważniejsze i która odpowiedź realizuje je bez dokładania zbędnej złożoności. To jest moja inżynieria wsteczna: objaw → przyczyna → ograniczenie → rozwiązanie → kompromis.

Networking i VPC
Timeout do EC2
Widzę ERR_CONNECTION_TIMED_OUT do instancji EC2 z publicznym adresem IP. Nie zakładam od razu, że winna jest aplikacja. Idę po ścieżce pakietu: adres publiczny → tabela routingu → Internet Gateway → Security Group → NACL → usługa i port na EC2.

Najpierw sprawdzam, czy podsieć ma trasę 0.0.0.0/0 do Internet Gateway i czy brama jest podłączona do właściwego VPC. Potem sprawdzam Security Group, czyli zaporę stanową przy interfejsie sieciowym, oraz NACL, czyli bezstanową zaporę podsieci, w której trzeba uwzględnić oba kierunki ruchu.

Zdanie do zapamiętania: publiczny adres IP nie robi z podsieci publicznej; robi to trasa do Internet Gateway.

NAT Gateway
Widzę prywatną instancję, która ma pobierać aktualizacje z internetu, ale internet nie może inicjować połączeń do tej instancji. Myślę: NAT Gateway. Umieszczam go w publicznej podsieci, a w tabeli routingu prywatnej podsieci ustawiam 0.0.0.0/0 → NAT Gateway; publiczna podsieć NAT-u musi mieć trasę do Internet Gateway.

NAT Gateway jest zasobem strefowym, więc architektura odporna na awarię strefy używa NAT Gateway w każdej używanej AZ i kieruje prywatne podsieci do NAT-u w ich własnej AZ. Na egzaminie pamiętam prosty obraz: prywatna instancja wychodzi przez NAT, ale świat nie wchodzi przez NAT do instancji.

SG kontra NACL
Security Group działa przy ENI i jest stanowa: jeśli dopuściłem żądanie, odpowiedź może wrócić automatycznie. NACL działa na granicy podsieci i jest bezstanowa: reguły muszą pasować osobno do ruchu przychodzącego i wychodzącego.

Skrót pamięciowy: SG pamięta, NACL nie pamięta.

Compute i skalowanie
ALB, NLB i GWLB
Jeśli zadanie mówi o HTTP, HTTPS, hostach, nagłówkach albo ścieżkach takich jak /api, wybieram ALB, bo działa w warstwie 7. Jeśli liczy się TCP, UDP, TLS i bardzo wysoka wydajność warstwy transportowej, wybieram NLB, czyli warstwę 4. Jeśli ruch ma przechodzić przez wirtualne firewalle lub inne urządzenia bezpieczeństwa, wybieram GWLB, czyli warstwę 3.

Skrót pamięciowy: ALB rozumie aplikację, NLB przenosi połączenia, GWLB prowadzi ruch przez appliance bezpieczeństwa.

ALB i ASG
Widzę jedną instancję EC2 i od razu widzę dwa problemy: awaria jednej maszyny zatrzymuje aplikację, a nagły ruch ją przeciąża. Rozwiązaniem jest ALB przed aplikacją oraz Auto Scaling Group rozłożona na co najmniej dwie strefy dostępności.

ALB wysyła ruch tylko do zdrowych celów, a ASG utrzymuje zadaną liczbę instancji i skaluje flotę. Warm-up chroni nową instancję przed zbyt wczesną oceną przez politykę skalowania, bo aplikacja może jeszcze się uruchamiać.

EC2 Spot
Spot wybieram dla pracy odpornej na przerwanie: batch processing, CI/CD, analityka albo bezstanowe workery. Nie zapisuję ważnego stanu wyłącznie na instancji, bo EC2 może odzyskać pojemność; ostrzeżenie o przerwaniu zwykle daje do dwóch minut, ale aplikacja powinna działać poprawnie nawet bez skutecznego ostrzeżenia.[^13][^14]

Łączę różne typy instancji i różne AZ w ASG, włączam Capacity Rebalancing, dzielę zadania na małe części, a pracę trzymam w SQS. Gdy worker znika, ASG tworzy następcę, a niedokończone zadanie może zostać przetworzone ponownie.[^15][^13]

Zdanie do zapamiętania: Spot obniża koszt, ale odporność na przerwanie musi zapewnić architektura.

Bazy danych
Multi-AZ kontra Read Replica
Jeśli problemem jest awaria bazy albo całej AZ, wybieram RDS Multi-AZ. Primary replikuje synchronicznie do standby w innej AZ, a AWS wykonuje automatyczny failover; klasyczny standby nie służy do obsługi zwykłych zapytań odczytu.[^16][^17]

Jeśli problemem są tysiące zapytań SELECT, wybieram Read Replica. Replikacja jest asynchroniczna, replika może mieć opóźnienie i aplikacja musi jawnie kierować do niej odczyty.[^18][^16]

Skrót pamięciowy: Multi-AZ = availability, Read Replica = read scalability. Te mechanizmy można połączyć, bo baza Multi-AZ może mieć Read Replicas.[^16]

Aurora Serverless v2
Widzę nieprzewidywalne skoki ruchu i bazę, która przez większość czasu marnuje przydzieloną moc. Myślę o Aurora Serverless v2, gdzie writer i reader skalują pojemność w ACU, nawet w krokach po 0,5 ACU, zamiast wymagać ręcznej zmiany całej klasy instancji.[^19][^20]

Jeśli wiele funkcji Lambda otwiera krótkie połączenia do bazy, dokładam RDS Proxy. Proxy utrzymuje pulę połączeń, poprawia odporność i ogranicza presję wywieraną przez nagły napływ nowych połączeń.[^21]

Zdanie do zapamiętania: Aurora Serverless skaluje moc bazy, a RDS Proxy kontroluje połączenia do bazy.

S3 i backup
Klasy pamięci
Najpierw pytam, jak często dane są używane i jak szybko muszą wrócić. Dane gorące trafiają do S3 Standard. Dane rzadkie, ale potrzebne natychmiast, pasują do Standard-IA lub Glacier Instant Retrieval. Długoterminowe archiwum, którego nie trzeba odzyskać natychmiast, kieruję do Glacier Flexible Retrieval albo Deep Archive.

Jeśli wzorzec dostępu jest nieznany lub zmienny, wybieram S3 Intelligent-Tiering. Usługa monitoruje użycie i przenosi obiekty między warstwami dostępu; pobieranie z podstawowych warstw Intelligent-Tiering nie ma opłaty retrieval, ale obowiązuje mała opłata za monitoring i automatyzację.[^22][^23]

Jeśli znam cykl życia danych, ustawiam Lifecycle Policy: po określonym czasie przejście do tańszej klasy, a po zakończeniu retencji usunięcie. Lifecycle automatyzuje zarówno zmianę klasy, jak i wygaszanie obiektów.[^24][^25]

Zdanie do zapamiętania: znany wzorzec to Lifecycle, nieznany wzorzec to Intelligent-Tiering.

Cross-Region Replication
Widzę wymaganie kopii w drugim regionie, compliance albo regionalnego DR. Wybieram S3 Cross-Region Replication, włączam Versioning na obu bucketach i daję usłudze właściwą rolę IAM.[^26][^27]

Live replication kopiuje nowe obiekty asynchronicznie. Obiekty istniejące sprzed utworzenia reguły obsługuję przez S3 Batch Replication. Jeżeli wymagany jest przewidywalny czas, S3 Replication Time Control zapewnia SLA dla 99,99% nowych obiektów replikowanych w ciągu 15 minut.[^28][^29][^30]

Zdanie do zapamiętania: CRR potrzebuje Versioning po obu stronach; stare obiekty potrzebują Batch Replication.

Security i IAM
Cross-account access
Widzę konto produkcyjne i drugie konto, które potrzebuje dostępu do wybranego zasobu. Nie tworzę długoterminowego użytkownika z kluczem na koncie produkcyjnym. Tworzę rolę z trust policy, ograniczam permissions policy zgodnie z least privilege, a użytkownik lub workload z drugiego konta wykonuje AssumeRole przez STS.[^31][^32]

STS wydaje krótkotrwałe poświadczenia, które wygasają. AWS zaleca preferowanie poświadczeń tymczasowych nad długoterminowymi kluczami, również dla ludzi i workloadów.[^33][^31]

Zdanie do zapamiętania: Trust policy mówi, kto może wejść w rolę; permissions policy mówi, co ta rola może zrobić.

Rola dla EC2
Jeśli aplikacja na EC2 potrzebuje S3 lub DynamoDB, nie zapisuję AccessKeyId i SecretAccessKey w kodzie, .env ani repozytorium. Przypisuję instancji IAM Role przez instance profile, a SDK pobiera poświadczenia tymczasowe.[^34][^33]

SCP
SCP to guardrail w AWS Organizations. Nie przyznaje uprawnień; wyznacza maksymalny zakres tego, na co mogą pozwolić polityki IAM w kontach członkowskich. Jawne Deny blokuje akcję nawet wtedy, gdy lokalna polityka IAM ją dopuszcza.[^35][^36]

SCP obejmuje konta członkowskie, włącznie z ich root userami, ale nie ogranicza użytkowników ani ról w management account.[^35]

Zdanie do zapamiętania: IAM daje pozwolenie, SCP stawia sufit.

Disaster Recovery
Najpierw rozdzielam dwa pojęcia. RTO mówi, jak długo usługa może być niedostępna. RPO mówi, ile najnowszych danych można utracić.[^37][^38]

Potem układam strategie od najtańszej i najwolniejszej do najdroższej i najszybszej:

Backup and Restore — przechowuję kopie, a środowisko odtwarzam po awarii.

Pilot Light — dane i rdzeń systemu czekają w drugim regionie, ale resztę trzeba uruchomić.

Warm Standby — pomniejszona, kompletna wersja systemu już działa i trzeba ją tylko skalować.

Multi-Region Active/Active — oba regiony aktywnie obsługują ruch, więc RTO i RPO mogą być bliskie zeru, ale rosną koszt i złożoność.[^39][^40]

Skrót pamięciowy: backup buduję, pilot uruchamiam, warm skaluję, active/active już działa.

Decoupling
Widzę producenta, który może zalać wolniejszego konsumenta. Wstawiam SQS, aby kolejka przyjęła skok ruchu i oddzieliła tempo obu elementów. Visibility Timeout ukrywa pobraną wiadomość na czas pracy, a DLQ przejmuje wiadomości, których nie udało się przetworzyć po ustalonej liczbie prób.

Jeśli jedna wiadomość ma trafić do wielu odbiorców, myślę o SNS i modelu pub/sub. Jeśli potrzebuję routingu zdarzeń według ich treści, integracji usług AWS lub automatyzacji reakcji na zdarzenia, myślę o EventBridge.

Skrót pamięciowy: SQS kolejkuje pracę, SNS rozsyła komunikat, EventBridge wybiera drogę zdarzenia.

Ostatnia minuta
Przed odpowiedzią powtarzam sobie:

Publiczna podsieć ma trasę do IGW; prywatna wychodzi przez NAT.

SG jest stateful; NACL jest stateless.

ALB to warstwa 7; NLB to warstwa 4; GWLB to warstwa 3.[^12]

ASG skaluje i odtwarza instancje; ALB rozdziela ruch.

Multi-AZ chroni dostępność; Read Replica skaluje odczyt.[^16]

Spot jest tani, ale przerywalny.[^14]

Lifecycle obsługuje znany cykl danych; Intelligent-Tiering zmienny wzorzec dostępu.[^25][^23]

CRR wymaga Versioning na obu bucketach.[^27]

IAM Role i STS dają dostęp tymczasowy; nie wkładam kluczy do kodu.[^31][^33]

SCP nie nadaje praw; ogranicza maksymalne prawa.[^35]

RTO to czas powrotu, a RPO to dopuszczalna utrata danych.[^38]

Test bez podglądania
EC2 ma publiczne IP, ale połączenie kończy się timeoutem. Jakie elementy sprawdzam po kolei?

Prywatna instancja ma pobierać aktualizacje, lecz nie może przyjmować połączeń z internetu. Czego potrzebuje?

Kiedy wybieram ALB, kiedy NLB, a kiedy GWLB?

Dlaczego pojedynczy worker Spot nie powinien przechowywać jedynej kopii stanu?

Czym różni się cel Multi-AZ od celu Read Replica?

Co rozwiązuje Aurora Serverless v2, a co rozwiązuje RDS Proxy?

Kiedy wybieram Lifecycle, a kiedy Intelligent-Tiering?

Jak replikuję obiekty istniejące przed uruchomieniem CRR?

Czym różni się trust policy od permissions policy?

Dlaczego SCP nie zastępuje polityki IAM?

Jaka jest różnica między RTO i RPO?

Która strategia DR wymaga po awarii budowania, która uruchamiania, która skalowania, a która działa od razu?

Jeśli odpowiedź nie wychodzi bez patrzenia, nie czytam całej notatki ponownie. Odsłaniam tylko brakujący fragment, zamykam go i od razu odpowiadam jeszcze raz. To zamienia README z tekstu do oglądania w trening aktywnego przypominania
