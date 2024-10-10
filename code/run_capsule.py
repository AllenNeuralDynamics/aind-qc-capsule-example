""" top level run script """
from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.quality_control import QCEvaluation, QualityControl, QCMetric, Stage, Status, QCStatus
import boto3
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth


### HOW TO USE
# This capsule demonstrates how to make QCEvaluations and either:
# 
# Preferred workflow, when you generate QC as part of a pipeline:
#   Attach them to the output of the capsule (in the results), along with any other metadata if you are making a data asset
#   the results will then be indexed as normal and entered into the DocDB.
#
# Alternate workflow, for when you need to generate QC for an existing asset
#  In this case we send the QCEvaluations directly to the DocDB (here the dev DocDB). 
#  You will need to know your asset's ID in DocDB. This is NOT the UUID of the data asset!! 
#
# Please also see the QC documentation https://aind-data-schema.readthedocs.io/en/latest/quality_control.html
# and send any questions to Dan Birman

# [todo: we'll move this boilerplate communication into aind-data-access-api in the future]
## DO NOT EDIT BELOW ##
session = boto3.Session()
credentials = session.get_credentials()
host = "api.allenneuraldynamics-test.org"

auth = AWSRequestsAuth(
aws_access_key=credentials.access_key,
aws_secret_access_key=credentials.secret_key,
aws_token=credentials.token,
aws_host="api.allenneuraldynamics-test.org",
aws_region='us-west-2',
aws_service='execute-api'
)
url = f"https://{host}/v1/add_qc_evaluation"
## DO NOT EDIT ABOVE ##


def run():
    """ Demonstration of building QC """


    # Build a timestamp
    t = datetime(2022, 11, 22, 0, 0, 0, tzinfo=timezone.utc)

    # Build some status objects
    s = QCStatus(evaluator="Automated", status=Status.PASS, timestamp=t.isoformat())
    sp = QCStatus(evaluator="", status=Status.PENDING, timestamp=t.isoformat())

    # Example of how to use a dictionary to provide options a metric, see https://github.com/AllenNeuralDynamics/aind-qcportal-schema
    drift_value_with_options = {
        "value": "",
        "options": ["Low", "Medium", "High"],
        "status": [
            "Pass",
            "Fail",
            "Fail",
        ],  # when set, this field will be used to automatically parse the status, blank forces manual update
        "type": "dropdown",  # other type options: "checkbox"
    }

    # Example of how to use a dictionary to provide multiple checkable flags, some of which will fail the metric
    drift_value_with_flags = {
        "value": "",
        "options": ["Drift visible in entire session", "Drift visible in part of session", "Sudden movement event"],
        "status": ["Fail", "Pass", "Fail"],
        "type": "checkbox",
    }

    # Build some evaluations
    eval0 = QCEvaluation(
        name="Drift map",
        description="Qualitative check that drift map shows minimal movement",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        metrics=[
            QCMetric(
                name="Probe A drift",
                value=drift_value_with_options,
                reference="ecephys-drift-map",
                status_history=[sp],
            ),
            QCMetric(
                name="Probe B drift",
                value=drift_value_with_flags,
                reference="ecephys-drift-map",
                status_history=[sp],
            ),
            QCMetric(name="Probe C drift", value="Low", reference="ecephys-drift-map", status_history=[s]),
        ],
        notes="",
    )

    eval1 = QCEvaluation(
        name="Video frame count check",
        modality=Modality.BEHAVIOR_VIDEOS,
        stage=Stage.RAW,
        metrics=[
            QCMetric(name="video_1_num_frames", value=662, status_history=[s]),
            QCMetric(name="video_2_num_frames", value=662, status_history=[s]),
        ],
        notes="Pass when video_1_num_frames==video_2_num_frames",
    )

    eval2 = QCEvaluation(
        name="Probes present",
        modality=Modality.ECEPHYS,
        stage=Stage.RAW,
        metrics=[
            QCMetric(name="ProbeA_success", value=True, status_history=[s]),
            QCMetric(name="ProbeB_success", value=True, status_history=[s]),
            QCMetric(name="ProbeC_success", value=True, status_history=[s]),
        ],
    )

    # PREFERRED WORKFLOW
    qc = QualityControl(evaluations=[eval0, eval1, eval2])
    qc.write_standard_file(output_directory="/results")

    # ALTERNATE WORKFLOW

    # Repeat as needed for multiple evaluations, or put them into a list
    post_request_content = {"data_asset_id": "884810cc-ed54-45d8-bd32-de45f9583a68", "qc_evaluation": eval0.model_dump(mode='json')}    
    response = requests.post(url=url, auth=auth, json=post_request_content)
    print(f"Status: {response} with content: {response.text}")


if __name__ == "__main__": run()