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
import { VueBotUI } from "vue-bot-ui-audio";
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
        botAvatarImg: "https://i.ibb.co/GsWtJzz/Sanjivani-logo2.png",
        botAvatarSize: 50,
        msgBubbleBgUser: "#382966",
        boardContentBg: "#D5B9AE",
        colorScheme: "#00140D",
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
      // http://localhost:5005/webhooks/rest/webhook
      axios.post('https://rasa-server-saurabhsadhwani.cloud.okteto.net/webhooks/rest/webhook', { 'message': value.text }).then((res) => {
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
