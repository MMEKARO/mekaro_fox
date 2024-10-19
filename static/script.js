function capturarVoz() {
    const botaoGravar = document.getElementById('botao-gravar');
    botaoGravar.innerHTML = "Gravando...";

    // Captura o áudio do microfone
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            let audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", function(event) {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", function() {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

                const formData = new FormData();
                formData.append('file', audioBlob);

                // Envia o áudio para o backend para transcrição
                fetch('/transcrever_audio', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    const transcricaoDiv = document.getElementById('transcricao');
                    transcricaoDiv.innerHTML = <p><strong>Transcrição:</strong> ${data.transcricao}</p>;
                    
                    enviarMensagem(data.transcricao);
                })
                .catch(error => console.error('Erro ao transcrever:', error));
            });

            setTimeout(function() {
                mediaRecorder.stop();
                botaoGravar.innerHTML = "Gravar Voz";
            }, 5000);  // Grava por 5 segundos
        });
}

function enviarMensagem(mensagem) {
    fetch('/conversar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: mensagem }),
    })
    .then(response => response.json())
    .then(data => {
        const respostaIaDiv = document.getElementById('resposta-ia');
        respostaIaDiv.innerHTML = <p><strong>Resposta da Raposa:</strong> ${data.resposta}</p>;
    })
    .catch(error => {
        console.error('Erro ao enviar a mensagem:', error);
    });
}