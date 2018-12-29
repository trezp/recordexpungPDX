#!/usr/bin/env python3

import collections
import enum

# TODO we may need to change this to Enum since only a few valid values are allowed.
class CrimeLevel(object):
    """ Crime Level.

    Describes crime level. e.g. Felony Class A.

    Attributes:
        type_: A string describing the type of crime.
        class_: A string of length 1 specifying the class.
    """
    def __init__(self, type_, class_=None):
        self.type_ = type_
        self.class_ = class_

    def __str__(self):
        if class_:
            return '{} Class {}'.format(self.type_, self.class_)
        else:
            return self.type_

DispositionType = enum.Enum('DispositionType',
                            ' '.join([
                                'CONVICTED',
                                'PROBATION_REVOKED',
                                'DISMISSED',
                                'ACQUITTED',
                                'NO_COMPLAINT'
                                ]))

class Disposition(object):
    """ Disposition for a charge.

    Attributes:
        type_: An enum of type DispositionType.
        date: A datetime.date specifying the date of the disposition.
    """
    def __init__(self, type_, date):
        self.type_ = type_
        self.date = date

class Statute(object):
    """ Statute corresponding to a law

    Statutes are represented by numbers in hierarchical manner:
    chapter.subchapter(section)(subsection) e.g. 653.412(5)(c)

    Attributes:
        chapter: An integer that specifies statute chapter.
        subchapter: An integer that specifies statute sub-chapter.
        section: An integer that specifies the section within sub-chapter.
        subsection: A string of length 1 that specifies the sub-section within
                    section.
    """
    def __init__(self, chapter, subchapter, section=None, subsection=None):
        self.chapter = chapter
        self.subchapter = subchapter
        self.section = section
        self.subsection = subsection
        # TODO we may need to add components beyond subsection

    def __eq__(self, other):
        return (self.chapter == other.chapter and
                self.subchapter == other.subchapter and
                ((not self.section and not other.section) or
                 self.section == other.section) and
                ((not self.subsection and not other.subsection) or
                 self.subsection == other.subsection))

    def __str__(self):
        # TODO do these need to have leading zeros?
        statute = '{}'.format(self.chapter)
        if self.subchapter:
            statute = '{}.{:03d}'.format(statute, self.subchapter)
        if self.section:
            statute = '{}({})'.format(statute, self.section)
        if self.subsection:
            statute = '{}({})'.format(statute, self.subsection)
        return statute

class Charge(object):
    """ Charge filed on a Client.

    Attributes:
        name: A string describing the charge.
        statute: A Statute object that applies for the charge.
        date: A datetime.date object specifying the date of the charge.
        disposition: A Disposition object for the charge.
    """
    def __init__(
            self,
            name,
            statute,
            level,
            date,
            disposition):
        self.name = name
        self.statute = statute
        self.level = level
        self.date = date
        self.disposition = disposition

CaseState = enum.Enum('CaseState', 'OPEN CLOSED')

class Case(object):
    """ Case associated with a Client.

    Attributes:
        charges: A list of Charge(s).
        state: A CaseState enum.
        balance_due: A float that tells how much money is owed to the court.
    """
    def __init__(self, charges, state, balance_due=0.0):
        self.charges = charges
        self.state = state
        self.balance_due = balance_due

    def num_charges(self):
        return len(self.charges)

class Client(object):
    """ Client - An individual who wants to expunge charges from their record.

    Attributes:
        name: A string that specifies client's name.
        dob: A datetime.date that specifies date of birth.
        cases: A list of Case(s).
    """
    def __init__(self, name, dob, cases):
        self.name = name
        self.dob = dob
        self.cases = cases

    def num_charges(self):
        num = 0
        for case in self.cases:
            num += case.num_charges()
        return num
