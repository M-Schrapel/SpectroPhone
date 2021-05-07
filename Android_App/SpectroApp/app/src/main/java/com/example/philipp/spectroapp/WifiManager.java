/*
 * Wifi manager class
 */

package com.example.philipp.spectroapp;

import android.util.Log;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Serializable;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;


public class WifiManager implements Serializable {

    private Socket socket;
    private String serverIp;
    private int serverPort;

    // open wifi connection to server
    public void openConnection(String serverIp, int serverPort){
        this.serverIp = serverIp;
        this.serverPort = serverPort;
        new Thread(new ClientThread()).start();
    }


    // wifi client thread
    class ClientThread implements Runnable {
        @Override
        public void run() {
            try {
                InetAddress serverAddr = InetAddress.getByName(serverIp);
                socket = new Socket(serverAddr, serverPort);
            } catch (UnknownHostException e1) {
                e1.printStackTrace();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
        }
    }


    // send request to classify a surface
    public void sendClassifyRequest(ArrayList<byte[]> imageByteList, int ledMode, int lightMode) {

        try {
            DataOutputStream os = new DataOutputStream(socket.getOutputStream());
            Log.e("WifiManager", "Sending image data to server");
            os.writeInt(ledMode);
            os.writeInt(lightMode);
            os.writeInt(imageByteList.size());

            for (byte[] imageBytes : imageByteList) {
                os.writeInt(imageBytes.length);
                os.write(imageBytes, 0, imageBytes.length);
            }

            os.flush();

        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    // returns the classify result of the surface
    public String receiveClassifyResult() {
        try {
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String message = input.readLine();

            return message;
        } catch (IOException e) {
            return "Error receiving response:  " + e.getMessage();
        }
    }

    // close wifi connection to server
    public void closeConnection() {
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

