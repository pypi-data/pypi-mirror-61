# rivm-conversion

- Installation:

```
$ pip install rivm
```

## Usage - Scripts

Aerius **rekenpunten & overdrachtslijnen**:

```
$ convert_to_aerius --rekenpunten=path/to/csv --destination=.
```

Aerius **wegvakken SRM1 & wegvakken SRM2**:

```
$ convert_to_aerius --wegvakken=path/to/csv --destination=.
```

Aerius **maatregelen**:

```
$ convert_to_aerius --maatregelen=path/to/csv --destination=.
```

Aerius **correcties**:

```
$ convert_to_aerius --correcties=path/to/csv --destination=.
```

NSL Monitoring **rekenpunten**:

```
$ convert_to_nsl --rekenpunten=path/to/csv --overdrachtslijnen=path/to/csv --destination=.
```

NSL Monitoring **overdrachtslijnen**:

```
$ convert_to_nsl --wegvakken_srm1=path/to/csv --wegvakken_srm2=path/to/csv --destination=.
```

## Usage - Python

Prepare the input CSV's:

```python
from rivm.conversion.input import InputCSV(), InputBundle

input_csv_1 = InputCSV('path/to/csv', primary_key='receptorid')
input_csv_2 = InputCSV('path/to/csv', primary_key='calculation_point_id')

input_bundle = InputBundle(input_csv_1, input_csv_2)
```

Convert to a desired output format:

```python
from rivm.conversion.builder import AeriusRekenpunten

builder = AeriusRekenpunten(input_bundle)
result = builder.build()

result.to_csv('path/to/destination', sep=';', index=False)
```

Available **Aerius** output formats:

```python
from rivm.conversion.builder import AeriusRekenpunten
from rivm.conversion.builder import AeriusOverdrachtslijnen
from rivm.conversion.builder import AeriusWegvakkenSRM1
from rivm.conversion.builder import AeriusWegvakkenSRM2
from rivm.conversion.builder import AeriusMaatregelen
from rivm.conversion.builder import AeriusCorrecties
```

Available **NSL-Monitoring** output formats:

```python
from rivm.conversion.builder import NSLMonitoringRekenpunten
from rivm.conversion.builder import NSLMonitoringWegvakken
from rivm.conversion.builder import NSLMonitoringMaatregelen
from rivm.conversion.builder import NSLMonitoringCorrecties
from rivm.conversion.builder import NSLMonitoringResultaten
```
