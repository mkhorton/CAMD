#  Copyright (c) 2019 Toyota Research Institute.  All rights reserved.
"""
This is a quick utility script for adding plots to the
existing runs prior to version
"""

import os
import pickle
from camd import CAMD_S3_BUCKET
from camd.loop import Loop
from camd.analysis import AnalyzeStability_mod
from monty.os import cd, makedirs_p
from monty.serialization import loadfn, dumpfn
import boto3


def get_all_s3_folders():
    client = boto3.client('s3')
    result = client.list_objects(
        Bucket=CAMD_S3_BUCKET, Prefix="proto-dft/runs/", Delimiter='/')
    runs = [o.get('Prefix') for o in result.get('CommonPrefixes')]
    return runs


def sync_s3_folder(s3_folder, bucket=CAMD_S3_BUCKET,
                   local_folder=None):
    local_folder = local_folder or "."
    os.system('aws s3 sync s3://{}/{} {}'.format(
        bucket, s3_folder, local_folder))
    return True


def update_run(folder):
    """
    Updates existing runs in s3 to include plots

    Returns:
        List of modified chemsys

    """
    with cd(folder):
        analyzer = AnalyzeStability_mod(hull_distance=0.2)
        with open("seed_data.pickle", "rb") as f:
            result_df = pickle.load(f)

        # Generate report plots
        for iteration in range(0, 6):
            print("{}: {}".format(folder, iteration))
            if not os.path.isdir(str(iteration)):
                continue
            all_result_ids = loadfn(
                os.path.join(str(iteration), "consumed_candidates.json"))
            new_result_ids = loadfn(
                os.path.join(str(iteration), "submitted_experiment_requests.json"))
            analyzer.present(
                df=result_df,
                new_result_ids=new_result_ids,
                all_result_ids=all_result_ids,
                filename="hull_{}.png".format(iteration)
            )

        Loop.generate_report_plot()


def update_s3(s3_folder, bucket=CAMD_S3_BUCKET,
              local_folder=None):
    local_folder = local_folder or "."
    os.system('aws s3 sync {} s3://{}/{}'.format(
        local_folder, bucket, s3_folder))


def main():
    all_s3_prefixes = get_all_s3_folders()
    makedirs_p("cache")
    os.chdir("cache")
    for run in all_s3_prefixes:
        local_folder = run.split('/')[-2]
        sync_s3_folder(run, local_folder=local_folder)
        update_run(local_folder)
        update_s3(run, local_folder=local_folder)


if __name__ == "__main__":
    main()
