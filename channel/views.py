from django.shortcuts import render

# Create your views here.




class SearchChannel(APIView):
    permission_classes = []

    def get(self, request, format=None):
        try:
            from django.db.models import Q
            query = request.GET['query']  # string
            search_caregory = ''
            if request.GET.get('search_category') != None:
                search_caregory = request.GET['search_category']
            data = []
            if (request.GET.get('search_category') != None) or (search_caregory !=''):
                #  ch = Channel.objects.filter(consultant==)
                Channels = Channel.objects.filter(consultant__user_type=search_caregory).filter(
                    Q(name__icontains=query) | Q(description__icontains=query))
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'consultant_full_name': channel.consultant.first_name + " " + channel.consultant.last_name,
                        'invite_link': channel.invite_link,
                        'channelID': channel.pk,
                        'avatar': channel.avatar.url if channel.avatar else None,
                    })
            else:
                Channels = Channel.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'consultant_full_name': channel.consultant.first_name + " " + channel.consultant.last_name,
                        'invite_link': channel.invite_link,
                        'channelID': channel.pk,
                        'avatar': channel.avatar.url if channel.avatar else None,

                    })

            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll Check it later!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


