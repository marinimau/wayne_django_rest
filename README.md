# Wayne Django Rest

Wayne is a REST-API project. It aims to store contact information (social, email and telephone) for each user.

## Endpoints

#### Public

##### Get public email accounts of a given user:
```
GET https://oudi.herokuapp.com/api/v1/public/get/{$USERNAME}/account/email_based
```

response:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "user": {$WAYNE_ACCOUNT},
      "required": false,
      "creation_timestamp": "2021-01-04T13:32:38.423757Z",
      "platform": "GMAIL",
      "value": "email1@gmail.com"
    },
    {
      "id": 4,
      "user": 25,
      "required": false,
      "creation_timestamp": "2021-01-04T14:58:24.457715Z",
      "platform": "GMAIL",
      "value": "email2@gmail.com"
    }
  ]
}
```


##### Get username based social account of a given user
```
GET https://oudi.herokuapp.com/api/v1/public/get/{$USERNAME}/account/username_based
```

response:
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {$WAYNE_ACCOUNT},
      "required": false,
      "creation_timestamp": "2021-01-04T14:26:30.866510Z",
      "platform": "FACEBOOK",
      "value": "facebook_username"
    }
  ]
}
```


##### Get user detail:
```
GET https://oudi.herokuapp.com/api/v1/public/get/{$USERNAME}/detail
```

response:
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "user": {$WAYNE_ACCOUNT},
      "bio": "user bio",
      "location": "Cagliari",
      "cellular": null,
      "gender": "U",
      "birth_date": 1997-04-24,
      "url_img_profile": null,
      "email_confirmed": true
    }
  ]
}
```


##### Reverse lookup by email (find user ID and username of the owner of a given email):
```
GET https://oudi.herokuapp.com/api/v1/public/reverse/email_based/${EMAIL_PROVIDER}/{$EMAIL_ADDRESS}
```

response:
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {$WAYNE_ACCOUNT_OF_THE_OWNER},
      "required": false,
      "creation_timestamp": "2021-01-04T14:26:30.866510Z",
      "platform": "{$EMAIL_PROVIDER}",
      "value": "{$EMAIL_ADDRESS}"
    }
  ]
}
```

important: EMAIL_PROVIDER must be a value of Email Provider Enumeration


##### Reverse lookup by username (like email lookup)
```
 GET https://oudi.herokuapp.com/api/v1/public/reverse/username_based/{$SOCIAL_PLATFORM}/{$USERNAME_IN_THE_GIVEN_SOCIAL_PLATFORM}
```

response:
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {$WAYNE_ACCOUNT_OF_THE_OWNER},
      "required": false,
      "creation_timestamp": "2021-01-04T14:26:30.866510Z",
      "platform": "{$SOCIAL_PLATFORM}",
      "value": "{$USERNAME_IN_THE_GIVEN_SOCIAL_PLATFORM}"
    }
  ]
}
```

important: SOCIAL_PLATFORM must be a value of Social Platform Enumeration


## Author

[Mauro Marini](https://github.com/marinimau)
 
 ## License
 
 [MIT](https://github.com/marinimau/wayne_django_rest/blob/master/LICENSE)
