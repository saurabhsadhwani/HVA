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
import { VueBotUI } from "vue-bot-ui";
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
        msgBubbleBgUser: "#892cdc",
        boardContentBg: "#151515",
        colorScheme: "#892cdc",
      },
    };
  },
  mounted() {
      this.messages.push({
        agent: "bot",
        type: "text",
        text: "Hello!! I'm Your Hindi Voice Assistant. How can I help you?",
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

      console.log(value.text)

      axios.post('http://localhost:5005/webhooks/rest/webhook', { 'message': value.text }).then((res) => {
	//console.log(res);
	//console.log(res['data']);
	var response = res['data'];
	console.log(response);

	var convertImgToDataURLviaCanvas = function(url, callback) {
		var img = new Image();
		img.crossOrigin = 'Anonymous';
		img.onload = function() {
			var canvas = document.createElement('CANVAS');
			var ctx = canvas.getContext('2d');
			var dataURL;
			canvas.height = this.height;
			canvas.width = this.width;
			ctx.drawImage(this, 0, 0);
			dataURL = canvas.toDataURL();
			callback(dataURL);
			canvas = null;
		};
		img.src = url;
	}



	for(var i = 0; i < response.length; i++){
	var isImage = "image" in response[i]; 
	console.log(isImage);
	if(isImage){	
		convertImgToDataURLviaCanvas(response[i]['image'], function( base64_data ) {
		console.log( base64_data );
		} );

		this.messages.push({
		agent: "bot",
		type: "text",
		text: response[i]['image'],
	});
	}
	else {
		this.messages.push({
                agent: "bot",
                type: "text",
                text: response[i]['text'],
	});
	}
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
