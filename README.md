**Skrypt pozwalający wyznaczyć powierzchnie skrzydeł, generowane przez nie opory i inne wynikające parametry na podstawie danych projektowych do budowy łodzi solarnej**

1. **Moduł wizualizacji wyników** 

Skrypt umożliwia wizualizacje wyników z symulacji CFD oraz danych pobranych ze strony AirFoil Tools. Docelowym plikiem w którym znajdują się wszystkie metody związane z tworzeniem wykresów jest FoilPlotter.py.

- Tworzenie wykresów 2D i 3D dla badanych parametrów (lift, drag, moments, coefficients)
- Porównywanie na jednym wykresie parametrów różnych profili
Na przykład:![AoAvsVel](https://github.com/user-attachments/assets/995b431e-f5d7-436e-9cb3-9b1add91f24b)

Poprawne przygotownie pliku .csv wyników z symulacji CFD jest kluczowe. Należy to zrobić zgodnie z przykładowymi plikami .csv znajdującymi się w katalogu data_CFD.

2. **Moduł modelowania lotu łodzi**

Skrypt umożliwia m.in
- Wprowadzenie danych łodzi,
- Obliczenie rozkładu masy na 2 różne sposoby
- Całościowe obliczenie oporów łodzi w locie
- Badanie wpływu zmiany powierzchni skrzydeł na opory/sprawność
- Badanie wpływu zmiany rozkładu masy na opory/sprawność



