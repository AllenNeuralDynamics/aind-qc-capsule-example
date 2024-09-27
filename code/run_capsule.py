""" top level run script """
from aind_data_schema.core.quality_control import QualityControl, QCEvaluation, QCMetric, Stage, QCStatus, Status
from aind_data_schema_models.modalities import Modality

from datetime import date

def run():
    """ Make a QC object, dump to json """
    status_example = QCStatus(
        evaluator="Automated",
        timestamp=date(2024, 9, 27),
        status=Status.PASS,
    )

    metric_example = QCMetric(
        name="Average spike rate (hz)",
        description="Pass when >1",
        value=5,
    )

    evaluation_example = QCEvaluation(
        evaluation_name="Spike rate check",
        evaluation_modality=Modality.ECEPHYS,
        evaluation_stage=Stage.RAW,
        qc_metrics=[metric_example],
        evaluation_status=[status_example],
    )

    qc = QualityControl(
        overall_status=[status_example],
        evaluations=[
            evaluation_example
        ],
    )

    qc.write_standard_file()


if __name__ == "__main__": run()