using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class RespirationLightController : MonoBehaviour
{
    [Header("Configuration Réseau")]
    public int port = 5005;

    [Header("Configuration Lumière")]
    public Light roomLight;
    public float minIntensity = 0.8f;
    public float maxIntensity = 1.8f;
    
    [Header("Valeurs du Capteur (BPM)")]
    public float minRespiration = 60f;
    public float maxRespiration = 130f;

    [Header("Gestion des erreurs")]
    public float timeoutDuration = 2.0f; // Temps en secondes avant d'assombrir la pièce

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = false;
    
    private float currentRespirationRate = 75f;
    private float timeSinceLastData = 0f;
    private bool newDataReceived = false;

    void Start()
    {
        if (roomLight == null)
        {
            roomLight = GetComponent<Light>();
        }

        StartNetworkListener();
    }

    private void StartNetworkListener()
    {
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        isRunning = true;
        receiveThread.Start();
    }

    private void ReceiveData()
    {
        udpClient = new UdpClient(port);
        IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);

        while (isRunning)
        {
            try
            {
                byte[] data = udpClient.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);

                if (float.TryParse(text, System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out float rate))
                {
                    currentRespirationRate = rate;
                    newDataReceived = true; 
                }
            }
            catch (System.Exception e)
            {
                if (isRunning) Debug.LogError("Erreur UDP : " + e.Message);
            }
        }
    }

    void Update()
    {
        // Chronomètre pour vérifier la bonne réception des données
        if (newDataReceived)
        {
            timeSinceLastData = 0f;
            newDataReceived = false;
        }
        else
        {
            timeSinceLastData += Time.deltaTime;
        }

        // Vérifie si le signal est perdu
        bool isSignalLost = timeSinceLastData > timeoutDuration || currentRespirationRate <= 0f;

        if (roomLight == null) return;

        float targetIntensity;

        // Assombrit la pièce si le signal est perdu
        if (isSignalLost)
        {
            targetIntensity = 0f;
        }
        else
        {
            float t = Mathf.InverseLerp(minRespiration, maxRespiration, currentRespirationRate);
            targetIntensity = Mathf.Lerp(minIntensity, maxIntensity, t);
        }

        // Applique la transition de la lumière
        roomLight.intensity = Mathf.Lerp(roomLight.intensity, targetIntensity, Time.deltaTime * 3f);
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        if (udpClient != null) udpClient.Close();
        if (receiveThread != null && receiveThread.IsAlive) receiveThread.Abort();
    }
}
