/*
 * Manager class for the bluetooth connection
 */

package com.example.philipp.spectroapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.Context;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static android.bluetooth.BluetoothAdapter.STATE_CONNECTED;
import static android.bluetooth.BluetoothAdapter.STATE_CONNECTING;
import static android.bluetooth.BluetoothProfile.STATE_DISCONNECTED;
import static android.content.ContentValues.TAG;

public class BleManager implements Serializable {

    private ArrayList<BluetoothDevice> moduleBTList = new ArrayList<BluetoothDevice>();
    private BluetoothLeScanner bluetoothLeScanner;
    private BluetoothAdapter mBluetoothAdapter;
    private boolean mScanning;
    private int mConnectionState;
    private String bluetoothAddress;
    private BluetoothGatt mBluetoothGatt;
    private Context mContext;
    private String mDeviceName;
    private UUID uuid = UUID.fromString("36ae4f48-419b-421a-95a1-af80b7f418ec");
    private byte[] btData = new byte[] {0,0,0,0,0,0};


    public BleManager(Context context, String deviceName, BluetoothManager bluetoothManager){
        mContext = context;
        mDeviceName = deviceName;
        mBluetoothAdapter = bluetoothManager.getAdapter();
    };


    // check for bluetooth devices
    public int openConnection(){
        if(mConnectionState == STATE_DISCONNECTED){
            moduleBTList.clear();
            startScanning(true);
        }
        return mConnectionState;
    }



    private ScanCallback scanCallback = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            super.onScanResult(callbackType, result);
            moduleBTList.add(result.getDevice());
            Log.d(TAG, "Device found: " + result.getDevice().getName());
        }
        @Override
        public void onBatchScanResults(List<ScanResult> results) {
            super.onBatchScanResults(results);
        }

        @Override
        public void onScanFailed(int errorCode) {
            super.onScanFailed(errorCode);
            Log.d(TAG, "Scanning Failed " + errorCode);
        }
    };


    // scan for 2 seconds
    private static final long SCAN_PERIOD = 2000;

    private void startScanning(final boolean enable) {
        bluetoothLeScanner = mBluetoothAdapter.getBluetoothLeScanner();
        Handler mHandler = new Handler();
        if (enable) {
            bluetoothLeScanner.startScan(scanCallback);
            mHandler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    mScanning = false;
                    bluetoothLeScanner.stopScan(scanCallback);
                    if(moduleBTList.size()<=0){
                        Log.d(TAG, "Found no Device");
                    }
                    connect();
                }
            }, SCAN_PERIOD);
            mScanning = true;
        } else {
            mScanning = false;
            bluetoothLeScanner.stopScan(scanCallback);
        }
    }


    private BluetoothGattCallback bluetoothGattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            super.onConnectionStateChange(gatt, status, newState);
            Log.d(TAG, "onConnectionStateChange " + newState);

            String intentAction;
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                intentAction = "CONNECTED!";
                mConnectionState = STATE_CONNECTED;
                Log.i(TAG, "Connected to GATT server.");
                Log.i(TAG, "Attempting to start service discovery:" +
                        mBluetoothGatt.discoverServices());

            } else if (newState == STATE_DISCONNECTED) {
                intentAction = "DISCONNECTED!";
                mConnectionState = STATE_DISCONNECTED;
                Log.i(TAG, "Disconnected from GATT server.");

            }
        }
    };


    // connect to bluetooth device
    private boolean connect() {
        String address = getDeviceAddress();

        if (mBluetoothAdapter == null || address == null) {
            Log.w(TAG, "BluetoothAdapter not initialize or unspecified address");
            Toast.makeText(mContext, "Bluetooth target not found!", Toast.LENGTH_SHORT).show();
            return false;
        }

        if (mBluetoothAdapter != null && address.equals(bluetoothAddress) && mBluetoothGatt != null) {
            Log.d(TAG, "Try to use existing connection");
            if (mBluetoothGatt.connect()) {
                mConnectionState = STATE_CONNECTING;
                return true;
            } else {
                return false;
            }
        }
        final BluetoothDevice bluetoothDevice = mBluetoothAdapter.getRemoteDevice(address);
        if (bluetoothDevice == null) {
            Log.w(TAG, "Device not found");
            return false;
        }

        mBluetoothGatt = bluetoothDevice.connectGatt(mContext, false, bluetoothGattCallback);
        bluetoothAddress = address;
        mConnectionState = STATE_CONNECTING;
        return true;
    }


    // send data via bluetooth
    public boolean writeBtData(byte[] btData){

        //check mBluetoothGatt is available
        if (mBluetoothGatt == null) {
            Log.e(TAG, "lost connection");
            return false;
        }
        BluetoothGattService privateService = mBluetoothGatt.getService(uuid);


        for (BluetoothGattService serv:mBluetoothGatt.getServices()) {
            Log.e(TAG, serv.getUuid().toString() );
        }

        if (privateService == null) {
            Log.e(TAG, "service not found!");
            return false;
        }
        BluetoothGattCharacteristic privateCharac = privateService.getCharacteristic(uuid);
        if (privateCharac == null) {
            Log.e(TAG, "char not found!");
            return false;
        }

        privateCharac.setValue(btData);
        boolean status = mBluetoothGatt.writeCharacteristic(privateCharac);
        return status;
    }



    // set led lights on the hardware
    public void setExtFlash(int flashNumber, boolean state, int intensity) {
        boolean status;

        // set led number on off an which intensity
        switch (flashNumber) {
            case 1:
                if(state) {
                    btData[0] = 1;

                    if(intensity>0){
                        btData[3] = ((byte) (intensity*255/100));
                    } else {
                        btData[3] = ((byte) (intensity));
                    }
                    status = writeBtData(btData);
                } else {
                    btData[0] = 0;

                    if(intensity>0){
                        btData[3] = ((byte) (intensity*255/100));
                    } else {
                        btData[3] = ((byte) (intensity));
                    }
                    status = writeBtData(btData);
                }
                break;

            case 2:
                if(state) {
                    btData[1] = 1;

                    if(intensity>0){
                        btData[4] = ((byte) (intensity*255/100));
                    } else {
                        btData[4] = ((byte) (intensity));
                    }
                    status = writeBtData(btData);
                } else {
                    btData[1] = 0;

                    if(intensity>0){
                        btData[4] = ((byte) (intensity*255/100));
                    } else {
                        btData[4] = ((byte) (intensity));
                    }
                    status = writeBtData(btData);
                }
                break;

            case 3:
                if(state) {
                    btData[2] = 1;

                    if(intensity>0){
                        btData[5] = ((byte) (intensity*255/100));
                    } else {
                        btData[5] = ((byte) (intensity));
                    }
                    status = writeBtData(btData);
                } else {
                    btData[2] = 0;

                    if(intensity>0){
                        btData[5] = ((byte) (intensity*255/100));
                    } else {
                        btData[5] = ((byte) (intensity));
                    }
                    status = writeBtData(btData);
                }
                break;

            default:
                status = false;
        }

        if(status){
            Log.e(TAG,  "Data transferred");
        } else {
            Log.e(TAG, "Data transfer didnt work");
        }
    }


    // return address of bluetooth device
    private String getDeviceAddress(){

        String address = null;

        for (BluetoothDevice device: moduleBTList) {
            if(device.getName()!= null && device.getName().equals(mDeviceName)){
                address = device.getAddress();
            }
        }
        return address;
    }


    // close bluetooth connection
    public void closeConnection() {
        if (mBluetoothGatt == null) {
            return;
        }
        mBluetoothGatt.close();
        mBluetoothGatt = null;
    }
}

