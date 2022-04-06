<template>
  <div id="app">
    <HomeTemplate />
    <VueBotUI
      :messages="messages"
      :options="botOptions"
      :bot-typing="botTyping"
      :input-disable="botTyping"
      @msg-send="messageSendHandler"
    />
  </div>
</template>

<script>
import axios from "axios";
import { VueBotUI } from "vue-bot-ui-audio-p";
import HomeTemplate from "@/components/HomeTemplate.vue";

export default {
  name: "App",
  created () {
    document.title = "Hindi Voice Assistant";
  },
  components: {
    VueBotUI,
    HomeTemplate,
  },
  data() {
    return {
      messages: [],
      botTyping: false,
      botOptions: {
        botTitle: "Hindi Voice Assistant",
        botAvatarImg: "https://i.ibb.co/F0fmSK6/favicon.png",
        msgBubbleBgUser: "#8A2B21",
        boardContentBg: "#151515",
        colorScheme: "#8A2B21",
      },
    };
  },
  mounted() {
      this.messages.push({
        agent: "bot",
        type: "text",
        text: "🖋️ बीमारी की भविष्यवाणी करने के लिए कहे - मैं अपनी बीमारी जानना चाहता हूँ 🙏🙏"
      });
  },
  methods: {
    messageSendHandler(value) {
      this.messages.push({
        agent: "user",
        type: "text",
        text: value.text,
      });

      this.botTyping = true;

      axios.post('http://localhost:5005/webhooks/rest/webhook', { 'message': value.text }).then((res) => {
        var response = res['data'];
        console.log(response);

        for(var i = 0; i < response.length; i++){
        var areButtons = "buttons" in response[i]; 
        console.log(areButtons);
        if(areButtons){	
          this.messages.push({
          agent: 'bot',
            type: 'button',
            text: response[i]['text'],
            disableInput: true,
            options: 
              [{
                text: response[i]['buttons'][0]['title'],
                value: response[i]['buttons'][0]['payload'],
                action: 'postback'
              },
              {
                text: response[i]['buttons'][1]['title'],
                value: response[i]['buttons'][1]['payload'],
                action: 'postback'
              }],
        });
        let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
        console.log(sleep)
        }
        else {
            this.messages.push({
                agent: "bot",
                type: "text",
                text: response[i]['text'],
      });
      let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
      console.log(sleep)
      }
      let sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
      console.log(sleep)
    this.botTyping = false;
  }
      });
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
#app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}
</style>
