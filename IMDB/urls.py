from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from IMDB import views
from IMDB.views import LoginUser, MovieRating, ListCelebrities, GoogleLogin, FacebookLogin, Watchlist, SearchMovieView


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('ratings', views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('movies/', views.ListMovies.as_view()),
    path('movies/<int:pk>/', views.RetrieveMovie.as_view()),
    path('login/', LoginUser.as_view(), name='login_view'),
    path('rating/', MovieRating.as_view(), name='get_rating_view'),
    path('celebrities/', ListCelebrities.as_view(), name='celebrities'),
    path('accounts/', include('allauth.urls')),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('add_watchlist/', Watchlist.as_view(), name='add_to_watchlist'),
    path('add_watchlist/<int:user_id>/', Watchlist.as_view(), name='get_watchlist'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('search/<str:query>', SearchMovieView.as_view(), name='search-movies'),
    path('search/<int:rating>/<str:query>', SearchMovieView.as_view(), name='search-movies'),
    path('search/<str:genre>/<str:query>', SearchMovieView.as_view(), name='search-movies'),
    path('search/<str:genre>/<int:rating>/<str:query>', SearchMovieView.as_view(), name='search-movies'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
