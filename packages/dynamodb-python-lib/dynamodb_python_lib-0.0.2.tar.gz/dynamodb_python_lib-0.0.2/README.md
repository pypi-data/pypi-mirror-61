# dynamodb-python-lib

### Jobs
[Kumo](https://console.kumo.expedia.biz/apps/dynamodb-python-lib) | [Pipeline](https://console.kumo.expedia.biz/apps/dynamodb-python-lib/pipeline)

| Job | Status |
| --- | ------ |
| [Scan](https://primer.builds.tools.expedia.com/job/dynamodb-python-lib-all/) | [![Build Status](https://primer.builds.tools.expedia.com/buildStatus/icon?job=dynamodb-python-lib-all)](https://primer.builds.tools.expedia.com/job/dynamodb-python-lib-all/lastBuild/) |
| [Build](https://primer.builds.tools.expedia.com/job/dynamodb-python-lib-master/)|[![Build Status](https://primer.builds.tools.expedia.com/buildStatus/icon?job=dynamodb-python-lib-master)](https://primer.builds.tools.expedia.com/job/dynamodb-python-lib/lastBuild/) |
| [Deploy](https://gcobuild-jenkins.sb.karmalab.net:8443/job/dynamodb-python-lib/) | [![Build Status](https://gcobuild-jenkins.sb.karmalab.net:8443/buildStatus/icon?job=dynamodb-python-lib)](https://gcobuild-jenkins.sb.karmalab.net:8443/job/dynamodb-python-lib/lastBuild/) |

### Proxy Class
This is the primary class constructor that will provide access to various methods used for CRUDE (Create, Read, Update, Delete, Export) operations on the CP NLU data set stored in DynamoDB.
 
### Parameters
##### query_params *[dict]*
The key "index" is required to have a value that corresponds to a field in the DynamoDB table. Whatever field is used as a value must also have a key/value respresentation. In the example code, the index is "intent" so a corresponding key/value must also be present and in this case *"intent": "amenities"* is provided.
 
##### ready_only *[bool]*
If True, an additional filter will be added that limits items returned from the query to only those with a status of "ready".
 
### Return Value
##### dataframe
 Provides access to data from DynamoDB, limited by query_params, in a pandas.DataFrame object.
 
### Example Code

##### Query Sample
    from dynamodb_python_lib.proxy import Proxy
    
    # select *
    # from cpnlu_UnderstandingData (Using intent index)
    # where intent="amenities"
    # and (product="flight" or product="lodging")
    # and sentiment="positive"
    query_dict = {
        "index": "intent",
        "intent": "amenities",
        "product": ["flight", "lodging"],
        "sentiment": ["positive"]
    }
    
    proxy = Proxy.get_instance(table_name="cpnlu_UnderstandingData", aws_region="us-west-2")
    df = proxy.query(query_dict)
    
    selected_column = ["utterance", "intent"]
    df = df[selected_column]
    df.to_csv("query_result.csv", encoding="UTF-8", index=False)
    
##### Insert Sample
```
proxy = Proxy.get_instance(table_name="cpnlu_UnderstandingData", aws_region="us-west-2")

record = {
    "locale": locale,
    "utterance": utterance,
    # more fields if you want
}
proxy.insert(record)
```

##### Update Sample
```
proxy = Proxy.get_instance(table_name="cpnlu_UnderstandingData", aws_region="us-west-2")

record = {
    "locale": locale,
    "utterance": utterance,
    # more fields if you wish
}
proxy.update(record)
```

### Version History
- 0.0.1 - Very first version with select, insert, update and local_dynamo_db
- 0.0.2 - Added annotating, cleaning, scoring and level 1 tagging utilities