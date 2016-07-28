import json
import logging
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def json_handler(raw_data,data_config):
    #with open(data_name) as data_file:
    data = json.loads(raw_data)

    data_setting = {}
    data_use_cases = []
    selector(data, data_use_cases, data_setting,data_config)
    logging.debug("Finished encoding JSON")

    return data_use_cases


def get_list_setting(data_dict, flag):
    list_agent = []
    for k, v in data_dict.items():
        try:
            logging.debug("Key % --Value %s", k, v)
            if (k ==flag):
                list_agent = v
                return list_agent
        except KeyError as ae:
            logging.debug("ERROR: %", ae)
    return []


def selector(data, data_use_cases,data_setting,data_config):
    try:
        for k,v in data.items():
            if (k=='Simulation'):
                iterator(v,data_use_cases, data_setting,data_config, k)
    except AttributeError as abc:
        logging.debug("////// ERROR %s", abc)


def iterator(data, data_use_cases, data_setting, data_config, prev, preprev=""):
    if(type(data) == type({}) or type(data) == type({}.items())):
        #logging.debug("Dict: %s Prev: %s Preprev: %s", data, prev, preprev)
        #logging.debug("DataSetting: %s", data_setting)
        x = ''
        y = ''
        lx = ''
        ly = ''
        try:
            for k,v in data.items():
                #logging.debug("DataSetting FOR: %s", data_setting)

                if (type(v) is type(0) ):
                    if (preprev == 'UseCase'):
                        if (k=='x'):
                            x = v
                        elif (k=='y'):
                            y = v
                        elif (k=='lx'):
                            lx = v
                        elif (k=='ly'):
                            ly = v
                        else:
                            logging.debug("\nDefault: %s",v)
                        try:
                            if (any(data_setting[prev])):
                                pass

                        except KeyError as ke:
                            data_setting[prev] = []
                    else :
                        logging.debug("CONFIG %s: %s",k, v)
                        data_config[k]=[]
                        data_config[k].append(v)
                elif type(v) is str:
                    data_setting[k]=[]
                    data_setting[k].append(v)

                else:
                    iterator(v, data_use_cases,data_setting,data_config, k, prev)
            #Storing the values of X,Y into the list of the dictionary.
            if(preprev == 'UseCase'):
                data_setting[prev].append((x,y,lx,ly))
        except AttributeError as err: #FOR k,v
            logging.debug("Err: %s",err)
    elif (type(data) == type([])):
        #logging.debug("List:", data)
        for i,j in enumerate(data):
            iterator(data[i], data_use_cases,data_setting,data_config, prev, preprev)
            if (prev == "UseCase"):
                # Storing the use cases into a list.
                # Several use cases can be stored in this list (data_use_cases).
                data_use_cases.append(data_setting)
                # The data_setting is reset before starting the new loop
                # because a new fresh data_setting must be stored in the use case list
                data_setting = {}

    else:
        logging.debug("Default: %s Data: %s", type(data), data)
