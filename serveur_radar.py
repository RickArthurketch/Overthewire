using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

[System.Serializable]
public class DonneesRadar
{
    public float rr; 
}

public class UdpReceiver : MonoBehaviour
{
    public LightController lightController;
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
    }

    void Update()
    {
        if (nouvelleDonnee && lightController != null)
        {
            lightController.MettreAJourRespiration(derniereRespiration);
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
                
                DonneesRadar radarData = JsonUtility.FromJson<DonneesRadar>(jsonString);

                if (!float.IsNaN(radarData.rr))
                {
                    derniereRespiration = radarData.rr;
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
