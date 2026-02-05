# Quality Control Collector for AIND ephys pipeline
## aind-ephys-qc-collector


### Description

This capsule is designed to compute collect all `aind-data-schema QualityControl` JSON files generated for different streams and aggregate them into a single `quality_control.json`

### Inputs

The `data/` folder must include the pairs of `quality_control_{recording_name}.json` and `quality_control_{recording_name}` folders with associated figures.

### Parameters

The `code/run` script takes no arguments.


### Output

The capsule produces the following output:

- `results/quality_control.json` file, representing a valid `aind_data_schema.core.QualityControl` object with aggregated matrics from all streams.
- `results/quality_control` folder, with reference figures for the `quality_control.json` file.
