## ERPRO App
[![Python](https://img.shields.io/badge/python-3.4_3.5_3.6-blue.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-84-green.svg)]()

### Initial server set-up
1. `git clone https://github.com/5hirish/erpro`
2. [Install RabbiMQ](https://tecadmin.net/install-rabbitmq-server-on-ubuntu/)
3. [Install Python3](https://help.dreamhost.com/hc/en-us/articles/115000702772-Installing-a-custom-version-of-Python-3)
4. [Install PostgreSQL](https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html)
5. [Setup Virtual Env for Python3](https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3)

#### Post-Installation

1) Activate virtual environment `source`
2) `pip install -r requirements.txt`
3) Update `.env` files; refer the `.env_sample` file
4) Clone unit files `*.service` to `/etc/systemd/system`
5) Set up AWS `.credentials` ARN roles, set up `.bash_profile` variables

#### Monitor
* Flask: {baseUrl}:5000
* RabbitMQ: {baseUrl}:15672

#### Documentation
* Postman API Documentation: https://documenter.getpostman.com/view/1937121/S1TVWHDu
* Postman API Collection: `docs/ERPRO.postman_collection.json`

#### Tests
* 9 unit test cases with 100% file coverage and 84% line coverage.