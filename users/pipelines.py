from io import BytesIO

from PIL import Image

from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthException, AuthForbidden

from geekshop.settings import MEDIA_URL
from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'personal', 'photo_max_orig')),
                    access_token=response['access_token'], v=5.131)), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass

    if data['about']:
        user.userprofile.about = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

    age = timezone.now().date().year-bdate.year
    user.age = age
    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['personal']:
        langs = data['personal']['langs']
        langs_str = ', '.join(str(lang) for lang in langs)

        user.userprofile.language = langs_str

    if data['photo_max_orig']:
        image_url = data['photo_max_orig']
        path_dir = 'vk_auth_photo/'
        root = 'media/'
        filename_full = image_url.split('/')[-1]
        filename = filename_full.split('?')[0]
        photo_file = path_dir + filename
        img_data = requests.get(image_url).content
        with open(root + photo_file, 'wb') as handler:
            handler.write(img_data)

        user.image = photo_file

    user.save()
