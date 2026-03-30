using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using TMPro; // Nécessaire pour contrôler le texte

[System.Serializable]
public class RadarData
{
    public float rr;
    public float hr;
    public float hr_brut;
    public float snr_hr;
    public float prom_hr;
    public float hr_ref_hz;
    public int bin;
}

public class UdpReceiver : MonoBehaviour
{
    public BreathingLightController lightController;
    public TextMeshProUGUI affichageTexte; // Ta nouvelle case d'affichage
    public int port = 6000; 

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;

    private float derniereRespiration = 15f;
    private float dernierRythmeCardiaque = 0f;
    private bool nouvelleDonnee = false;

    void Start()
    {
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    void Update()
    {
        if (nouvelleDonnee)
        {
            // Met à jour la lumière
            if (lightController != null)
            {
                lightController.simulatedBreathingRate = derniereRespiration;
            }

            // Met à jour le texte dans la scène
            if (affichageTexte != null)
            {
                affichageTexte.text = $"Respiration : {derniereRespiration:F1} rpm\nCardiaque : {dernierRythmeCardiaque:F1} bpm";
            }

            nouvelleDonnee = false;
        }
    }

    private void ReceiveData()
    {
        udpClient = new UdpClient(port);
        IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, port);

        while (isRunning)
        {
            try
            {
                byte[] data = udpClient.Receive(ref anyIP);
                string jsonString = Encoding.UTF8.GetString(data);
                
                RadarData radarData = JsonUtility.FromJson<RadarData>(jsonString);

                if (!float.IsNaN(radarData.rr))
                {
                    derniereRespiration = radarData.rr;
                    dernierRythmeCardiaque = radarData.hr; // On enregistre le coeur
                    nouvelleDonnee = true;
                }
            }
            catch (System.Exception) {}
        }
    }

    void OnDestroy()
    {
        isRunning = false;
        if (udpClient != null) udpClient.Close();
        if (receiveThread != null) receiveThread.Abort();
    }
}
