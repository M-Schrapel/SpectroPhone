/*
 * Android Application Spectrophone for a Master thesis at the Leibniz University Hanover
 * Detecting spectroscopic features of surfaces with smartphone cameras
 */

package com.example.philipp.spectroapp;

import android.Manifest;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private BleManager btManager;
    private WifiManager wifiManager;
    private int MY_PERMISSIONS_REQUEST_ACCESS_COARSE=1;
    private String serverIp;
    private int serverPort;
    private boolean wifiIsConnected = false;
    private boolean btIsConnected = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // declaration and initialization of gui elements
        final ImageButton btn_bt = findViewById(R.id.btn_bt);
        final ImageButton btn_classification = findViewById(R.id.btn_classification);
        final ImageButton btn_dataset = findViewById(R.id.btn_dataset);
        final ImageButton btn_fader = findViewById(R.id.btn_fader);
        final ImageButton btn_server = findViewById(R.id.btn_server);

        btn_bt.setBackgroundResource(android.R.drawable.btn_default);
        btn_classification.setBackgroundResource(android.R.drawable.btn_default);
        btn_dataset.setBackgroundResource(android.R.drawable.btn_default);
        btn_fader.setBackgroundResource(android.R.drawable.btn_default);
        btn_server.setBackgroundResource(android.R.drawable.btn_default);

        // declaration and initialization of connection elements
        wifiManager = new WifiManager();
        PublicDataApplication.setWifiManager(wifiManager);
        final BluetoothManager bluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        btManager = new BleManager(this, "LEDBOARD", bluetoothManager);
        PublicDataApplication.setBtManager(btManager);

        // listener to open and close a bluetooth connection
        btn_bt.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(btIsConnected){
                    btManager.closeConnection();
                    btn_bt.setBackgroundResource(android.R.drawable.btn_default);
                    btIsConnected = false;
                } else {
                    // permission check for bluetooth
                    if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_COARSE_LOCATION)
                            != PackageManager.PERMISSION_GRANTED) {
                        if (ActivityCompat.shouldShowRequestPermissionRationale(MainActivity.this,
                                Manifest.permission.ACCESS_COARSE_LOCATION)) {
                        } else {
                            ActivityCompat.requestPermissions(MainActivity.this,
                                    new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},
                                    MY_PERMISSIONS_REQUEST_ACCESS_COARSE);
                        }
                    }

                    try {
                        btManager.openConnection();
                        btn_bt.setBackgroundColor(Color.parseColor("#00477e"));
                        btIsConnected = true;
                    } catch (NullPointerException e){
                        Toast.makeText(MainActivity.this, "BT or GPS inactive",
                                Toast.LENGTH_LONG).show();
                    }
                }
            }
        });


        // open function to classify a surface
        btn_classification.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(!wifiIsConnected || !btIsConnected) {
                    if(!btIsConnected){
                        Toast.makeText(MainActivity.this, "No Bluetooth Connection",
                                Toast.LENGTH_LONG).show();
                    }
                    if(!wifiIsConnected){
                        Toast.makeText(MainActivity.this, "No Server Connection",
                                Toast.LENGTH_LONG).show();
                    }
                } else {
                    Intent myIntent = new Intent(MainActivity.this, CameraActivity.class);
                    myIntent.putExtra("isClassify", true);
                    MainActivity.this.startActivity(myIntent);
                }
            }
        });


        // open function to create a dataset of surfaces
        btn_dataset.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(!btIsConnected) {
                    Toast.makeText(MainActivity.this, "No Bluetooth Connection",
                            Toast.LENGTH_LONG).show();
                } else {
                    Intent myIntent = new Intent(MainActivity.this, CameraActivity.class);
                    myIntent.putExtra("isClassify", false);
                    MainActivity.this.startActivity(myIntent);
                }
            }
        });


        // open function for led check
        btn_fader.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(!btIsConnected) {
                    Toast.makeText(MainActivity.this, "No Bluetooth Connection",
                            Toast.LENGTH_LONG).show();
                } else {
                    Intent myIntent = new Intent(MainActivity.this, LedFaderActivity.class);
                    MainActivity.this.startActivity(myIntent);
                }
            }
        });


        // listener to open and close a connection to the server via tcp socket
        btn_server.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(wifiIsConnected) {
                    wifiManager.closeConnection();
                    btn_server.setBackgroundResource(android.R.drawable.btn_default);
                    wifiIsConnected = false;
                } else {
                    LinearLayout layout = new LinearLayout(MainActivity.this);
                    layout.setOrientation(LinearLayout.VERTICAL);
                    AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                    builder.setTitle("Connect to Classification Server");

                    // Set up the input
                    final EditText ipText = new EditText(MainActivity.this);
                    final EditText portText = new EditText(MainActivity.this);
                    ipText.setInputType(InputType.TYPE_CLASS_TEXT);
                    portText.setInputType(InputType.TYPE_CLASS_NUMBER);
                    TextView txtIp = new TextView(MainActivity.this);
                    txtIp.setText("IP Adress:");
                    TextView txtPort = new TextView(MainActivity.this);
                    txtPort.setText("Port:");
                    layout.addView(txtIp);
                    layout.addView(ipText);
                    layout.addView(txtPort);
                    layout.addView(portText);
                    builder.setView(layout);

                    // Set up the buttons
                    builder.setPositiveButton("Connect", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            serverIp = ipText.getText().toString();
                            serverPort = Integer.parseInt(portText.getText().toString());
                            System.out.println(serverIp);
                            System.out.println(serverPort);
                            wifiManager.openConnection(serverIp, serverPort);
                            btn_server.setBackgroundColor(Color.parseColor("#004d33"));
                            wifiIsConnected = true;
                        }
                    });
                    builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.cancel();
                        }
                    });
                    builder.show();
                }
            }
        });
    }
}
