# python-recvani
This contains the client side api for use with recvani server. Recvani is collabrative learning platform for any bussiness  where a user and item interact. So client can send score for user interactions and ask for recommendation for user. And all these things in real time.

Check us out  at https://www.recvani.com
## Features
* **Ease to integration:** 

 &nbsp;&nbsp;&nbsp;&nbsp;Integrating is as simple as integrating a database.
* **Real time system:** 
    
 &nbsp;&nbsp;&nbsp;&nbsp;User interaction are taken care within milliseconds for recommendation
* **Can Scale very easily:** 

 &nbsp;&nbsp;&nbsp;&nbsp;It can easily support upto millions of users. 
* **Low on cost:** 

 &nbsp;&nbsp;&nbsp;&nbsp;Cost for deploying will be much less than your inhouse machine learning cost.
* **Support categorization:** 

 &nbsp;&nbsp;&nbsp;&nbsp;Client can easily ask for specific category of item for a user.
    

## Installation
We can directly install python client using pip

    pip install recvani
    

## Examples
Client need model name, client key and model key for connecting to recvani server. You can get these by contacting us.

### Creating connection 

Setting up connection is quite easy. 

    from recvani.rv_client import rv_client
    #Don't forget to replace these by the keys you will get.
    client = rv_client(CLIENT_KEY, MODEL_NAME, MODEL_KEY)
    
### Sending Interacations

#### Send Single Interaction
    
    from recvani.rv_requests import simple_interaction
    import time
    
    USER = "USER1"           # unique id for user
    ITEM = "ITEM1"           # item id (item can be news id, video id, product id etc.)
    SCORE = 1.0              # score client want to give for interaction. Should be devised intelligently
    ITIME = int(time.time()) # time for the interaction in seconds
    
    interaction = simple_interaction(USER, ITEM, SCORE, ITIME)
    
    result = client.send(interaction)  #result will 1 on sucess otherwise exception will be thrown. Better to catch it.

   
#### Send Batch Interactions
    
    from recvani.rv_requests import batch_interaction, simple_interaction
    import time
    
    bi = []
    bi.append(simple_interaction("USER1", "ITEM1", 0.0, int(time.time())))
    bi.append(simple_interaction("USER2", "ITEM1", 1.0, int(time.time())))
    bi.append(simple_interaction("USER1", "ITEM2", 0.0, int(time.time())))
    
    bis = batch_interaction(bi)
    
    result = client.send(bis)


### Sending Parameters


We can attach tags and expiry time for every item
    
#### Send expiry time 
    
    from recvani.rv_requests import exp_request
    import time
  
    EXP_TIME = time.time() + 30*24*3600 # The time you want to expire the item. 
    rexp = exp_request("ITEM1", EXP_TIME)
    result = client.send(rexp)

#### Send tags 

    from recvani.rv_requests import tag_request
    TAGS = ["TAG1", "TAG2"]
    trequest = tag_request("STORY1", TAGS)
    result = client.send(trequest)
    
#### Send in bulk
    
     from recvani.rv_requests import batch_param, item_param
     import time
     
     param1 = item_param("ITEM1", int(time.time()) + 365*24*3600, ["TAG1"])
     param2 = item_param("ITEM2", None, ["TAG2"])
     param3 = item_param("ITEM3", exp_time = int(time.time()) + 365*24*3600)
     
     bparam = batch_param([param1, param2, param3])
     
     result = client.send(bparam)
       


### Getting Result

We can get the final recommendation for the user. We can filter history and send you items for particular tag.

#### Overall Recommendation

    from recvani.rv_requests import rec_request 
    
    USER = "USER1"      # USER ID
    COUNT = 10          # Count of Recommended item to fetch
    TAGS = []           # Tags of item, Empty for overall 
    HISTORY = rec_request.FULL_HISTORY_FILTER     # Will not serve already serverd item.
    
    rc = rec_request(USER, COUNT, [], HISTORY)
    result = client.send(rc) # Result will be list of items
  
#### Tagged Recommedation

    rc = rec_request(USER, COUNT, [["TAG1"]], HISTORY)
    result = client.send(rc) # Will give 10 stories with "TAG1" attached to it  

#### Complex Queries 

Tags can be used to make complex queries. For Example 

    TAGS = [["TAG1", "TAG2"], ["TAG4"]]
    
The inner lists provide intersection and outer lists provide union. The tags above will return  all time which are either marked "TAG4" or have both "TAG1" and "TAG2"  attached to it.


For any help feel free to contact anshuman@recvani.com
 

