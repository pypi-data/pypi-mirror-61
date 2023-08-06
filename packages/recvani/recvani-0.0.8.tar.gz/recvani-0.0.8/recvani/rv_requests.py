
class base_request(object):
    
    def get_method(self):
        raise NotImplementedError("get_method must be implemented to return string")

    def get_params(self):
        raise NotImplementedError("get_params must be implemented to return array")

    def _get_params(self):
        result = self.get_params()
        assert (type(result) == list), "Params must be a list"
        return result

class simple_interaction(base_request):
    
    def __init__(self, uid, eid, score, time):
        self.uid = uid
        self.eid = eid
        self.score = score
        self.time = time

    def get_method(self):
        return "save"

    def get_params(self):
        dt = {"uid": self.uid, "eid": self.eid, "score": self.score, "time": self.time}
        return [dt]

class batch_interaction(base_request):

    def __init__(self, interaction_arr = []):
        self.arr = interaction_arr

    def append(self, interaction):
        self.arr.append(interaction)

    def clear():
        self.arr = []

    def get_method(self):
        return "save_batch"

    def get_params(self):
        return [[x.get_params()[0] for x in self.arr]]

class tag_request(base_request):
    
    def __init__(self, eid, tags):
        self.eid = eid
        self.tags = tags

    def get_method(self):
        return 'set_tag'

    def get_params(self):
        return [self.eid, self.tags]

class exp_request(base_request):
    
    def __init__(self, eid, exp):
        self.eid = eid
        self.exp = exp

    def get_method(self):
        return 'set_exp'

    def get_params(self):
        return [self.eid, self.exp]

class rec_request(base_request):

    FULL_HISTORY_FILTER =  -100
    NO_HISTORY_FILTER  = -1

    def __init__(self, uid, count, tags, historyFilterTime=FULL_HISTORY_FILTER ):
        self.uid = uid
        self.count = count
        self.tags = tags
        self.historyFilterTime = historyFilterTime

    def get_method(self):
        return 'get_rec'

    def get_params(self):
        return [{"uid":self.uid, "count":self.count, "tags":self.tags, "history":self.historyFilterTime}]

class item_param():
    def __init__(self, eid, exp_time=None, tags=None):
        self.eid = eid
        self.exp_time = exp_time
        self.tags = tags

    def get_params(self):
        result = {"eid": self.eid}
        if (self.exp_time != None):
            result["exp_time"]  = self.exp_time
        if (self.tags != None):
            result["tags"] = self.tags
        return result

    
class batch_param(base_request):

    def __init__(self, params  ):
        self.params = params

    def get_method(self):
        return 'set_batch_param'

    def get_params(self):
        return [[param.get_params() for param in self.params]]

