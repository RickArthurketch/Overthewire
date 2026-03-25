<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools" xmlns:horizonos="http://schemas.horizonos/sdk">
  <uses-permission android:name="android.permission.BLUETOOTH" />
  <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
  <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
  <uses-permission android:name="android.permission.BLUETOOTH_SCAN" android:usesPermissionFlags="neverForLocation" tools:targetApi="31" />
  <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" tools:targetApi="31" />
  <uses-feature android:name="android.hardware.bluetooth_le" android:required="true" />
  <application android:label="@string/app_name" android:icon="@mipmap/app_icon" android:allowBackup="false">
    <!--Used when Application Entry is set to Activity, otherwise remove this activity block-->
    <activity android:name="com.unity3d.player.UnityPlayerGameActivity" android:theme="@style/UnityThemeSelector">
      <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
        <category android:name="com.oculus.intent.category.VR" />
      </intent-filter>
      <meta-data android:name="unityplayer.UnityActivity" android:value="true" />
      <meta-data android:name="com.oculus.vr.focusaware" android:value="true" />
    </activity>
    <!--Used when Application Entry is set to GameActivity, otherwise remove this activity block-->
    <activity android:name="com.unity3d.player.UnityPlayerGameActivity" android:theme="@style/BaseUnityGameActivityTheme">
      <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
      </intent-filter>
      <meta-data android:name="unityplayer.UnityActivity" android:value="true" />
      <meta-data android:name="android.app.lib_name" android:value="game" />
    </activity>
    <meta-data android:name="com.oculus.ossplash.background" android:value="black" />
    <meta-data android:name="com.oculus.telemetry.project_guid" android:value="8ec47c71-082d-42eb-a393-211d383d4cb3" />
    <meta-data android:name="com.oculus.supportedDevices" android:value="quest|quest2|questpro|quest3|quest3s" tools:replace="android:value" />
  </application>
  <uses-feature android:name="android.hardware.vr.headtracking" android:version="1" android:required="true" />
  <horizonos:uses-horizonos-sdk horizonos:minSdkVersion="60" horizonos:targetSdkVersion="85" />
</manifest>
