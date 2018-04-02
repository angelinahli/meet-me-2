"""
Builds objects used to schedule an event.
"""

from datetime import datetime, date, time, timedelta

class Event(object):

    def __init__(self, start, end):
        """ start and end are both datetime objects """
        self.start = start
        self.end = end

    def __repr__(self):
        return "Event start: {} | end: {}".format(self.start, self.end)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Scheduler(object):

    def __init__(self, users, name, start_date, end_date, start_time, end_time, 
            minutes):
        self.users = users
        self.name = name
        self.time_length = timedelta(minutes=minutes)
        
        self.start_date = start_date
        self.start_time = start_time
        self.start_dt = datetime.combine(self.start_date, self.start_time)
        
        self.end_date = end_date
        self.end_time = end_time
        self.end_dt = datetime.combine(self.end_date, self.end_time)

        # will check for times every 15 min interval
        self.increment = timedelta(minutes=15)
        self.user_events = []
        for user in self.users:
            self.user_events += user.get_events_between_dts(
                self.start_dt, self.end_dt)

    def _ceil_dt(self, dt):
        return dt + (datetime.min - dt) % self.increment

    def _in_time_range(self, event):
        """
        returns true if this event falls within the time range specified
        """
        return event.start.time() >= self.start_time and \
            event.end.time() <= self.end_time

    def _in_date_range(self, event):
        return event.start.date() >= self.start_date and \
            event.end.date() <= self.end_date

    def _has_conflict(self, event):
        """ returns true if any person has a conflict with this event """
        for user_evt in self.user_events:
            if user_evt.start_time:
                pass

    def get_times(self):
        """ """
        times = []
        dt = self.start_dt
        end_dt = self.end_dt
        rounded = False
        while dt <= end_dt:
            evt = Event(dt, dt + self.time_length)
            if self._in_time_range(evt) and self._in_date_range(evt):
                times.append(evt)
            if not rounded:
                new_dt = self._ceil_dt(dt)
                dt = new_dt if dt != new_dt else dt + self.increment
                rounded = True
            else:
                dt = dt + self.increment
        return times


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

    def __repr__(self):
        usernames = [u.username for u in self.users]
        return "<Event: {} for users: {}>".format(self.name, ", ".join(usernames))


if __name__ == "__main__":
    pass
