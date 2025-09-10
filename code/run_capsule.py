import sys
import logging
import json
import shutil
import time
from pathlib import Path

import numpy as np

from aind_data_schema.core.quality_control import QualityControl


data_folder = Path("../data")
results_folder = Path("../results")


logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")


if __name__ == "__main__":
    logging.info("\nEPHYS QC COLLECTION")
    t_qc_start_all = time.perf_counter()

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
    for quality_control_json_file in quality_control_json_files:
        # json file names are: quality_control_{recording_name}.json
        recording_name = "_".join(quality_control_json_file.name.split("_")[2:])[:-5]
        recording_names.append(recording_name)

        # copy figures
        input_figure_folder = data_folder / f"quality_control_{recording_name}"
        output_figure_folder = results_folder / "quality_control" / recording_name
        output_figure_folder.mkdir(parents=True, exist_ok=True)

        for fig_file in input_figure_folder.iterdir():
            if fig_file.suffix in [".png", ".pdf"]:
                shutil.copy(fig_file, output_figure_folder / fig_file.name)

        # read json and remap reference strings
        qc_json_str = json.dumps(json.load(open(quality_control_json_file)))
        qc_json_str = qc_json_str.replace(f"quality_control_{recording_name}", f"quality_control/{recording_name}")

        # load qc and append evaluations
        qc = QualityControl(**json.loads(qc_json_str))
        all_metrics.extend(qc.metrics)
        default_grouping.extend(qc.default_grouping)

    # create main QC with all metrics and detault tags
    default_grouping = sorted(list(set(default_grouping)))
    logging.info(f"\tCollected {len(all_metrics)} metrics for {len(default_grouping)} tags and {len(recording_names)} streams.")
    # add recording names for grouping
    default_grouping.extend(recording_names)

    main_qc = QualityControl(
        metrics=all_metrics,
        default_grouping=default_grouping
    )
    
    main_qc.write_standard_file(output_directory=results_folder)

    t_qc_end_all = time.perf_counter()
    elapsed_time_qc_all = np.round(t_qc_end_all - t_qc_start_all, 2)

    logging.info(f"EPHYS QC COLLECTION time: {elapsed_time_qc_all}s")

