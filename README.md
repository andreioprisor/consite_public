# Consite: Comprehensive AI Construction Management App

Consite is a robust application designed for construction companies, built to streamline all aspects of document management on the construction site. This includes materials procurement, inventory management, and invoice handling. Consite is built using a stack that combines Node.js, Express, Sequelize, and Vue.js, ensuring a solid and scalable backend coupled with a responsive frontend.

## Key Features

- **Authentication and Authorization:** Ensures secure access to the application.
- **ORM, Migration, and Seed:** Efficient database management and data seeding.
- **Logging and Testing:** Comprehensive logging and systematic testing for robustness.
- **Caching and Bi-directional Communication:** Enhanced performance and real-time data exchange.
- **Job Scheduler and Dependency Management:** Automated tasks and well-managed dependencies.
- **Environment Variables and CORS:** Secure and flexible configuration management.
- **Docker Support and Linting:** Simplified deployment and consistent code quality.

## Centralized Document Data Management

Consite centralizes all document data extracted from the construction site, such as materials bought, inventory records, and invoices, into a user-friendly interface. This centralization is organized into three main tables:
- **Documents:** Stores all the documents.
- **Suppliers:** Maintains records of all suppliers.
- **Products:** Lists all the products bought.

### Intelligent Document Processing with LLMs

The system includes a sophisticated Parser module (`invoice_parser/`) that processes documents through a three-step pipeline:

1. **Text Extraction**: Identifies and extracts text boxes along with their bounding boxes from PDF documents
2. **Alignment Retention Algorithm**: Applies a proprietary algorithm to assemble the extracted text into a string that maintains the original PDF alignment
3. **Data Parsing**: Utilizes inference on a finely tuned LLAMA 3.1 model to convert the structured text into JSON format


## Run with Docker

1. Clone this repository
2. Install Docker if you don't have it already
3. Create the image for santier with `docker build -t santier:v7 .` command in the root directory
4. Create the parser image with `docker build -t parser:v7 .` in src/invoice_parser
5. Run docker compose up in root directory and you are done


## Features of the Backend architecture

- **ORM**: [Sequelize](https://sequelize.org/)  orm for object data modeling
- **Migration and Seed**: DB migration and Seed using [Sequelize-CLI](https://github.com/sequelize/cli) 
- **Authentication and authorization**: using [passport](http://www.passportjs.org)
- **Error handling**: centralized error handling
- **Validation**: request data validation using [Joi](https://github.com/hapijs/joi)
- **Logging**: using [winston](https://github.com/winstonjs/winston) 
- **Testing**: unittests using [Mocha](https://mochajs.org/)
- **Caching**: Caching using [Redis](https://redis.io/)
- **Bidirectional Communication**: using [Scoket](https://socket.io/)
- **Job scheduler**: with [Node-cron](https://www.npmjs.com/package/node-cron)
- **Dependency management**: with [Yarn](https://yarnpkg.com)
- **Environment variables**: using [dotenv](https://github.com/motdotla/dotenv) and [cross-env](https://github.com/kentcdodds/cross-env#readme)
- **CORS**: Cross-Origin Resource-Sharing enabled using [cors](https://github.com/expressjs/cors)
- **Docker support**
- **Linting**: with [ESLint](https://eslint.org) and [Prettier](https://prettier.io)

### AI Document Parser

The system includes a sophisticated Parser module (`invoice_parser/`) that processes documents through a three-step pipeline:

1. **Text Extraction**:  
   Identifies and extracts text boxes along with their bounding boxes from PDF documents.

2. **Alignment Retention Algorithm**:  
   Applies a proprietary algorithm to assemble the extracted text into a string that maintains the original PDF alignment.  

3. **LLM Inference**:  
   Utilizes inference on a fine-tuned LLAMA 3.1 model to extract key fields from the structured text into JSON format.  
   The extracted output looks like this:  

   ```json
   {
       "beneficiary": "string",
       "supplier": "string",
       "supplier_fiscal_code": "string",
       "phone": "string or null",
       "email": "string or null",
       "iban": "string",
       "bank": "string",
       "invoice_number": "string",
       "issuance_date": "string",
       "due_date": "string or null",
       "total": "string",
       "total_with_tva": "string",
       "products": [
           {
               "name": "string",
               "quantity": "number",
               "unit_price": "number",
               "currency": "string",
               "unit_of_measure": "string",
               "total_value": "string",
               "tva": "string"
           }
       ]
   }

Examples of inputs and outputs of the model can be found in `/invoice_parser/parser_output.txt` and the corresponding PDF invoices in `/invoice_parser/tests/inputs`.  
For the training of the model I've used 30% real data and 70% syntetic data generated with models like GPT 4, as the procurement of invoices is not an easy task.

## Environment Variables

The environment variables can be found and modified in the `.env` file. They come with these default values:

```bash
#Server environment
NODE_ENV=development
#Port number
PORT=5000

#Db configuration
DB_HOST=db-host
DB_USER=db-user
DB_PASS=db-pass
DB_NAME=db-name


# JWT secret key
JWT_SECRET=your-jwt-secret-key
# Number of minutes after which an access token expires
JWT_ACCESS_EXPIRATION_MINUTES=5
# Number of days after which a refresh token expires
JWT_REFRESH_EXPIRATION_DAYS=30

#Log config
LOG_FOLDER=logs/
LOG_FILE=%DATE%-app-log.log
LOG_LEVEL=error

#Redis
REDIS_HOST=redis-host
REDIS_PORT=6379
REDIS_USE_PASSWORD=no
REDIS_PASSWORD=your-password

```

## Project Structure

```
specs\
invoice_parser\ # Invoice Parser with it's docker support
src\
 |--config\         # Environment variables and configuration related things
 |--controllers\    # Route controllers (controller layer)
 |--dao\            # Data Access Object for models
 |--db\             # Migrations and Seed files
 |--models\         # Sequelize models (data layer)
 |--routes\         # Routes
 |--services\       # Business logic (service layer)
 |--helper\         # Helper classes and functions
 |--validations\    # Request data validation schemas
 |--app.js          # Express app
 |--cronJobs.js     # Job Scheduler
 |--index.js        # App entry point
```

## License

[MIT](LICENSE)
