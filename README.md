## Step 1: Initialise prisma for a specific datasource provider ( only once )
Run `npx prisma init --datasource-provider postgresql`

## Step 2: Change provider type to python in prisma/schema.prisma ( only once )
Change `provider = "prisma-client-js"` to `provider = "prisma-client-py" `

## Step 3: Setup the database URL environment variable
Set the `DATABASE_URL in the .env file or in the system` to point to your existing database.

## Step 4: Creating prisma client ( for querying, saving etc)
Run `prisma generate` to generate the Prisma Client

## Optional step: In case your DB already have tables created that you want to use
Run `prisma db pull` to turn your database schema into a Prisma schema.

## Step 5: In case there are no tables in the DB yet
1. Define the schema in schema.prisma file 
2. Run `prisma db push` ( this creates the DB tables )

Update: No need to do this step manually, it is being done on application startup anyways ( and is Idempotent so no data loss/overriding etc )

## Step 6: How to run this app
Run `uvicorn main:app --reload`



