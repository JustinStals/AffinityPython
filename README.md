# Affinity Python Wrapper

A Python wrapper for Affinity's CRM platform. Includes functions for all available requests to their API and an OOD representation of their data model.

# Classes

List: The Affinity equivalent of a spreadsheet. It contains a collection of either people or organizations (aka entities).
List Entry: The Affinity equivalent of a row in a spreadsheet.

Field: The Affinity equivalent of a column in a spreadsheet. A field can be specific to a given list, or it can be global.

Field Value: The Affinity equivalent of the data in a spreadsheet cell.

Person: Contacts of your organization.

Organization: An external company that your team is in touch with - this could be an organization that you are trying to invest in, sell to, or establish a relationship with.

Note: A note object contains content, which is a string containing the note body. In addition, a note can be associated with multiple people or organizations.

# API Methods

LISTS

get_all_lists()

get_list(list_id)

populate_list(json_in)


LIST ENTRIES

get_all_list_entries(list_id)

get_list_entry(list_id, list_entry_id)

create_list_entry(list_id, entity_id, creator_id)

delete_list_entry(list_id, list_entry_id)

populate_list_entry(json_in)


FIELDS

populate_field(json_in)


FIELD VALUES

get_field_values(person_id, organization_id, list_entry_id)

create_field_value(field_id, entity_id, list_entry_id, value)

update_field_value(field_value_id, value)

delete_field_value(field_value_id)

populate_field_value(json_in)


PEOPLE

get_persons(term, page_size, page_token)

create_person(first_name, last_name, emails, phone_numbers, organization_ids)

update_person(person_id, first_name, last_name, emails, phone_numbers, organization_ids)

delete_person(person_id)

get_people_global_fields(person_id)

populate_person(json_in)


ORGANIZATION

get_organizations(term, page_size, page_token)

create_organization(name, domain, person_ids)

update_organization(organization_id, name, domain, person_ids)

delete_organization(organizaton_id)

get_organizations_global_fields()

populate_organization(json_in)


NOTES

populate_note(json_in)

