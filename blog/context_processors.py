from django.conf import settings


def oauth_settings(request):
    return {
        'google_client_id': getattr(settings, 'GOOGLE_CLIENT_ID', ''),
        'github_client_id': getattr(settings, 'GITHUB_CLIENT_ID', ''),
    }
