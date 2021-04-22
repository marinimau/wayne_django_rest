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
      "id": {$CONTACT_INSTANCE},
      "user": {$WAYNE_ACCOUNT},
      "required": {$REQUIRED_ACCOUNT_FLAG},
      "creation_timestamp": {$CREATION_TIMESTAMP},
      "platform": {$EMAIL_PROVIDER},
      "value": {$EMAIL_ADDRESS}
    },
    
    ...
    
    {
      "id": {$CONTACT_INSTANCE},
      "user": {$WAYNE_ACCOUNT},
      "required": {$REQUIRED_ACCOUNT_FLAG},
      "creation_timestamp": "2021-01-04T14:58:24.457715Z",
      "platform": {$EMAIL_PROVIDER},
      "value": {$EMAIL_ADDRESS}
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
      "id": {$CONTACT_INSTANCE},
      "user": {$WAYNE_ACCOUNT},
      "required": {$REQUIRED_ACCOUNT_FLAG},
      "creation_timestamp": {$CREATION_TIMESTAMP},
      "platform": "{$USERNAME_IN_THE_PLATFORM}",
      "value": "{$USERNAME_IN_THE_PLATFORM}"
    },
    
    ...
     
    {
      "id": {$CONTACT_INSTANCE},
      "user": {$WAYNE_ACCOUNT},
      "required": {$REQUIRED_ACCOUNT_FLAG},
      "creation_timestamp": {$CREATION_TIMESTAMP},
      "platform": "{$USERNAME_IN_THE_PLATFORM}",
      "value": "{$USERNAME_IN_THE_PLATFORM}"
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
      "bio": {$USER_BIO},
      "location": {$USER_LOCATION},
      "cellular": {$USER_CELLULAR},
      "gender": {$USER_GENDER},  // M, F or U
      "birth_date": {$USER_BIRTH_DATE},  // YYYY-MM-DD
      "url_img_profile": {$URL_IMG_PROFILE},
      "email_confirmed": {$EMAIL_CONFIRMED_FLAG}
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
      "id": {$CONTACT_INSTANCE},
      "user": {$WAYNE_ACCOUNT_OF_THE_OWNER},
      "required": {$REQUIRED_ACCOUNT_FLAG},
      "creation_timestamp": {$CREATION_TIMESTAMP},
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
      "id": {$CONTACT_INSTANCE},
      "user": {$WAYNE_ACCOUNT_OF_THE_OWNER},
      "required": {$REQUIRED_ACCOUNT_FLAG},
      "creation_timestamp": {$CREATION_TIMESTAMP},
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
