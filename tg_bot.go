package main

import (
	"github.com/Dimonchik0036/vk-api"
	"log"
	"reflect"
)

const (
	token = "6ccf486634bd961cd18148534d58c1d2cc892edfdb99c5197edb46c35c2735a8cad7ee8d5cf5e44e91e58"
)

var client *vkapi.Client

//DB для тестоввых заданий и для полноценныйх огэ (сделать после того как всё основное напишу) +-
//либо прямые запросы к решуОГЭ ?
//либо просто брать тесты из файла/функции (пока что так, временно)


func handler(messages <-chan vkapi.LPUpdate) {
	var msg vkapi.MessageConfig
	userId := (<-messages).Message.FromID

	msg = vkapi.NewMessage(vkapi.NewDstFromUserID(userId), "Hello user!\nВыберете нужную опцию:")
	client.SendMessage(msg)
	<-messages

}

func vkBot() {
	var err error

	client, err = vkapi.NewClientFromToken(token)
	if err != nil {
		log.Fatal(err)
	}

	if err := client.InitLongPoll(0, 2); err != nil {
		log.Fatal(err)
	}

	updates, _, err := client.GetLPUpdatesChan(100, vkapi.LPConfig{25, vkapi.LPModeAttachments})
	if err != nil {
		log.Fatal(err)
	}

	for update := range updates {
		if update.Message == nil || !update.IsNewMessage() || update.Message.Outbox() {
			continue
		}

		if reflect.TypeOf(update.Message.Text).Kind() == reflect.String && update.Message.Text != "" {
			handlerChan := make(chan vkapi.LPUpdate, 1)
			go handler(handlerChan)
			handlerChan <- update
		} else {
			msg := vkapi.NewMessage(vkapi.NewDstFromUserID(update.Message.FromID), "Пожалуйста, отсылайте текстовые сообщения")
			client.SendMessage(msg)
		}
	}
}

func main() {
	//Call Bot
	vkBot()
}