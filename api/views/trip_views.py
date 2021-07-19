from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.trip import Trip
from ..serializers import TripSerializer

# Create your views here
class Trips(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = TripSerializer
    def get(self, request):
        """Index request"""
        # get all trips
        print('you are in index request')
        trips = Trip.objects.filter(owner=request.user.id)
        data = TripSerializer(trips, many=True).data
        return Response({ 'trips': data })

    def post(self, request):
        """Create request"""
        # add user to request data object
        print("value of request.data['trip']", request.data['trip'])
        # print("value of request.data['trip']['data']", request.data['trip']['data'])
        request.data['trip']['owner'] = request.user.id
        # serialize/create trip
        trip = TripSerializer(data=request.data['trip'])
        if trip.is_valid():
            trip.save()
            return Response({ 'trip': trip.data }, status=status.HTTP_201_CREATED)
        return Response(trip.errors, status=status.HTTP_400_BAD_REQUEST)

class TripDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        print('You are in Show')
        trip = get_object_or_404(Trip, pk=pk)
        if not request.user.id == trip.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this trip post')
        data = TripSerializer(trip).data
        return Response({ 'trip': data })

    def delete(self, request, pk):
        """Delete request"""
        trip = get_object_or_404(Trip, pk=pk)
        if not request.user.id == trip.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this trip')
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Trip
        # get_object_or_404 returns a object representation of our Trip
        trip = get_object_or_404(Trip, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == trip.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this trip')

        # Ensure the owner field is set to the current user's ID
        request.data['trip']['owner'] = request.user.id
        # Validate updates with serializer
        data = TripSerializer(trip, data=request.data['trip'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
