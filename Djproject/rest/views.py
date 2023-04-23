from django.shortcuts import redirect, render
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
from httplib2 import Response

 

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "credentials.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection and REDIRECT URL.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
'https://www.googleapis.com/auth/calendar',
'https://www.googleapis.com/auth/calendar.events.readonly',
'https://www.googleapis.com/auth/calendar.events']
REDIRECT_URL = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'





def GoogleCalendarInitView(request):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = REDIRECT_URL

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    return redirect(authorization_url)


def GoogleCalendarRedirectView(request):
    
    state = request.GET.get('state')

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES,state=state)

    # getting the token
    flow.fetch_token(authorization_response=request)
    credentials = flow.credentials

    # Use the credentials to fetch the user's events from the Google Calendar API
    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary').execute()
    
    print(events_result)

    return Response(events_result) 

    
    

    

    






    


