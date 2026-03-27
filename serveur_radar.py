package com.tonnom.vr;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.content.Context;
import android.os.Build;
import com.unity3d.player.UnityPlayer;
import java.util.UUID;

public class BLEBridge {
    private BluetoothGatt bluetoothGatt;
    private Context context;
    
    private static final UUID SERVICE_UUID = UUID.fromString("12345678-1234-5678-1234-56789abcdef0");
    private static final UUID CHAR_UUID = UUID.fromString("12345678-1234-5678-1234-56789abcdef1");

    public BLEBridge() {
        this.context = UnityPlayer.currentActivity;
    }

    private void envoyerDebug(String message) {
        UnityPlayer.UnitySendMessage("RadarManager", "OnJavaDebug", message);
    }

    public void connectToRaspberry() {
        BluetoothManager bluetoothManager = (BluetoothManager) context.getSystemService(Context.BLUETOOTH_SERVICE);
        BluetoothAdapter bluetoothAdapter = bluetoothManager.getAdapter();

        if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled()) {
            envoyerDebug("Erreur : Bluetooth désactivé sur le casque.");
            return;
        }

        envoyerDebug("Java : Tentative de connexion...");
        BluetoothDevice device = bluetoothAdapter.getRemoteDevice("30:E3:A4:CF:80:72");
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            bluetoothGatt = device.connectGatt(context, false, gattCallback, BluetoothDevice.TRANSPORT_LE);
        } else {
            bluetoothGatt = device.connectGatt(context, false, gattCallback);
        }
    }

    private final BluetoothGattCallback gattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            if (status != BluetoothGatt.GATT_SUCCESS) {
                envoyerDebug("Erreur GATT status : " + status);
                return;
            }

            if (newState == BluetoothProfile.STATE_CONNECTED) {
                envoyerDebug("Java : Connecté ! Découverte...");
                gatt.requestConnectionPriority(BluetoothGatt.CONNECTION_PRIORITY_HIGH);
                gatt.discoverServices();
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                envoyerDebug("Java : Appareil déconnecté.");
            }
        }

        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                BluetoothGattCharacteristic characteristic = gatt.getService(SERVICE_UUID).getCharacteristic(CHAR_UUID);
                
                if (characteristic != null) {
                    gatt.setCharacteristicNotification(characteristic, true);
                    UUID CCCD_UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb");
                    android.bluetooth.BluetoothGattDescriptor descriptor = characteristic.getDescriptor(CCCD_UUID);
                    
                    if (descriptor != null) {
                        descriptor.setValue(android.bluetooth.BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
                        gatt.writeDescriptor(descriptor);
                        envoyerDebug("Java : Écoute + Descriptor OK !");
                    } else {
                        envoyerDebug("Erreur : Descriptor introuvable.");
                    }
                } else {
                    envoyerDebug("Erreur : Caractéristique introuvable.");
                }
            }
        }

        @Override
        public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic) {
            byte[] data = characteristic.getValue();
            if (data != null && data.length > 0) {
                String jsonString = new String(data);
                UnityPlayer.UnitySendMessage("RadarManager", "OnDataReceived", jsonString);
            }
        }
    };

    public void disconnect() {
        if (bluetoothGatt != null) {
            bluetoothGatt.close();
            bluetoothGatt = null;
        }
    }
}
