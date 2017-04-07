'''
Created on 10-Sep-2015

@author: utkarsh
'''
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from instagram_service.service_api_handlers.get_best_time_to_post_handler import handle_request
from instagram_service.utils.logger import logger
import json
import traceback


class BestTimeToPost(APIView):

    def get(self, request):
        '''
        Gets the best time to post w.r.t. the query data
        '''
        try:
            logger.info("GET Best Time To Post")
            request_dict = json.loads(request.GET.values()[0])
            if request_dict:
                return handle_request(request_dict)
            else:
                logger.info("Nothing found for given query data")
                return Response("No Results matching the search query",
                                status.HTTP_204_NO_CONTENT)
        except:
            logger.error(traceback.format_exc())
            return Response("Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
