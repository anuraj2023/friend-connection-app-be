# Friend Connection App APIs

This project uses Fast API framework to write REST APIs for friend connection app.
<br>ORM Used : Prisma
<br>DB Used: PostgreSQL

## Deployed App API documentation ( Swagger )
You can find the details of all APIs here: https://friend-connection-app-be.onrender.com/docs 

## Steps to run the app in local

### Step 1: Initialise prisma for a specific datasource provider ( only once )
Run `npx prisma init --datasource-provider postgresql`

### Step 2: Change provider type to python in prisma/schema.prisma ( only once )
Change `provider = "prisma-client-js"` to `provider = "prisma-client-py" `

### Step 3: Setup the database URL environment variable
Set the `DATABASE_URL in the .env file or in the system` to point to your existing database.

### Step 4: Creating prisma client ( for querying, saving etc)
Run `prisma generate` to generate the Prisma Client

### Step 5: Create tables in DB with the help of prisms schema 
1. Define the schema in schema.prisma file 
2. Run `prisma db push` ( this creates the DB tables )

### Step 6: Run the app in watch mode
Run `uvicorn main:app --reload`



