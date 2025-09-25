package com.example.frontend;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import android.util.Base64;
import android.media.MediaPlayer;

import java.net.URI;
import java.nio.ByteBuffer;
import java.io.File;
import java.io.FileOutputStream;

public class TranslationWebSocketClient extends WebSocketClient {

    public TranslationWebSocketClient(URI serverUri) {
        super(serverUri);
    }

    @Override
    public void onOpen(ServerHandshake handshakedata) {
        System.out.println("Connected to backend WebSocket");
    }

    @Override
    public void onMessage(String message) {
        System.out.println("Text message: " + message);
    }

    @Override
    public void onMessage(ByteBuffer bytes) {
        byte[] audioBytes = new byte[bytes.remaining()];
        bytes.get(audioBytes);
        playAudio(audioBytes);
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("Connection closed: " + reason);
    }

    @Override
    public void onError(Exception ex) {
        ex.printStackTrace();
    }

    private void playAudio(byte[] audioBytes) {
        try {
            File tempFile = File.createTempFile("tts", ".wav");
            FileOutputStream fos = new FileOutputStream(tempFile);
            fos.write(audioBytes);
            fos.close();

            MediaPlayer mediaPlayer = new MediaPlayer();
            mediaPlayer.setDataSource(tempFile.getAbsolutePath());
            mediaPlayer.prepare();
            mediaPlayer.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void sendAudio(byte[] audioBytes, String callerLang, String receiverLang) {
        String audioBase64 = Base64.encodeToString(audioBytes, Base64.NO_WRAP);
        String json = "{\"caller_lang\":\"" + callerLang + "\",\"receiver_lang\":\"" + receiverLang + "\",\"audio\":\"" + audioBase64 + "\"}";
        send(json);
    }
}

