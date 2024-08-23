## Running the App

1. **Create local .env config**

After cloning the repo create an .env file in the root `Pump-Backend` directory and populate it with the following metadata:
```bash
touch .env

echo "POSTGRES_HOST=pump-db-host:5432
POSTGRES_DB=pump_db
POSTGRES_USER=jennings_and_siq
POSTGRES_PASSWORD=bobcancode955
JWT_SECRET=supersecret" >> .env
```

2. **Install Docker Desktop**

If you already have Docker Desktop installed, you can skip this step.

If you do not already have Docker Desktop installed, go to the Docker website (https://www.docker.com/products/docker-desktop/) to install Docker Desktop for your OS.

If you are trying to run Docker on Apple Silicon (M1), you may run into a CPU compatibility issue, in which case you should install from this updated DMG: https://docs.docker.com/docker-for-mac/apple-m1/.

3.  **Docker Compose**:

Ensure the Docker Desktop application is running in the background. Sometimes you need to open it manually by clicking on the Application icon. The home UI should say “Your running containers show up here.”

From within the root directory `Pump-Backend`, aggregate the Docker service:
```bash
docker compose up
```

If your docker is complaining that you need the Postgres credentials to complete this step, go into your `docker-compose.yml` file and replace the following env variables with whatever you want. The values don't matter because this is a local instance spun up in your own Docker container. For instance:
```
POSTGRES_USER: postgres_user
POSTGRES_PASSWORD: postgres_password
POSTGRES_DB: postgres_db
```

Once the debugger is active, you're up and running. Hit `V` in the terminal to view your instance in Docker Desktop. You should see 3 packages running.

## Adminer

To use Adminer (https://www.adminer.org/) for database management, Docker Compose then navigate to http://localhost:8080 in a browser.

## Making Migrations

After creating or updating models (or making a new db container), the db schema must be updated using Alembic (https://alembic.sqlalchemy.org/en/latest/index.html)

1. **Detached Docker Compose**:
```bash
make detached
```

2. **If required, create the migration version**:
```bash
make makemigration MESSAGE="<message>"
```

3. **Apply migration**:
```bash
make migrate
```

You should see your local DB spun up in `migrations/versions/`. If you are having trouble, run `docker compose down` to kill the running Docker instance, remove all files inside `migrations/versions/`, before recomposing `docker compose up` and trying the migration again.

## Postman ##

You may want to use the Postman interface to populate your local DB with object instances and test end-to-end functionality.

1. **Download Postman (https://www.postman.com/downloads/) desktop application.**

2. **Import the following APIs**

File > Import > [Copy + Paste]:
```
{
	"info": {
		"_postman_id": "4bce5eea-72f3-4e78-8364-e16564dd599e",
		"name": "PUMP Local APIs",
		"description": "# 🚀 Get started here\n\nThis template guides you through CRUD operations (GET, POST, PUT, DELETE), variables, and tests.\n\n## 🔖 **How to use this template**\n\n#### **Step 1: Send requests**\n\nRESTful APIs allow you to perform CRUD operations using the POST, GET, PUT, and DELETE HTTP methods.\n\nThis collection contains each of these [request](https://learning.postman.com/docs/sending-requests/requests/) types. Open each request and click \"Send\" to see what happens.\n\n#### **Step 2: View responses**\n\nObserve the response tab for status code (200 OK), response time, and size.\n\n#### **Step 3: Send new Body data**\n\nUpdate or add new data in \"Body\" in the POST request. Typically, Body data is also used in PUT request.\n\n```\n{\n    \"name\": \"Add your name in the body\"\n}\n\n ```\n\n#### **Step 4: Update the variable**\n\nVariables enable you to store and reuse values in Postman. We have created a [variable](https://learning.postman.com/docs/sending-requests/variables/) called `base_url` with the sample request [https://postman-api-learner.glitch.me](https://postman-api-learner.glitch.me). Replace it with your API endpoint to customize this collection.\n\n#### **Step 5: Add tests in the \"Tests\" tab**\n\nTests help you confirm that your API is working as expected. You can write test scripts in JavaScript and view the output in the \"Test Results\" tab.\n\n<img src=\"https://content.pstmn.io/b5f280a7-4b09-48ec-857f-0a7ed99d7ef8/U2NyZWVuc2hvdCAyMDIzLTAzLTI3IGF0IDkuNDcuMjggUE0ucG5n\">\n\n## 💪 Pro tips\n\n- Use folders to group related requests and organize the collection.\n- Add more [scripts](https://learning.postman.com/docs/writing-scripts/intro-to-scripts/) in \"Tests\" to verify if the API works as expected and execute workflows.\n    \n\n## 💡Related templates\n\n[API testing basics](https://go.postman.co/redirect/workspace?type=personal&collectionTemplateId=e9a37a28-055b-49cd-8c7e-97494a21eb54&sourceTemplateId=ddb19591-3097-41cf-82af-c84273e56719)  \n[API documentation](https://go.postman.co/redirect/workspace?type=personal&collectionTemplateId=e9c28f47-1253-44af-a2f3-20dce4da1f18&sourceTemplateId=ddb19591-3097-41cf-82af-c84273e56719)  \n[Authorization methods](https://go.postman.co/redirect/workspace?type=personal&collectionTemplateId=31a9a6ed-4cdf-4ced-984c-d12c9aec1c27&sourceTemplateId=ddb19591-3097-41cf-82af-c84273e56719)",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "25583517"
	},
	"item": [
		{
			"name": "Users",
			"item": [
				{
					"name": "Create user",
					"event": [
						{
							"listen": "test",
							"script": {
								"exec": [
									"pm.test(\"Successful POST request\", function () {",
									"    pm.expect(pm.response.code).to.be.oneOf([200, 201]);",
									"});",
									""
								],
								"type": "text/javascript",
								"packages": {}
							}
						}
					],
					"request": {
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n\t\"username\": \"user3\",\n    \"email\": \"user3@test.com\",\n    \"password\": \"test\",\n    \"name\": \"User3 Local\"\n    // \"profile_pic\": \"user3.com\",\n    // \"location\": \"New York\",\n    // \"bio\": \"User3 bio\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/users",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"users"
							]
						},
						"description": "This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.\n\nA successful POST request typically returns a `200 OK` or `201 Created` response code."
					},
					"response": []
				},
				{
					"name": "Get user",
					"event": [
						{
							"listen": "test",
							"script": {
								"exec": [
									"pm.test(\"Status code is 200\", function () {",
									"    pm.response.to.have.status(200);",
									"});"
								],
								"type": "text/javascript",
								"packages": {}
							}
						}
					],
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "{{base_url}}/users/3",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"users",
								"3"
							]
						},
						"description": "This is a GET request and it is used to \"get\" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).\n\nA successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data."
					},
					"response": []
				},
				{
					"name": "Get User's Friends",
					"protocolProfileBehavior": {
						"disableBodyPruning": true
					},
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							},
							{
								"key": "Content-Type",
								"value": "application/json",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/users/3/friends?page=1",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"users",
								"3",
								"friends"
							],
							"query": [
								{
									"key": "page",
									"value": "1"
								}
							]
						}
					},
					"response": []
				},
				{
					"name": "Update user",
					"event": [
						{
							"listen": "test",
							"script": {
								"exec": [
									"pm.test(\"Successful PUT request\", function () {",
									"    pm.expect(pm.response.code).to.be.oneOf([200, 201, 204]);",
									"});",
									""
								],
								"type": "text/javascript",
								"packages": {}
							}
						}
					],
					"request": {
						"method": "PATCH",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n\t\"profile_pic\": \"https://pump-profilepics.s3.us-west-1.amazonaws.com/3.jpg\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/users/3",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"users",
								"3"
							]
						},
						"description": "This is a PUT request and it is used to overwrite an existing piece of data. For instance, after you create an entity with a POST request, you may want to modify that later. You can do that using a PUT request. You typically identify the entity being updated by including an identifier in the URL (eg. `id=1`).\n\nA successful PUT request typically returns a `200 OK`, `201 Created`, or `204 No Content` response code."
					},
					"response": []
				},
				{
					"name": "Delete user",
					"event": [
						{
							"listen": "test",
							"script": {
								"exec": [
									"pm.test(\"Successful DELETE request\", function () {",
									"    pm.expect(pm.response.code).to.be.oneOf([200, 202, 204]);",
									"});",
									""
								],
								"type": "text/javascript",
								"packages": {}
							}
						}
					],
					"request": {
						"method": "DELETE",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/users/1",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"users",
								"1"
							]
						},
						"description": "This is a DELETE request, and it is used to delete data that was previously created via a POST request. You typically identify the entity being updated by including an identifier in the URL (eg. `id=1`).\n\nA successful DELETE request typically returns a `200 OK`, `202 Accepted`, or `204 No Content` response code."
					},
					"response": []
				}
			]
		},
		{
			"name": "Workouts",
			"item": [
				{
					"name": "Get Workout",
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/workouts/1",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"1"
							]
						}
					},
					"response": []
				},
				{
					"name": "List Workout Attendees",
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/workouts/13/users",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"13",
								"users"
							]
						}
					},
					"response": []
				},
				{
					"name": "Accept Workout",
					"request": {
						"method": "POST",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/workouts/7/accept",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"7",
								"accept"
							]
						}
					},
					"response": []
				},
				{
					"name": "Reject Workout",
					"request": {
						"method": "POST",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/workouts/8/reject",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"8",
								"reject"
							]
						}
					},
					"response": []
				},
				{
					"name": "Get upcoming workouts",
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/workouts/upcoming?date=06/17/24&page=1",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"upcoming"
							],
							"query": [
								{
									"key": "date",
									"value": "06/17/24"
								},
								{
									"key": "page",
									"value": "1"
								}
							]
						}
					},
					"response": []
				},
				{
					"name": "Get workout invites",
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/workouts/invites?date=06/17/24",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"invites"
							],
							"query": [
								{
									"key": "date",
									"value": "06/17/24"
								}
							]
						}
					},
					"response": []
				},
				{
					"name": "Delete Workout",
					"request": {
						"method": "DELETE",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/workouts/5",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"5"
							]
						}
					},
					"response": []
				},
				{
					"name": "Create Workout",
					"request": {
						"method": "POST",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"title\": \"Push day\",\n    \"description\": \"I hope you like dips...\",\n    // \"workout_pic\": \"demo.com\",\n    \"location\": \"Office Gym\",\n    \"city\": \"San Francisco\",\n    \"datetime\": \"08/06/24 08:00\"// ,\n    // \"invitees\": [4]\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/workouts",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts"
							]
						}
					},
					"response": []
				},
				{
					"name": "Update Workout",
					"request": {
						"method": "PATCH",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"city\": \"San Francisco\",\n    \"location\": \"Golden Gate Park\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/workouts/1",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"workouts",
								"1"
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Friendships",
			"item": [
				{
					"name": "Create Friendship",
					"request": {
						"method": "POST",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"recipient_id\": 7\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/friendships",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"friendships"
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Friendship",
					"protocolProfileBehavior": {
						"disableBodyPruning": true
					},
					"request": {
						"method": "GET",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/friendships/5",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"friendships",
								"5"
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Friend Requests",
					"protocolProfileBehavior": {
						"disableBodyPruning": true
					},
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/friendships/requests?page=1",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"friendships",
								"requests"
							],
							"query": [
								{
									"key": "page",
									"value": "1"
								}
							]
						}
					},
					"response": []
				},
				{
					"name": "Delete Friendship",
					"request": {
						"method": "DELETE",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/friendships/7",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"friendships",
								"7"
							]
						}
					},
					"response": []
				},
				{
					"name": "Update Friendship",
					"request": {
						"method": "PATCH",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"status\": \"accepted\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/friendships/5",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"friendships",
								"5"
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Attendees",
			"item": [
				{
					"name": "Create Attendee",
					"request": {
						"method": "POST",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"user_id\": 5,\n    \"workout_id\": 6\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/attendees",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"attendees"
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Attendee",
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "{{base_url}}/attendees/14",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"attendees",
								"14"
							]
						}
					},
					"response": []
				},
				{
					"name": "Update Attendee",
					"request": {
						"method": "PATCH",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"status\": \"accepted\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{base_url}}/attendees/3",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"attendees",
								"3"
							]
						}
					},
					"response": []
				},
				{
					"name": "Delete Attendee",
					"request": {
						"method": "DELETE",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/attendees/14",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"attendees",
								"14"
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Data Composition APIs",
			"item": [
				{
					"name": "Get Profile",
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/profiles/3",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"profiles",
								"3"
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Feed",
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/feed?page=1",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"feed"
							],
							"query": [
								{
									"key": "page",
									"value": "1"
								}
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Profile Workouts",
					"request": {
						"method": "GET",
						"header": [
							{
								"key": "Authorization",
								"value": "Bearer {{auth}}",
								"type": "text"
							}
						],
						"url": {
							"raw": "{{base_url}}/profiles/4/workouts",
							"host": [
								"{{base_url}}"
							],
							"path": [
								"profiles",
								"4",
								"workouts"
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Login",
			"event": [
				{
					"listen": "test",
					"script": {
						"exec": [
							"var jsonData = pm.response.json();",
							"",
							"var token = jsonData.token;",
							"",
							"if (token) {",
							"    pm.collectionVariables.set(\"auth\", token);",
							"}"
						],
						"type": "text/javascript",
						"packages": {}
					}
				}
			],
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"username\": \"user1\",\n    \"password\": \"test\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "{{base_url}}/login",
					"host": [
						"{{base_url}}"
					],
					"path": [
						"login"
					]
				}
			},
			"response": []
		},
		{
			"name": "Index",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "{{base_url}}/",
					"host": [
						"{{base_url}}"
					],
					"path": [
						""
					]
				}
			},
			"response": []
		},
		{
			"name": "User Search",
			"request": {
				"method": "GET",
				"header": [
					{
						"key": "Authorization",
						"value": "Bearer {{auth}}",
						"type": "text"
					}
				],
				"url": {
					"raw": "{{base_url}}/search?q=User&page=1",
					"host": [
						"{{base_url}}"
					],
					"path": [
						"search"
					],
					"query": [
						{
							"key": "q",
							"value": "User"
						},
						{
							"key": "page",
							"value": "1"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "Get Presigned Url",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "{{base_url}}/presigned_url?key=random.jpg",
					"host": [
						"{{base_url}}"
					],
					"path": [
						"presigned_url"
					],
					"query": [
						{
							"key": "key",
							"value": "random.jpg"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "https://pump-profilepics.s3.amazonaws.com/testing.jpg?AWSAccessKeyId=AKIAUDZMNAYBOLDGPPDH&Signature=3s3orbVyG0dmMtv0yFpMH6vqOOk%3D&content-type=image%2Fjpeg&Expires=1718864401",
			"request": {
				"method": "PUT",
				"header": [],
				"body": {
					"mode": "file",
					"file": {
						"src": "/Users/maxsicherman/Desktop/testing.jpg"
					}
				},
				"url": {
					"raw": "https://pump-profilepics.s3.amazonaws.com/random.jpg?AWSAccessKeyId=AKIAUDZMNAYBOLDGPPDH&Signature=C08qutuL4ATrpffc9TX%2FoGB%2FPEc%3D&content-type=image%2Fjpeg&Expires=1718866421",
					"protocol": "https",
					"host": [
						"pump-profilepics",
						"s3",
						"amazonaws",
						"com"
					],
					"path": [
						"random.jpg"
					],
					"query": [
						{
							"key": "AWSAccessKeyId",
							"value": "AKIAUDZMNAYBOLDGPPDH"
						},
						{
							"key": "Signature",
							"value": "C08qutuL4ATrpffc9TX%2FoGB%2FPEc%3D"
						},
						{
							"key": "content-type",
							"value": "image%2Fjpeg"
						},
						{
							"key": "Expires",
							"value": "1718866421"
						}
					]
				}
			},
			"response": []
		}
	],
	"event": [
		{
			"listen": "prerequest",
			"script": {
				"type": "text/javascript",
				"exec": [
					""
				]
			}
		},
		{
			"listen": "test",
			"script": {
				"type": "text/javascript",
				"exec": [
					""
				]
			}
		}
	],
	"variable": [
		{
			"key": "id",
			"value": "1"
		},
		{
			"key": "base_url",
			"value": "http://localhost:8000"
		},
		{
			"key": "auth",
			"value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MTYwMDg5ODN9.hB-AbjNChwO_7N9_kBVFhoCcZ2fiSrSpRrMRoBtTZ-g",
			"type": "string"
		}
	]
}

```

