# Energy Community MultiAgent Approach

Simulare multi-agent a unei comunități energetice formate din locuințe cu panouri fotovoltaice, construită cu Mesa și date reale de consum și radiație solară.

---

## Descriere

O comunitate energetică este un grup de locuințe care produc și consumă energie electrică local, de regulă din surse regenerabile. Proiectul modelează un astfel de grup: fiecare locuință are un istoric real de consum orar și o producție fotovoltaică estimată din date de radiație solară, iar un agent manager trimite periodic recomandări de comportament (menținere, creștere sau reducere a consumului la un moment dat).

Simularea măsoară efectul acestor recomandări asupra a doi indicatori standard din literatura de specialitate:

- **rata de autoconsum (self-consumption)**, cât din producția fotovoltaică este folosită direct de locuință;
- **rata de autosuficiență (self-sufficiency)**, cât din consumul locuinței este acoperit de propria producție.

Pe lângă comportamentul locuinței, proiectul evaluează și partea economică: cât ar putea economisi comunitatea prin schimbarea furnizorului de energie, comparând ofertele reale de preț și procent de energie regenerabilă preluate de pe platforma românească de comparare a furnizorilor, posf.ro.

## Caracteristici principale

### Simulare multi-agent cu Mesa
- **Trei tipuri de agenți-locuință**, `IDEAL`, `ENTHUSIASTIC`, `NON_ENTHUSIASTIC`, care diferă prin probabilitatea de a urma o recomandare (1.0, 0.7, respectiv 0.3)
- **Un agent manager** care emite, la fiecare pas, o recomandare per locuință pe baza consumului curent față de media consumului din ultima săptămână
- **Rulare paralelă** a tuturor combinațiilor dintre cele 3 tipuri de agenți și dimensiunile de comunitate 1, 5, 10, 15, 20, 23 locuințe (18 scenarii în total), cu `multiprocessing.Pool` (`AgentModel/parallel_simulation.py`)

### Pipeline de procesare a datelor
- Curățare a anomaliilor de consum cu `IsolationForest` și winsorizare
- Estimare a producției fotovoltaice pornind de la radiația solară măsurată
- Detectare a intervalelor de funcționare a electrocasnicelor prin clusterizare KMeans pe două niveluri, cu prag stabilit din valori trecute printr-o funcție sigmoidă

### Analiză economică și de furnizori
- Extragere automată a ofertelor de preț și a procentului de energie regenerabilă de pe posf.ro
- Alegere aleatorie a unui furnizor din ofertele extrase, folosit drept furnizor curent simulat al comunității pentru fiecare rulare, deoarece proiectul nu are acces la furnizorul real al locuințelor din setul de date
- Determinare a celor mai bune 5 oferte alternative față de acest furnizor simulat, mai ieftine și cel puțin la fel de regenerabile
- Detectare a zonei geografice curente printr-un API de geolocalizare, pentru a raporta prețul relevant local

### Analiză a tiparelor de recomandare
- Determinare a procentului de momente în care se emite o recomandare, per locuință, per oră a zilei și per electrocasnic (`RecommendationModel/recommendation_analytics.py`)
- Distincție zi/noapte (noapte definită ca intervalul 22:00–6:59) folosită atât pentru distribuția recomandărilor pe ore, cât și pentru consumul mediu pe electrocasnic (`HelperFiles/hours_for_day_and_night.py`, reutilizat în patru module)
- Aceste analize există ca funcționalitate separată, apelabilă prin `RecommendationFacade`, dar nu sunt încă invocate din fluxul curent al `main.py`

### Analiză de rezultate
- Grafice de autoconsum, autosuficiență și economii monetare per scenariu
- Frontieră Pareto (autoconsum versus autosuficiență) calculată cu biblioteca `paretoset`, pentru a identifica cele mai bune combinații de scenarii
- Clasament al locuințelor cel mai puternic afectate de recomandări, pe categorii de dimensiune a comunității

## Arhitectură

Codul este organizat pe module de domeniu (`HouseModel`, `SolarRadiationModel`, `PowerEstimatedModel`, `SelfConsumptionModel`, `SelfSufficiencyModel`, `HouseWithAppliancesModel`, `RecommendationModel`), fiecare urmând aceeași structură internă:

- **Builder** (`*_builder.py`), citește un CSV și construiește obiectele de domeniu. Builderele formează un lanț de moștenire care oglindește pipeline-ul de procesare: `PowerEstimatedBuilder` extinde `SolarRadiationHouseBuilder`, care extinde `HouseBuilder`.
- **Facade** (`*_facade.py`), oferă un singur punct de intrare (`process_*_pipeline`) care înlănțuie construirea, preprocesarea, reeșantionarea și plotarea. `main.py` interacționează doar cu fațade, nu direct cu clasele interne.
- **Attribute adder** (`*_attribute_adder.py`), aplică formula template method din `HelperFiles/base_class_for_adding_attributes_to_house_objects.py` pentru a atașa un atribut calculat (autoconsum, autosuficiență, producție estimată) pe obiectele `House` deja construite.
- **Plotter**, moștenește `HelperFiles/base_plotter_interface.py` pentru a reutiliza logica de filtrare pe interval de timp în toate graficele.

Obiectele de domeniu formează la rândul lor o ierarhie de clase: `House` → `SolarRadiationHouse` → `PowerEstimator` → `SelfConsumption` → `SelfSufficiency`, fiecare nivel adăugând un singur atribut și metoda `determine_*` corespunzătoare.

### Structura proiectului

```
Energy-Community-MultiAgent-Approach/
├── AgentModel/                    # Simularea multi-agent (Mesa)
│   ├── house_agent.py             # Comportamentul unei locuințe
│   ├── manager_agent.py           # Logica de recomandare
│   ├── agent_types.py             # IDEAL / ENTHUSIASTIC / NON_ENTHUSIASTIC
│   ├── house_model.py             # Modelul Mesa (schedule, step)
│   ├── parallel_simulation.py     # Orchestrarea scenariilor în paralel
│   ├── agent_plots.py             # Grafice, inclusiv frontiera Pareto
│   └── ...
├── HouseModel/                    # Încărcare și preprocesare consum locuințe
├── SolarRadiationModel/           # Date de radiație solară
├── PowerEstimatedModel/           # Estimarea producției fotovoltaice
├── SelfConsumptionModel/          # Calculul ratei de autoconsum
├── SelfSufficiencyModel/          # Calculul ratei de autosuficiență
├── HouseWithAppliancesModel/      # Consum defalcat pe electrocasnice
├── ConsumptionProcessingModel/    # Clusterizare și analiză sigmoidă
├── RecommendationModel/           # Determinarea momentelor de recomandare
├── EnergyDataScrapperModel/       # Extragere oferte furnizori (posf.ro)
├── DataBaseModel/                 # Script-uri ETL dintr-o bază SQLite sursă
├── HelperFiles/                   # Clase de bază și utilitare comune
├── CSVs/                          # Date preprocesate, gata de rulare
└── main.py                        # Punct de intrare
```

## Fluxul de date

1. **Încărcare locuințe**, `HouseFacade` citește `CSVs/houses_after_filtering_and_matching_with_weather_data.csv`.
2. **Radiație solară**, `SolarRadiationHouseFacade` citește datele de radiație pentru aceleași locuințe.
3. **Estimare producție (NEEG)**, `PowerEstimatedFacade` calculează producția orară cu formula panoului fotovoltaic și determină NEEG, energia efectiv utilizabilă la fața locului, ca sumă a valorii minime dintre producție și consum.
4. **Autoconsum și autosuficiență**, `SelfConsumptionBuilder` și `SelfSufficiencyBuilder` aplică aceeași formulă de bază cu numitori diferiți (vezi mai jos) și ele sunt atașate pe obiectele `House`.
5. **Consum pe electrocasnice**, `HouseWithAppliancesFacade` încarcă `appliance_consumption_preprocessed.csv`, folosit pentru a determina intervalele de funcționare ale fiecărui electrocasnic.
6. **Dicționare de recomandare**, generate în două etape:
   - offline, `RecommendationDictionaryBuilder.export_to_csv` determină pragurile de activitate ale electrocasnicelor (prin `ConsumptionProcessingFacade`) și aplică logica de recomandare bazată pe sigmoid (prin `RecommendationFacade`), scriind rezultatul în `recommendation_dictionaries.csv`;
   - la rulare, `main.py` doar citește acest CSV deja calculat, într-un dicționar `{id_locuință: {pas: 0/1}}`, care marchează momentele în care un număr suficient de electrocasnice sunt active simultan pentru ca o recomandare să merite trimisă.
7. **Alegere a furnizorului simulat**, `get_random_company_provider` alege aleatoriu o ofertă din datele extrase de pe posf.ro, folosită ca furnizor curent al comunității pentru toate scenariile din rularea respectivă.
8. **Simulare pe agenți**, pentru fiecare combinație dintre cele 3 tipuri de agenți și dimensiunile de comunitate din `[1, 5, 10, 15, 20, 23]` (18 scenarii), se construiește un `HouseModel` Mesa și se rulează pentru numărul maxim de pași comuni tuturor locuințelor incluse.
9. **Statistici și grafice**, se calculează economiile monetare față de furnizorul simulat, se identifică cele mai afectate locuințe și se desenează frontiera Pareto pe toate scenariile rulate.

## Modelul agenților

La fiecare pas de simulare:

1. `ManagerAgent` calculează, pentru fiecare locuință marcată în dicționarul de recomandare, dacă consumul curent depășește media ultimei săptămâni cu peste 10%, situație în care recomandă `increase`; dacă este sub media cu peste 10%, recomandă `decrease`; altfel recomandă `maintain`.
2. Fiecare `HouseAgent` primește recomandarea și decide, cu o probabilitate egală cu pragul specific tipului său de agent, dacă o urmează. Dacă nu o urmează, acțiunea aplicată este întotdeauna `maintain`.
3. Acțiunea aleasă modifică consumul de referință al pasului curent cu ±20% (`increase`/`decrease`) sau îl lasă neschimbat (`maintain`), iar autoconsumul și autosuficiența simulate se recalculează incremental.

Schimbarea furnizorului de energie nu este încă o decizie individuală a fiecărui agent, ci este evaluată o singură dată, la nivel de comunitate, pentru fiecare scenariu rulat (vezi secțiunea Plan de dezvoltare).

## Formule și algoritmi cheie

| Indicator | Formulă |
|---|---|
| Producție fotovoltaică estimată | `P(t) = Pmax × f × N_panouri × (radiație(t) / 1000)`, cu `Pmax = 575 W`, `f = 0.8` |
| Rată de autoconsum (estimată, pe istoric) | `SC = Σ min(producție, consum) / Σ producție` |
| Rată de autosuficiență (estimată, pe istoric) | `SS = Σ min(producție, consum) / Σ consum` |
| Economii monetare | `(consum estimat − consum simulat) × preț per kWh` |

Ratele de mai sus sunt calculate pentru valorile istorice, atașate o singură dată pe fiecare `House` (`SelfConsumptionModel`, `SelfSufficiencyModel`). În simularea pe agenți, `HouseAgent.determine_simulated_self_consumption_and_self_sufficiency` (`AgentModel/house_agent.py`) calculează aceleași două mărimi la fiecare pas, dar cu numitorii inversați față de convenția de mai sus: `simulated_self_consumption` împarte la consumul simulat, iar `simulated_self_sufficiency` împarte la producție. Practic, valorile simulate corespund matematic formulei opuse celei sugerate de numele lor. Toate graficele care compară "simulat versus estimat" pentru aceiași doi indicatori moștenesc această inconsistență (vezi Limitări cunoscute).

Pragul de activitate al fiecărui electrocasnic se determină prin scalare min-max a valorilor de consum nenule, trecere prin funcția sigmoidă `1 / (1 + e^-x)` și clusterizare KMeans în două etape, care izolează limita dintre stările oprit și pornit.

Frontiera Pareto se calculează pe punctele `(1 − SC, 1 − SS)` ale tuturor scenariilor, cu biblioteca `paretoset` și sensul de optimizare `["max", "max"]`, pentru a evidenția combinațiile neomise de niciun alt scenariu.

## Tehnologii utilizate

| Bibliotecă | Rol în proiect |
|---|---|
| `mesa` | Cadrul de simulare multi-agent (modele, agenți, scheduler) |
| `pandas` | Prelucrarea seriilor de timp (reeșantionare orară, parsare timestamp-uri) |
| `plotly` | Toate graficele generate |
| `scikit-learn` | `IsolationForest` pentru anomalii, `KMeans` pentru detectarea stărilor electrocasnicelor |
| `scipy` | Winsorizare pentru limitarea anomaliilor de consum |
| `numpy` | Operații vectoriale în procesarea consumului |
| `paretoset` | Calculul frontierei Pareto |
| `requests` | Apeluri către API-ul de geolocalizare și către posf.ro |

## Instalare și rulare

Proiectul folosește [`uv`](https://docs.astral.sh/uv/) pentru gestionarea dependențelor și a mediului virtual.

```bash
git clone https://github.com/deniz2104/Energy-Community-MultiAgent-Approach.git
cd Energy-Community-MultiAgent-Approach
uv run main.py
```

`uv run` creează automat mediul virtual (`.venv`) și instalează dependențele fixate în `uv.lock` la prima rulare.

Datele necesare rulării simulării sunt deja incluse, preprocesate, în directorul `CSVs/`, deci nu este nevoie de un pas separat de descărcare pentru a rula simularea. Script-urile din `DataBaseModel/` reprezintă pasul ETL anterior, care a produs aceste CSV-uri dintr-o bază de date SQLite sursă (`irise.sqlite3`) și nu sunt necesare pentru rulare; ele nu sunt incluse în depozit.

Fiecare dintre `HouseFacade`, `SolarRadiationHouseFacade` și `HouseWithAppliancesFacade` are și o metodă `process_*_pipeline`, care rulează curățarea completă (eliminare anomalii, potrivire pe interval de timp, reeșantionare orară) pornind de la un CSV brut. `main.py` nu apelează niciuna dintre acestea; el citește direct CSV-urile din `CSVs/`, deja curățate.

Nu este necesară nicio cheie API: geolocalizarea folosește serviciul public `ip-api.com`, iar prețurile furnizorilor sunt preluate direct de pe posf.ro.

## Rezultate generate

Toate graficele se deschid direct în browser prin Plotly, fără a fi salvate automat pe disc:

- comparație autoconsum/autosuficiență/economii, simulat versus estimat, per scenariu;
- evoluția în timp a consumului de referință față de cel simulat, pentru o singură locuință;
- frontiera Pareto pe toate combinațiile de tip de agent și dimensiune a comunității;
- clasamentul locuințelor cele mai afectate de recomandări, pe categorii de dimensiune;
- economiile în lei și procentul de energie regenerabilă pentru cele mai bune 5 oferte alternative de furnizor.

## Sursele de date

- **Consum electric la nivel de locuință și date meteo/solare**, un set de date de tip IRISE, cu identificatori de locuință și serii orare de consum. Setul original nu este menționat explicit în depozit; se recomandă adăugarea sursei și a licenței exacte atunci când sunt confirmate.
- **Prețuri și procent de energie regenerabilă ale furnizorilor**, extrase din comparatorul public posf.ro.
- **Zonă geografică curentă**, determinată prin `ip-api.com`.

## Plan de dezvoltare

Pornind de la comentariile lăsate în `main.py` și de la stadiul actual al codului:

- [x] extragere automată a prețurilor și a procentului de energie regenerabilă ale furnizorilor
- [x] rulare a simulării pentru mai multe dimensiuni de comunitate (1, 5, 10, 15, 20, 23 locuințe), cu grafice comparative pe același set de axe
- [x] desenarea frontierei Pareto peste rezultatele tuturor scenariilor
- [ ] mutarea logicii complete de rulare din `main.py` în `AgentModel/parallel_simulation.py`, singurul punct care astăzi apelează toate etapele (multi-scenariu, paralel, cu frontieră Pareto)
- [ ] decizie individuală de schimbare a furnizorului la nivel de agent, nu doar evaluare agregată la nivel de comunitate, astfel încât fiecare locuință să poată alege dacă vrea preț mai mic, procent mai mare de energie regenerabilă sau ambele
- [ ] configurare a unui devcontainer pentru un mediu de dezvoltare reproductibil

## Limitări cunoscute

- Nu există încă un fișier de licență în depozit.
- `DataBaseModel/` presupune un fișier SQLite sursă (`irise.sqlite3`) care nu este inclus în depozit; regenerarea CSV-urilor de la zero necesită acest fișier obținut separat.
- Furnizorul curent al comunității este ales aleatoriu dintre ofertele extrase de pe posf.ro, nu corespunde unui furnizor real asociat locuințelor din setul de date; economiile calculate trebuie interpretate ca potențial relativ la acest furnizor simulat, nu ca economii reale.
- `RecommendationFacade` este instanțiată în `main.py`, dar metodele ei de analiză (procent de recomandări, distribuție orară, distribuție per electrocasnic) nu sunt încă apelate în fluxul curent.
- Valorile `simulated_self_consumption` și `simulated_self_sufficiency` calculate per agent folosesc numitori inversați față de convenția folosită pentru valorile istorice `self_consumption`/`self_sufficiency` (detaliu în secțiunea Formule și algoritmi cheie). Orice comparație directă "simulat versus estimat" pentru acești doi indicatori ar trebui verificată înainte de a fi interpretată.
- `HouseModel/house_preprocessing_data.py::eliminate_days_after_a_year_per_house` calculează fereastra corespunzătoare ultimelor 365 de zile, dar apoi păstrează exact ce se află în afara ei, eliminând ultimul an în loc să trunchieze datele la un an. Metoda nu este apelată din `main.py` (vezi mai sus), dar a fost folosită la generarea CSV-urilor curente din depozit.
- `DataBaseModel/database_appliance.py` combină un import relativ la fișierul din același director (`from database_house import DatabaseHandler`) cu un import de pachet de la rădăcina proiectului (`from HelperFiles.file_to_get_house_ids import house_ids`); cele două presupun directoare de lucru diferite, deci scriptul nu rulează ca atare fără o ajustare a `sys.path`.
