"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'filter_1' block
    filter_1(container=container)

    return

def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_1() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.threat_object_type", "==", "ip"],
            ["artifact:*.cef.threat_object", "not in", "10.0.0.0/8"],
            ["artifact:*.cef.threat_object", "not in", "172.16.0.0/12"],
            ["artifact:*.cef.threat_object", "not in", "192.168.0.0/16"],
        ],
        logical_operator='and',
        name="filter_1:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        ip_reputation_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        geolocate_ip_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def ip_reputation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('ip_reputation_1() called')

    # collect data for 'ip_reputation_1' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filter_1:condition_1:artifact:*.cef.threat_object', 'filtered-data:filter_1:condition_1:artifact:*.id'])

    parameters = []
    
    # build parameters list for 'ip_reputation_1' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'ip': filtered_artifacts_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act(action="ip reputation", parameters=parameters, assets=['virustotal'], callback=ip_reputation_1_callback, name="ip_reputation_1")

    return

def ip_reputation_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('ip_reputation_1_callback() called')
    
    join_filter_2(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
    join_format_2(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_2() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["ip_reputation_1:action_result.data.*.detected_communicating_samples.*.positives", ">=", 3],
        ],
        name="filter_2:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        format_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        filter_3(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def join_filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_filter_2() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['ip_reputation_1', 'geolocate_ip_1']):
        
        # call connected block "filter_2"
        filter_2(container=container, handle=handle)
    
    return

def pin_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('pin_1() called')

    formatted_data_1 = phantom.get_format_data(name='format_1')

    phantom.pin(container=container, data=formatted_data_1, message="Suspicious IP", pin_type="card", pin_style="red", name=None)

    return

def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_1() called')
    
    template = """Malware sample that communicates to \"{0}\" has a score > 3 on VirusTotal"""

    # parameter list for template variable replacement
    parameters = [
        "filtered-data:filter_2:condition_1:ip_reputation_1:action_result.parameter.ip",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    pin_1(container=container)

    return

def cf_rba_master_update_artifact_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('cf_rba_master_update_artifact_1() called')
    
    filtered_artifacts_data_0 = phantom.collect2(container=container, datapath=['filtered-data:filter_3:condition_1:artifact:*.id'])
    literal_values_0 = [
        [
            "{ \"cef\": {\"automation_flag\": \"true\"}}",
        ],
    ]

    parameters = []

    for item0 in literal_values_0:
        for item1 in filtered_artifacts_data_0:
            parameters.append({
                'data': item0[0],
                'overwrite': None,
                'artifact_id': item1[0],
            })
    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################    

    # call custom function "rba-master/update_artifact", returns the custom_function_run_id
    phantom.custom_function(custom_function='rba-master/update_artifact', parameters=parameters, name='cf_rba_master_update_artifact_1')

    return

def filter_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_3() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["filtered-data:filter_2:condition_1:ip_reputation_1:action_result.parameter.ip", "==", "filtered-data:filter_1:condition_1:artifact:*.cef.threat_object"],
        ],
        name="filter_3:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        cf_rba_master_update_artifact_1(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def geolocate_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('geolocate_ip_1() called')

    # collect data for 'geolocate_ip_1' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filter_1:condition_1:artifact:*.cef.threat_object', 'filtered-data:filter_1:condition_1:artifact:*.id'])

    parameters = []
    
    # build parameters list for 'geolocate_ip_1' call
    for filtered_artifacts_item_1 in filtered_artifacts_data_1:
        if filtered_artifacts_item_1[0]:
            parameters.append({
                'ip': filtered_artifacts_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_item_1[1]},
            })

    phantom.act(action="geolocate ip", parameters=parameters, assets=['maxmind'], callback=geolocate_ip_1_callback, name="geolocate_ip_1")

    return

def geolocate_ip_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('geolocate_ip_1_callback() called')
    
    join_filter_2(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
    join_format_2(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def update_event_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('update_event_1() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'update_event_1' call
    filtered_artifacts_data_1 = phantom.collect2(container=container, datapath=['filtered-data:filter_1:condition_1:artifact:*.cef.event_id', 'filtered-data:filter_1:condition_1:artifact:*.id'])
    formatted_data_1 = phantom.get_format_data(name='format_2')

    parameters = []
    
    # build parameters list for 'update_event_1' call
    #for filtered_artifacts_item_1 in filtered_artifacts_data_1:
    if filtered_artifacts_data_1[0][0]:
        parameters.append({
                'event_ids': filtered_artifacts_data_1[0][0],
                'owner': "",
                'status': "in progress",
                'integer_status': "",
                'urgency': "",
                'comment': formatted_data_1,
                'wait_for_confirmation': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': filtered_artifacts_data_1[0][1]},
            })

    phantom.act(action="update event", parameters=parameters, assets=['splunk_es'], name="update_event_1", parent_action=action)

    return

def format_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_2() called')
    
    template = """%%
Artifact Name: {3}
IP address: {0}
VT Detected Communicating Samples: {1}
Geolocated Country: {2}

%%"""

    # parameter list for template variable replacement
    parameters = [
        "ip_reputation_1:action_result.parameter.ip",
        "ip_reputation_1:action_result.data.*.detected_communicating_samples.*.positives",
        "geolocate_ip_1:action_result.data.*.country_name",
        "filtered-data:filter_1:condition_1:artifact:*.name",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_2")

    update_event_1(container=container)

    return

def join_format_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None):
    phantom.debug('join_format_2() called')

    # check if all connected incoming playbooks, actions, or custom functions are done i.e. have succeeded or failed
    if phantom.completed(action_names=['ip_reputation_1', 'geolocate_ip_1']):
        
        # call connected block "format_2"
        format_2(container=container, handle=handle)
    
    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return