from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.views import SocialLoginView
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from IMDB.models import User, Movie, Rating, Celebrity
from IMDB.serializers import UserSerializer, CreateUserSerializer, MovieSerializer, RatingSerializer, \
    CelebritySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class MovieRating(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            rating = Rating.objects.get(user=request.data['user'], movie=request.data['movie'])
        except Rating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):

        user = User.objects.get(id=request.data['user'])
        movie = Movie.objects.get(id=request.data['movie'])

        old_rating = Rating.objects.filter(user=request.data['user'], movie=request.data['movie'])
        if old_rating.exists():
            # As old rating exists, remove it from average rating
            old_rating = old_rating[0]
            if movie.number_of_reviews == 1:
                movie.average_rating = 0
                movie.number_of_reviews = 0
            else:
                movie.average_rating = ((movie.average_rating * movie.number_of_reviews) -
                                        old_rating.rating) / (movie.number_of_reviews - 1)
                movie.number_of_reviews = movie.number_of_reviews - 1
        else:
            old_rating = Rating.objects.create(user=user, movie=movie, rating=request.data['rating'])

        movie.average_rating = ((movie.average_rating * movie.number_of_reviews) +
                                request.data['rating']) / (movie.number_of_reviews + 1)
        movie.number_of_reviews = movie.number_of_reviews + 1
        old_rating.rating = request.data['rating']
        old_rating.save()
        movie.save()
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class ListMovies(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ListCelebrities(generics.ListAPIView):
    queryset = Celebrity.objects.all()
    serializer_class = CelebritySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveMovie(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class Watchlist(APIView):

    def get(self, request, user_id,  *args, **kwargs):
        if user_id:
            user = User.objects.get(id=user_id)
            watchlist_ids = user.watchlist
            watchlist_movies = []
            for id in watchlist_ids:
                movie = Movie.objects.get(id=id)
                watchlist_movies.append(movie)
            watchlist_movies = MovieSerializer(watchlist_movies, many=True)
            return Response(watchlist_movies.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        movie_id = request.data['movie_id']
        user_id = request.data['user_id']
        user = User.objects.get(id=user_id)
        message = ''
        if movie_id in user.watchlist:
            user.watchlist.remove(movie_id)
            message = 'Removed from watchlist'
        else:
            user.watchlist.append(movie_id)
            message = 'Added to watchlist'
        user.save()
        return Response({'message': message})


@method_decorator(csrf_exempt, name='dispatch')
class LoginUser(APIView):

    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user:
            serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            return Response({'user': serializer.data, 'token': str(refresh.access_token)})
        return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        username = request.data['email']
        first_name = request.data['givenName']
        last_name = request.data['familyName']
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)

        user.save()
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data, 'token': str(refresh.access_token)})


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def post(self, request, *args, **kwargs):
        username = request.data['email']
        first_name = request.data['name']
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(username=username, first_name=first_name, email=email)

        user.save()
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data, 'token': str(refresh.access_token)})


class SearchMovieView(APIView):
    """
    Searches and returns movies as per search query
    """
    def get(self, request, query, genre='', rating=0):
        if query:
            movies = Movie.objects.filter(name__icontains=query)
            if genre:
                movies = movies.filter(genre__icontains=genre)
            if rating:
                movies = movies.filter(average_rating__gte=rating)
            if movies.exists():
                movies = MovieSerializer(movies, many=True)
                return Response(movies.data)
            else:
                return Response({'invalid_query': 'No data found.'})
        return Response({'error': 'Query is invalid.'})
