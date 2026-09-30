import argparse
import sys
import re
import logging
import json
import shutil
import time
from pathlib import Path

import numpy as np

from aind_data_schema.core.quality_control import QualityControl


data_folder = Path("../data")
results_folder = Path("../results")

# Define argument parser
parser = argparse.ArgumentParser(description="Compute Quality Control for Ephys pipeline")

parser.add_argument("--params", default=None, help="Path to the parameters file or JSON string. If given, it will override all other arguments.")


logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")


def run() -> None:
    logging.info("\nEPHYS QC COLLECTION")
    t_qc_start_all = time.perf_counter()

    args = parser.parse_args()
    PARAMS = args.params

    if PARAMS is not None:
        try:
            # try to parse the JSON string first to avoid file name too long error
            qc_collector_params = json.loads(PARAMS)
        except json.JSONDecodeError:
            if Path(PARAMS).is_file():
                with open(PARAMS, "r") as f:
                    qc_collector_params = json.load(f)
            else:
                raise ValueError(f"Invalid parameters: {PARAMS} is not a valid JSON string or file path")
    else:
        with open("params.json", "r") as f:
            qc_collector_params = json.load(f)

    # TODO: temporary - remove from params.json when logging is distributed by pipeline
    LOGGING = qc_collector_params.pop("logging", None)

    # setup logging before any other logging call
    if LOGGING is None:
        logging.basicConfig(level="INFO", stream=sys.stdout, format="%(message)s")
    else:
        if LOGGING["package"] == "logging":
            logging_cfg = LOGGING.get("logging_cfg", {})
            logging.basicConfig(stream=sys.stdout, **logging_cfg)
        elif LOGGING["package"] == "log-schema":
            import log_schema

            pipeline_name = LOGGING.get("pipeline_name", "AIND Ephys Pipeline")
            acquisition_name = LOGGING.get("acquisition_name", None)

            if acquisition_name is None:
                data_description_json = list(data_folder.glob("**/data_description.json"))
                if len(data_description_json) > 0:
                    data_description_json = data_description_json[0]
                    with open(data_description_json, "r") as f:
                        data_description = json.load(f)
                    acquisition_name = data_description["name"]

            config = LOGGING.get("logging_cfg")
            if config is not None and len(config) == 0:
                config = None
            log_schema.setup_logging(
                config=config,
                model={
                    "pipeline_name": pipeline_name,
                    "acquisition_name": acquisition_name,
                    "process_name": "QC collector"
                }
            )

    logging.info("Begin processing...", extra={"event_type": "stage_start"})

    # find quality_metrics JSON files in data_folder
    quality_control_json_files = [
        p for p in data_folder.iterdir() if p.name.startswith("quality_control") and p.suffix == ".json"
    ]
    # this ensures that metrics are also sorted by recording name
    quality_control_json_files = sorted(quality_control_json_files)

    logging.info(f"Found {len(quality_control_json_files)} quality control files")
    main_qc = None

    recording_names = []
    all_metrics = []
    default_grouping = []
    recording_segments = []
    for quality_control_json_file in quality_control_json_files:
        # json file names are: quality_control_{recording_name}.json
        recording_name = "_".join(quality_control_json_file.name.split("_")[2:])[:-5]
        recording_names.append(recording_name)
        if "group" in recording_name:
            segment_str = recording_name.split("_")[-2]
        else:
            segment_str = recording_name.split("_")[-1]
        recording_segments.append(segment_str)

    drop_recording_segment = len(set(recording_segments)) == 1
    if drop_recording_segment:
        logging.info(
            "All recording segments are the same. Dropping recording segment from recording name."
        )

    allow_tag_failures = []
    for quality_control_json_file in quality_control_json_files:
        # load original QC to retrieve abbreviated recording name (default_grouping)
        recording_name = "_".join(quality_control_json_file.name.split("_")[2:])[:-5]
        with open(quality_control_json_file) as f:
            original_qc_data = json.load(f)
        original_qc = QualityControl(**original_qc_data)
        abbrv_recording_name = original_qc.metrics[0].tags["probe"]

        if drop_recording_segment:
            recording_str = f"_{recording_segments[0]}"
            new_recording_name = abbrv_recording_name.replace(recording_str, "")
        else:
            new_recording_name = abbrv_recording_name

        # copy figures
        input_figure_folder = data_folder / f"quality_control_{recording_name}"
        output_figure_folder = results_folder / "quality_control" / new_recording_name
        output_figure_folder.mkdir(parents=True, exist_ok=True)

        for fig_file in input_figure_folder.iterdir():
            if fig_file.suffix in [".png", ".pdf"]:
                shutil.copy(fig_file, output_figure_folder / fig_file.name)

        # read json and remap reference strings
        qc_json_str = json.dumps(json.load(open(quality_control_json_file)))
        qc_json_str = qc_json_str.replace(f"quality_control_{recording_name}", f"quality_control/{new_recording_name}")
        if drop_recording_segment:
            # replace all segment entries except when segment string is in a zarr paths
            qc_json_str = re.sub(rf"{re.escape(recording_str)}(?!(?:(?!/).)*\.zarr)", "", qc_json_str)

        # load qc and append evaluations
        qc = QualityControl(**json.loads(qc_json_str))
        all_metrics.extend(qc.metrics)
        allow_tag_failures.extend(qc.allow_tag_failures)

    # create main QC with all metrics and detault tags
    logging.info(
        f"\tCollected {len(all_metrics)} metrics for {len(default_grouping)} tags and {len(recording_names)} streams."
    )
    logging.info(f"\tTags allowed to fail: {allow_tag_failures}")

    main_qc = QualityControl(
        metrics=all_metrics,
        default_grouping=[("probe"), ("stage")],
        allow_tag_failures=allow_tag_failures
    )
    
    main_qc.write_standard_file(output_directory=results_folder)

    t_qc_end_all = time.perf_counter()
    elapsed_time_qc_all = np.round(t_qc_end_all - t_qc_start_all, 2)

    logging.info(f"EPHYS QC COLLECTION time: {elapsed_time_qc_all}s")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.exception("Pipeline stage failed", extra={"event_type": "stage_error"})
        raise
