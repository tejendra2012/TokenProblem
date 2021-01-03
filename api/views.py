from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import secrets
from django.utils import timezone
from datetime import timedelta
from .models import Token
import redis


def event_handler(msg):
    print("Handler", msg)
    try:
        key = msg["data"].decode("utf-8")
        print(key)
        if "releaseKey:" in key:
        	key = key.replace("releaseKey:","")
        	token = r.get(key)
        	tokenObj = Token.objects.get(token=token.decode("utf-8"))
        	tokenObj.activate = False
        	tokenObj.update_time = timezone.now()
        	tokenObj.save()
        if "removeKey:" in key:
        	key = key.replace("removeKey:","")
        	token = r.get(key)
        	tokenObj = Token.objects.get(token=token.decode("utf-8"))
        	tokenObj.delete()
        # Once we got to know the value we remove it from Redis and do whatever required
        r.delete(key)
        print("Got Token: ", token)
    except Exception as exp:
    	print(exp)

r = redis.Redis()
pubsub = r.pubsub()
pubsub.psubscribe(**{"__keyevent@0__:expired": event_handler})
pubsub.run_in_thread(sleep_time=0.01)


class CreateTokenView(APIView):
	def get(self, request):
		create_token = secrets.token_hex(20)
		token = Token(token = create_token,update_time=timezone.now())
		token.save()
		r.set(create_token,create_token)
		r.setex("removeKey:"+create_token,timedelta(seconds=300),value=create_token)
		return Response({'Token': create_token})

class AssignTokenView(APIView):
	def post(self, request):
		request_data = request.data
		if 'username' not in request_data:
			return Response({'detail':'username parameter is missing'},status=status.HTTP_400_BAD_REQUEST)
		username = request_data['username']
		if r.exists(username):
			tokenData = r.get(username)
			updateObj = Token.objects.get(token=tokenData)
			updateObj.activate = True
			updateObj.update_time = timezone.now()
			updateObj.username = username
			updateObj.save()
			r.set(username , tokenData)
			r.setex("releaseKey:"+username,timedelta(seconds=60),value=tokenData)
			r.setex("removeKey:"+tokenData,timedelta(seconds=300),value=tokenData)
			return Response({'Token':tokenData},status=status.HTTP_200_OK)
		try:
			tokenObj = Token.objects.filter(activate=False)
			if len(tokenObj) == 0:
				return Response({'detail':'token not exists'},status=status.HTTP_404_NOT_FOUND)
			else:
				tokenData = tokenObj[0].token
				updateObj = Token.objects.get(token=tokenData)
				updateObj.activate = True
				updateObj.update_time = timezone.now()
				updateObj.username = username
				updateObj.save()
				r.set(username,tokenData)
				r.setex("releaseKey:"+username,timedelta(seconds=60),value=tokenData)
				r.setex("removeKey:"+tokenData,timedelta(seconds=300),value=tokenData)
				return Response({'Token':tokenData},status=status.HTTP_200_OK)
		except:
			pass
			
		

class UnblockTokenView(APIView):
	def post(self, request):
		request_data = request.data
		if 'Token' not in request_data:
			return Response({'detail':'Token parameter is missing'},status=status.HTTP_400_BAD_REQUEST)
		elif 'username' not in request_data:
			return Response({'detail':'username parameter is missing'},status=status.HTTP_400_BAD_REQUEST)
		else:
			token = request_data['Token']
			username = request_data['username']

			if r.exists("releaseKey:"+username):
				r.expire("releaseKey:"+username, timedelta(seconds=1))
			try:
				tokenObj = Token.objects.get(token=token)
				tokenObj.activate = False
				tokenObj.update_time = timezone.now()
				tokenObj.save()
				return Response({'Unblock-Token': request_data['Token']})
			except Token.DoesNotExist:
				return Response({'detail':'token not exists'},status=status.HTTP_404_NOT_FOUND)

class RemoveTokenView(APIView):
	def post(self, request):
		request_data = request.data
		if 'Token' not in request_data:
			return Response({'detail':'Token parameter is missing'},status=status.HTTP_400_BAD_REQUEST)
		elif 'username' not in request_data:
			return Response({'detail':'username parameter is missing'},status=status.HTTP_400_BAD_REQUEST)
		else:
			username = request_data['username']
			token = request_data['Token']
			if r.exists("releaseKey:"+username):
				r.expire("releaseKey:"+username,timedelta(seconds=1))
			if r.exists("removeKey:"+token):
				r.expire("removeKey:"+token,timedelta(seconds=1))
				return Response({'Removed-Token': request_data['Token']})
			else:
				try:
					tokenObj = Token.objects.get(token=token)
					tokenObj.delete()
					return Response({'Removed-Token': request_data['Token']})
				except Token.DoesNotExist:
					return Response({'detail':'token not exists'},status=status.HTTP_404_NOT_FOUND)

		

class KeepaliveTokenView(APIView):
	def post(self, request):
		request_data = request.data
		if 'Token' not in request_data:
			return Response({'detail':'Token parameter is missing'},status=status.HTTP_400_BAD_REQUEST)
		elif 'username' not in request_data:
			return Response({'detail':'username parameter is missing'},status=status.HTTP_400_BAD_REQUEST)
		else:
			token = request_data['Token']
			username = request_data['username']
			try:
				tokenObj = Token.objects.get(token=token)
				if r.exists("releaseKey:"+username):
					r.setex("releaseKey:"+username,timedelta(seconds=60),value=token)
					r.setex("removeKey:"+token,timedelta(seconds=300),value=token)
					return Response({'Keep-Alive-Token': request_data['Token']})
				else:
					return Response({'detail':'token is unblocked'},status=status.HTTP_404_NOT_FOUND)
			except Token.DoesNotExist:
				return Response({'detail':'token not exists'},status=status.HTTP_404_NOT_FOUND)

		
