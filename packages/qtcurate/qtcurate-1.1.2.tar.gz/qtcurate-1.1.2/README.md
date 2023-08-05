# qtcurate-sdk-python
Python SKD for Search and Data extraction

## Theia documentation; Overview and Definitions
**Theia** is a managed solution to mine and retrieve Entities* or Typed Entities** out of unstructured data. In the following we cover details of configuring and submitting data mining jobs via Python SDK

***Entity** : An entity is a word or phrase and *can be* associated with a meaning. For example, "AWS" is an entity and it can be associated with "Amazon Inc."

****Typed Entity** : An entity that is meaningful only if it co-occurs with a number, date or another entity. For example, "Revenue" is considered a Typed Entity only if it is found in a context where the actual dollar value is reported:

>Amazon Inc reported $68.8 billion in revenue

## Table of content

- [Installation](#installation)
- [Authentication](#authentication)
- [Data Dictionaries](#data-dictionaries)
- [Create a New Dictionary](#create-a-new-dictionary)
- [Upload a TSV Dictionary File](#upload-a-tsv-dictionary-file)
- [Update an Existing Dictionary](#update-an-existing-dictionary)
- [Delete a Dictionary](#delete-a-dictionary)
- [List Available Dictionaries](#list-available-dictionaries)
- [Fetch dictionary](#fetch-dictionary)
- [Extraction and Mining](#extraction-and-mining)
- [Mining Content Files](#mining-content-files)
- [Mining Web URLs](#mining-web-urls)
- [Mining Data Streams](#mining-data-streams)
- [Extracting Typed Entities](#extracting-typed-entities)
- [Status Monitoring](#status-monitoring)
- [Searching in the Results](#searching-in-the-results)
- [Exporting the Results](#exporting-the-results)
- [Exporting in Excel Format](#exporting-in-excel-format)
- [Exporting in JSON](#exporting-in-json)
- [Clear temporary data](#clear-temporary-data)


### Installation

You can install it with pip. You have to have Python 3.5 or above
```
pip install qtcurate
```

### Authentication

Valid API key is required for all operations.

#### Request


If API key is valid, than the response will be `HTTP 200` containing user profile data.

If API key is missing or not valid, the endpoint will return `HTTP 401`:

#### Response

```
{
"error": "unauthorized",
"error_description": "Full authentication is required to access this resource"
}
```


"Net Revenue" is a Typed Entity:

```
"Apple reported net revenue of $53.3 billion in 2018."
```

"Net Revenue" is not a Typed Entity:

```
"Tim Cook will go over net revenue of Apple in the upcoming conference call."
```


### Entity Dictionaries

Entity dictionaries are lists of entities that can be used in a data mining task. Each item of a entity dictionary has a `key` and a `value`. The `key` is the associated or normalized phrase and the `value` is the actual word or phrase that represents the entity.

**Theia** scans all input utterances for every word or phrase in the dictionary and if found, map it to the associated value:

Dictionary (one item):
```M&A => merger and acquisition```

Input utterance:

>Merger and acquisitions report published in 2019.

The above will be labeled with `M&A`

**Theia** uses various strategies for matching of dictionary values allowing users to configure the fuzziness of search. User can also provide a list of synonyms and stop phrases for the value matching. For example, you can only have "Apple Inc" as one entity in your dictionary and provide "inc", "corp", "corporation" and "company" as synonyms, allowing you to find all occurrences of "Apple the Company", "Apple Corporations" and "Apple Corp" in the content.


Entity dictionaries can be created in two ways:
- By providing dictionary entries in the request payload
- By uploading a TSV file containing dictionary entries in the format of `key<TAB>value`.

### Data Dictionaries

Authentication with API KEY
```
dic = QtDict(api_key='1234567')
```

#### Create A New QtDict
Create data dictionaries with create() function
First we prepare data
Name is required.
```
dic.name("Name of QtDict)
```
Two ways to create entries
```
key = "some key"
value = "some value"
dic.add_entry(key, value)
```
or
```
tmp_dictionary = {"key": "some key", "value": "some value"}
dic.entries(tmp_dictionary)
```
where method entries take a Python dictionary with 2 elements where KEYS have string value "key" and "value"
After that we can create our QtDict
```
dic.create()
```
#### Response

```
{
"id": "58608b1f-a0ff-45d0-b12a-2fb93af1a9ad",
"key": "user-example-com/58608b1f-a0ff-45d0-b12a-2fb93af1a9ad.csv.gz",
"name": "Name of dictionary",
"global": false,
"entries": [
{
"key": "some key",
"value": "some value"
}
]
}
```

#### Upload a TSV Dictionary File

Upload TSV data dictionaries with upload function:
```
dic.upload("file-path.tsv", "Name of dictionary")
```
TSV is required file format. Response is the same as create function response.

#### Update an Existing QtDict

To update an existing QtDict:
```
dic.update("58608b1f-a0ff-45d0-b12a-2fb93af1a9ad")
```
We use ID as argument of function.

#### Delete a QtDict

To delete an existing QtDict:
```
dic.delete("58608b1f-a0ff-45d0-b12a-2fb93af1a9ad")

```
#### List Available Dictionaries:

To list all of your existing dictionaries:
```
dic.list()
```
Response is a list of dictionaries
```
[
{
"id": "58608b1f-a0ff-45d0-b12a-2fb93af1a9ad",
"key": "user-example-com/58608b1f-a0ff-45d0-b12a-2fb93af1a9ad.csv.gz",
"name": "My dictionary",
"global": false,
"entries": []
}
{
...
}
]
```

#### Fetch QtDict:
To fetch data from the QtDict
```
dic.fetch("58608b1f-a0ff-45d0-b12a-2fb93af1a9ad")
```
Response
```
{
"id": "58608b1f-a0ff-45d0-b12a-2fb93af1a9ad",
"key": "user-example-com/58608b1f-a0ff-45d0-b12a-2fb93af1a9ad.csv.gz",
"name": "My dictionary",
"global": false,
"entries": []
}
```

### Extraction and Mining

Data extraction and mining is the process of identifying entities found in the unstructured content using entity dictionaries and formatting them it into structured format. Unstructured data can be streamed from content files, data APIs or directly from public URLs.

Authenticate with API_KEY

```
tag = DataProcess(api_key="1234")
```

#### Mining Content Files

First, upload all content files for DataProcess:
```
tag.upload("file.pdf")
```

PDF, TXT and HTML formats are supported.

#### Response

```
{
"uuid": "c351283c-330c-418b-8fb7-44cf3c7a09d5",
"fileName": "file.pdf",
"link": "http://portal.document.quantxt.amazonaws.com/user@example.com/c351283c-330c-418b-8fb7-44cf3c7a09d5",
"date": "2019-10-25T20:14:41.925+02:00",
"contentType": "application/pdf",
"source": "file.pdf"
}
```

Now you can mine data via dictionaries. First you have to prepare additional options.
`title` is optional but it is highly recommended for easier distinction between different tagging jobs.

`vocabValueType` (Optional): can have one of the following values: `NONE`, `STRING`, `DOUBLE`, `DATETIME`. If set, the engine will extract only entities that are associated with an entity of this type.
`vocabPath` (Required): The path to entity QtDict. Path is returned either after creation of a new QtDict or via listing of existing dictionaries.**There is no limit on the number of files and dictionaries that can be processed via tagging_files function**
```
tag.files("c351283c-330c-418b-8fb7-44cf3c7a09d5")
tag.title("My data mining with files and dictionaries")
tag.search_rule("user-example-com/58608b1f-a0ff-45d0-b12a-2fb93af1a9ad.csv.gz", DictionaryType.NONE)

tag.tagging_files()
```
#### Response

```
{
"index": "puvqrjfhqq",
"title": "My data mining with files and dictionaries",
"get_phrases": true,
"maxTokenPerUtt": 35,
"minTokenPerUtt": 6,
"excludeUttWithoutEntities": false,
"stitle": null,
"files": ["c351283c-330c-418b-8fb7-44cf3c7a09d5"],
"searchDictionaries": [
{
"vocabPath": "user-example-com/58608b1f-a0ff-45d0-b12a-2fb93af1a9ad.csv.gz",
"vocabValueType": "NONE"
}
]
}
```

`index` represents the unique identification for the container that holds output labeled data.
You can set index, autotag, maxTokenPerUtt, minTokenPerUtt, excludeUttWithoutEntities with following methods:
```
tag.index("some index")
tag.autotag(True)
tag.exclude_utt_without_entities(True)
tag.max_token_per_utt(101)
tag.min_token_per_utt(101)
tag.stitle("some stitle string")
```


**Request parameters:**

`chunk`
(Optional, string) can be `SENTENCE` or `PARAGRAPH` or `NONE`. This will result in splitting of data into semantic chunks before processing. For example, this allows user to split the content of an article in semantic sentences and apply entity dictionaries at sentence level.

`excludeUttWithoutEntities`
(Optional, boolean) if `true` the output will only include chunks that have at least one label from the input dictionaries.

`get_phrases`
(Optional, boolean) if `true` auto tagging will be performed.

`minTokenPerUtt` (Optional, int)

`maxTokenPerUtt` (Optional, int)

`stitle` (Optional, string) Override command.

To delete a data container:
```
tag.delete("puvqrjfhqq")
```

#### Mining Web URLs:

Mining can be performed on a list of URLs. All parameters used in tagging files are applicable here.
```
tag.mining_url()
```

**Theia can process both static and dynamic web pages. However, a number of websites use mechanisms to block webpage scrapping. Theia built-in Web parser is not designed to bypass such blocking mechanisms**

#### Mining Data Streams

Tagging data from data streams such as third party APIs is supported. Please contact <support@quantxt.com> for details.


#### Extracting Typed Entities

Entity dictionaries allow the user to quickly search and label thousands of phrases in unstructured content. There are cases when users want to label a keyword or phrase as an entity only if it is associated with a value. For example:

A "release => "Manufactured" dictionary item will label both of the following utterances:

> The first automobile in the US **released** by Ford.
> The first automobile in the US **released** in 1908 by Ford.

However, if the user is looking for only release year of the car makers, the first utterance won't have much use for him. He can only label the second utterance using a **Typed Entities**.

Supported types for associated entities are:

`REGEX`, `DOUBLE`, `DATETIME`

types are passed via `vocabValueType` parameter.

If a type is set, a dictionary item will be extracted only if a type is found in its close proximity.
In the above example, user can set *vocabValueType* in the request to `DOUBLE` to identify **1908** only if it is associated with the entity **released**

#### Status Monitoring

The progress endpoint allows user to check the progress of a submitted data mining job:

#### Request

```
tag.progress()
```

The search result is an array of active data mining jobs:

```
[
{
"index": "cjaejhvtao",
"progress": 36,
"progress_msg": "Collecting data..."
}
]

```

`index` Unique ID of the running job

`progress`  Progress in % (a number between 0 to 100).

`progress_msg` (Optional) Progress message.


It is also possible to check the progress of a specific data mining job:

#### Request

```
tag.progress("cjaejhvtao")
```

#### Response

```
{
"index": "cjaejhvtao",
"progress": 36,
"progress_msg": "Collecting data..."
}
```

### Searching in the Results


The search endpoint allows user to run full-text and [faceted search](https://en.wikipedia.org/wiki/Faceted_search) in the extracted data.

#### Request

```
tag.search("puvqrjfhqq", param_from, size, f1, f2)
```

**Request parameters:**

`q`
(Optional, string) Search query that filters the main content `title` field. It supports boolean `OR`, `AND` and `NOT` parameters.

`f`
(Optional, string) Query filters must be used in pairs. Filters are created for each input dictionary. For example, to include results that have one or more label from `Vehicle` dictionary the request should look like: `&f=Vehicle&f=*`. To include results that are labeled with `Ford` or `BMW` from the `Vehicle` dictionary, the request would be `&f=Vehicle&f=BMW&f=Vehicle&f=Ford`

`from`
(Optional, int) Offset for paging results. Defaults to 0. Each page contains 20 items.

`size`
(Optional, int) Number of results to return. Maximum is 200.


#### Response

```
{
"Total": 2610,
"results": [
{
"title": "The Federal Reserve Bank of New York provides gold custody to several central banks, governments and official international organizations on behalf of the Federal Reserve System.",
"id": "Wv8fBG4Bc3WI8L9MbaO2",
"link": "https://www.hamilton.edu/news/story/hamilton-nyc-program-tours-federal-reserve-museum",
"score": 0.10268514747565982,
"source": "abc15.com",
"date": "2018-05-24T00:00:00.000Z",
"tags": [
"Federal Reserve",
"New York"
]
}
],
"aggs": {
"Tag": [{
"key": "Central bank",
"count": 878
}, {
"key": "Gold",
"count": 523
}
}
}
```

`Total`: Number of results.

`result []`: The array that contains result items.

`aggs` : Facets over the results with count of items for each facet.


### Exporting the Results

Results can be exported in XLSX or JSON format:

#### Exporting in Excel Format

```
tag.report_to_xlsx("puvqrjfhqq", "name-of-output-file.xlsx")
```


#### Exporting in JSON

```
tag.report_to_json("puvqrjfhqq", "name-of-output-file.json")

```

### Clear temporary data
Both classes QtDict and DataProcess have a method clear() to delete all used variable.
```
dic.clear()
tag.clear()
```
The export output is limited to 5000. All `/search` parameters can be passed here to export the desired slice of the data.


For technical questions please contact <support@quantxt.com>
