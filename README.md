# Wayne Django Rest

Wayne is a REST-API project. It aims to store contact information (social, email and telephone) for each user.

## Endpoints

#### Public

##### Get public email accounts of a given user:
```
GET https://oudi.herokuapp.com/api/v1/public/get/{$USERNAME}/account/email_based
```

response:
```
200 OK

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
      "creation_timestamp": {$CREATION_TIMESTAMP},
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
200 OK

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

##### Get user basic info:
```
GET https://oudi.herokuapp.com/api/v1/public/get/ottavio
```

response:
```
200 OK

{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": {$WAYNE_ACCOUNT},
      "email": {$MAIN_EMAIL_ADDRESS},
      "username": {$WAYNE_USERNAME},
      "is_active": {$ACCOUNT_ACTIVE_FLAG},
      "first_name": {$FIRST_NAME},
      "last_name": {$LAST_NAME},
      "date_joined": {$REGISTRATION_TIMESTAMP}
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
200 OK

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
200 OK

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
200 OK

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


#### User

##### User registraiton
```
POST https://oudi.herokuapp.com/api/v1/user/

HEADER:
Content-type: multipart/form-data

BODY:
multipart : {
  "username": {$USERNAME},
  "email": {$EMAIL},
  "password": {$PASSWORD}
  "password2": {$PASSWORD}
}

```

response:
```
201 CREATED

{
  "id": {$USER_ID},
  "email": {$EMAIL},
  "username": {$USERNAME},
  "is_active": false,
  "first_name": "",
  "last_name": "",
  "date_joined": {$REGISTRATION_TIMESTAMP}
}
```

**check email for activate your account



##### Activate account

```
GET https://oudi.herokuapp.com/api/v1/user/activate/${KEY}/${TOKEN}/
```


**you can find this one-time url in your email


##### Alter user data
```
PUT https://oudi.herokuapp.com/api/v1/user/${YOUR_USER_ID}/

HEADER:
Content-type: multipart/form-data

AUTH:

Bearer: Token {$YOUR_AUTH_TOKEN}

BODY:
multipart : {
  "first_name": {$YOUR_NAME} // you can change more fields
}

```

response:
```
200 OK

{
  "id": {$USER_ID},
  "email": {$EMAIL},
  "username": {$USERNAME},
  "is_active": false,
  "first_name": {$YOUR_NAME},
  "last_name": "",
  "date_joined": {$REGISTRATION_TIMESTAMP}
}
```


##### GET Auth Token
```
POST https://oudi.herokuapp.com/api/v1/token-auth/

HEADER:
Content-type: multipart/form-data

BODY:
multipart : {
  "username": {$USERNAME},
  "password": {$PASSWORD}
}

```

response:
```
200 OK

{
  "token": ${YOUR_AUTH_TOKEN}
}
```

##### Generate reset password token
```
POST https://oudi.herokuapp.com/api/v1/password_recovery/

HEADER:
Content-type: multipart/form-data

BODY:
multipart : {
  "email": {$EMAIL},
}

```

response:
```
201 CREATED

{
  "user": {$USER_ID},
  "email": {$EMAIL},
  "ip": {$REQUEST_IP},
  "user_agent": {$REQUEST_USER_AGENT},
  "creation_timestamp": {$CREATION_TIMESTAMP} // token expires after 30 minutes
}
```

**you can find the token only in your email



##### Reset password using token
```
POST https://oudi.herokuapp.com/api/v1/password_recovery/confirm/

HEADER:
Content-type: multipart/form-data

BODY:
multipart : {
  "token": {$RESET_PASSWORD_TOKEN},
  "email": {$YOUR_EMAIL} // token works only for the email used for request it
  "password": {$NEW_PASSWORD}
  "password2": {$NEW_PASSWORD}
  
}

```

response:
```
200 OK

{
  "token": {$TOKEN}, // this token has been destroyed
  "email": {$EMAIL}
}
```

#### Profile details

##### Get your profile details
```
GET https://oudi.herokuapp.com/api/v1/user/personal_data/${YOUR_USER_ID}/

HEADER:
Content-type: multipart/form-data

AUTH:

Bearer: Token {$YOUR_AUTH_TOKEN}

```

response:
```
200 OK

{
  "user": {$USER_ID},
  "bio": {$BIO},
  "location": {$LOCATION},
  "cellular": {$CELLULAR},
  "gender": {$GENDER},
  "birth_date": {$BIRTH_DATE},
  "url_img_profile": {$URL_IMG_PROFILE},
  "email_confirmed": {$EMAIL_CONFIRMED_FLAG}
}
```


##### Edit your profile details
```
PUT https://oudi.herokuapp.com/api/v1/user/personal_data/${YOUR_USER_ID}/

HEADER:
Content-type: multipart/form-data

AUTH:

Bearer: Token {$YOUR_AUTH_TOKEN}

DATA:
multipart : {
  {$FIELD1}: {$VALUE1},
  ...
  {$FIELDk}: {$VALUEk},
}

```

response:
```
200 OK

{
  "user": {$USER_ID},
  "bio": {$BIO},
  "location": {$LOCATION},
  "cellular": {$CELLULAR},
  "gender": {$GENDER},
  "birth_date": {$BIRTH_DATE},
  "url_img_profile": {$URL_IMG_PROFILE},
  "email_confirmed": {$EMAIL_CONFIRMED_FLAG}
}
```

#### Client configuration

##### Get your client configuration
```
GET https://oudi.herokuapp.com/api/v1/config/${YOUR_USER_ID}/

HEADER:
Content-type: multipart/form-data

AUTH:

Bearer: Token {$YOUR_AUTH_TOKEN}

```

response:
```
200 OK

{
  "user": {$USER_ID},
  "country": {$COUNTRY_CODE},
  "language": {$LANGUAGE_CODE},
  "ui_pref": {$UI_APPAREANCE_CODE}
}
```


##### EDIT your client configuration
```
PUT https://oudi.herokuapp.com/api/v1/config/${YOUR_USER_ID}/

HEADER:
Content-type: multipart/form-data

AUTH:

Bearer: Token {$YOUR_AUTH_TOKEN}

DATA:
multipart : {
  {$FIELD1}: {$VALUE1},
  ...
  {$FIELDk}: {$VALUEk},
}

```

response:
```
200 OK

{
  "user": {$USER_ID},
  "country": {$COUNTRY_CODE},
  "language": {$LANGUAGE_CODE},
  "ui_pref": {$UI_APPAREANCE_CODE}
}
```


## Author

[Mauro Marini](https://github.com/marinimau)
 
 ## License
 
 [MIT](https://github.com/marinimau/wayne_django_rest/blob/master/LICENSE)
