# AI Engineering Workshop
This repository acts as a starting point to get into engineering an exemplary system which utilizes LLMs as
parts of applications.

We're using https://docs.langchain4j.dev/intro to integrate a Spring Boot application with OpenAI.

There are a lot of things that exist in this repository already. This is necessary to allow us to get to the core
of the challenge of working with LLMs rather than spending all of our time constructing a use-case.

I have distributed various hints and questions throughout the code-base in the form of `// TODO:` comments.

## Setup
* Install SDKMan - https://sdkman.io/
* Run `sdk env install`
* `cp .env.example .env` and add you OPENAI API Key
* Start the application using `./gradlew bootRun` or directly from your IDE
* Start WebUI using `docker compose up`

We'll be using an in-memory H2 database. You can connect to it from:
* http://localhost:8080/h2-console
* JDBC URL: `jdbc:h2:mem:testdb`
* Username: `sa`
* Password: `password`

## Use
* You can use the setup with `docker compose up` - which will bootstrap a WebUI instance
OR
* You just use curl with `curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, how are you?"}' http://localhost:8080/curl/chat`