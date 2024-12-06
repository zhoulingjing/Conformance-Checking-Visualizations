import pm4py
import os
from pm4py.util import constants, pandas_utils
from pm4py.objects.log.util import dataframe_utils
import examples_conf
import importlib.util


def execute_script():
    log = pm4py.read_xes("receipt.xes")

    if importlib.util.find_spec("graphviz"):
        pm4py.view_performance_spectrum(log, ["Confirmation of receipt", "T04 Determine confirmation of receipt",
                                             "T10 Determine necessity to stop indication"], format=examples_conf.TARGET_IMG_FORMAT)

    df = pandas_utils.read_csv("receipt.csv")
    df = dataframe_utils.convert_timestamp_columns_in_df(df, timest_format=constants.DEFAULT_TIMESTAMP_PARSE_FORMAT, timest_columns=["time:timestamp"])

    if importlib.util.find_spec("graphviz"):
        pm4py.view_performance_spectrum(df, ["Confirmation of receipt", "T04 Determine confirmation of receipt",
                                             "T10 Determine necessity to stop indication"], format=examples_conf.TARGET_IMG_FORMAT)


if __name__ == "__main__":
    execute_script()