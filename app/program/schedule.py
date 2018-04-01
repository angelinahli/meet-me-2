"""
Builds objects used to schedule an event.
"""

from datetime import datetime, timedelta

class ScheduledEvent(object):

    def __init__(self, users, name, start_dt, end_dt, minutes):
        self.users = users
        self.name = name
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.time_length = timedelta(minutes=minutes)

    def _is_conflicting(event1, event2):
        return ()

    def get_times(self):
        times = []

    def is_conflicting(evt1, evt2):
        return (evt1.start < evt2.end) and (evt1.end > evt2.start)

    def reasonable_time(evt):
        """Returns true if the event occurs not within 12-6am"""
        return int(evt.start.hour) not in xrange(0, 6)

    def schedule(start, end, minutes, user_list):
        """
        Return list of events that work for all users
        Without hours between 12-6am
        """
        leng = timedelta(minutes=minutes)

        pos = []
        time = start
        while(time < end - leng):
            new_event = events.Event("free", utc.localize(time), utc.localize(time + leng))
            pos.append(new_event)
            time += leng

        sched = []
        conflicts = []
        for user in user_list:
            conflicts += user.events

        for candidate in pos:
            is_possible = True
            for event in conflicts:
                if is_conflicting(candidate, event) or not reasonable_time(candidate):
                    is_possible = False
                    break
            if is_possible:
                sched.append(candidate)
        return sched