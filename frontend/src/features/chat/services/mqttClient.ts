import mqtt from 'mqtt'

const MQTT_BROKER = 'ws://localhost:8083/mqtt' // EMQX websocket portu
const MQTT_USERNAME = 'mqttuser'
const MQTT_PASSWORD = 'strongpassword123'

export const connectMQTT = () => {
  return mqtt.connect(MQTT_BROKER, {
    username: MQTT_USERNAME,
    password: MQTT_PASSWORD,
    reconnectPeriod: 1000,
  })
}
