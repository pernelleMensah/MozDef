#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2017 Mozilla Corporation

from lib.alerttask import AlertTask
from mozdef_util.query_models import SearchQuery, TermMatch, ExistsMatch, PhraseMatch


class AlertBugzillaPBruteforce(AlertTask):
    def main(self):
        self.parse_config('bugzilla_auth_bruteforce.conf', ['url'])
        search_query = SearchQuery(minutes=15)

        search_query.add_must([
            TermMatch('category', 'bro'),
            TermMatch('source', 'notice'),
            PhraseMatch('details.note', 'BugzBruteforcing::HTTP_BugzBruteforcing_Attacker')
        ])

        self.filtersManual(search_query)

        # Search events
        self.searchEventsSimple()
        self.walkEvents()

    # Set alert properties
    def onEvent(self, event):
        category = 'httperrors'
        tags = ['http']
        severity = 'NOTICE'
        hostname = event['_source']['hostname']
        url = self.config.url

        # the summary of the alert is the same as the event
        summary = '{0} {1}'.format(hostname, event['_source']['summary'])

        # Create the alert object based on these properties
        return self.createAlertDict(summary, category, tags, [event], severity=severity, url=url)
