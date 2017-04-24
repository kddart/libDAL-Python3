#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""
 * dalclient library - provides utilities to assist in using KDDart-DAL servers
 * Copyright (C) 2017  Diversity Arrays Technology
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from diversityarrays.dalclient.DefaultDALClient import DefaultDALClient
from diversityarrays.dalclient.ResponseType import ResponseType
from diversityarrays.dalclient.DALResponseVisitor import DALResponseVisitor
from diversityarrays.dalclient.DALResponseException import DALResponseException
from diversityarrays.dalclient.DALEntityBuilder import DALEntityBuilder
import getpass

__author__ = "alexs"
__copyright__ = "Copyright (C) 2017  Diversity Arrays Technology"
__license__ = "GPL 3.0"
__email__ = ""

"""
Below is the example login for DALClient along with some basic listing commands
and response handling
"""

resultsPerPage = 10

# URL of the KddartInstance
url = "YOUR_URL"

# Username for User
user = input("Please enter username: ")

# Password (entered)
password = getpass.getpass()

# Initialising client and setting the URL
client = DefaultDALClient(debug=1)
client.URL = url

# Setting response content type to .json
client.reponse_type = ResponseType(xmlTrue=False)

# Logging In
client.login(user, password)

# Queries the dal for a response to list Genus's
dalResponse = client.perform_query("list/genus")

# Building a visitor function and passing it in to visit the response records (Genus's)
# If the visitor function returns True, it means continue, this way a visitor loop can be
# Broken once a specific entity is found.
def visitorFunction(responseRecord):
    print("Row data for object ->" + str(responseRecord.rowdata))
dalResponse.visit_response(DALResponseVisitor(visitorFunction))

# List to be populated
genuses = []

# Building a visitor function and passing it in to visit the response records (Genus's)
# Here though Class objects reflecting the entity e.g. Genus, are created dynamically for use.
# Also, the visitor function always returns ture, meaning we want to visit every entity returned.
def visitorFunction(genus):
    genuses.append(genus)
    print("Genus name for found entity: " + str(genus.GenusName))
    return True

dalResponse.visit_entities(DALResponseVisitor(visitorFunction))

# Queries the dal to get Specimen with id: 424856 (May not be applicable to your Kddart)
dalResponse = client.perform_query("get/specimen/%s" % "424856")

# Building a visitor function and passing it in to visit the response records (Specimen's)
def visitorFunction(specimen):
    print("Specimen name " + str(specimen.SpecimenName))
    print("Pedigree: " + str(specimen.Pedigree))
    print("Filial generation: " + str(specimen.FilialGeneration))
    return True

    # DAL provides entities with nested data sometimes.
    # This can be useful. In the example of Specimen, its
    # Genotype is returned as nested data (This is also dynamically turned into an object):
    specimenGenotype = specimen.Genotype[0]

    print("Genotype name: " + str(specimenGenotype.GenotypeName))
    print("Genotype Id: " + str(specimenGenotype.GenotypeId))

dalResponse.visit_entities(DALResponseVisitor(visitorFunction))

# using Site Id (This may not be applicable to your Kddart)
siteId = 1

# Listing Trials for Site 1
dalResponse = client.perform_query("site/%s/list/trial" % siteId)

# Printing Id and Name of Trials for site 1
def visitorFunction(trial):
    print("Found Trial Id: " + trial.TrialId)
    print("Found Trial Name: " + trial.TrialName)
    return True

dalResponse.visit_entities(DALResponseVisitor(visitorFunction))

# Uploading a new Genus (For other entities check the APIDoc at www.Kddart.org)
newGenusData = {"GenusName":"Dartian"}
response = client.perform_update("add/genus", newGenusData)

# Lets set the Id's for the new Genus (returned by dal)
print(str(response.returned_ids))
returnedIds = response.returned_ids
for idObject in returnedIds:
    # Setting a new Id field
    idFieldName = idObject[DefaultDALClient.ATTR_PARA_NAME]
    id = idObject[DefaultDALClient.ATTR_VALUE]

    # Adding to the map of to-be attributes for the new object
    newGenusData[idFieldName] = id

# We can use this to build a new Genus object from the entity data
entityBuilder = DALEntityBuilder()
genusObject = entityBuilder.build_entity("Genus", newGenusData)

# Lets look at the new entity!
print("New genus Id in Kddart -> " + genusObject.GenusId)

# If we attempt to add the a Genus of the same name again, we get an error:
try:
 response = client.perform_update("add/genus", newGenusData)
except DALResponseException as e:
    pass

# Exporting samples for all Trial's available (This may not be applicable to your Kddart - if you have no Trial data)
response = client.perform_query("export/samplemeasurement/csv")

# Output files to collect for download (DAL creates the file on the fly following the export query)
outputFiles = response.output_files

# Download the content. It is returned, or you can specify a file to write the data to
content = client.download_file(outputFiles[0]["csv"], localFile="./TrialData.csv")


