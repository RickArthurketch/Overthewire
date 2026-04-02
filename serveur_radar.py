using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using TMPro; // Requis pour l'interface texte

public class RespirationLightController : MonoBehaviour
{
    [Header("Configuration Réseau")]
    public int port = 5005;

    [Header("Configuration Lumière")]
    public Light roomLight;
    public float minIntensity = 0.5f;
    public float maxIntensity = 2.0f;
    
    [Header("Valeurs de Respiration Attendues")]
    public float minRespiration = 12f;
    public float maxRespiration = 25f;

    [Header("Affichage UI")]
    public TextMeshProUGUI rateText; // Champ pour lier ton texte

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = false;
    private float currentRespirationRate = 15f;

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
        Debug.Log($"Écoute UDP démarrée sur le port {port}");
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
        // Mise à jour du texte à l'écran
        if (rateText != null)
        {
            rateText.text = $"Respiration : {currentRespirationRate:0.0} /min";
        }

        if (roomLight == null) return;

        float t = Mathf.InverseLerp(minRespiration, maxRespiration, currentRespirationRate);
        float targetIntensity = Mathf.Lerp(minIntensity, maxIntensity, t);
        roomLight.intensity = Mathf.Lerp(roomLight.intensity, targetIntensity, Time.deltaTime * 3f);
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        if (udpClient != null) udpClient.Close();
        if (receiveThread != null && receiveThread.IsAlive) receiveThread.Abort();
    }
}
