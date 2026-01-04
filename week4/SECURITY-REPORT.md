Manual Security test cases :-> 

1. Payload whitelisting:->
    {
  "name": "Phone",
  "price": 300,
  "isAdmin": true -> This will get stripped
}

Result :-> 
    {
    "success": false,
    "message": "Validation error",
    "errors": [
        "Unrecognized key: \"isValid\""
    ]
}


2.Wrong Datatype :->
    {
  "name": "Phone",
  "price": "cheap"
}


Result :->
    {
    "success": false,
    "message": "Validation error",
    "errors": [
        "Invalid input: expected number, received string"
    ]
}

3.NoSQL injection :->
    {
  "email": { "$gt": "" }
}

Result :->
    {
    "success": false,
    "message": "Validation error",
    "errors": [
        "Invalid input: expected string, received object" // expected String and recieved object due to NoSQL injection
    ]
}


4. Rate limiting :-> 

max = 10 , times a user can hit this end point :-> http://localhost:3000/api/register/

Hitting more than that : -> 

res =>  Too many requests, please try again later.


5. Paload Size limits :->

max size of the payload  :-> 10kb


GET/http://localhost:3000/api/products/

and json body :->

{
    "name" : "vivek singh",
    "desscription" : "Too large", // this make this json payload size more than 10 kb
    "price" : 80000
}

Res => PayloadTooLargeError: request entity too large
    at readStream (/home/viveksingh/Desktop/Launchpad/week4/node_modules/raw-body/index.js:163:17)
    at getRawBody (/home/viveksingh/Desktop/Launchpad/week4/node_modules/raw-body/index.js:116:12)
    at read (/home/viveksingh/Desktop/Launchpad/week4/node_modules/body-parser/lib/read.js:114:3)
    at jsonParser (/home/viveksingh/Desktop/Launchpad/week4/node_modules/body-parser/lib/types/json.js:90:5)
    at Layer.handleRequest (/home/viveksingh/Desktop/Launchpad/week4/node_modules/router/lib/layer.js:152:17)
    at trimPrefix (/home/viveksingh/Desktop/Launchpad/week4/node_modules/router/index.js:342:13)
    at /home/viveksingh/Desktop/Launchpad/week4/node_modules/router/index.js:297:9
    at processParams (/home/viveksingh/Desktop/Launchpad/week4/node_modules/router/index.js:582:12)
    at next (/home/viveksingh/Desktop/Launchpad/week4/node_modules/router/index.js:291:5)
    at router.handle (/home/viveksingh/Desktop/Launchpad/week4/node_modules/router/index.js:186:3)