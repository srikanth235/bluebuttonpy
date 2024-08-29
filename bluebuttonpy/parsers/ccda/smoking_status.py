from bluebuttonpy import documents
from bluebuttonpy.core import wrappers

"""
Created on Mon Jul  2 21:32:38 2018

@author: mansooralam, yanjingwang

Modified on Jul 26, 2024:

@author: srikanth235
"""

"""
Parser for the CCDA smoking status in social history section
"""


def smoking_status(ccda):
    parse_date = documents.parse_date

    # Initialize lists to store extracted data
    all_data = []

    # Access the social history section
    social_history = ccda.section('social_history')
    entries = social_history.entries()

    # Iterate over all entries in the social history section
    for entry in entries:
        smoking_status_ = entry.template('2.16.840.1.113883.10.20.22.4.78')
        if smoking_status_.is_empty():
            smoking_status_ = entry.template('2.16.840.1.113883.10.22.4.78')

        if smoking_status_.is_empty():
            continue

        el = smoking_status_.tag('effectiveTime')
        entry_date = parse_date(el.attr('value'))

        el = smoking_status_.tag('value')
        name = el.attr('displayName')
        code = el.attr('code')
        code_system = el.attr('codeSystem')
        code_system_name = el.attr('codeSystemName')

        # Append each entry's data to the list
        all_data.append(
            wrappers.ObjectWrapper(
                date=entry_date,
                name=name,
                code=code,
                code_system=code_system,
                code_system_name=code_system_name
            )
        )

    # Return a list wrapper containing all data entries
    return wrappers.ListWrapper(all_data)
