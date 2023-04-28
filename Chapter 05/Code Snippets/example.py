import sys

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    CorsOptions,
    EntityRecognitionSkill,
    IndexingParameters,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SearchFieldDataType,
    SearchIndex,
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SearchIndexerSkillset,
    SimpleField,

)


def create_skillset():
    s1 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="organizations",
                                                                 target_name="organizationsS1")])
    s2 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="people",
                                                                 target_name="peopleS2")])
    s3 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="locations",
                                                                 target_name="locationsS3")])
    s4 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="keyphrases",
                                                                 target_name="keyphrasesS4")])
    s5 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="language",
                                                                 target_name="languageS5")])
    s6 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="translated_text",
                                                                 target_name="translated_textS6")])
    s7 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="pii_entities",
                                                                 target_name="pii_entitiesS7")])
    s8 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="masked_text",
                                                                 target_name="masked_textS8")])
    s9 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                outputs=[OutputFieldMappingEntry(name="merged_content",
                                                                 target_name="merged_contentS9")])
    s10 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                 outputs=[OutputFieldMappingEntry(name="normalized_images/*/text",
                                                                  target_name="textS10")])
    s11 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                 outputs=[OutputFieldMappingEntry(name="normalized_images/*/layoutText",
                                                                  target_name="layoutTextS11")])
    s12 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                 outputs=[OutputFieldMappingEntry(name="normalized_images/*/imageTags/*/name",
                                                                  target_name="imageTagsS12")])
    s13 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                 outputs=[OutputFieldMappingEntry(name="normalized_images/*/imageCaption",
                                                                  target_name="imageCaptionS13")])
    s14 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                 outputs=[OutputFieldMappingEntry(
                                     name="normalized_images/*/imageCelebrities/*/detail/celebrities/*/name",
                                     target_name="imageCelebritiesS40")])
    s15 = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                 outputs=[OutputFieldMappingEntry(name="metadata_storage_path",
                                                                  target_name="filepath")])

    new_skillset = SearchIndexerSkillset(name='cog-search-skillset', skills=list(
        [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]), description="cog-search skillset")
    result = indexer_client.create_skillset(new_skillset)
    return result


def create_datasource():
    container = SearchIndexerDataContainer(name='files')
    data_source_connection = SearchIndexerDataSourceConnection(
        name="files-data-source-connection",
        type="azureblob",
        connection_string=connection_string,
        container=container
    )
    return indexer_client.create_data_source_connection(data_source_connection)


def create_indexer():
    name = "cog-search-indexer"
    parameters = IndexingParameters(configuration={"parsingMode": "jsonArray"})
    new_indexer = SearchIndexer(
        name=name,
        data_source_name=datasource,
        target_index_name=index,
        skillset_name=skillset,
        parameters=parameters
    )
    indexer_client.create_indexer(new_indexer)
    return name


def run_indexer():
    indexer_client.run_indexer(indexer)
    print("Ran the Indexer '{}'".format(indexer))


def create_index() -> SearchIndex:
    fields = [
        SimpleField(name="metadata_storage_path", type=SearchFieldDataType.String, key=True),
    ]

    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profiles = []

    new_index = SearchIndex(
        name=index_name,
        fields=fields,
        scoring_profiles=scoring_profiles,
        cors_options=cors_options)

    return index_client.create_index(new_index)


def search_index(query: str) -> list:
    returned_list = list()
    client = SearchClient(endpoint=endpoint,
                          index_name=index_name,
                          credential=credential)
    results = client.search(search_text=query)

    for result in results:
        returned_list.append(result)

    return returned_list


def main():
    try:
        index_client.get_index(index_name)
    except ResourceNotFoundError:
        print("Missing index ({}), creating...".format(index_name))
        create_index()

    results = search_index("Garbo")

    if len(results) < 1:
        sys.exit("No results found, exiting...")

    for r, result in enumerate(results):
        print("\n***************\n* Document {} *\n***************\n".format(r + 1))
        for k, v in result.items():
            if k in skipped_keys:
                continue
            print(k)
            if isinstance(v, list) or isinstance(v, dict):
                for i in v:
                    print("    " + str(i))
            else:
                print("    " + str(v))


if __name__ == "__main__":
    # Get the service endpoint and API key from the environment
    endpoint = "https://cogsrch-oceansmart.search.windows.net"
    key = "13A3A3BBA0179ADDA7C6BD50EEA57BB7"
    connection_string = "DefaultEndpointsProtocol=https;AccountName=sacogsrch;AccountKey=c8lRpS5/Y127dhsOP/YUem4Ukv9/9blJDVU/iTwXO+CUkM998LUND6Qo4ChQzqbE3DYO7XX7cEr9GD22eRYqPA==;EndpointSuffix=core.windows.net"
    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(endpoint, credential)
    indexer_client = SearchIndexerClient(endpoint, credential)
    index_name = "azureblob-index"

    skipped_keys = (
        "layoutText",
        "content",
        "merged_content",
        "text",
        "translated_text",
        "masked_text",
    )

    # skillset = create_skillset().name
    # datasource = create_datasource().name
    # index = create_index().name
    # indexer = create_indexer()
    # run_indexer()
    # indexer_client.get_indexer_status(indexer)
    main()
