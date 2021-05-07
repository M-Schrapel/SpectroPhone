/*
 * connection data which is necessary in more than one class
 */

package com.example.philipp.spectroapp;

import android.app.Application;


public class PublicDataApplication extends Application {

    static BleManager btManager = null;
    static WifiManager wifiManager = null;


    public static void setBtManager(BleManager pBtManager){
        btManager = pBtManager;
    }

    public static BleManager getBtManager(){
        return btManager;
    }

    public static void setWifiManager(WifiManager pWifiManager){
        wifiManager = pWifiManager;
    }

    public static WifiManager getWifiManager(){
        return wifiManager;
    }

}
