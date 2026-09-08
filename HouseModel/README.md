# HouseModel

Owns the `House` domain object and everything that builds, cleans, and plots per-house consumption series.

## Registry pattern (`house.py`)

`House` keeps its own instances in a class-level registry (`_instances: dict[house_id, House]`) instead of callers threading dicts/lists around by hand.

- `House.get_or_create(house_id)` — the builder's single entry point per CSV row: look up or create.
- `House.get_instances()` / `count_instances()` / `return_ids_of_instances()` — read the current set.
- `House.unregister(house_id)` — drop a house (used by the pipeline's filter steps).
- `House.reset()` — clear everything. Called at the start of every `HouseBuilder.build()`, so each run starts clean instead of accumulating houses from a previous run.

Each subclass (`SolarRadiationHouse`, `HouseWithAppliancesConsumption`, `PowerEstimator`) gets its **own independent registry** — `__init_subclass__` gives every subclass a fresh `_instances` dict, so building solar-radiation houses never touches `House`'s registry and vice versa. Filtering therefore always unregisters via `type(house).unregister(...)`, not the literal `House` class, so it always hits the correct registry no matter which subclass is being processed.

This replaced an earlier version that kept two separate, unsynced records of the same houses — a registry on `House` that nothing read, plus a private dict inside `HouseBuilder`. The registry is now the single source of truth.

## Pipeline (`house_pipeline.py`)

`house_pipeline.py` cleans a raw list of houses through a fixed sequence of steps. Every step shares one contract:

```python
Step = Callable[[list[House]], list[House]]
```

Every step takes the current list of houses and returns the (possibly smaller or changed) list — that's what lets `run()` chain them with one generic line: `houses = step(houses)`. Python doesn't enforce this contract at runtime; it's a discipline every step in the file has to keep by hand.

Three roles in the file:

- **`run()`** — the orchestrator. Walks `PIPELINE` in order, feeding each step's output into the next step's input. It doesn't know or care what any individual step does.
- **`apply_per_house` / `filter_houses`** — adapters. They don't process houses themselves; they wrap a *simple, one-house rule* into something that satisfies the `Step` contract.
  - `apply_per_house(transform)` wraps a function that mutates one house and returns nothing (e.g. `eliminate_anomalies_in_data`).
  - `filter_houses(predicate)` wraps a yes/no question about one house, and unregisters the houses that answer "no" as it filters.
- **`resampling_houses_based_on_time_period`** — the one step written by hand instead of through an adapter, because its job (resample one house's series, write the result back) doesn't match either adapter's shape.

`PIPELINE` is the ordered list of steps that actually run. Cheap filters run first, to shrink the list before the expensive per-house anomaly detection (`IsolationForest`).

## Possible follow-ups

- `remove_houses_with_few_data_points` (`50000`) and `remove_houses_with_lot_of_zeros` (`0.15`) still hardcode their thresholds inline, unlike the rest of the pipeline's tunables (`DIFFERENCE_DAYS`, `N_ESTIMATORS`, ... in `constants.py`). Worth moving alongside them for consistency.
- `SolarRadiationHouseBuilder`, `HouseWithAppliancesBuilder`, and `PowerEstimatedBuilder` still hand-roll their own local "dict + for-loop + get-or-create" logic instead of using `House.get_or_create`. Natural next candidates for the same registry pattern.