![Tarantulla YouTube: a module for YouTube data extraction](./tarantulla-youtube-post.png)

![PyPI - Python Version](https://img.shields.io/badge/PYTHON-3.5,%203.6,%203.7-blue.svg?style=for-the-badge) 
![LINUX](https://img.shields.io/badge/PLATFORM-LINUX-blue.svg?style=for-the-badge) 
![CRAN](https://img.shields.io/badge/LICENSE-GPLv3-blue.svg?style=for-the-badge) 
![LOVE](https://img.shields.io/badge/BUILT%20WITH-LOVE-red.svg?style=for-the-badge)
[![TWITTER](https://img.shields.io/badge/BY-@oncase-lightgrey.svg?style=for-the-badge)](https://twitter.com/oncase) 


## **"Tarantulla-YouTube: the solution to gather YouTube data from publishers of your interest"**

If you want to know more, check out Tarantulla's [landing page](http://tarantulla.io/) and our [post]() in Medium.

On this document you will find information about:  

- [Requirements](#requirements)  
- [Installation](#installation)   
- [How to Run](#how-to-run)  
- [Running with PDI - Database Integration](#running-with-pdi---database-integration)


## Requirements 
- [Python 3.x (>=3.5)](https://www.python.org/getit/)


## Installation

First things first: *git clone* this project. Prefer to clone in folder `/opt/git`.

## How to Run

### Configuration

1 - Edit `config-users.json`

All publishers and information such as output folders and python call should be defined on this file, according to the example:

```json
{
	"temp_output": "/../data/",
	"python-command":"python3",	
	"publishers":
	[
		{
			"_youtube_user": "AndroidPITcom",
			"name": "AndroidPIT US",
			"isChannel": false
		}
	]	
}
```

with fields:

- temp_output = output folder used to store files created during execution  
	```Attention! Folder path specified is relative to project's folder `/core` ```
- python-command = command that calls Python 3.x
- publishers =
    - _youtube_user = user name to be queried
    - name = user full name
    - isChannel = whether it is a **channel** or a **user** (booleans `True` or `False`)
    ```Attention! Tarantulla Youtube is currently only implemented for users.```

The `_youtube_user` is **fixed**, defined by YouTube, whereas `name` is **not fixed**, what means you can choose any `name` you think is representative for you. Additionaly, you can add more fields in case you need other information for any further application development. 

2 - Edit `api-keys.json`

The YouTube API access key should be specified on this file. The script will require the following access key:

```json
{
	"YTAPIKEY":"[YOUR YOUTUBE DATA API KEY]"
}
```
You can obtain the YouTube Data API keys (v3) for your project following these [steps](https://developers.google.com/youtube/registering_an_application).

### Execution

Execute the script `statsMain.py`, in the folder `/core`, with the **Python 3** command set on your machine. The API returns statistics from the gathered videos for the specified publishers. 

```bash
$ python3 statsMain.py
```

The **output** is a JSON file containing the fields:

- title
- channel ID
- channel name
- publication date
- description
- playlist ID
- video ID
- number of views
- number of likes
- number of dislikes
- number of comments
- language
- locale
- category
- publisher name
- engagement

## Running with PDI - Database Integration

PDI or *Pentaho Data Integration* is a platform to accelerate data pipeline, providing visual tools to reduce complexity. In this project PDI was used to integrate the results into a database such as PostgreSQL. If you want to organize your data in a database as well, follow the next steps. 

To know more about PDI, check out the [documentation](https://help.pentaho.com/Documentation/8.1). It is worth remember that PDI requires JAVA installed on your machine.

### Configuration

Steps 1 and 2 are the same as above, what means you must configure both files: `config-users.json` and `api-keys.json`. Additionaly, in order to run Tarantulla-YouTube with PDI you should perform 2 more steps:

3- Edit file `config-db.json` - Set JDBC connection, Database and Table.

```json
{
	"database_config" :  
	{
		"database_name" : "postgres",
		"database_url" : "jdbc:postgresql://localhost:5432/",
		"database_driver" : "org.postgresql.Driver",
		"database_username" : "postgres",
		"database_password" : "[YOUR PASSWORD]",
		"database_schema" : "staging",
		"database_table" : "stg_youtube"  
	}
}
```

The above JSON is an example and you can change the fields' values according to your database configurations. 


4- Execute DDL

Execute the script `tarantulla-youtube/scripts/ddl.sql` with the appropriate changes for your environment/database. Remember to change `<yourSCHEMA>` and `<yourTABLE>` names in the script, according to the variables set in `config-db.json`.

``` Attention! If the schema does not already exist, you should create it before execute the SQL script. ```

```Attention! In order to establish a connection to the database, PDI must have the correspondent database driver in the folder `<YOURPENTAHO>/design-tools/data-integration/lib`.  ```

### Execution


When all is set, you can execute `main.kjb` directly from Pentaho `kitchen.sh` script. You should locate the **folder with PDI files** (PDI_HOME) and run:

```bash
$ <PDI_HOME>/./kitchen.sh  -file="<YOUR TARANTULLA YOUTUBE FOLDER>/etl/main.kjb"    
```

Alternatively, if your **PDI_HOME** is set to `/opt/Pentaho/design-tools/data-integration`, you can directly run the `etl.sh` script. 

```bash
$ <YOUR TARANTULLA YOUTUBE FOLDER>/scripts/etl.sh job ../etl/main.kjb    
```

Please, note that in order to execute `etl.sh`, the script must have the appropriate execution permissions in your system.


## License

Tarantulla-YouTube is released under the GPLv3 license.