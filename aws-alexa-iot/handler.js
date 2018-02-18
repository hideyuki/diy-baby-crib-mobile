const AWS = require('aws-sdk')
const iotData = new AWS.IotData({endpoint: process.env.AWS_IOT_ENDPOINT})

/**
 * AlexaのDiscoveryリクエストにレスポンスする
 * https://developer.amazon.com/ja/docs/smarthome/steps-to-build-a-smart-home-skill.html のコードのコピペ
 * @param {*} request 
 * @param {*} context 
 */
function handleDiscovery(request, context) {
  const payload = {
    endpoints:
      [
        require(__dirname + '/endpoints/mobile.json') 
      ]
  }
  let header = request.directive.header
  header.name = 'Discover.Response'
  console.log('DEBUG', 'Discovery Response: ', JSON.stringify({ header: header, payload: payload }))
  context.succeed({ event: { header: header, payload: payload } })
}


/**
 * ON/OFFのコントロール
 * @param {*} request 
 * @param {*} context 
 * @param {Function} callback 
 */
function handlePowerControl(request, context, callback) {
  const requestMethod = request.directive.header.name
  const endpointId = request.directive.endpoint.endpointId    
  let powerResult = 'ON'

  console.log('requestMethod: ', requestMethod, ', endpointId: ', endpointId)

  if (requestMethod === 'TurnOn') {
    powerResult = 'ON'
  }
  else if (requestMethod === 'TurnOff') {
    powerResult = 'OFF'
  }

  switch (endpointId) {
    // endpoints/mobile.json の endpointId で指定した "mobile" がメリーの endpointId です
    case 'mobile':
      const params = {
        topic: 'home/mobile/1',  // トピック
        qos: 0,
        payload: `{"power": "${powerResult}"}`  // power は ON か OFF が設定される
      }

      // AWS IoTにメリーの回転 ON/OFF のメッセージを送信
      iotData.publish(params, (err, data)=>{
        console.log(err, data)
        sendResponse()
      })
      break

    default:
      sendResponse()
  }

  /**
   * Alexaサービスに返すレスポンス。powerState が現在どうなったかのレスポンスを返す
   * このレスポンスを受信したAlexaサービスは、Echo に「はい」とつぶやかせる
   */
  function sendResponse() {
    const contextResult = {
      properties: [{
        namespace: 'Alexa.PowerController',
        name: 'powerState',
        value: powerResult,
        timeOfSample: '2017-09-03T16:20:50.52Z',
        uncertaintyInMilliseconds: 50
      }]
    }
    let responseHeader = request.directive.header
    responseHeader.namespace = 'Alexa'
    responseHeader.name = 'Response'
    responseHeader.messageId = responseHeader.messageId + '-R'
    const endpoint = {
      scope: {
        type: 'BearerToken',
        token: 'Alexa-access-token'
      },
      endpointId: endpointId
    }
    const response = {
      context: contextResult,
      event: {
        header: responseHeader
      },
      endpoint: endpoint,
      payload: {}
    }

    // console.log('DEBUG', 'Alexa.PowerController ', JSON.stringify(response))
    context.succeed(response)
  }
}

/**
 * Alexaサービスからコールされる関数。
 * @param {*} request 
 * @param {*} context 
 * @param {Function} callback 
 */
module.exports.alexa = (request, context, callback) => {
  if (request.directive.header.namespace === 'Alexa.Discovery' && request.directive.header.name === 'Discover') {
    // スマートホームスキルを追加し、デバイス検出を行ったときにAlexaサービスからコールされたとき

      // console.log('DEGUG:', 'Discover request', JSON.stringify(request))
    handleDiscovery(request, context, '')
  }
  else if (request.directive.header.namespace === 'Alexa.PowerController') {
    // メリーのインタフェースである Alexa.PowerController のネームスペースでAlexaサービスからコールされたとき
    if (request.directive.header.name === 'TurnOn' || request.directive.header.name === 'TurnOff') {
      // console.log('DEBUG:', 'TurnOn or TurnOff Request', JSON.stringify(request))
      handlePowerControl(request, context, callback)
    }
  }
}
