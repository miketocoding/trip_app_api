# Memory Lane

Past travels application. I've always loved traveling and reminiscing on them afterwards. Sometimes we forget about aspects of our trips away and that's why I created Memory Lane. With my app, users will be able to keep trip data in one place such as location, start and end dates, trip rating, other travelers, and standouts from the adventure.

## User Stories
- As a user, I want to be able to create a trip post
- As a user, I want to be able to see all posts I’ve made
- As a user, I want to be able to update a specific post i’ve made
- As a user I want to be able to delete a post
- As a user, I want to see trip posts i’ve been tagged in

## Links
- [Deployed Client](https://miketocoding.github.io/trip-app-client/#/)
- [Deployed API](https://trip-app-api-capstone.herokuapp.com/)
- [Front-end Client Repository](https://github.com/miketocoding/trip-app-client)
- [Back-end API Repository](https://github.com/miketocoding/trip_app_api)

## List of Technologies used
- HTML, CSS, JavaScript, React, Bootstrap, Python, PostgreSQL, Django, Git, GitHub, Heroku, Postman

## List of Unsolved Problems
- (Reach goal) Unable to get react charts library working for v1 but will implemented in v2

## Planning, Process, and Problem-Solving Strategy
I came into this process as methodical as I could. For the planning portion, I layed out an app idea that at its base would be a travel blog with the potential to grow into a much more well rounded product. The initial stage would be to complete the minimum viable product(MVP) of CRUD then move on to additional functionality when all requirements were met.

My process started with completing the backend API using Python, PostgreSQL, and Django. Throughout this, I used Postman to test my CRUD on trip resource instead of the standard curl-scripts. Once everything worked, I moved onto my React front-end client. Using Hooks, I then coded the front-end CRUD, added some functionality with search, and styled my app mainly using Bootstrap.

My problem-solving strategy revolved around reading the docs, google the issues to see if they were solved by others, leaning on my cohort, and if none of the other options solved my problem, submit an issue ticket to see if an instructor would be able to assist. In most instances this solved any barriers to progression.


## Images
### Entity Relationship Diagram
![Trip App ERD](https://github.com/miketocoding/trip-app-client/blob/main/travel-app-erd.png?raw=true)

## Catalog of Routes the API expects
```JavaScript
# Restful routing
path('mangos/', Mangos.as_view(), name='mangos'),
path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
path('sign-up/', SignUp.as_view(), name='sign-up'),
path('sign-in/', SignIn.as_view(), name='sign-in'),
path('sign-out/', SignOut.as_view(), name='sign-out'),
path('change-pw/', ChangePassword.as_view(), name='change-pw'),
# our urls
path('trips/', Trips.as_view(), name='trips'),
path('trips/<int:pk>/', TripDetail.as_view(), name='trip_detail'),
```

```JavaScript
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
```

## Setup and Installation Instructions for back-end Application
First step is to download the Django-auth-template. From here user is to `pipenv shell` and then install all required packages. We then need to create a database and set up our .env file with our env name, db name and secret. Once completed we then push our existing repo to GitHub by following the instructions on the GitHub website.

To deploy, we need to install gunicorn, create a Procfile, and migrate. Once this is done we will run `python manage.py collectstatic` then install the whitenoise package. After this we will `pipenv run pip freeze > requirements.txt` and create heroku app with `heroku apps:create trip-app-api-capstone`. Then add PostgreSQL `heroku addons:create heroku-postgresql:hobby-dev`, config keys, then finall deploy using `git push heroku main`.

## Creator
Michael Van Le
