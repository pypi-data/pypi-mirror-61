# -*- coding: utf-8 -*-

from Acquisition import aq_inner, aq_parent
from collective.contract_management.content.contract import IContract
from collective.contract_management.content.contracts import IContracts
from datetime import datetime, timedelta
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.event.base import default_timezone
from plone.event.interfaces import IICalendarEventComponent
from plone.event.utils import utc
from Products.CMFPlone.utils import safe_unicode
from Products.ZCatalog.interfaces import ICatalogBrain
from zope.globalrequest import getRequest
from zope.interface import implementer, Interface

import icalendar


PRODID = "-//Plone.org//NONSGML collective.contract_management//EN"
VERSION = "2.0"


def construct_icalendar(context, events):
    """Returns an icalendar.Calendar object.

    :param context: A content object, which is used for calendar details like
                    Title and Description. Usually a container, collection or
                    the event itself.

    :param events: The list of event objects, which are included in this
                   calendar.
    """
    cal = icalendar.Calendar()
    cal.add("prodid", PRODID)
    cal.add("version", VERSION)

    cal_tz = default_timezone(context)
    if cal_tz:
        cal.add("x-wr-timezone", cal_tz)

    for event in events:
        if ICatalogBrain.providedBy(event) or IContentListingObject.providedBy(event):
            event = event.getObject()
        if not (IContract.providedBy(event)):
            # Must be a contract.
            continue
        ical_event = IICalendarEventComponent(event).to_ical()
        if event.end and event.notice_period:
            ical_alarm = icalendar.Alarm()
            ical_alarm.add("action", "DISPLAY")
            reminder = int(event.reminder)  # default 30
            alarm_value = (event.end - event.notice_period).days + reminder
            ical_alarm.add("trigger", timedelta(days=-alarm_value))
            ical_event.add_component(ical_alarm)
        cal.add_component(ical_event)
    return cal


class IICalendar(Interface):
    """Adapter, which is used to construct an icalendar object.

    """


@implementer(IICalendar)
def calendar_from_event(context):
    """Event adapter. Returns an icalendar.Calendar object from an Event
    context.
    """
    context = aq_inner(context)
    return construct_icalendar(context, [context])


@implementer(IICalendar)
def calendar_from_collection(context):
    """Container/Event adapter. Returns an icalendar.Calendar object from a
    Collection.
    """
    context = aq_inner(context)
    # The keyword argument brains=False was added to plone.app.contenttypes
    # after 1.0
    result = context.results(batch=False, sort_on="start")
    return construct_icalendar(context, result)


@implementer(IICalendarEventComponent)
class ICalendarContractEventComponent(object):
    """Returns an icalendar object of the event.
    """

    def __init__(self, context):
        self.context = context
        self.event = self.context
        self.ical = icalendar.Event()

    def get_summery_prefix(self):
        """ get summery prefix from most upper parent Contracts obj
        """
        parent = aq_parent(self.context)
        while IContracts.providedBy(parent):
            context = parent
            parent = aq_parent(parent)
        return context.title

    @property
    def dtstamp(self):
        # must be in uc
        return {"value": utc(datetime.now())}

    @property
    def created(self):
        # must be in uc
        return {"value": utc(self.event.created())}

    @property
    def last_modified(self):
        # must be in uc
        return {"value": utc(self.event.modified())}

    @property
    def summary(self):
        prefix = self.get_summery_prefix()
        return {"value": u"[{0}]: {1}".format(prefix, self.event.title)}

    @property
    def description(self):
        return {"value": self.event.description}

    @property
    def dtstart(self):
        start = self.event.end and {"value": self.event.end.date()} or None
        return start

    @property
    def dtend(self):
        end = self.event.end and {"value": self.event.end.date() + timedelta(days=+1)} or None
        return end

    @property
    def categories(self):
        ret = []
        for cat in self.event.subjects or []:
            ret.append(cat)
        if ret:
            return {"value": ret}

    @property
    def url(self):
        return {"value": safe_unicode(self.context.absolute_url())}

    @property
    def uid(self):
        request = getRequest() or {}
        domain = request.get("HTTP_HOST", None)
        domain = "@" + domain if domain else ""
        sync_uid = self.context.UID() + domain if self.context.UID() else None
        return {"value": sync_uid}

    def ical_add(self, prop, val):
        if not val:
            return

        if not isinstance(val, list):
            val = [val]

        for _val in val:
            assert isinstance(_val, dict)
            value = _val["value"]
            if not value:
                continue
            prop = _val.get("property", prop)
            params = _val.get("parameters", None)
            self.ical.add(prop, value, params)

    def to_ical(self):

        ical_add = self.ical_add
        ical_add("dtstamp", self.dtstamp)
        ical_add("created", self.created)
        ical_add("uid", self.uid)
        ical_add("url", self.url)
        ical_add("last-modified", self.last_modified)
        ical_add("summary", self.summary)
        ical_add("description", self.description)
        ical_add("dtstart", self.dtstart)
        ical_add("dtend", self.dtend)
        ical_add("categories", self.categories)

        return self.ical
