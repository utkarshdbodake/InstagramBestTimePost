'''
Created on 10-Sep-2015

@author: utkarsh
'''
from rest_framework.response import Response
from instagram_service.utils.logger import logger
import traceback
import  requests, json
import datetime
import unidecode

weekdays_dict = {0: 'Monday',
                 1: 'Tuesday',
                 2: 'Wednesday',
                 3: 'Thursday',
                 4: 'Friday',
                 5: 'Saturday',
                 6: 'Sunday',}

created_hour_list = {0: 0,
                     1: 0,
                     2: 0,
                     3: 0,
                     4: 0,
                     5: 0,
                     6: 0,}

def handle_request(request_dict):
    '''
    handles the GET request for best time to post
    '''
    try:
        logger.info("request_dict is: " + str(request_dict))
        #user_id = unidecode.unidecode(str(request_dict))
        user_id = request_dict['id']
        try:
            check = int(user_id)
        except:
            user_dict = search_user(user_id)
            user = user_dict['data'][0]
            user_id = user['id']
        print 'user_id is: ' + str(user_id)

        user_info_dict = get_user_info(user_id)
        print 'user_info:\n\n' + json.dumps(user_info_dict, indent=4, sort_keys=True)

        user_followers_dict = get_user_followers(user_id)
        print 'user_followers:\n\n' + json.dumps(user_followers_dict, indent=4, sort_keys=True)
        user_followers_list = user_followers_dict['data']
        user_ids_followers = []
        for follower in user_followers_list:
            user_ids_followers.append(follower['id'])

        print user_ids_followers
        print len(user_ids_followers)

        frequency_of_active_days = []
        frequency_of_active_hours_dict = {}


        for follower_id in user_ids_followers:
            most_active_day, most_active_hour = get_most_active_day_and_time(follower_id)
            print "-"*90
            frequency_of_active_days.append(most_active_day)
            if most_active_day in frequency_of_active_hours_dict.keys():
                frequency_of_active_hours_dict[most_active_day] = (frequency_of_active_hours_dict[most_active_day] + most_active_hour)/2
            else:
                frequency_of_active_hours_dict[most_active_day] = most_active_hour

        print "\n\n" + "="*90
        global weekdays_dict
        print frequency_of_active_days
        #print frequency_of_active_hours
        highest_frequency_of_active_day = max(set(frequency_of_active_days), key=frequency_of_active_days.count)
        #highest_frequency_of_active_hour = max(set(frequency_of_active_hours), key=frequency_of_active_hours.count)
        print highest_frequency_of_active_day
        print "*"*90
        result =  "User should Post on : %s @ %s hr" % (weekdays_dict[highest_frequency_of_active_day],
                                                        frequency_of_active_hours_dict[highest_frequency_of_active_day])
        print result
        print "*"*90
        return Response({"result": result})
    except:
        logger.info(traceback.format_exc())


def get_user_followers(user_id):
    '''
    Gets the followers of the User .
    '''
    headers = {'content-type':'application/json'}
    url = 'https://api.instagram.com/v1/users/' + user_id + '/followed-by?access_token=311097588.53dfd03.040d705da6c04ba4873d91fe1bafa0a9'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print response


def get_user_recent_post(user_id):
    '''
    Gets the recent media/post of the given User .
    '''
    headers = {'content-type':'application/json'}
    url = 'https://api.instagram.com/v1/users/' + user_id + '/media/recent/?access_token=311097588.53dfd03.040d705da6c04ba4873d91fe1bafa0a9'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print response

def get_most_active_day_and_time(user_id):
    '''
    Gets the most active day of the User
    '''
    try:
        print "Processing user_id: " + str(user_id)
        user_recent_post_dict = get_user_recent_post(user_id)
        user_recent_post_list = user_recent_post_dict['data']
        created_day_list = []
        created_hour_dict = {}
        for e in user_recent_post_list:
            d = datetime.datetime.fromtimestamp(int(e['created_time']))
            week_day = datetime.datetime.fromtimestamp(int(e['created_time'])).weekday()
            created_day_list.append(week_day)
            if week_day in created_hour_dict.keys():
                created_hour_dict[week_day] = (created_hour_dict[week_day] + d.hour)/2
            else:
                created_hour_dict[week_day] = d.hour
        #Monday is 0 and Sunday is 6
        print "Posted on day: " + str(created_day_list)
        print "Posted on hour: " + str(created_hour_dict)

        most_active_day = max(set(created_day_list), key=created_day_list.count)
        most_active_hour = created_hour_dict[most_active_day]
    except:
        #print traceback.format_exc()
        most_active_day = 6
        most_active_hour = 18
    print "Most Active Day: " + str(most_active_day)
    print "Most Active Hour: " + str(most_active_hour)
    return most_active_day, most_active_hour

def get_user_info(user_id):
    '''
    Gets the info of the User .
    '''
    headers = {'content-type':'application/json'}
    url = 'https://api.instagram.com/v1/users/' + user_id + '/?access_token=311097588.53dfd03.040d705da6c04ba4873d91fe1bafa0a9'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print response


def search_user(search_name):
    '''
    Gets the json of similar names
    '''
    headers = {'content-type':'application/json'}
    url = 'https://api.instagram.com/v1/users/search?q=' + search_name + '&access_token=311097588.53dfd03.040d705da6c04ba4873d91fe1bafa0a9'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print response