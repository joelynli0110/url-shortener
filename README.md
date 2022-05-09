

# URL Shortener with Flask and Redis

The implemented URL-shortener is a distributed URL-shortening service that uses: 

- **Apache ZooKeeper** that provides tokens for hash generation 
- **Redis** as a cache that stores the mapping between the original URL and the generated short id

## Features

- Encode the original long URL to the shortened URL
- Decode the shortened URL to the original long URL
- Insert the mapping to the cache
- Provide tokens for hash generation

## System Design

### Assumptions and Constraints

1. **Number of the servers**: Due to the time constraint of the assignment, the implemented service is now only manageable for **one server** (server_id is set to default value 1)

2. **Unique id generation**: The unique id of short URLs is generated via a **Base62** encoding algorithm and assumed to have the **length 4**, i.e., we have 62^4 string combinations.

3. **Token range size**: The token range of each batch is set to 100000 by default.

4. **Cache for storing encoding histories:** 

   - For decoding, we assume that a short URL is already generated before and therefore stored in the cache, so that we can get the uniquely mapped long URL.
   - For encoding, once an encoding of a given long URL is already carried out, we will directly get the long URL from the cache, otherwise we proceed the encoding like normal.

   

### Pipeline

1. Generate a number given by the counter for the long URL

2. Use Base62 algorithm to hash this number to a unique id (4-digit char string) 
3. Insert the mapping (long_url, short_id) into the cache
4. Increase the counter by 1 (to ensure the uniqueness of the number) if a new encoding is proceeded; Otherwise remain the same;



## Usage

### Installation

Install required packages:

```markdown
pip install -r requirements.txt
```

### Start the Zookeeper and Redis server

#### 1. Go to the zookeeper folder and start the zookeeper server

```
./bin/.zkServer.cmd
```

#### 2. Configure the Redis client password

- Go to the redis folder, start the redis server and client

```
./redis-server.exe
./redis-cli.exe
```

- Configure the password in redis-cli.exe:

```
127.0.0.1.6379> config set requirepass 123456
```

- Authenticate to the server with the given password:

```
127.0.0.1.6379> AUTH 123456
```

Now the Redis server is ready.

### Run the main application

```
python main.py
```

Then access the API using:

```
http://localhost:5000/
```


## API Endpoints

```python
POST:
    /to-short-url [body : {"full" : original_url, "short": short_url}] : Shorten the URL and store in the cache
    /to-original-url [body : {"short" : short_url, "full": full_url}] : Return the original URL
    
Both endpoints return JSON
```



## Testing

1. Go to the /tests/ folder and run: 

```python
python unit_test.py # Unit Test
```

and

```python
python integration_test.py # Integration Test
```



2. Access the API via <u>localhost:5000</u> and play around with different URLs
