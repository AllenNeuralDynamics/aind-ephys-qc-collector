import sys
import logging
import json
import shutil
from pathlib import Path

from aind_data_schema.core.quality_control import QualityControl


data_folder = Path("../data")
results_folder = Path("../results")


logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")


if __name__ == "__main__":

    # find quality_metrics JSON files in data_folder
    quality_control_json_files = [
        p for p in data_folder.iterdir() if p.name.startswith("quality_control") and p.suffix == ".json"
    ]
    quality_control_json_files = sorted(quality_control_json_files)

    logging.info(f"Found {len(quality_control_json_files)} quality control files")
    evaluations = []

    for quality_control_json_file in quality_control_json_files:
        # json file names are: quality_control_{recording_name}.json
        recording_name = "_".join(quality_control_json_file.name.split("_")[2:])[:-5]
        logging.info(f"\tMerging metrics for {recording_name}")

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
        evaluations.extend(qc.evaluations)

    # write final quality_metrics.json
    quality_control = QualityControl(evaluations=evaluations)

    with (results_folder / f"quality_control.json").open("w") as f:
        f.write(quality_control.model_dump_json(indent=3))

