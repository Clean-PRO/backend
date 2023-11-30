from django.db.models import QuerySet
from rest_framework.authtoken.models import Token
from transliterate import translit

from api.utils import create_password
from cleanpro.settings import (
    SOCIAL_AUTH_LOGIN_REDIRECT_URL, SOCIAL_USER_FIELDS,
    SOCIAL_USER_PASSWORD_CYCLES,
)
from users.models import User
from django.shortcuts import redirect


def create_user_social_pipeline(strategy, details, backend, *args, **kwargs):
    """
    Пользовательский pipeline для обработки данных OAuth2.
    Создает нового пользователя с указанным email, если не существует.
    Перенаправляет на главную страницу сайта,
    передает токен доступа в качестве query параметра.
    """
    user_data: dict[str, any] = {
        field: details.get(field, kwargs.get(field))
        for field in SOCIAL_USER_FIELDS
    }
    user: QuerySet = User.objects.filter(email=user_data.get('email'))
    if user.exists():
        user: User = user.first()
    else:
        username: str = translit(
            value=(
                f"{user_data.get('first_name').strip()} "
                f"{user_data.get('last_name').strip()}"
            ),
            language_code='ru',
        )
        user: User = User.objects.create(
            username=username,
            email=user_data.get('email'),
        )
        user.set_password(
            raw_password=create_password(
                email=user_data.get('email'),
                cycles=SOCIAL_USER_PASSWORD_CYCLES,
            )
        )
        user.save()
    token, _ = Token.objects.get_or_create(user=user)
    redirect_url = f'{SOCIAL_AUTH_LOGIN_REDIRECT_URL}?token={token.key}'
    return redirect(redirect_url)


"""OAuth backend fields documentation."""


github_backend_name = 'github'

github_details_keys_example = {
    'username': 'TheSuncatcher222',
    'email': 'TheSunCatcher222@gmail.com',
    'fullname': 'Kirill Svidunovich',
    'first_name': 'Kirill',
    'last_name': 'Svidunovich',
}

github_kwargs_keys_example = {
    'response': {
        'access_token': str,
        'token_type': str,
        'scope': 'user:email',
        'login': 'TheSuncatcher222',
        'id': int,
        'node_id': str,
        'avatar_url': 'https://avatars.githubusercontent.com/u/123456789?v=4',
        'gravatar_id': '',
        'url': 'https://api.github.com/users/TheSuncatcher222',
        'html_url': 'https://github.com/TheSuncatcher222',
        'followers_url': 'https://api.github.com/users/TheSuncatcher222/followers',    # noqa (E501)
        'following_url': 'https://api.github.com/users/TheSuncatcher222/following{/other_user}',    # noqa (E501)
        'gists_url': 'https://api.github.com/users/TheSuncatcher222/gists{/gist_id}',    # noqa (E501)
        'starred_url': 'https://api.github.com/users/TheSuncatcher222/starred{/owner}{/repo}',    # noqa (E501)
        'subscriptions_url': 'https://api.github.com/users/TheSuncatcher222/subscriptions',    # noqa (E501)
        'organizations_url': 'https://api.github.com/users/TheSuncatcher222/orgs',    # noqa (E501)
        'repos_url': 'https://api.github.com/users/TheSuncatcher222/repos',    # noqa (E501)
        'events_url': 'https://api.github.com/users/TheSuncatcher222/events{/privacy}',    # noqa (E501)
        'received_events_url': 'https://api.github.com/users/TheSuncatcher222/received_events',    # noqa (E501)
        'type': str,
        'site_admin': bool,
        'name': 'Kirill Svidunovich',
        'company': None,
        'blog': '',
        'location': None,
        'email': 'TheSuncatcher222@gmail.com',
        'hireable': bool,
        'bio': str,
        'twitter_username': str,
        'public_repos': int,
        'public_gists': int,
        'followers': int,
        'following': int,
        'created_at': '2000-01-00T00:00:00Z',
        'updated_at': '2000-01-00T00:00:00Z',
    },
    'user': str,
    'storage': "<class 'social_django.models.DjangoStorage'>",  # Без скобок ("").    # noqa (E501)
    'is_new': bool,
    'request': "<WSGIRequest: GET '/oauth/complete/github/?code=<code>&state=<state>'>",  # Без скобок ("").  # noqa (E501)
    'pipeline_index': int,
    'uid': int,  # Совпадает с id.
    'social': None,
    'new_association': bool,
    'username': 'TheSuncatcher222',
}
