# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2017 Mozilla Corporation

from positive_alert_test_case import PositiveAlertTestCase
from negative_alert_test_case import NegativeAlertTestCase

from alert_test_suite import AlertTestSuite


class TestWriteAudit(AlertTestSuite):
    alert_filename = "write_audit"

    # This event is the default positive event that will cause the
    # alert to trigger
    default_event = {
        "_type": "auditd",
        "_source": {
            "category": "write",
            "summary": "Write: /etc/audit/",
            "details": {
                "processname": "vi",
                "hostname": "exhostname",
                "originaluser": "randomjoe",
                "auditkey": "audit",
            }
        }
    }

    # This alert is the expected result from running this task
    default_alert = {
        "category": "write",
        "severity": "WARNING",
        "summary": "5 Filesystem write(s) to an auditd path by randomjoe on exhostname (5 hits)",
        "tags": ['audit'],
        "notify_mozdefbot": True,
    }

    test_cases = []

    test_cases.append(
        PositiveAlertTestCase(
            description="Positive test with default event and default alert expected",
            events=AlertTestSuite.create_events(default_event, 5),
            expected_alert=default_alert
        )
    )

    events = AlertTestSuite.create_events(default_event, 5)
    for event in events:
        event['_source']['summary'] = 'Write: /etc/audit/rules.d/.audit.rules.swp'
    test_cases.append(
        PositiveAlertTestCase(
            description="Positive test with events with a summary of 'Write: /etc/audit/rules.d/.audit.rules.swp'",
            events=events,
            expected_alert=default_alert
        )
    )

    events = AlertTestSuite.create_events(default_event, 5)
    for event in events:
        event['_source']['summary'] = 'Write: /etc/audit/rules.d/'
    test_cases.append(
        PositiveAlertTestCase(
            description="Positive test with events with a summary of 'Write: /etc/audit/rules.d/'",
            events=events,
            expected_alert=default_alert
        )
    )

    events = AlertTestSuite.create_events(default_event, 5)
    events[3]['_source']['details']['originaluser'] = "randomjoe"
    events[2]['_source']['details']['originaluser'] = "randomjane"
    test_cases.append(
        NegativeAlertTestCase(
            description="Negative test case with 5 events however one has different originaluser",
            events=events,
        )
    )

    test_cases.append(
        NegativeAlertTestCase(
            description="Negative test case with not enough events",
            events=AlertTestSuite.create_events(default_event, 1),
        ),
    )

    events = AlertTestSuite.create_events(default_event, 5)
    for event in events:
        event['_source']['summary'] = 'Write: /etc/audisp/'
    test_cases.append(
        NegativeAlertTestCase(
            description="Negative test case with events with summary without 'audit'",
            events=events,
        )
    )

    events = AlertTestSuite.create_events(default_event, 5)
    for event in events:
        event['_source']['summary'] = 'audit'
    test_cases.append(
        NegativeAlertTestCase(
            description="Negative test case with events with summary with only 'audit'",
            events=events,
        )
    )

    events = AlertTestSuite.create_events(default_event, 5)
    for event in events:
        event['_source']['summary'] = 'Write'
    test_cases.append(
        NegativeAlertTestCase(
            description="Negative test case with events with summary with only 'Write'",
            events=events,
        )
    )

    events = AlertTestSuite.create_events(default_event, 5)
    for event in events:
        event['_source']['details']['processname'] = 'process1'
    test_cases.append(
        NegativeAlertTestCase(
            description="Negative test case with events with processname that matches exclusion of 'process1'",
            events=events,
        )
    )

    events = AlertTestSuite.create_events(default_event, 5)
    for event in events:
        event['_source']['details']['originaluser'] = None
    test_cases.append(
        NegativeAlertTestCase(
            description="Negative test case aggregation key excluded",
            events=events,
        )
    )
