#!/usr/bin/python
__author__ = "Justin Stals"

# ------------------------------------------------------ #
# AFFINITY PYTHON WRAPPER
# ------------------------------------------------------ #


# ------------------------------------------------------ #
# KEY DEPENDENCIES
# ------------------------------------------------------ #

import json
import datetime
import requests as re
from requests.auth import HTTPBasicAuth

# ------------------------------------------------------ #
# GLOBAL VARIABLES
# ------------------------------------------------------ #

api_key = ''
daily_rate_limit = 150000
endpoint_base = 'https://api.affinity.vc/'
headers = {'Content-Type': 'application/json'}

# ------------------------------------------------------ #
# API CALLS
# ------------------------------------------------------ #

def get(call):
	r = re.get(call, auth=HTTPBasicAuth('', api_key), headers=headers)
	if check_err(r):
		return None
	return r.json()

def post(call, data):
	r = re.post(call, data=data, auth=HTTPBasicAuth('', api_key))
	if check_err(r):
		return None
	return r.json()

def put(call, data):
	r = re.put(call, data=data, auth=HTTPBasicAuth('', api_key))
	if check_err(r):
		return None
	return r.json()

def delete(call):
	r = re.delete(call, auth=HTTPBasicAuth('', api_key))
	if check_err(r):
		return None
	return r.json()

# ------------------------------------------------------ #
# LISTS
# ------------------------------------------------------ #

class List:
	
	'The Affinity equivalent of a spreadsheet. It contains a collection of either people or organizations (aka entities).'
	
	def __init__(self, list_id, list_type, name, public, owner_id, list_size):
		self.id = list_id
		# (integer) The unique identifier of the list object.
		self.type = list_type
		# (integer)	The type of the entities contained within the list. A list can contain people or organizations, but not both.
		self.name = name
		# (string) The title of the list that is displayed in Affinity.
		self.public = public
		# (boolean) If the list is publicly accessible to all users in your team, this is true. Otherwise, this is false.
		self.owner_id = owner_id
		# (integer) The unique id of the internal person who created this list.
		self.list_size = list_size
		# (integer) The number of list entries contained within the list.

def populate_list(json_in):
	list_out = List(
		json_in['id'],
		json_in['type'],
		json_in['name'],
		json_in['public'],
		json_in['owner_id'],
		json_in['list_size']
	)
	return list_out

def get_all_lists():
# Returns a collection of all the lists visible to you.
	call = endpoint_base + '/lists'
	r = get(call)
	return r

def get_list(list_id):
# Gets the details for a specific list given the existing list id.
	call = endpoint_base + '/lists/' + str(list_id)
	return get(call)

# ------------------------------------------------------ #
# LIST ENTRIES
# ------------------------------------------------------ #

class ListEntry:
	
	'The Affinity equivalent of a row in a spreadsheet.'
	
	def __init__(self, list_entry_id, list_id, creator_id, entity_id, entity, created_at):
		self.id = list_entry_id
		# (integer) The unique identifier of the list entry object.
		self.list_id = list_id
		# (integer)	The unique identifier of the list on which the list entry resides.
		self.creator_id = creator_id
		# (integer)	The unique identifier of the user who created the list entry.
		self.entity_id = entity_id
		# (integer) The unique identifier of the entity corresponding to the list entry.
		self.entity = entity
		# (object) Object containing entity-specific details like name, email address, domain etc.
		self.created_at = created_at
		# (datetime) The time when the list entry was created.

def populate_list_entry(json_in):
	list_entry_out = ListEntry(
		json_in['id'],
		json_in['list_id'],
		json_in['creator_id'],
		json_in['entity_id'],
		json_in['entity'],
		json_in['created_at']
	)
	return list_entry_out

def get_all_list_entries(list_id):
# Fetches all the list entries in the list with the supplied list id.
	call = endpoint_base + '/lists/' + str(list_id) + '/list-entries'
	return get(call)

def get_list_entry(list_id, list_entry_id):
# Fetches a list entry with a specified id.
	call = endpoint_base + '/lists/' + str(list_id) + '/list-entries/' + list_entry_id
	return get(call)

def create_list_entry(list_id, entity_id, creator_id):
# Creates a new list entry in the list with the supplied list id.
	call = endpoint_base + '/lists/' + str(list_id) + '/list-entries'
	data = {'entity_id':entity_id, 'creator_id':creator_id}
	return post(call, data)

def delete_list_entry(list_id, list_entry_id):
# Deletes a list entry with a specified list_entry_id.
	call = endpoint_base + '/lists/' + str(list_id) + '/list-entries/' + str(list_entry_id)
	return delete(call)

# ------------------------------------------------------ #
# FIELDS
# ------------------------------------------------------ #

class Field:
	
	'The Affinity equivalent of a column in a spreadsheet. A field can be specific to a given list, or it can be global.'
	
	def __init__(self, field_id, name, allows_multiple, dropdown_options, value_type):
		self.id = field_id
		# (integer) The unique identifier of the field object.
		self.name = name
		# (string) The name of the field.
		self.allows_multiple = allows_multiple
		# (boolean) This determines whether multiple values can be added to a single cell for the field.
		self.dropdown_options = dropdown_options
		# (object[]) Affinity supports pre-entered dropdown options for fields of the 'Ranked Dropdowon value_type.
		self.value_type = value_type
		# (integer) Describes what values can be associated with the field.

def populate_field(json_in):
	field_out = Field(
		json_in['field_id'],
		json_in['name'],
		json_in['allows_multiple'],
		json_in['dropdown_options'],
		json_in['value_type']
	)
	return field_out

# ------------------------------------------------------ #
# FIELD VALUES
# ------------------------------------------------------ #

class FieldValue:
	
	'The Affinity equivalent of the data in a spreadsheet cell.'

	def __init__(self, field_value_id, field_id, entity_id, list_entry_id, value):
		self.id = field_value_id
		# (integer) The unique identifier of the field value object.
		self.field_id = field_id
		# (integer)	The unique identifier of the field the value is associated with.
		self.entity_id = entity_id
		# (integer) The unique identifier of the person or organization object the field value is associated with.
		self.list_entry_id = list_entry_id
		# (integer) The unique identifier of the list entry object the field value is associated with. 
		self.value = value
		# (One of many) The value attribute can take on many different types, depending on the field value_type.

def populate_field_value(json_in):
	field_value_out = FieldValue(
		json_in['field_value_id'],
		json_in['field_id'],
		json_in['entity_id'],
		json_in['list_entry_id'],
		json_in['value']
	)
	return field_value_out

def get_field_values(person_id, organization_id, list_entry_id):
# Returns all field values attached to a person, organization or list_entry.
	call = endpoint_base + '/field-values'
	if person_id:
		call += '?person_id=' + str(person_id)
	if organization_id:
		call += '?organization_id=' + str(organization_id)
	if list_entry_id:
		call += '?list_entry_id=' + str(list_entry_id)
	return get(call)

def create_field_value(field_id, entity_id, list_entry_id, value):
# Creates a new field value with the supplied parameters.
	call = endpoint_base + '/field-values'
	data = {'field_id':field_id, 'entity_id':entity_id, 'list_entry_id':list_entry_id, 'value':value}
	return post(call, data)

def update_field_value(field_value_id, value):
# Updates the existing field value with field_value_id with the supplied parameters.
	call = endpoint_base + '/field-values/' + str(field_value_id)
	data = {'value':value}
	return put(call, data)

def delete_field_value(field_value_id):
# Deletes an field value with the specified field_value_id.
	call = endpoint_base + '/field-values/' + str(field_value_id)
	return delete(call)

# ------------------------------------------------------ #
# PEOPLE
# ------------------------------------------------------ #

class Person:
	
	'Contacts of your organization.'
	
	def __init__(self, person_id, person_type, first_name, last_name, emails, phone_numbers, primary_email, organization_ids, list_entries):
		self.id = person_id
		# (integer) The unique identifier of the person object.
		self.type = person_type
		# (integer) The type of person, either (0 - external) or (1 - internal) to your organization.
		self.first_name = first_name
		# (string) The first name of the person.
		self.last_name = last_name
		# (string) The last name of the person.
		self.emails = emails
		# (string[]) The email addresses of the person.
		self.phone_numbers = phone_numbers
		# (string[]) The phone numbers of the person.
		self.primary_email = primary_email
		# (string) The email (automatically computed) that is most likely to the current active email address of the person.
		self.organization_ids = organization_ids
		# (integer[]) An array of unique identifiers of organizations that the person is associated with.
		self.list_entries = list_entries
		# (ListEntry[]) An array of list entry resources associated with the person, only returned as part of the 'Get a specific person' endpoint.

def populate_person(json_in):
	person_out = Person(
		json_in['field_value_id'],
		json_in['field_id'],
		json_in['entity_id'],
		json_in['list_entry_id'],
		json_in['value']
	)
	return person_out

def get_persons(term, page_size, page_token):
# Searches your teams data and fetches all the persons that meet the search criteria.
	call = endpoint_base + 'persons'
	if term:
		call += '?term=' + term
	else:
		print('Usage: get_persons(term, page_size, page_token)')
		return
	if page_size:
		call += '&page_size=' + page_size
	if page_token:
		call += '&page_token=' + page_token
	return get(call)

def get_person(person_id):
# Fetches a person with a specified person_id.
	call = endpoint_base + '/persons/' + str(person_id)
	return get(call)

def create_person(first_name, last_name, emails, phone_numbers, organization_ids):
# Creates a new person with the supplied parameters.
	call = endpoint_base + '/persons'
	data = {'first_name':first_name, 'last_name':last_name, 'emails[]':emails, 'phone_numbers[]':phone_numbers, 'organization_ids[]':organization_ids}
	return post(call, data)

def update_person(person_id, first_name, last_name, emails, phone_numbers, organization_ids):
# Updates an existing person with person_id with the supplied parameters. Only attributes that need to be changed must be passed in.
	call = endpoint_base + '/persons/' + str(person_id)
	data = {'first_name':first_name, 'last_name':last_name, 'emails':emails, 'phone_numbers[]':phone_numbers, 'organization_ids[]':organization_ids}
	return put(call, data)

def delete_person(person_id):
# Deletes a person with a specified person_id.
	call = endpoint_base + '/persons/' + str(person_id)
	return delete(call)

def get_people_global_fields():
# Fetches an array of all the global fields that exist on people.
	call = endpoint_base + '/persons/fields'
	return get(call)

# ------------------------------------------------------ #
# ORGANIZATIONS
# ------------------------------------------------------ #

class Organization:
	
	'An external company that your team is in touch with - this could be an organization that you are trying to invest in, sell to, or establish a relationship with.'
	
	def __init__(self, organization_id, name, domain, person_ids, org_global, list_entries):
		self.id = organization_id
		# (integer) The unique identifier of the organization object.
		self.name = name
		# (integer) The name of the organization (see below).
		self.domain = domain
		# (string) The website name of the organization. 
		self.person_ids = person_ids
		# (string[]) An array of unique identifiers of people that are associated with the organization
		self.org_global = org_global
		# (boolean) Returns whether this organization is a part of Affinity's global dataset of organizations.
		self.list_entries = list_entries
		# (ListEntry[])	An array of list entry resources associated with the organization, only returned as part of the Get a specific organization endpoint.

def populate_organization(json_in):
	try:
		person_ids = json_in['person_ids']
	except KeyError:
		person_ids = ''
	try:
		list_entries = json_in['list_entries']
	except KeyError:
		list_entries = ''

	organization_out = Organization(
		json_in['id'],
		json_in['name'],
		json_in['domain'],
		person_ids,
		json_in['global'],
		list_entries
	)
	return organization_out

def get_organizations(term, page_size, page_token):
# Searches your team's data and fetches all the organizations that meet the search criteria.
	call = endpoint_base + '/organizations'
	if term:
		call += '?term=' + term
	else:
		print('Usage: get_organizations(term, page_size, page_token)')
		return
	if page_size:
		call += '&page_size=' + page_size
	if page_token:
		call += '&page_token=' + page_token
	return get(call)

def get_organization(organization_id):
# Fetches an organization with a specified organization_id.
	call = endpoint_base + '/organizations/' + str(organization_id)
	return get(call)

def create_organization(name, domain, person_ids):
# Creates a new organization with the supplied parameters.
	call = endpoint_base + '/organizations'
	data = {'name':name, 'domain':domain, 'person_ids':person_ids}
	return post(call, data)

def update_organization(organization_id, name, domain, person_ids):
# Updates an existing organization with organization_id with the supplied parameters.
	call = endpoint_base + '/organizations/' + str(organization_id)
	data = {'name':name, 'domain':domain, 'person_ids':person_ids}
	return put(call, data)

def delete_organization(organization_id):
# Deletes an organization with a specified organization_id.
	call = endpoint_base + '/organizations/' + str(organization_id)
	return delete(call)

def get_organizations_global_fields():
# Fetches an array of all the global fields that exist on organizations.
	call = endpoint_base + '/organizations/fields'
	return get(call)


# ------------------------------------------------------ #
# OPPORTUNITIES
# ------------------------------------------------------ #

class Organization:
	
	'A potential future sale or deal for your team, generally used to track the progress of and revenue generated from sales and deals in your pipeline with a specific organization.'
	
	def __init__(self, opportunity_id, name, person_ids, organization_ids, list_entries):
		self.id = opportunity_id
		# (integer) The unique identifier of the opportunity object.
		self.name = name
		# (integer) The name of the opprtunity (see below).
		self.person_ids = person_ids
		# (string[]) An array of unique identifiers of people that are associated with the opportunity.
		self.organization_ids = organization_ids
		# (string[]) An array of unique identifiers of organizations that are associated with the opportunity.
		self.list_entries = list_entries
		# (ListEntry[])	An array of list entry resources associated with the organization, only returned as part of the Get a specific organization endpoint.

def populate_organization(json_in):
	try:
		person_ids = json_in['person_ids']
	except KeyError:
		person_ids = ''
	try:
		organization_ids = json_in['organization_ids']
	except KeyError:
		organization_ids = ''
	try:
		list_entries = json_in['list_entries']
	except KeyError:
		list_entries = ''

	organization_out = Organization(
		json_in['id'],
		json_in['name'],
		person_ids,
		organization_ids,
		list_entries
	)
	return organization_out

def get_opportunities(term, page_size, page_token):
# Searches your team's data and fetches all the opportunities that meet the search criteria.
	call = endpoint_base + '/opportunities'
	if term:
		call += '?term=' + term
	else:
		print('Usage: get_opportunities(term, page_size, page_token)')
		return
	if page_size:
		call += '&page_size=' + page_size
	if page_token:
		call += '&page_token=' + page_token
	return get(call)

def get_opportunity(opportunity_id):
# Fetches an organization with a specified opportunity_id.
	call = endpoint_base + '/opportunities/' + str(opportunity_id)
	return get(call)

def create_opportunities(name, person_ids, organization_ids):
# Creates a new opportunity with the supplied parameters.
	call = endpoint_base + '/opportunities'
	data = {'name':name, 'list_id':list_id, 'person_ids':person_ids, 'organization_ids':organization_ids}
	return post(call, data)

def update_opportunity(organization_id, name, person_ids, orgnaization_ids):
# Updates an existing opportunity with opportunity_id with the supplied parameters.
	call = endpoint_base + '/opportunities/' + str(opportunity_id)
	data = {'name':name, 'person_ids':person_ids, 'organization_ids':organization_ids}
	return put(call, data)

def delete_opportunity(opportunity_id):
# Deletes an opportunity with a specified opportunity_id.
	call = endpoint_base + '/opportunities/' + str(opportunity_id)
	return delete(call)

# ------------------------------------------------------ #
# NOTES
# ------------------------------------------------------ #

class Note:

	'A note object contains content, which is a string containing the note body. In addition, a note can be associated with multiple people or organizations.'
	
	def __init__(self, note_id, creator_id, person_ids, organization_ids, content, created_at):
		self.id = note_id
		# (integer) The unique identifier of the note object.
		self.creator_id = creator_id
		# (integer) The unique identifier of the person object who created the note.
		self.person_ids = person_ids
		# (integer[]) An array of unique identifiers of person objects that are associated with the note.
		self.organization_ids = organization_ids
		# (integer[]) An array of unique identifiers of organization objects that are associated with the note.
		self.content = content
		# (string) The string containing the content of the note.
		self.created_at = created_at
		# (datetime) The string representing the time when the note was created.

def populate_note(json_in):
	note_out = Note(
		json_in['note_id'],
		json_in['creator_id'],
		json_in['person_ids'],
		json_in['organization_ids'],
		json_in['content'],
		json_in['created_at']
	)

def create_note(person_ids, organization_ids, opportunity_ids, content, gmail_id, creator_id):
# Creates a new organization with the supplied parameters.
	call = endpoint_base + '/notes'
	data = {'person_ids':person_ids, 'organization_ids':organization_ids, 'opportunity_ids':opportunity_ids, 'content':content, 'gmail_id':gmail_id, 'creator_id':creator_id}
	return post(call, data)

# ------------------------------------------------------ #
# RELATIONSHIP STRENGTHS
# ------------------------------------------------------ #

def get_relationship_strength(internal_id, external_id):
	call = endpoint_base + '/relationship-strengths'
	if internal_id and external_id:
		call += '?external_id=' + str(external_id) + '&internal_id=' + str(internal_id)
	else:
		print('Usage: get_relationship_strength(internal_id, external_id)')
		return
	return get(call)

# ------------------------------------------------------ #
# ERRORS
# ------------------------------------------------------ #

def check_err(r):
    if r.status_code != 200:
        print "Error:",r.status_code
        print r.text
        return True
    else:
        return False
