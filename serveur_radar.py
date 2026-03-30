using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

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
    public int port = 6000; 

    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isRunning = true;

    private float derniereRespiration = 15f;
    private bool nouvelleDonnee = false;

    void Start()
    {
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
        Debug.Log("Écoute UDP prête sur le port " + port);
    }

    void Update()
    {
        if (nouvelleDonnee && lightController != null)
        {
            lightController.simulatedBreathingRate = derniereRespiration;
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
                    nouvelleDonnee = true;
                }
            }
            catch (System.Exception)
            {
                // Ignore les erreurs de fermeture de socket
            }
        }
    }

    void OnDestroy()
    {
        isRunning = false;
        if (udpClient != null) udpClient.Close();
        if (receiveThread != null) receiveThread.Abort();
    }
}
