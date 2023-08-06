joker-minions
=============

Simple cache server using gevent.

Run a cache server:

    $ python3 -c "from joker.minions.cache import CacheServer; CacheServer().runserver()"

Play with `netcat`:
    
    $ echo 'set url https://pypi.org/project/joker-minions/' | netcat 127.0.0.1 8333
    
    $ echo 'get url' | netcat 127.0.0.1 8333
    https://pypi.org/project/joker-minions/ 
    
There's also a `BloomFilter` class using `mmh3` hash.

