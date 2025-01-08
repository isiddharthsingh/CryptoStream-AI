CREATE KEYSPACE coinbase
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE processed_data (
            ...     id UUID PRIMARY KEY,
            ...     amount FLOAT,
            ...     base_currency TEXT,
            ...     target_currency TEXT,
            ...     timestamp TIMESTAMP
            ... );