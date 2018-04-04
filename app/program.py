"""
Builds objects used to schedule an event.
"""

from datetime import datetime, date, time, timedelta

class Event(object):

    def __init__(self, start, end):
        """ start and end are both datetime objects """
        self.start_dt = start
        self.end_dt = end

    def get_str_date(self):
        return self.start_dt.date().strftime("%A, %d %B %Y")

    def get_str_start(self):
        return self.start_dt.strftime("%I:%M%p")

    def get_str_end(self):
        diff_date = self.end_dt.date() != self.start_dt.date()
        if diff_date:
            return self.end_dt.strftime("%A, %d %B %I:%M%p")
        return self.end_dt.strftime("%I:%M%p")

    def get_format_start(self):
        return self.start_dt.isoformat()

    def get_format_end(self):
        return self.end_dt.isoformat()

    def __repr__(self):
        return "Event start: {} | end: {}".format(self.start_dt, self.end_dt)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Scheduler(object):

    def __init__(self, users, name, start_date, end_date, start_time, end_time, 
            minutes):
        self.users = users
        self.name = " ".join([wd.capitalize() for wd in name.split()])
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
        start_dt = datetime.combine(event.start_dt.date(), self.start_time)

        # event must end on the same day unless the specified end time of
        # this scheduler is before the specified start time 
        # (the event can be overnight)
        if self.end_time > self.start_time:
            end_date = event.start_dt.date()
        else:
            end_date = event.start_dt.date() + timedelta(days=1)
        end_dt = datetime.combine(end_date, self.end_time)

        return event.start_dt >= start_dt and event.end_dt <= end_dt

    def _in_date_range(self, event):
        return event.start_dt.date() >= self.start_date and \
            event.end_dt.date() <= self.end_date

    def _events_conflict(self, evt1, evt2):
        """
        event objects must have attributes start_dt and end_dt
        source: https://stackoverflow.com/questions/325933/
                determine-whether-two-date-ranges-overlap
        """
        return (evt1.start_dt < evt2.end_dt) and (evt1.end_dt > evt2.start_dt)

    def _has_conflict(self, event):
        """ returns true if any person has a conflict with this event """
        for user_evt in self.user_events:
            if self._events_conflict(user_evt, event):
                return True
        return False

    def get_times(self):
        """ """
        times = []
        dt = self.start_dt
        end_dt = self.end_dt
        rounded = False
        while dt <= end_dt:
            evt = Event(dt, dt + self.time_length)
            if self._in_time_range(evt) and self._in_date_range(evt) and \
                    not self._has_conflict(evt):
                times.append(evt)
            
            if not rounded:
                new_dt = self._ceil_dt(dt)
                dt = new_dt if dt != new_dt else dt + self.increment
                rounded = True
            else:
                dt = dt + self.increment
        return times

    def get_formatted_times(self):
        """ """
        times = []
        dt = self.start_dt
        end_dt = self.end_dt
        rounded = False
        while dt <= end_dt:
            evt = Event(dt, dt + self.time_length)
            if self._in_time_range(evt) and self._in_date_range(evt) and \
                    not self._has_conflict(evt):
                evt_dict = {
                    "title": self.name,
                    "start": evt.get_format_start(), 
                    "end": evt.get_format_end()
                }
                times.append(evt_dict)
            
            if not rounded:
                new_dt = self._ceil_dt(dt)
                dt = new_dt if dt != new_dt else dt + self.increment
                rounded = True
            else:
                dt = dt + self.increment
        return times

    def get_times_by_date(self):
        all_events = self.get_times()
        events = {}
        for event in all_events:
            date = event.get_str_date()
            updated_events = events.get(date, [])
            updated_events.append(event)
            events[date] = updated_events
        for date in events:
            events[date] = sorted(events[date], key=lambda evt: evt.start_dt)
        return events

    def __repr__(self):
        usernames = [u.username for u in self.users]
        return "<Event: {} for users: {}>".format(self.name, ", ".join(usernames))

if __name__ == "__main__":
    pass
