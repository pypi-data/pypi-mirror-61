Greendeck-Logging:
---
![Greendeck](https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/gd_transparent_blue_bg.png)  ![logging]

### Install from pip
https://pypi.org/project/greendeck-logging/

```pip install greendeck-logging```

This library can be used for save the critical log, message, info data for your internal services in elasticsearch and create a nice visualization through kibana.
For creating  visualization in kibana you can refer this  [documentation](https://www.elastic.co/guide/en/kibana/current/createvis.html)

if you don't have elasticsearch and kibana you can refer this  [blog](https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html)

### How to use?
##### import the library
```
from greendeck_logging import GdLogging
from greendeck_logging import GdLoggingStack
```

### There are Two ways to save the log data, by bulk (*GdLoggingStack*) and one by one ( *GdLogging*)

If you want to save the log in memory as stack and send data after process completes, use **GdLoggingStack**. It saves the log messages in stack and send to elastic search on calling push method.

### Variables to connect elasticsearch to store the log data
    LOG_ECS_HOST =  < YOUR_LOG_ECS_HOST >
    LOG_ECS_INDEX = < LOG_ECS_INDEX >
    LOG_ECS_TYPE = < LOG_ECS_TYPE >
    service_name = < service_name >

>  if elasticsearch requires username and password to connect, provide in LOG_ECS_HOST in a standard format like  [https://username:password@elasticsearch_host:port_no]() Eg : [https://admin:admin123@127.0.0.0:9200/]()


Some Default Values are :
> LOG_ECS_INDEX = gdlogging,  LOG_ECS_TYPE  = '_doc'

if you want save data in other index name instead of gdlogging , assign  **LOG_ECS_INDEX = "your index name"**

**GdLoggingStack :**  Send the bulk log data to elasticsearch
```
from greendeck_logging import GdLoggingStack
gdl_stack = GdLoggingStack(LOG_ECS_HOST = LOG_ECS_HOST,
                          service_name = service_name  
                          LOG_ECS_INDEX = "gdlogging",
                          LOG_ECS_TYPE = "_doc",
                          )
```
> **default value:
      LOG_ECS_INDEX = 'gdlogging',
      LOG_ECS_TYPE = '_doc',

> ##### **LOG_ECS_TYPE and SERVICE_NAME are required field


#### Methods and their functionality

There are following function for capturing the events

- For capturing Error message and info of the error due to which occur ,  
` gdl_stack.error("your message", info = {}, value = 1) `  
default, value = 1, info = {} # info can be dictionary

- To save Debug message and send the object as info    
` gdl_stack.debug("your debug message", info = {}, value = 1) `  

- To increament the response status of the services like 200, 404 etc   
` gdl_stack.counter_message(message, info = {}, value = 1)`  
default, value = 1  

- To increment the  message  for a particular ```website ```  ( It can be your unique identifier depending on requirement )   
`gdl_stack.counter_website(website, message, info = {}, value = 1)`  
default, value = 1

- clear the stack  
`gdl_stack.clear()`  

- total element in stack  
`gdl_stack.count()`  

- show the first element in the stack  
`gdl_stack.show_one()`  

- show all elements in the stack  
`gdl_stack.show()`  

- push all elements to elastic search  
`gdl_stack.push()`  

> ** Don't forget to push the element to elastic search at end of your stack, use `gdl_stack.push()` for update the data in elastic search

**GdLogging** : It updates one element at a time

```
from greendeck_logging import GdLogging
gdl = GdLogging(LOG_ECS_HOST = LOG_ECS_HOST,
                          service_name = service_name  
                          LOG_ECS_INDEX = "gdlogging",
                          LOG_ECS_TYPE = "_doc",
                          )
```

> **default value:
      LOG_ECS_INDEX = 'gdlogging',
      LOG_ECS_TYPE = '_doc',

### Usage and functionality  

There are following function for capturing the events  

- For capturing Error message and info due to which occur  
`gdl.error("your message", info = {}, value = 1) `  
default, value = 1 , info = {}  

- For capturign Debug message  
` gdl.debug("your message", info = {}, value = 1) `
default, value = 1  

- To increament the response status of the services like 200, 404 etc  
` gdl.counter_message(message, info = {}, value = 1)`  
default, value = 1  

- To increment the  message  for a particular ```website ```  ( It can be your unique identifier depending on requirement )   
`gdl.counter_website(website, message, info = {}, value = 1)`  
default, value = 1   

Example of the object which will save into the elastic search

         "_index" : "gd_logging",
            "_type" : "_doc",
            "_id" : "0TASCGsBFBI3I7B8680B",
            "_score" : 2.3312538,
            "_source" : {
              "service_name" : "class_service",
              "log_type" : "info",
              "created_at" : "2019-05-30T14:59:45.452035",
              "meta" : {
                "file_name" : "service.py",
                "user_name" : "user",
                "system_name" : "user-300-15ISK",
                "os_name" : "Linux"
              },
              "counter_status" : {  
                "message" : "response status",
                "counter_type" : "status",
                "counter_name" : "201",
                "counter_value" : 1
              }
            }
          }
