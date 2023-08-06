# silence inputer

## description
This extension of [voicekit_client_python](https://github.com/TinkoffCreditSystems/voicekit_client_python) 
allows you to manage pauses in synthesis text.

__#(integer)__ in synthesis string determines time section of pause 
between part of texts. One quantitative value of silence time 
section equals 100ms like [comma in synthesis text with VoiceKit](https://voicekit.tinkoff.ru/docs/synthesis).

Syntesis audio has __wav__ format.

## examples

```python
from speech_semaphore import ClientTTS

API_KEY = "api_key"
SECRET_KEY = "secret_key"

client = ClientTTS(API_KEY, SECRET_KEY)

text_with_pause = "Поторопись! #(3) у нас щас котлетки #(6) с макарошками? #(6) Нет #(4) с пюрэшкой"
without_pause = "Поторопись! у нас щас котлетки с макарошками? Нет с пюрэшкой"

client.synthesize_with_pause(text_with_pause, "with_pause.wav")
client.synthesize_with_pause(without_pause, "without_pause.wav")
```