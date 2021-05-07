/*
 * LED Fader function to test the hardware
 */

package com.example.philipp.spectroapp;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.SeekBar;
import android.widget.Switch;

import static android.content.ContentValues.TAG;

public class LedFaderActivity extends AppCompatActivity {


    private byte[] btData;
    //seekbarlevel
    private int skbLed1Val = 0;
    private int skbLed2Val = 0;
    private int skbLed3Val = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_led_fader);
        getSupportActionBar().setTitle("LED Fader");
        btData = new byte[] {0,0,0,0,0,0};

        // declaration and initialization of gui elements
        final Switch swt_led1 = findViewById(R.id.swt_led1);
        final Switch swt_led2 = findViewById(R.id.swt_led2);
        final Switch swt_led3 = findViewById(R.id.swt_led3);
        final SeekBar skb_led1 = findViewById(R.id.skb_led1);
        final SeekBar skb_led2 = findViewById(R.id.skb_led2);
        final SeekBar skb_led3 = findViewById(R.id.skb_led3);
        final BleManager btManager = PublicDataApplication.getBtManager();


        // returns if led 1 is switched on off
        swt_led1.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                boolean status;
                if(swt_led1.isChecked()){
                    btData[0] = 1;
                    status = btManager.writeBtData(btData);
                } else {
                    btData[0] = 0;
                    status = btManager.writeBtData(btData);
                }

                if(status){
                    Log.e(TAG,  "Data transferred");
                } else {
                    Log.e(TAG, "Data transfer didnt work");
                }
            }
        });


        // returns if led 2 is switched on off
        swt_led2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                boolean status;
                if(swt_led2.isChecked()){
                    btData[1] = 1;
                    status = btManager.writeBtData(btData);
                } else {
                    btData[1] = 0;
                    status = btManager.writeBtData(btData);
                }

                if(status){
                    Log.e(TAG,  "Data transferred");
                } else {
                    Log.e(TAG, "Data transfer didnt work");
                }
            }
        });


        // returns if led 3 is switched on off
        swt_led3.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                boolean status;
                if(swt_led3.isChecked()){
                    btData[2] = 1;
                    status = btManager.writeBtData(btData);
                } else {
                    btData[2] = 0;
                    status = btManager.writeBtData(btData);
                }

                if(status){
                    Log.e(TAG,  "Data transferred");
                } else {
                    Log.e(TAG, "Data transfer didnt work");
                }
            }
        });


        // returns new level of seekbar for led 1
        skb_led1.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,boolean fromUser) {
                // TODO Auto-generated method stub

                Boolean status;
                if(progress>0){
                    skbLed1Val = progress*255/100;
                    btData[3] = ((byte) (skbLed1Val));
                } else {
                    skbLed1Val = 0;
                    btData[3] = ((byte) skbLed1Val);
                }
                status = btManager.writeBtData(btData);

                if(status){
                    Log.e(TAG,  "Data transferred");
                } else {
                    Log.e(TAG, "Data transfer didnt work");
                }

            }
        });


        // returns new level of seekbar for led 2
        skb_led2.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,boolean fromUser) {
                // TODO Auto-generated method stub

                Boolean status;
                if(progress>0){
                    skbLed2Val = progress*255/100;
                    btData[4] = ((byte) (skbLed2Val));
                } else {
                    skbLed2Val = 0;
                    btData[4] = ((byte) skbLed2Val);
                }
                status = btManager.writeBtData(btData);

                if(status){
                    Log.e(TAG,  "Data transferred");
                } else {
                    Log.e(TAG, "Data transfer didnt work");
                }

            }
        });


        // returns new level of seekbar for led 3
        skb_led3.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,boolean fromUser) {
                // TODO Auto-generated method stub

                Boolean status;
                if(progress>0){
                    skbLed3Val = progress*255/100;
                    btData[5] = ((byte) (skbLed3Val));
                } else {
                    skbLed3Val = 0;
                    btData[5] = ((byte) skbLed3Val);
                }
                status = btManager.writeBtData(btData);

                if(status){
                    Log.e(TAG,  "Data transferred");
                } else {
                    Log.e(TAG, "Data transfer didnt work");
                }

            }
        });

    }
}
