import pandas
import pm4py
import pm4py.algo.filtering
import pm4py.algo.filtering.log
def calc_frequency(event_log):
    frequencies = {}
    for activity in event_log['Activity']:
        if activity in frequencies.keys():
            frequencies[activity] += 1
        else:
            frequencies.update({activity : 1})
    return frequencies


event_log = pm4py.read_xes('receipt.xes')
vars = pm4py.get_variants(event_log)
variant_number = max(vars, key=vars.get)
print(variant_number)
print(list(variant_number))