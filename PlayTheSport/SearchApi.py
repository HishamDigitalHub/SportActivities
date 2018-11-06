from django.contrib.auth import get_user_model
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import filters
from django.db.models import Q

from ActivityApp.models import Activity, ActivityPreference
from ActivityApp.serializers import ActivityCreateSerializer
from TeamApp.models import Team, TeamPreference
from TeamApp.serializers import TeamCreateSerializer
from UserRegistrationApp.models import Profile, UserPreference
from UserRegistrationApp.serializers import ProfileListSerializer
from VenueApp.models import VenuePreference, Venue
from VenueApp.serializers import VenueCreateSerializer
from lookup.models import City, Country
from math import sin, cos, sqrt, radians, asin

User = get_user_model()


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 15


class SearchFilterView(ObjectMultipleModelAPIView):
    filter_backends = (filters.SearchFilter,)

    search_fields = ('players', 'team', 'name', 'max_distance')
    pagination_class = LimitPagination

    def get_querylist(self):
        pref = self.request.query_params.get('p', None)  # .replace('-', ' ')   # to Activate user preferences
        q = self.request.query_params.get('q', None)  # ['q'].replace('-', ' ')  # string to search
        filter_flg = self.request.query_params.get('f', None)  # ['f'].replace('-', ' ')  # to activate manual filters
        city = self.request.query_params.get('ci', None)  # ['ci'].replace('-', ' ')  # to activate city
        country = self.request.query_params.get('co', None)  # ['a'].replace('-', ' ')  # to activate country
        mx_age = self.request.query_params.get('mx_a', None)  # ['v'].replace('-', ' ')  # to activate max_age
        mi_age = self.request.query_params.get('mi_a', None)  # ['v'].replace('-', ' ')  # to activate minimum_age
        mx_distance = self.request.query_params.get('mx_d', None)  # ['v'].replace('-', ' ')  # to activate max_distance
        gender = self.request.query_params.get('g', None)  # ['g'].replace('-', ' ') # to activate search on spec gender

        # if f == 'true' or f == 'True':
        if pref:  # p should be true in url to activate user preferences
            userpref = UserPreference.objects.get(user=self.request.user)  # to get user preferences as object
            user_sports = userpref.sport.all()  # To  get all sports in user preferences
            user_max_distance = userpref.max_distance  # To  get user_max_distance in user preferences
            user_country = userpref.country  # To  get user_country in user preferences
            user_city = userpref.city_id  # To  get user_city in user preferences
            user_min_age = userpref.min_age  # To  get user_min_age in user preferences
            user_max_age = userpref.max_age  # To  get user_max_age in user preferences
            user_gender = userpref.gender  # To  get user_gender in user preferences

            if filter_flg == 'true' or filter_flg == 'True':
                if gender:
                    user_gender = gender
                if city:
                    user_city = City.objects.get(id=user_city)
                if country:
                    user_country = Country.objects.get(id=user_country.pk)
                if mx_age:
                    user_max_age = mx_age
                if mi_age:
                    user_min_age = mi_age


            print('# # # # # # # # FOR USER: ''  max: ' + str(user_max_distance), '  country: ' + str(user_country),
                  '  city: ' + str(user_city),
                  '  gender: ' + str(user_gender), '  min_age: ' + str(user_min_age),
                  '  max_age: ' + str(user_max_age), )

            # to get team preferences based on user preferences
            if q:
                teampref = TeamPreference.objects.filter(sport__in=user_sports, country=user_country, city=user_city,
                                                         min_age__gte=user_min_age, max_age__lte=user_max_age,
                                                         team__name__contains=q).distinct()
                activitypref = ActivityPreference.objects.filter(sport__in=user_sports, country=user_country, city=user_city,
                                                                 min_age__gte=user_min_age, max_age__lte=user_max_age,
                                                                 activity__name__contains=q).distinct()
                venuepref = VenuePreference.objects.filter(sport__in=user_sports, min_age__gte=user_min_age,
                                                           max_age__lte=user_max_age, venue__name__contains=q).distinct()

            else:
                teampref = TeamPreference.objects.filter(sport__in=user_sports, country=user_country, city=user_city,
                                                         min_age__gte=user_min_age, max_age__lte=user_max_age).distinct()
                activitypref = ActivityPreference.objects.filter(sport__in=user_sports, country=user_country,city=user_city,
                                                                 min_age__gte=user_min_age, max_age__lte=user_max_age).distinct()

                venuepref = VenuePreference.objects.filter(sport__in=user_sports, min_age__gte=user_min_age,
                                                           max_age__lte=user_max_age).distinct()
            if user_gender == 'B':  # if user pref = B or manual select both of genders
                teampref = teampref
                activitypref = activitypref
                venuepref = venuepref
            elif user_gender == userpref.gender:  # if user pref = F or = M regardless of user manual selection because it didnt make any changes
                teampref = teampref.filter(Q(gender=user_gender) | Q(gender='B')).distinct()
                activitypref = activitypref.filter(Q(gender=user_gender) | Q(gender='B')).distinct()
                venuepref = venuepref.filter(Q(gender=user_gender) | Q(gender='B')).distinct()
            else:
                teampref = teampref.filter(
                    Q(gender=user_gender)).distinct()  # if user pref not equal the manual selected gender
                activitypref = activitypref.filter(
                    Q(gender=user_gender)).distinct()
                venuepref = venuepref.filter(
                    Q(gender=user_gender)).distinct()  # if user pref not equal the manual selected gender
            teampref_new = []
            activitypref_new = []
            venuepref_new = []
            if mx_distance:
                user_max_distance = mx_distance

            def haversine(lon1, lat1, lon2, lat2):
                """
                Calculate the great circle distance between two points
                on the earth (specified in decimal degrees)
                """
                # convert decimal degrees to radians
                lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

                # haversine formula
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                c = 2 * asin(sqrt(a))
                r = 6371  # Radius of earth in kilometers. Use 3956 for miles
                return c * r

            user_profile = Profile.objects.get(user=self.request.user)

            center_point = [{'lat': user_profile.latitude, 'lng': user_profile.longitude}]
            radius = int(user_max_distance)  # in kilometer

            for i in range(len(teampref)):

                test_point = [{'lat': teampref[i].team.latitude, 'lng': teampref[i].team.longitude}]

                lat1 = center_point[0]['lat']
                lon1 = center_point[0]['lng']
                lat2 = test_point[0]['lat']
                lon2 = test_point[0]['lng']

                a = haversine(lon1, lat1, lon2, lat2)

                print('Team Distance (km) : ', a)

                if a <= radius:
                    print('Team Inside the area')
                    teampref_new.append(teampref[i])
                else:
                    print('Team Outside the area')
            for i in range(len(activitypref)):

                test_point = [{'lat': activitypref[i].activity.latitude, 'lng': activitypref[i].activity.longitude}]

                lat1 = center_point[0]['lat']
                lon1 = center_point[0]['lng']
                lat2 = test_point[0]['lat']
                lon2 = test_point[0]['lng']

                a = haversine(lon1, lat1, lon2, lat2)

                print('Activity Distance (km) : ', a)

                if a <= radius:
                    print('Activity Inside the area')
                    activitypref_new.append(activitypref[i])
                else:
                    print('Activity Outside the area')
            for i in range(len(venuepref)):

                test_point = [{'lat': venuepref[i].venue.latitude, 'lng': venuepref[i].venue.longitude}]

                lat1 = center_point[0]['lat']
                lon1 = center_point[0]['lng']
                lat2 = test_point[0]['lat']
                lon2 = test_point[0]['lng']

                a = haversine(lon1, lat1, lon2, lat2)

                print('Venue Distance (km) : ', a)

                if a <= radius:
                    print('Venue Inside the area')
                    venuepref_new.append(venuepref[i])
                else:
                    print('Venue Outside the area')

            teams_ids = []
            venues_ids = []
            activities_ids = []
            for i in range(len(teampref_new)):
                teams_ids.append(teampref_new[i].team_id)
            result_teams = Team.objects.filter(pk__in=teams_ids)
            for i in range(len(venuepref_new)):
                venues_ids.append(venuepref_new[i].venue_id)
            result_venues = Venue.objects.filter(pk__in=venues_ids)
            for i in range(len(activitypref_new)):
                activities_ids.append(activitypref_new[i].activity_id)
            result_activities = Activity.objects.filter(pk__in=activities_ids)
            querylist = (
                {'queryset': result_teams.distinct(), 'serializer_class': TeamCreateSerializer},
                {'queryset': result_activities.distinct(), 'serializer_class': ActivityCreateSerializer},
                {'queryset': result_venues.distinct(), 'serializer_class': VenueCreateSerializer},
                # {'queryset': result_users.distinct(), 'serializer_class': ProfileListSerializer},
            )

            return querylist



