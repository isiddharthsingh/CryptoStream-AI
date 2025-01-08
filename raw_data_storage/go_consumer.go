package main

import (
    "context"
    "fmt"
    "github.com/segmentio/kafka-go"
)

func main() {
    r := kafka.NewReader(kafka.ReaderConfig{
        Brokers: []string{"localhost:9092"},
        Topic:   "coinbase_topic",
    })

    for {
        m, err := r.ReadMessage(context.Background())
        if err != nil {
            fmt.Println(err)
            break
        }
        fmt.Printf("message at offset %d: %s = %s\n", m.Offset, string(m.Key), string(m.Value))
        // Store message to HDFS (write HDFS logic here)
    }
}