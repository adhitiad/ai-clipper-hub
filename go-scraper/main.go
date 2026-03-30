package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Comment struct {
	Niche     string    `bson:"niche" json:"niche"`
	Hashtag   string    `bson:"hashtag" json:"hashtag"`
	Text      string    `bson:"text" json:"text"`
	Timestamp time.Time `bson:"timestamp" json:"timestamp"`
	Processed bool      `bson:"processed" json:"processed"`
}

func main() {
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Disconnect(context.TODO())

	collection := client.Database("clipper_db").Collection("raw_comments")
	fmt.Println("[*] Scraper Go Berjalan... Menyuntikkan Data.")

	mockData := []interface{}{
		Comment{"Gosip Selebriti", "#ArtisViral", "Baju merah pas klarifikasi beli di mana ya? Salah fokus.", time.Now(), false},
		Comment{"Ceramah Religi", "#KajianPagi", "MasyaAllah, ustadz ini kalau ngasih contoh related banget.", time.Now(), false},
		Comment{"Drama Ojol", "#OjolViral", "Kasihan motornya ditarik leasing di jalan.", time.Now(), false},
	}

	res, err := collection.InsertMany(context.TODO(), mockData)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("[+] Berhasil menyimpan %v komentar ke MongoDB.\n", len(res.InsertedIDs))
}
