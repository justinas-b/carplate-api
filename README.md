# carplate-api

**Story:** User can register/store Lithuanian car number plates, their owner names and car model to web application through API and application should asynchronously retrieve Car model image using Celery Framework, store it locally and display later on

## Requirements:

* [X] It does not require any authentication or authorization.
* [X] The user should be able to do CRUD operations on car numbers stored in database.
* [X] The API must be done using Django rest framework.
* [ ] Asynchronous car model image retrieval needs to be implemented using Celery Framework.
* [ ] Django and Celery should communicate through RabbitMQ broker.
* [X] During development use version control (git) for your project and publish it to any public version control vendors – github, bitbucket, gitlab or any other you prefer.
* [X] Put a small README.md file which shows how to launch the project in local environment.
* [X] You can pick any database that Django supports.
 
## Optionally:

* [ ] Provide any tests for your code
* [ ] Create a Django admin view to access this data
* [X] Think about input data validations
* [ ] Database and rabbitMQ containers provided through docker compose file to easily test this portable solution.
* [X] Minimalistic design (render the forms as simply as possible)

## Valstybinių numerių formatai:

https://www.regitra.lt/lt/paslaugos-ir-veikla/numerio-zenklai/numerio-zenklu-tipai

* `XXX 000` - automobiliams ženklinti skirtuose numerio ženkluose – trys raidės ir trys skaitmenys
* `XX 000` - priekaboms ir puspriekabėms ženklinti skirtuose numerio ženkluose – dvi raidės ir trys skaitmenys
* `000 XX` - motociklams ženklinti skirtuose numerio ženkluose – trys skaitmenys ir dvi raidės
* `00 XXX` - mopedams (motociklams) ženklinti skirtuose 4-ojo formato numerio ženkluose – du skaitmenys ir trys raidės
* `XX 00` - galingiesiems keturračiams ženklinti skirtuose 3-ojo formato numerio ženkluose – du skaitmenys ir dvi raidės
* `0XXXXX` - automobiliams  – nuo 1 iki 6 simbolių, kurių vienas privalo būti skaičius
* `0XXXX` - motociklams – nuo 1 iki 5 simbolių, kurių vienas privalo būti skaičius
* `T00000` - taksi. Šio tipo numerio ženklai yra skirti žymėti automobilius, o jų užrašą sudaro „T“ raidė  ir penki skaitmenys.
* `H00000` - Istorinio numerio ženklo pavyzdžiai: automobilių
* `0000H` - Istorinio numerio ženklo pavyzdžiai: motociklų
* `P00000` - Laikinieji numerio ženklai gali būti išduodami automobiliams, priekaboms ir motociklams, o jų užrašus sudaro: automobiliai ir priekabos ženklinami „P“ raide ir penkiais skaitmenimis, nurodančiais eilės numerį
* `P0000` - Laikinieji numerio ženklai gali būti išduodami automobiliams, priekaboms ir motociklams, o jų užrašus sudaro: motociklai ženklinami „P“ raide ir keturiais skaitmenimis, nurodančiais eilės numerį
* `0000XX` - Laikinųjų numerio ženklų pavyzdžiai: automobilių ir priekabų
* `0000X` - Laikinųjų numerio ženklų pavyzdžiai: motociklų
* `EX0000` - Elektromobilio numerio ženklo pavyzdžiai
* `000000` - diplomatiniai
* `00000` - diplomatiniai
* `0XXXXX` - lentelė vežamiems dviračiams žymėti

## API

* `http://127.0.0.1:8000/api` - retrieve all entries (Read)
* `http://127.0.0.1:8000/api?&owner=John+Doe` - retrieve all entries filtered by owner (Read)
* `http://127.0.0.1:8000/api?plate=AB123` - retrieve all entries filtered by plate (Read)
* `http://127.0.0.1:8000/api?search=123` -  retrieve all entries where search phrase is mentioned (Read)
* `http://127.0.0.1:8000/api/1/` - retrieve entry by it's ID (Read, Update, Delete)
* `http://127.0.0.1:8000/api/plate/ABC123/` - retrieve entry by plate (Read, Update, Delete)